import sys
import unreal
import json
from pathlib import Path
from importlib import reload, import_module

BASE_PATH = Path(r'D:\Work\Gms\Ark\ASADevKit-scripts')
sys.path.append(str(BASE_PATH))

MODULES_TO_RELOAD = ('ue_utils', 'stats', 'consts', 'clean_numbers', 'jsonutils', 'colors')
for module in MODULES_TO_RELOAD:
    # Load the module, then force reload it
    module = import_module(module)
    reload(module)

from jsonutils import save_as_json
from ue_utils import find_all_species, get_dcsc_from_bp
from stats import values_for_species
from consts import SKIP_SPECIES
from colors import color_hex_to_decimal

DATA_PATH = BASE_PATH / 'data'
CURRENT_VALUES = Path(r'D:\Work\Gms\Ark\Purlovia\output\data\asb\values.json')
MUTATION_OUTPUT = DATA_PATH / 'mutation_mults.toml'
SPECIES_OUTPUT = DATA_PATH / 'stats.toml'
NEW_SPECIES_JSON = DATA_PATH / 'new_values.json'
CHANGED_SPECIES_JSON = DATA_PATH / 'changed_values.json'
DYE_DATA = BASE_PATH / 'asa-dyes.csv'

# Load ASE values so it can be compared to the current values
with open(CURRENT_VALUES) as f:
    old_raw_values = json.load(f)

# Convert it to a dictionary for easier access
old_species_data = {species['blueprintPath']: species for species in old_raw_values['species']}

# Load the dye data
with open(DYE_DATA) as f:
    dye_data = [(row[1],color_hex_to_decimal(row[2])) for row in (line.split(',') for line in f)]


def append_file(path: Path, text: str) -> None:
    with open(path, 'at') as f:
        f.write(text)

with(open(MUTATION_OUTPUT, 'wt')) as f:
    f.write("[species]\n")
with(open(SPECIES_OUTPUT, 'wt')) as f:
    f.write("[species]\n\n")


it = find_all_species()
new_species_data = {}
changed_species_data = {}
# for i in range(100):
while True:
    bp = None
    try:
        bp, char = next(it)
        unreal.log_warning(bp.get_path_name())
    except StopIteration:
        break
    except Exception as e:
        unreal.log_error(f"Error loading asset: {e}")
        continue

    bp_name = bp.get_path_name()
    if bp_name in SKIP_SPECIES:
        unreal.log_warning(f"Override: skip")
        continue

    dcsc = get_dcsc_from_bp(bp)
    if not dcsc:
        unreal.log_error("Unable to select DCSC")
        continue

    new_data = values_for_species(bp_name, char, dcsc)
    if not new_data:
        unreal.log_error("Skipping species")
        continue

    try:
        old_data = old_species_data[new_data['blueprintPath']]
    except KeyError:
        unreal.log_error(f"Species {new_data['blueprintPath']} not found in old data!")
        continue

    new_species_data[new_data['blueprintPath']] = new_data

    changes = {}
    # Collect changes per key
    for key, new_value in new_data.items():
        old_value = old_data.get(key, None)
        if new_value != old_value:
            changes[key] = new_value

    if changes:
        changes = {
            "blueprintPath": new_data['blueprintPath'],
            **changes,
        }
        changed_species_data[new_data['blueprintPath']] = changes

        output_string = f'''["{new_data['blueprintPath']}"]\n'''
        for key, value in changes.items():
            output_string += f'"{key}" = {value!r}\n'
        output_string += '\n'
        append_file(SPECIES_OUTPUT, output_string)


def make_json_from_species(species: dict) -> dict:
    return dict(
        version="25.53.449745",
        format="1.15-asa",
        mod=dict(id="ASA", tag="", title="Ark: Survival Ascended"),
        species=sorted(species.values(), key=lambda x: x['blueprintPath']),
        dyeStartIndex=128,
        dyeDefinitions=dye_data,
    )

save_as_json(make_json_from_species(new_species_data), NEW_SPECIES_JSON, pretty=True)
save_as_json(make_json_from_species(changed_species_data), CHANGED_SPECIES_JSON, pretty=True)

print("Done")







# unreal.EditorUtilityLibrary().get_selected_assets()
# cls = dodo_dcsc.get_class()
# bp = unreal.EditorAssetLibrary.load_blueprint_class(cls.get_path_name())
# default = unreal.get_default_object(bp)
#
# for asset in assets:
#   name = str(asset.package_name)
#   if "Character_BP" in name and "Dodo" in name:
#     break


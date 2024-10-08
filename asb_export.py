import sys
import json
from datetime import datetime
from typing import Any, Optional
import unreal
from pathlib import Path


# Make sure we can load local modules
SCRIPT_FILE = Path(__file__).absolute()
print(f'Running {SCRIPT_FILE}')
BASE_PATH = SCRIPT_FILE.parent
if str(BASE_PATH) not in sys.path:
    sys.path.append(str(BASE_PATH))

# We need to reload all our modules to ensure we're using the latest versions
from ue_utils import reload_local_modules
reload_local_modules(BASE_PATH)

from jsonutils import save_as_json
from ue_utils import find_all_species, get_cdo_from_asset, get_dcsc_from_character_bp, load_asset
from consts import COLOR_REGION_WHITELIST, MANUAL_SPECIES, SKIP_SPECIES, SKIP_SPECIES_ROOTS, SPECIES_REMAPS, WHITELIST_PATHS
from colors import parse_dyes
from species.values import values_for_species

# Constants
CURRENT_VALUES = Path(r'D:\Work\Gms\Ark\Purlovia\output\data\asb\values.json')
DATA_PATH = BASE_PATH / 'data'
MUTATION_OUTPUT = DATA_PATH / 'mutation_mults.toml'
SPECIES_OUTPUT = DATA_PATH / 'stats.toml'
NEW_SPECIES_JSON = DATA_PATH / 'new_values.json'
CHANGED_SPECIES_JSON = DATA_PATH / 'changed_values.json'


# Load ASE values so it can be compared to the current values
with open(CURRENT_VALUES) as f:
    old_raw_values = json.load(f)

# Convert it to a dictionary for easier access
old_species_data = {species['blueprintPath']: species for species in old_raw_values['species']}


def main(version: str):
    start_time = datetime.now()

    unreal.log_warning("Loading PrimalGameData...")
    pgd = get_cdo_from_asset(load_asset('/Game/PrimalEarth/CoreBlueprints/COREMEDIA_PrimalGameData_BP'))
    if not isinstance(pgd, unreal.PrimalGameData):
        unreal.log_error("Unable to load PrimalGameData!")
        return

    unreal.log("Parsing dye list")
    dyes = parse_dyes(pgd.master_dye_list)

    unreal.log("Calculating species remaps")
    old_remaps: dict[str,str] = old_raw_values.get('remaps', {})
    new_remaps = {k: v for k, v in SPECIES_REMAPS.items() if v and k != v}
    # Only keep remaps that have changed
    remaps = {k: v for k, v in new_remaps.items() if old_remaps.get(k, None) != v}
    unreal.log(f"Species remaps: {remaps}")

    unreal.log_warning("Checking all species for changes...")
    new_species_data = {}
    changed_species_data = {}
    for bp, char in find_all_species(filter_species):
        short_bp = bp.get_path_name().split('.')[0]
        unreal.log_warning(short_bp)
        unreal.log_flush()

        # Extract "new" data from the DevKit
        new_data = extract_species(bp, char)
        if not new_data:
            continue

        # Pull old data from the existing values file
        old_data = old_species_data.get(new_data['blueprintPath'], None)

        # New color data is only used for new species or when whitelisted
        if old_data and short_bp not in COLOR_REGION_WHITELIST:
            new_data.pop('colors', None)

        new_species_data[new_data['blueprintPath']] = new_data

        # Record changes between the two
        if old_data:
            changes = {}
            # Collect changes per new field
            for key, new_value in new_data.items():
                old_value = old_data.get(key, None)
                old_value = sanitise_old_value(old_value, key)
                if new_value != old_value:
                    changes[key] = new_value
                    print('(changed)')

            if changes:
                changes = {
                    "blueprintPath": new_data['blueprintPath'],
                    **changes,
                }
                changed_species_data[new_data['blueprintPath']] = changes
        else:
            changed_species_data[new_data['blueprintPath']] = {
                "blueprintPath": new_data['blueprintPath'],
                **new_data,
            }

    # Also add manual species
    for bp_path, char in MANUAL_SPECIES.items():
        if bp_path in new_species_data:
            unreal.log_error(f"Manual species already exists: {bp_path}")
            continue

        new_species_data[bp_path] = char
        changed_species_data[bp_path] = char

    def make_json_from_species(species: dict) -> dict:
        return dict(
            version=version,
            format="1.16-mod-remap",
            mod=dict(id="ASA", tag="", title="Ark: Survival Ascended", shortTitle="ASA", official=True),
            species=sorted(species.values(), key=lambda x: x['blueprintPath']),
            dyeStartIndex=128,
            dyeDefinitions=dyes,
            remaps=remaps,
        )

    save_as_json(make_json_from_species(new_species_data), NEW_SPECIES_JSON, pretty=True)
    save_as_json(make_json_from_species(changed_species_data), CHANGED_SPECIES_JSON, pretty=True)

    end_time = datetime.now()
    elapsed = end_time - start_time
    unreal.log_warning(f"Elapsed time: {elapsed}")


def filter_species(short_bp: str):
    # Only process whitelisted paths
    if WHITELIST_PATHS and not any(short_bp.startswith(whitelist) for whitelist in WHITELIST_PATHS):
        return False

    # Check if we should skip this species
    if short_bp in SKIP_SPECIES:
        return False
    for skip_root in SKIP_SPECIES_ROOTS:
        if short_bp.startswith(skip_root):
            return False

    return True


def sanitise_old_value(value: Any, key: str) -> Any:
    if key == 'altBaseStats':
        # Convert string keys to integers
        value = {int(k): v for k, v in value.items()}
        return value

    return value


def extract_species(bp: unreal.Blueprint, char: unreal.PrimalDinoCharacter) -> Optional[dict[str, Any]]:
    bp_name = bp.get_path_name()
    alt_dcsc, dcsc = get_dcsc_from_character_bp(bp)
    if not dcsc or not alt_dcsc:
        unreal.log_error("Unable to select DCSC")
        return None

    species_data = values_for_species(bp_name, char, dcsc, alt_dcsc)
    if not species_data:
        unreal.log_error("Skipping species")
        return None

    return species_data



if __name__ == '__main__':
    version = sys.argv[-1]
    if version.count('.') != 2 or not all(part.isdigit() for part in version.split('.')):
        raise ValueError(f"Invalid version: {version}")

    main(version)
    unreal.log_warning(f"Finished.")

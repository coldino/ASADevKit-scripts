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


data = {}
assets = unreal.EditorUtilityLibrary().get_selected_assets()
for asset in assets:
    changes = asset.wc_get_all_nondefault_property_values()
    if not changes:
        continue

    change_data = {}
    for key,value in changes:
        if isinstance(value, (int, str, float, bool)):
            change_data[key] = value
        else:
            print(f'Unknown type for {key}: {type(value)}')

    data[asset.get_path_name()] = change_data

save_as_json(data, BASE_PATH / 'data' / 'difficulty.json', pretty=True)

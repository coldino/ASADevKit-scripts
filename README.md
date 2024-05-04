# Data Extractor for Ark: Survival Ascended DevKit

This project is a hacky attempt to extract https://github.com/arkutils/Obelisk data for ASA from its DevKit.

## Run it

In UE's command line enter, adapted for your own repository path:
```
py "D:/Work/Gms/Ark/ASADevKit-scripts/asb_export.py"
```

## Setup for dev

In order to get full type hinting and autocomplete your editor needs to be setup to point to the generated Python file
within the UE project.

For VSCode this is done via the `python.autoComplete.extraPaths` and `python.analysis.extraPaths`
settings in `.vscode/settings.json`. Unfortunately this means hardcoded paths within the repository currently.

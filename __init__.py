from .gecco_autosend import GeccoAutosend
from .gecco_selectchannel import GeccoSelectchannel
from .gecco_imagesave import GeccoImageSave

NODE_CLASS_MAPPINGS = {
    "GeccoAutosend": GeccoAutosend,
    "GeccoSelectchannel": GeccoSelectchannel,
    "GeccoImageSave": GeccoImageSave
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeccoAutosend": "Gecco Autosend",
    "GeccoSelectchannel": "Gecco Select Channel",
    "GeccoImageSave": "Gecco Image Save"
}
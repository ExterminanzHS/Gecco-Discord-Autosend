from .channellist import channellist

class GeccoSelectchannel:
    def __init__(self):
        self.channel_list = channellist

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "saved_channels": (list(channellist.keys()), {"default": "Select a channel"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "select_channel"

    OUTPUT_NODE = True

    CATEGORY = "GeccoBot"

    def select_channel(self, saved_channels):
        if saved_channels in self.channel_list:
            return (str(self.channel_list[saved_channels]),)
        else:
            return ("",)

NODE_CLASS_MAPPINGS = {
    "GeccoSelectchannel": GeccoSelectchannel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeccoSelectchannel": "Gecco Select Channel"
}
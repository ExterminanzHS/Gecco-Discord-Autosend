import os
import asyncio
import torch
from PIL import Image
import io
import numpy as np

NEXTCORD_AVAILABLE = False

try:
    import nextcord
    from nextcord.ext import commands
    NEXTCORD_AVAILABLE = True
except ImportError:
    pass

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

class GeccoAutosend:
    def __init__(self):
        self.bot = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "channel_id": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "send_image"

    OUTPUT_NODE = True

    CATEGORY = "GeccoBot"

    async def login_bot(self):
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        
        await self.bot.login(BOT_TOKEN)
        asyncio.create_task(self.bot.connect())

        while not self.bot.is_ready():
            await asyncio.sleep(1)

    def tensor_to_image(self, image_tensor):
        if isinstance(image_tensor, torch.Tensor):
            image_array = image_tensor.cpu().numpy()
        else:
            image_array = np.array(image_tensor)

        if image_array.ndim == 3 and image_array.shape[2] == 3:
            image_array = (image_array * 255).clip(0, 255).astype(np.uint8)
            return Image.fromarray(image_array)
        else:
            raise ValueError(f"Unsupported tensor shape: {image_array.shape}")

    async def send_images(self, images, channel_id):
        discord_channel = self.bot.get_channel(int(channel_id))
        if not discord_channel:
            return

        for i, image_tensor in enumerate(images):
            try:
                image = self.tensor_to_image(image_tensor)
                with io.BytesIO() as image_binary:
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await discord_channel.send(file=nextcord.File(fp=image_binary, filename=f"GeccoUI_{i}.png"))
            except Exception:
                pass

    def send_image(self, images, channel_id):
        if not NEXTCORD_AVAILABLE or not BOT_TOKEN:
            return ()

        async def run_bot():
            try:
                await asyncio.wait_for(self.login_bot(), timeout=30)
                await asyncio.wait_for(self.send_images(images, channel_id), timeout=60)
            except Exception:
                pass
            finally:
                if self.bot:
                    await self.bot.close()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(run_bot())
        finally:
            loop.close()

        return ()

NODE_CLASS_MAPPINGS = {
    "GeccoAutosend": GeccoAutosend
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeccoAutosend": "Gecco Autosend"
}
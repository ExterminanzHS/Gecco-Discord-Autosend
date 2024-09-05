import os
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
import uuid

class GeccoImageSave:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "GeccoUI"}),
            },
            "optional": {
                "output_folder": ("STRING", {"default": ""}),
                "save_locally": ("BOOLEAN", {"default": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "process_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def process_images(self, images, filename_prefix="GeccoUI", output_folder="", save_locally=True, prompt=None, extra_pnginfo=None):
        try:
            for i, image_tensor in enumerate(images):
                if hasattr(image_tensor, 'cpu'):
                    image_array = image_tensor.cpu().numpy()
                else:
                    image_array = np.array(image_tensor)
                
                image_array = (image_array * 255).clip(0, 255).astype(np.uint8)
                if image_array.ndim == 3 and image_array.shape[0] in [1, 3, 4]:
                    image_array = np.transpose(image_array, (1, 2, 0))
                if image_array.shape[-1] == 1:
                    image_array = np.squeeze(image_array, axis=-1)
                
                img = Image.fromarray(image_array)

                if save_locally and output_folder:
                    output_folder = os.path.abspath(output_folder)
                    os.makedirs(output_folder, exist_ok=True)

                    metadata = PngInfo()
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                    file = f"{filename_prefix}_{i}_{uuid.uuid4().hex[:8]}.png"
                    file_path = os.path.join(output_folder, file)
                    img.save(file_path, pnginfo=metadata, compress_level=4)

        except Exception:
            pass

        return ()

NODE_CLASS_MAPPINGS = {
    "GeccoImageSave": GeccoImageSave
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeccoImageSave": "Gecco Image Save"
}
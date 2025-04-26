import torch
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageMath
from comfy.sd import VAE
from comfy.utils import common_upscale
from nodes import common_ksampler

class AdvancedColorAdjust:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0,
                    "max": 3.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0,
                    "max": 3.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "hdr_intensity": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "red": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "green": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "blue": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "mask": ("MASK",),
                "hdr_mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust_image"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def apply_hdr(self, img, intensity, hdr_mask=None):
        if intensity == 0:
            return img
            
        # Convert to numpy array
        arr = np.array(img)
        hdr = arr.astype(np.float32) / 255.0
        
        # HDR effect - tone mapping
        hdr = np.where(hdr > 0.5, 
                      0.5 + (hdr - 0.5) * (1 + intensity * 2), 
                      hdr * (1 + intensity))
        
        # Apply HDR mask if provided
        if hdr_mask is not None:
            mask_np = np.array(hdr_mask) if isinstance(hdr_mask, Image.Image) else hdr_mask
            if mask_np.ndim == 2:
                mask_np = mask_np[..., np.newaxis]
            hdr = arr/255.0 * (1 - mask_np) + hdr * mask_np
        
        return Image.fromarray(np.uint8(np.clip(hdr * 255, 0, 255)))

    def adjust_image(self, image, brightness, contrast, hdr_intensity, red, green, blue, mask=None, hdr_mask=None):
        batch_size, height, width, channels = image.shape
        result = torch.zeros_like(image)
        
        for b in range(batch_size):
            img = image[b].numpy() * 255.0
            img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
            
            # Apply channel adjustments
            if red != 1.0 or green != 1.0 or blue != 1.0:
                r, g, b_channels = img.split()  # Renamed to avoid conflict with loop variable
                if red != 1.0:
                    r = ImageEnhance.Brightness(r).enhance(red)
                if green != 1.0:
                    g = ImageEnhance.Brightness(g).enhance(green)
                if blue != 1.0:
                    b_channels = ImageEnhance.Brightness(b_channels).enhance(blue)
                img = Image.merge("RGB", (r, g, b_channels))
            
            # Apply brightness
            if brightness != 1.0:
                img = ImageEnhance.Brightness(img).enhance(brightness)
            
            # Apply contrast
            if contrast != 1.0:
                img = ImageEnhance.Contrast(img).enhance(contrast)
            
            # Apply HDR effect
            current_hdr_mask = None
            if hdr_mask is not None:
                if hdr_mask.dim() == 2:
                    hdr_mask = hdr_mask.unsqueeze(0)
                current_hdr_mask = hdr_mask[b] if b < hdr_mask.shape[0] else hdr_mask[-1]
                current_hdr_mask = Image.fromarray((current_hdr_mask.numpy() * 255).astype(np.uint8))
            
            if hdr_intensity > 0:
                img = self.apply_hdr(img, hdr_intensity, current_hdr_mask)
            
            # Convert back to tensor and remove the extra batch dimension
            img = np.array(img).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img)
            
            # Apply main mask
            if mask is not None:
                if mask.dim() == 2:
                    mask = mask.unsqueeze(0)
                current_mask = mask[b].unsqueeze(-1) if b < mask.shape[0] else mask[-1].unsqueeze(-1)
                current_mask = current_mask.expand_as(img_tensor)
                img_tensor = image[b] * (1 - current_mask) + img_tensor * current_mask
            
            result[b] = img_tensor
        
        return (result,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "AdvancedColorAdjust": AdvancedColorAdjust
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedColorAdjust": "Advanced Color Adjust (HDR+Channels)"
}
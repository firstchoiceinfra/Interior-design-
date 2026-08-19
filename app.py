import streamlit as st
import replicate
import os

# अपनी Replicate API Key यहाँ डालें (replicate.com से फ्री में मिलती है)
os.environ["REPLICATE_API_TOKEN"] = "r8_YOUR_REPLICATE_API_KEY_HERE"

def generate_real_interior(uploaded_image, sofa_style, mandir_style):
    # 4 अलग-अलग लेआउट्स के प्रॉम्प्ट
    prompts = [
        f"A photorealistic living room interior, perfectly placing {sofa_style} on the east wall, divine {mandir_style} with warm golden lighting in the northeast corner, 8k resolution, architectural photography",
        f"Modern home interior layout, {sofa_style} arranged along the west side, illuminated {mandir_style} on the opposite wall, clean floor plan, warm interior lights",
        f"Spacious hall setup, central cozy placement of {sofa_style}, {mandir_style} in a dedicated serene corner, photorealistic",
        f"Compact elegant arrangement, {sofa_style} against the main wall, wall-mounted backlit {mandir_style}, high-end apartment look"
    ]
    
    generated_images = []
    
    for i, p in enumerate(prompts):
        # Interior AI Model (ControlNet / SDXL Interior Inpainting)
        output = replicate.run(
            "jagil/controlnet-interior-design:latest", # या "stability-ai/sdxl"
            input={
                "image": uploaded_image,
                "prompt": p,
                "negative_prompt": "mountains, nature, outdoor, blurry, bad anatomy, deformed furniture, dark room",
                "structure": "depth",  # कमरे की दीवारों का ढांचा वैसा ही रखेगा
                "num_outputs": 1
            }
        )
        # Replicate से जनरेट हुई असली फोटो का URL
        generated_images.append({
            "title": f"लेआउट #{i+1}",
            "img": output[0] if isinstance(output, list) else output
        })
        
    return generated_images

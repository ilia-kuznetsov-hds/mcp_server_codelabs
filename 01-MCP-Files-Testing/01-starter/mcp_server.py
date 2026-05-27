from fastmcp import FastMCP
from google import genai
from google.genai import types
import io
from PIL import Image
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

mcp = FastMCP("holidays")

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY"))
genai_client = genai.Client(api_key=api_key)
TEXT_MODEL = "gemini-3.5-flash"
IMAGE_MODEL = "imagen-4.0-generate-001"

def generate_image(prompt: str, aspect_ratio: str, output_path: str, input_images=[]):
    """Take a prompt and input images (if any) and generate and 
    save a resulting image using a model."""
    logger.info(f"Generating image with prompt: {prompt[:50]}...")
    logger.info(f"Output path: {output_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    contents = [prompt]
    for image in input_images:
        contents.append(Image.open(image))
    
    # https://ai.google.dev/gemini-api/docs/imagen
    response = genai_client.models.generate_images(
        model=IMAGE_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            output_mime_type="image/png"
        )
    )

    if response.generated_images:
        for generated_image in response.generated_images:
            if hasattr(generated_image.image, 'save'):
                generated_image.image.save(output_path)
            else:
                image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                image.save(output_path)
    else:
        logger.error("No images generated. This could be due to safety filters.")

@mcp.tool
def generate_holiday_scene(interest: str) -> str:
    """
    Generate a holiday scene image

    Args:
        interest: A description of the user's interests (e.g., "birds", "music").
    """
    
    prompt = (
        f"""
        Create a fun, high-fidelity 2D image of a winter holiday scene with Doom Guy from Doom videogame.
        The scene should be warm and inviting with soft cinematic lighting.
        
        Seamlessly integrate the following specific theme/interest into the 
        holiday decor or landscape: {interest}.
        
        The style should be whimsical but detailed.
        Aspect Ratio: 16:9 Landscape 
        """
        )

    generate_image(prompt, "16:9", "static/generated_scene.png")
    return "Done! Saved at generated_scene.png"

@mcp.tool
def generate_sweater_pattern(motif: str) -> str:
    """
    Generate a holidays sweater pattern
    
    Args:
        motif: A description of the pattern on the sweater (e.g., "snowflake pattern", "reindeer pattern").
    """
    prompt = (
        f"""
        Design a seamless, tileable "ugly holiday sweater" pattern.
        The design should mimic a knitted wool texture with visible stitching details.
        Use a chaotic but festive color palette (reds, greens, whites, golds).
        The main motif on the design should be: {motif}
        
        View: Top-down, flat 2D texture map. 
        Do NOT show a shirt, a model, or folds. Show ONLY the rectangular pattern design.
        """
    )
    generate_image(prompt, "1:1", "static/generated_pattern.png")
    return "Done! Saved at generated_pattern.png"


def analyze_person_features(image_path: str) -> str:
    """
    Analyzes an image of a person to extract physical features for a cartoon avatar.
    """
    try:
        logger.info(f"Analyzing person features from: {image_path}")
        if not os.path.exists(image_path):
            logger.warning(f"Image not found for analysis: {image_path}")
            return "a happy person"

        image = Image.open(image_path)
        prompt = """
        Describe the physical appearance of the person in this image specifically for creating a cute, kawaii cartoon avatar.
        Focus on:
        1. Gender and approximate age group (e.g., young boy, woman).
        2. Hair color, length, and style.
        3. Eye color (if visible) and glasses (if worn).
        4. Facial hair (if any).
        5. Distinctive features (e.g., freckles, hat).
        
        Keep the description concise and descriptive (e.g., "a young woman with long brown hair and round glasses").
        Do not describe the clothing or background.
        """
        
        response = genai_client.models.generate_content(
            model=TEXT_MODEL,
            contents=[prompt, image]
        )
        
        if response.text:
            description = response.text.strip()
            logger.info(f"Person description: {description}")
            return description
            
    except Exception as e:
        logger.error(f"Error analyzing person features: {e}")
        
    return "a happy person"

@mcp.tool
def generate_wearing_sweater(image_path: str = None) -> str:
    """
    Generate a cute, kawaii, cartoon-style character wearing a sweater with the specified pattern.
    
    Args:
        image_path: Optional absolute path to an uploaded photo of the user. If provided, the avatar will resemble the user.
    """
    
    person_description = "a Doom Guy from Doom videogame"
    if image_path:
        person_description = analyze_person_features(image_path)
        
    prompt = (
        f"""
        Generate a cute, kawaii, cartoon-style 3D render of {person_description} wearing a knitted sweater.
        
        Sweater Pattern: Use the pattern in the attached image.
        
        Style:
        - Cute, chibi, or cartoon aesthetic.
        - Bright, cheerful colors.
        - Soft lighting, high fidelity 3D render (like a high-quality toy or animation character).
        - The character should be facing the camera.
        - The character should resemble the description: {person_description}
        
        Background: winter-themed hell background that complements the character.
        """
    )
    
    generate_image(prompt, "1:1", "static/generated_selfie.png", ["static/generated_pattern.png"])
    return "Done! Saved at generated_selfie.png"

@mcp.tool
def generate_final_photo() -> str:
    """
    Generate the final photo
    """

    prompt = (
        """
        Generate a photorealistic close-up shot of a rustic wooden fireplace mantle.
        
        Lighting: Warm, glowing ambient light from a fire below (out of frame).
        Background: Softly blurred (bokeh) pine garland and twinkling lights.
        
        Foreground Composition:
        1. A wooden picture frame containing the [attached selfie image]. 
           The face in the photo must be clearly visible.
        2. A folded holiday greeting card standing upright next to the frame. 
           The front of the card displays the [attached holiday scene image] as a print.
           
        Ensure the perspective is grounded and realistic, as if taken with a 50mm lens.
        """
    )
    generate_image(prompt, "16:9", "static/generated_final_photo.png", ["static/generated_selfie.png", "static/generated_scene.png"])
    return "Done! Saved at generated_final_photo.png"
    
    #REPLACE_GENERATE_FINAL_PHOTO

if __name__ == "__main__":
    mcp.run()
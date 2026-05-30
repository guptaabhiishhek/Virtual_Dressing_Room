from PIL import Image

def apply_clothing_with_dynamic_bbox(person_img, cloth_img, scale_factor=1.0, blend_alpha=0.9):
    """
    Apply clothing on the person's upper body by dynamically resizing the clothing based on the person’s size.
    """
    img_width, img_height = person_img.size

    # Estimate upper body area
    upper_body_height = int(0.45 * img_height)
    upper_body_width = int(0.7 * img_width)

    # Resize the clothing image based on scale factor
    cloth_aspect_ratio = cloth_img.width / cloth_img.height
    new_cloth_width = int(upper_body_width * scale_factor)
    new_cloth_height = int(new_cloth_width / cloth_aspect_ratio)

    # Adjust if too tall
    if new_cloth_height > upper_body_height:
        new_cloth_height = int(upper_body_height * scale_factor)
        new_cloth_width = int(new_cloth_height * cloth_aspect_ratio)

    # Resize the clothing image
    cloth_resized = cloth_img.resize((new_cloth_width, new_cloth_height))

    # Position the clothing
    upper_left_x = int((img_width - new_cloth_width) / 2)
    upper_left_y = int(0.25 * img_height)

    # Create an overlay and paste the resized clothing
    overlay = Image.new('RGBA', person_img.size)
    overlay.paste(cloth_resized, (upper_left_x, upper_left_y), cloth_resized)

    # Blend the overlay with the person image
    blended_image = Image.alpha_composite(person_img, overlay).convert('RGBA')
    blended_image = Image.blend(person_img, blended_image, blend_alpha)

    return blended_image


def virtual_tryon(person_image_path, cloth_image_path, output_path, scale_factor=1.0, blend_alpha=0.9):
    """
    Perform virtual try-on by applying a clothing image to a person image.

    Args:
    - person_image_path (str): Path to the person's image.
    - cloth_image_path (str): Path to the clothing image.
    - output_path (str): Path to save the output image with clothing applied.
    - scale_factor (float): Factor to scale the size of the clothing (increase/decrease).
    - blend_alpha (float): Blending factor between person and cloth image.
    """
    from PIL import Image

    # Open the person and cloth images
    person_img = Image.open(person_image_path).convert('RGBA')  # Ensure it's RGBA to allow transparency
    cloth_img = Image.open(cloth_image_path).convert('RGBA')    # Ensure it's RGBA to allow transparency

    # Get person image dimensions and adjust scale_factor dynamically
    img_width, img_height = person_img.size
    if img_width > 500:
        scale_factor = 2.5  # Adjust based on your preference for larger images
    else:
        scale_factor = 1.2  # Adjust for smaller images

    # Apply clothing on the person with the dynamic scaling and blending adjustments
    output_image = apply_clothing_with_dynamic_bbox(person_img, cloth_img, scale_factor, blend_alpha)

    # Convert the output image to RGB before saving (optional, if you don't need transparency)
    output_image = output_image.convert('RGB')

    # Save the result
    output_image.save(output_path)
    print(f"Virtual try-on image saved as '{output_path}'")


import os
import cv2
import numpy as np

def select_test_images(base_dir, num_categories=101):
    """
    Selects one image from each category in Caltech 101.
    Converts to grayscale 8-bit and resizes to 512x512.
    """
    categories = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    # Exclude BACKGROUND_Google if present to stick to 101 object categories
    if "BACKGROUND_Google" in categories:
        categories.remove("BACKGROUND_Google")
    
    # Take up to 101 categories
    categories = categories[:num_categories]
    
    selected_images = []
    
    for cat in categories:
        cat_path = os.path.join(base_dir, cat)
        files = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if files:
            img_path = os.path.join(cat_path, files[0]) # Take the first image
            img = cv2.imread(img_path)
            if img is not None:
                # Convert to grayscale 8-bit
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Resize to standard 512x512 for consistent watermarking
                resized = cv2.resize(gray, (512, 512))
                selected_images.append({
                    "category": cat,
                    "filename": files[0],
                    "image": resized
                })
                
    return selected_images

def attack_jpeg(image, quality=50):
    """
    Simulates JPEG compression attack.
    Encodes to JPEG and decodes back to return the distorted image.
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', image, encode_param)
    decimg = cv2.imdecode(encimg, cv2.IMREAD_GRAYSCALE)
    return decimg

def attack_resize(image):
    """
    Simulates resizing attack: Scale down to 50% and back up to 100%.
    """
    h, w = image.shape
    # Scale down by 50%
    small = cv2.resize(image, (w // 2, h // 2), interpolation=cv2.INTER_LINEAR)
    # Scale back up
    large = cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)
    return large

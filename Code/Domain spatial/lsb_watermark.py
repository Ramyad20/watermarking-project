import cv2
import numpy as np

def string_to_bits(text):
    """Converts a string to a list of bits (0 or 1)."""
    bits = []
    for char in text:
        bin_char = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_char])
    return bits

def bits_to_string(bits):
    """Converts a list of bits back to a string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char_code = int("".join(map(str, byte)), 2)
        chars.append(chr(char_code))
    return "".join(chars)

def int_to_16_bits(n):
    """Converts an integer to a 16-bit list."""
    return [int(b) for b in bin(n)[2:].zfill(16)]

def bits_to_int(bits):
    """Converts a list of bits (max 16) to an integer."""
    return int("".join(map(str, bits)), 2)

def embed_lsb(image, watermark_text):
    """
    Embeds a text watermark into the LSB of the image.
    Following Algorithm 1 from the paper.
    """
    # 1. Preprocess watermark into binary stream B
    data_bits = string_to_bits(watermark_text)
    L_data = len(data_bits)
    
    # 2. Prepend 16-bit header (length of data_bits)
    header_bits = int_to_16_bits(L_data)
    B = header_bits + data_bits
    L = len(B)
    
    # Ensure image is grayscale (as per requirements)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    iw = image.copy()
    h, w = iw.shape
    
    k = 0
    for i in range(h):
        for j in range(w):
            if k < L:
                # Replace LSB
                p = iw[i, j]
                # (p & 0xFE) clears the last bit, then | B[k] sets it to the watermark bit
                iw[i, j] = (p & 0xFE) | B[k]
                k += 1
            else:
                break
        if k >= L:
            break
            
    return iw

def extract_lsb(watermarked_image):
    """
    Extracts a text watermark from the LSB of the image.
    Following Algorithm 2 from the paper.
    """
    # Ensure image is grayscale
    if len(watermarked_image.shape) == 3:
        watermarked_image = cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2GRAY)
        
    iw = watermarked_image
    h, w = iw.shape
    
    # 1. Extract 16-bit header
    header_bits = []
    k = 0
    for i in range(h):
        for j in range(w):
            if k < 16:
                p = iw[i, j]
                header_bits.append(p & 1)
                k += 1
            else:
                break
        if k >= 16:
            break
            
    L_data = bits_to_int(header_bits)
    
    # 2. Extract data bits
    data_bits = []
    count = 0
    # Reset loop to start after header
    # k is already 16, but we need the coordinates
    # We'll just run the same loop logic but skip the first 16 bits
    
    k = 0
    for i in range(h):
        for j in range(w):
            if k < 16:
                k += 1
                continue
            
            if count < L_data:
                p = iw[i, j]
                data_bits.append(p & 1)
                count += 1
                k += 1
            else:
                break
        if count >= L_data:
            break
            
    return bits_to_string(data_bits)

def calculate_nc(original_bits, extracted_bits):
    """
    Calculates Normalized Correlation (NC) between original and extracted bits.
    Formula from paper: NC = 1 - (sum(B(k) ^ B'(k)) / L)
    """
    if len(original_bits) != len(extracted_bits):
        # Pad or truncate if necessary, though they should be same length
        L = min(len(original_bits), len(extracted_bits))
        original_bits = original_bits[:L]
        extracted_bits = extracted_bits[:L]
    else:
        L = len(original_bits)
    
    if L == 0:
        return 0
        
    xor_sum = sum(b1 ^ b2 for b1, b2 in zip(original_bits, extracted_bits))
    return 1 - (xor_sum / L)

if __name__ == "__main__":
    # Simple test
    test_img = np.full((100, 100), 128, dtype=np.uint8)
    watermark = "document"
    
    marked_img = embed_lsb(test_img, watermark)
    extracted = extract_lsb(marked_img)
    
    print(f"Original: {watermark}")
    print(f"Extracted: {extracted}")
    
    orig_bits = string_to_bits(watermark)
    extr_bits = string_to_bits(extracted)
    nc = calculate_nc(orig_bits, extr_bits)
    print(f"NC: {nc:.4f}")
    
    assert watermark == extracted, "Extraction failed!"
    assert nc == 1.0, "NC should be 1.0 for perfect extraction"
    print("Success!")

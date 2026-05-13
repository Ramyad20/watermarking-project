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

def generate_dft_coords(shape, num_bits, seed=42):
    """
    Generates unique, conjugate-symmetric coordinates in the mid-frequency band.
    Ensures that if (u, v) is picked, its conjugate (H-u, W-v) is handled.
    Uses permutation to ensure the first N coordinates are consistent regardless of num_bits.
    """
    h, w = shape
    rng = np.random.default_rng(seed)
    
    # Define mid-frequency band as an annulus
    # For a 512x512 image, center is at (256, 256) if shifted.
    # Without shift, DC is at (0,0).
    # We'll pick coordinates (u, v) such that they are in the "mid" frequencies.
    # To maintain symmetry and avoid DC/Nyquist:
    # We only pick from the top half (u < h/2) and exclude u=0.
    
    all_possible = []
    # Annulus-like selection in the unshifted spectrum
    for u in range(1, h // 2):
        for v in range(w):
            # Distance from DC (0,0) - considering wrap around
            dist_u = min(u, h - u)
            dist_v = min(v, w - v)
            dist = np.sqrt(dist_u**2 + dist_v**2)
            
            # Mid-frequency band: e.g., radius between 30 and 200
            if 30 <= dist <= 200:
                all_possible.append((u, v))
            
    if len(all_possible) < num_bits:
        raise ValueError(f"Not enough space in mid-frequency band. Need {num_bits}, have {len(all_possible)}")
        
    # Use permutation to ensure consistency
    indices = rng.permutation(len(all_possible))
    selected = [all_possible[i] for i in indices[:num_bits]]
    
    return selected

def embed_dft(image, watermark_text, alpha=0.1):
    """
    Embeds a text watermark into the DFT magnitudes.
    Following Algorithm 3 from the paper.
    """
    # 1. Preprocess watermark
    data_bits = string_to_bits(watermark_text)
    header_bits = int_to_16_bits(len(data_bits))
    B = header_bits + data_bits
    L = len(B)
    
    # Ensure grayscale and resize to 512x512 as per paper
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if image.shape != (512, 512):
        image = cv2.resize(image, (512, 512))
        
    img_float = image.astype(np.float64) / 255.0
    
    # 3. F = fft2(img)
    F = np.fft.fft2(img_float)
    
    # 4. Mag = |F|, 5. Phase = angle(F)
    mag = np.abs(F)
    phase = np.angle(F)
    
    # 6. Generate coordinates
    coords = generate_dft_coords(image.shape, L, seed=42)
    
    h, w = image.shape
    
    # 8-15. Modulate magnitudes
    for k in range(L):
        u, v = coords[k]
        # Symmetric coordinate for real-valued inverse FFT
        u_sym, v_sym = (h - u) % h, (w - v) % w
        
        if B[k] == 1:
            mag[u, v] *= (1 + alpha)
            mag[u_sym, v_sym] *= (1 + alpha)
        else:
            mag[u, v] *= (1 - alpha)
            mag[u_sym, v_sym] *= (1 - alpha)
            
    # 16. Fw = Mag * exp(j * Phase)
    Fw = mag * np.exp(1j * phase)
    
    # 17. Iw = real(ifft2(Fw))
    iw_float = np.real(np.fft.ifft2(Fw))
    
    # 18. Iw = im2uint8(Iw)
    iw = np.clip(iw_float * 255.0, 0, 255).astype(np.uint8)
    
    return iw

def extract_dft(watermarked_image, original_image, alpha=0.1):
    """
    Extracts a text watermark from the DFT magnitudes.
    Following Algorithm 4 from the paper. (Non-blind)
    """
    # Ensure grayscale
    if len(watermarked_image.shape) == 3:
        watermarked_image = cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2GRAY)
    if len(original_image.shape) == 3:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        
    # Normalize
    iw_float = watermarked_image.astype(np.float64) / 255.0
    io_float = original_image.astype(np.float64) / 255.0
    
    # 3-4. FFT of both
    Fw = np.fft.fft2(iw_float)
    Fo = np.fft.fft2(io_float)
    
    mag_w = np.abs(Fw)
    mag_o = np.abs(Fo)
    
    # First, we need to know the length. 
    # Extract 16-bit header first.
    h, w = watermarked_image.shape
    header_coords = generate_dft_coords((h, w), 16, seed=42)
    
    header_bits = []
    for u, v in header_coords:
        if mag_w[u, v] > mag_o[u, v]:
            header_bits.append(1)
        else:
            header_bits.append(0)
            
    L_data = bits_to_int(header_bits)
    # Sanity check: L_data shouldn't be larger than available space
    # Max bits for "document" is 64, but let's cap at 1000 for safety
    if L_data > 1000:
        L_data = 1000
        
    L_total = 16 + L_data
    
    # Now generate all coordinates
    all_coords = generate_dft_coords((h, w), L_total, seed=42)
    data_bits = []
    
    for k in range(16, L_total):
        u, v = all_coords[k]
        if mag_w[u, v] > mag_o[u, v]:
            data_bits.append(1)
        else:
            data_bits.append(0)
            
    return bits_to_string(data_bits)

def calculate_nc(original_bits, extracted_bits):
    """
    Calculates Normalized Correlation (NC) between original and extracted bits.
    """
    L = min(len(original_bits), len(extracted_bits))
    if L == 0: return 0
    xor_sum = sum(b1 ^ b2 for b1, b2 in zip(original_bits[:L], extracted_bits[:L]))
    return 1 - (xor_sum / L)

if __name__ == "__main__":
    # Test with a real-ish image size
    test_img = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
    watermark = "document" # Paper uses "document"
    
    alpha = 0.1
    marked_img = embed_dft(test_img, watermark, alpha=alpha)
    extracted = extract_dft(marked_img, test_img, alpha=alpha)
    
    print(f"Original: {watermark}")
    print(f"Extracted: {extracted}")
    
    orig_bits = string_to_bits(watermark)
    extr_bits = string_to_bits(extracted)
    nc = calculate_nc(orig_bits, extr_bits)
    print(f"NC: {nc:.4f}")
    
    assert watermark == extracted, "Extraction failed!"
    print("Success!")

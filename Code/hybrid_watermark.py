import numpy as np
import cv2
import sys
import os

# Ensure paths for imports
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain spatial'))
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain frequency'))

from lsb_watermark import embed_lsb, extract_lsb, string_to_bits as s2b_lsb, calculate_nc as nc_lsb
from dft_watermark import embed_dft, extract_dft, string_to_bits as s2b_dft, calculate_nc as nc_dft

def embed_hybrid(image, watermark_text, alpha=0.1):
    """
    Hybrid Embedding: Embeds watermark in DFT domain first, 
    then embeds the same watermark in LSB of the result.
    """
    # 1. Embed in Frequency Domain (DFT)
    dft_marked = embed_dft(image, watermark_text, alpha=alpha)
    
    # 2. Embed in Spatial Domain (LSB)
    hybrid_marked = embed_lsb(dft_marked, watermark_text)
    
    return hybrid_marked

def extract_hybrid(watermarked_image, original_image, alpha=0.1):
    """
    Hybrid Extraction: Extracts from both domains and returns both.
    The caller can then decide how to evaluate (e.g., max NC).
    """
    # 1. Extract from Spatial Domain (LSB)
    text_lsb = extract_lsb(watermarked_image)
    
    # 2. Extract from Frequency Domain (DFT)
    text_dft = extract_dft(watermarked_image, original_image, alpha=alpha)
    
    return text_lsb, text_dft

def calculate_hybrid_nc(orig_bits, extr_text_lsb, extr_text_dft):
    """
    Calculates the best NC between the two domains.
    """
    nc1 = nc_lsb(orig_bits, s2b_lsb(extr_text_lsb))
    nc2 = nc_dft(orig_bits, s2b_dft(extr_text_dft))
    return max(nc1, nc2)

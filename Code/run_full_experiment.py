import os
import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim
import sys

# Add subdirectories to path to import watermark modules
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain spatial'))
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain frequency'))

from lsb_watermark import embed_lsb, extract_lsb, calculate_nc as nc_lsb, string_to_bits as s2b_lsb
from dft_watermark import embed_dft, extract_dft, calculate_nc as nc_dft, string_to_bits as s2b_dft
from hybrid_watermark import embed_hybrid, extract_hybrid, calculate_hybrid_nc
from pipeline_utils import select_test_images, attack_jpeg, attack_resize

def run_experiment():
    dataset_path = 'caltech-101/101_ObjectCategories'
    watermark_text = "document"
    orig_bits = s2b_lsb(watermark_text) # same for both
    
    print("Selecting 101 images from dataset...")
    test_set = select_test_images(dataset_path)
    
    results = []
    
    for i, data in enumerate(test_set):
        cat = data['category']
        img = data['image']
        print(f"[{i+1}/101] Processing category: {cat}")
        
        # --- Algorithm 1: LSB (Spatial) ---
        marked_lsb = embed_lsb(img, watermark_text)
        ssim_lsb = ssim(img, marked_lsb)
        
        # JPEG Attack
        jpg_lsb = attack_jpeg(marked_lsb, quality=50)
        extr_jpg_lsb = extract_lsb(jpg_lsb)
        nc_jpg_lsb = nc_lsb(orig_bits, s2b_lsb(extr_jpg_lsb))
        
        # Resize Attack
        res_lsb = attack_resize(marked_lsb)
        extr_res_lsb = extract_lsb(res_lsb)
        nc_res_lsb = nc_lsb(orig_bits, s2b_lsb(extr_res_lsb))
        
        # --- Algorithm 2: DFT (Frequency) ---
        marked_dft = embed_dft(img, watermark_text, alpha=0.1)
        ssim_dft = ssim(img, marked_dft)
        
        # JPEG Attack
        jpg_dft = attack_jpeg(marked_dft, quality=50)
        extr_jpg_dft = extract_dft(jpg_dft, img, alpha=0.1)
        nc_jpg_dft = nc_dft(orig_bits, s2b_dft(extr_jpg_dft))
        
        # Resize Attack
        res_dft = attack_resize(marked_dft)
        extr_res_dft = extract_dft(res_dft, img, alpha=0.1)
        nc_res_dft = nc_dft(orig_bits, s2b_dft(extr_res_dft))

        # --- Algorithm 3: Hybrid (Spatial + Frequency) ---
        marked_hyb = embed_hybrid(img, watermark_text, alpha=0.1)
        ssim_hyb = ssim(img, marked_hyb)

        # JPEG Attack
        jpg_hyb = attack_jpeg(marked_hyb, quality=50)
        extr_jpg_hyb_lsb, extr_jpg_hyb_dft = extract_hybrid(jpg_hyb, img, alpha=0.1)
        nc_jpg_hyb = calculate_hybrid_nc(orig_bits, extr_jpg_hyb_lsb, extr_jpg_hyb_dft)

        # Resize Attack
        res_hyb = attack_resize(marked_hyb)
        extr_res_hyb_lsb, extr_res_hyb_dft = extract_hybrid(res_hyb, img, alpha=0.1)
        nc_res_hyb = calculate_hybrid_nc(orig_bits, extr_res_hyb_lsb, extr_res_hyb_dft)
        
        results.append({
            'Category': cat,
            'SSIM_LSB': ssim_lsb,
            'NC_JPEG_LSB': nc_jpg_lsb,
            'NC_Resize_LSB': nc_res_lsb,
            'SSIM_DFT': ssim_dft,
            'NC_JPEG_DFT': nc_jpg_dft,
            'NC_Resize_DFT': nc_res_dft,
            'SSIM_Hybrid': ssim_hyb,
            'NC_JPEG_Hybrid': nc_jpg_hyb,
            'NC_Resize_Hybrid': nc_res_hyb
        })
        
    df = pd.DataFrame(results)
    df.to_csv('experiment_results.csv', index=False)
    
    # Calculate Mean and Variance
    metrics_list = ['SSIM', 'NC_JPEG', 'NC_Resize']
    stats_data = {'Metric': metrics_list}
    
    for alg in ['LSB', 'DFT', 'Hybrid']:
        stats_data[f'Mean_{alg}'] = [df[f'{m}_{alg}'].mean() for m in metrics_list]
        stats_data[f'Var_{alg}'] = [df[f'{m}_{alg}'].var() for m in metrics_list]
    
    df_stats = pd.DataFrame(stats_data)
    df_stats.to_csv('experiment_stats.csv', index=False)
    
    print("\nExperiment Complete. Summary Statistics:")
    print(df_stats)

if __name__ == "__main__":
    run_experiment()

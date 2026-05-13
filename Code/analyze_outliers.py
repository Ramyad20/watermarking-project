import pandas as pd
import cv2
import os
import sys
import numpy as np

# Add subdirectories to path to import watermark modules
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain spatial'))
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Domain frequency'))

from lsb_watermark import embed_lsb, extract_lsb
from dft_watermark import embed_dft, extract_dft
from hybrid_watermark import embed_hybrid, extract_hybrid
from pipeline_utils import attack_jpeg, attack_resize, select_test_images

def analyze_specific_outliers():
    results_csv = 'experiment_results.csv'
    if not os.path.exists(results_csv):
        print("Run experiment first.")
        return

    df = pd.read_csv(results_csv)
    
    # 1. Find catastrophic failures in Resize
    resize_outliers = df[df['NC_Resize_Hybrid'] < 0.1]['Category'].tolist()
    
    # 2. Find lowest SSIM (highest distortion)
    ssim_outliers = df.nsmallest(2, 'SSIM_Hybrid')['Category'].tolist()
    
    # 3. Find lowest JPEG robustness
    jpeg_outliers = df.nsmallest(2, 'NC_JPEG_Hybrid')['Category'].tolist()

    target_categories = list(set(resize_outliers + ssim_outliers + jpeg_outliers))
    
    print(f"Analyzing {len(target_categories)} outlier categories: {target_categories}")
    
    # Reload images
    dataset_path = 'caltech-101/101_ObjectCategories'
    test_set = select_test_images(dataset_path)
    
    outlier_dir = 'outlier_analysis'
    if not os.path.exists(outlier_dir):
        os.makedirs(outlier_dir)

    report = []
    report.append("# Outlier Analysis Report\n")
    report.append("This report analyzes images where the Hybrid technique performed poorly.\n")

    for cat in target_categories:
        data = next((item for item in test_set if item['category'] == cat), None)
        if not data: continue
        
        img = data['image']
        watermark_text = "document"
        
        # Save original
        cv2.imwrite(f"{outlier_dir}/{cat}_orig.png", img)
        
        # Hybrid embedding
        marked = embed_hybrid(img, watermark_text)
        cv2.imwrite(f"{outlier_dir}/{cat}_watermarked.png", marked)
        
        # Attacks
        jpg = attack_jpeg(marked, quality=50)
        res = attack_resize(marked)
        cv2.imwrite(f"{outlier_dir}/{cat}_attack_jpeg.png", jpg)
        cv2.imwrite(f"{outlier_dir}/{cat}_attack_resize.png", res)
        
        # Analysis of image characteristics
        brightness = np.mean(img)
        contrast = np.std(img)
        # Simple edge density (Laplacian variance)
        edges = cv2.Laplacian(img, cv2.CV_64F).var()
        
        row = df[df['Category'] == cat].iloc[0]
        
        report.append(f"## Category: {cat}")
        report.append(f"- **SSIM**: {row['SSIM_Hybrid']:.4f}")
        report.append(f"- **NC JPEG**: {row['NC_JPEG_Hybrid']:.4f}")
        report.append(f"- **NC Resize**: {row['NC_Resize_Hybrid']:.4f}")
        report.append(f"- **Brightness**: {brightness:.2f}")
        report.append(f"- **Contrast (StdDev)**: {contrast:.2f}")
        report.append(f"- **Edge Density (Laplacian Var)**: {edges:.2f}")
        
        if row['NC_Resize_Hybrid'] < 0.1:
            report.append("- **Note**: Catastrophic Resize failure. High edge density or specific textures might be interfering with frequency stability after interpolation.")
        if row['SSIM_Hybrid'] < 0.995:
            report.append("- **Note**: Relatively low SSIM. Likely due to smooth background where watermark patterns are more visible.")
            
        report.append("\n---\n")

    with open(f"{outlier_dir}/ANALYSIS.md", "w") as f:
        f.writelines([line + "\n" for line in report])
    
    print(f"Analysis complete. See '{outlier_dir}/ANALYSIS.md' and images in that folder.")

if __name__ == "__main__":
    analyze_specific_outliers()

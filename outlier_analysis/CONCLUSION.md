# Conclusion: Understanding Watermark Recovery across Domains

This analysis evaluates the performance of three watermarking "ideas" (LSB, DFT, and Hybrid) across a diverse dataset (Caltech-101) to understand why robustness varies.

## 1. The Core Differences in "Ideas"

| Technique | Domain | Mechanism | Primary Strength | Primary Weakness |
| :--- | :--- | :--- | :--- | :--- |
| **LSB Substitution** | Spatial | Replaces the least significant bit of pixels. | High imperceptibility (SSIM ≈ 1.0). | Extremely fragile; nearly 0 robustness against JPEG. |
| **DFT Modulation** | Frequency | Modulates magnitudes of mid-frequency coefficients. | High robustness against JPEG compression. | Sensitive to geometric transformations (Resizing). |
| **Hybrid Technique** | Combined | DFT modulation followed by LSB substitution. | Best of both worlds; higher average NC and lower variance. | Slightly higher complexity; same frequency limitations as DFT. |

## 2. Impact of Image Characteristics

Our analysis reveals that image features significantly influence watermark survival:

### A. Edge Density (Laplacian Variance)
- **JPEG Robustness (Positive Correlation)**: Images with high edge density (e.g., *Dragonfly*, *Accordion*) provide a "richer" frequency spectrum that supports the DFT watermark. The quantization noise of JPEG is less disruptive in these "busy" regions.
- **Resize Robustness (Negative Correlation)**: High-frequency textures are the first to be distorted by interpolation during resizing. Catastrophic failures (NC=0) were observed in high-texture images like *Accordion* and *Pigeon*.

### B. Texture Complexity (Entropy)
- **Imperceptibility (Positive Correlation)**: High entropy images (complex textures) are better at "hiding" the watermark signal. SSIM remains higher because the artificial changes blend in with the natural "noise" of the image.
- **LSB Survival**: Surprisingly, higher entropy slightly correlates with better LSB survival, likely because the LSB changes are less distinguishable from the existing pixel variation.

### C. Smooth vs. Busy Backgrounds
- **Smooth Images** (e.g., *Sea Horse*): Often result in lower SSIM because watermark patterns (especially from DFT) become visible as "ghosting" or "halos" in uniform areas.

## 3. Why the Hybrid Technique Wins
The Hybrid technique achieved the highest mean NC for Resizing (**0.556**) compared to LSB (**0.432**) and DFT (**0.410**). 

**Key takeaway**: By embedding in both domains, the Hybrid method ensures that even if the frequency spectrum is shifted (Resize attack) or the LSBs are wiped (JPEG attack), there is a "fallback" recovery path. The significant reduction in NC variance (**0.017** for Hybrid vs **0.068** for DFT) proves that the Hybrid approach is far more consistent across different image categories.

## 4. Final Verdict
The difference in watermark recovery is a trade-off between **Local Precision (Spatial)** and **Global Stability (Frequency)**. 
- Use **Spatial (LSB)** if visual quality is the absolute priority and no attacks are expected.
- Use **Frequency (DFT)** for robust copyright protection against compression.
- Use **Hybrid** for a versatile solution that mitigates the specific weaknesses of each individual domain.

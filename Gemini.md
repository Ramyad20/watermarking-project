# Projeto Final: Técnicas de Marcação Digital em Imagem

## 📌 Project Overview
This project evaluates and compares the robustness and visual imperceptibility of two digital image watermarking techniques: a Spatial Domain method and a Frequency Domain method. [cite_start]The testing pipeline evaluates how well the hidden watermarks survive common image distortions[cite: 94].

## 📊 Dataset Requirements
* [cite_start]**Source:** Caltech 101[cite: 116].
* [cite_start]**Subset:** Exactly 101 images (one from each category)[cite: 117].
* [cite_start]**Preprocessing:** All images must be converted to 8-bit grayscale[cite: 118].

## ⚙️ Algorithms to Implement

### 1. Spatial Domain: Least Significant Bit (LSB) Substitution
* **Reference:** "Robustness and Imperceptibility Analysis of Hybrid Spatial-Frequency Domain Image Watermarking" (Anam, 2024).
* [cite_start]**Concept:** Directly modifies the pixel values of the host image[cite: 1082]. 
* [cite_start]**Mechanism:** Converts the watermark text into a binary stream and replaces the least significant bit of each target pixel with a watermark bit[cite: 1083].

### 2. Frequency Domain: Discrete Cosine Transform (DCT) LSB Modulation
* **Reference:** "Digital image watermarking using discrete cosine transformation based linear modulation" (Alomoush et al., 2023).
* [cite_start]**Concept:** Embeds information into the transformation domain of grayscale images[cite: 181].
* [cite_start]**Mechanism:** Divides the image into non-overlapping 8x8 blocks, applies the DCT, quantizes the coefficients, and embeds the watermark bits into the LSBs of the middle-frequency coefficients[cite: 307, 436].

## 🧪 Testing Pipeline
For each of the 101 test images, the CLI pipeline must execute the following sequence for BOTH algorithms:

1. [cite_start]**Embedding:** Insert the standard digital watermark into the original image[cite: 121].
2. [cite_start]**Quality Metric (Imperceptibility):** Calculate the SSIM (Structural Similarity Index) between the watermarked image and the original image[cite: 123].
3. [cite_start]**Attack 1 - JPEG Compression:** * Compress the watermarked image using JPEG at **50% quality**[cite: 125].
    * [cite_start]Decompress, extract the watermark, and calculate the Normalized Correlation (NC) with the original mark[cite: 125, 126].
4. **Attack 2 - Resizing:**
    * [cite_start]Reduce the watermarked image dimensions by exactly half (50%)[cite: 128].
    * [cite_start]Scale the image back up to its original resolution[cite: 128].
    * [cite_start]Extract the watermark and calculate the Normalized Correlation (NC)[cite: 129].

## 💻 Recommended Python Stack
To implement the mathematical algorithms and image processing attacks outlined in the papers, ensure the following dependencies are installed:

```bash
pip install numpy opencv-python scikit-image scipy matplotlib
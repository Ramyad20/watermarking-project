# User Guide: Watermarking Experiment Dashboard

This guide will help you navigate and use the application to evaluate digital image watermarking techniques.

## Navigation Overview

The application is divided into three main sections, accessible via the sidebar on the left:

1.  **Run Pipeline**: The execution hub.
2.  **Overall Results**: The performance dashboard.
3.  **Outlier Analysis**: The detailed investigation tool.

---

## 1. Run Pipeline
This is where you start the experiment.

- **Purpose**: Executes the full end-to-end testing sequence.
- **Process**:
    - **Phase 1**: Embeds watermarks in 101 images and applies JPEG/Resize attacks.
    - **Phase 2**: Generates statistical comparison charts.
    - **Phase 3**: Identifies failing categories and generates the outlier report.

- **How to use**:
    1. Click the **"Run Full Experiment"** button.
    2. Monitor the **"Process Logs"** section. You will see a real-time terminal-like output showing which image is being processed and which phase is currently active.
---

## 2. Overall Results
View the high-level performance of the LSB, DFT, and Hybrid algorithms.

- **Summary Statistics**: A table showing the **Mean** and **Variance** for SSIM (Visual Quality) and NC (Robustness).
- **Comparison Visualizations**:
    - **Boxplots**: Show the distribution of scores across all 101 images. Useful for spotting consistency.
    - **Bar Chart**: Shows the average performance side-by-side.

---

## 3. Outlier Analysis
Deep dive into the specific images where the watermarks failed or visual quality was lower.

- **Category Selector**: Use the dropdown menu to select a specific category (e.g., *accordion*, *pigeon*).

- **Visual Comparison**: A 4-column grid showing:
    1. **Original**: The source image.
    2. **Watermarked**: The result of the Hybrid embedding.
    3. **JPEG Attack**: The image after 50% compression.
    4. **Resize Attack**: The image after 50% scaling.
- **Metrics & Findings**: Displays specific data for that image, including:
    - **Brightness** and **Contrast**.
    - **Edge Density**: High values often explain failures in Resizing.
    - **Expert Notes**: Textual explanation of why this specific image was an outlier.
- **Global Insights**: Expand the bottom section to read the final scientific **Conclusions** and **Correlations** derived from the entire experiment.

---

## Troubleshooting

- **"No results found"**: You need to go to the **Run Pipeline** tab and execute the experiment first.
- **Logs not showing**: Ensure you are not running multiple experiments simultaneously.
- **Missing images**: Verify that the `caltech-101/` dataset is in the root directory of the project.

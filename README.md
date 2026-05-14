# Watermarking Experiment Project

This project evaluates and compares three digital image watermarking techniques: **LSB (Spatial Domain)**, **DFT (Frequency Domain)**, and a **Hybrid Approach**. It uses the Caltech-101 dataset for testing robustness against JPEG compression and Resizing attacks.


## Project Structure
- `Code/`: Contains the implementation of watermarking algorithms and utility scripts.
- `caltech-101/`: The source dataset (ensure this folder exists before running).
- `specs/`: Specifications of this project, including paper methods.
- `plots/`: Generated charts comparing SSIM and NC metrics.
- `outlier_analysis/`: Detailed investigation into catastrophic failures.
- `app.py`: The Streamlit GUI application.
- `requirements.txt`: List of required Python packages.
- `experiment_<x>`: CSVs containing global results.



## Environment Setup

To ensure all dependencies are correctly installed, it is recommended to use a Python virtual environment. You can use **Python 3.11+**, but recommended is 3.11

### 1. Create a Virtual Environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### 2. Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2.1. Deactivate the Virtual Environment (only after running the code)
```bash
deactivate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### Option A: Unified Graphical Interface (Recommended)
Launch the interactive dashboard in the Virtual Environment to run experiments and visualize results in one place.
```bash
streamlit run app.py
```
*   **Run Pipeline**: Execute the full testing sequence.
*   **Overall Results**: View boxplots and summary statistics.
*   **Outlier Analysis**: Interactively explore specific image categories that failed.

### Option B: Manual Execution (Command Line)
If you prefer to run the components individually without the GUI:

1.  **Run the core experiment**:
    ```bash
    python Code/run_full_experiment.py
    ```
    *This generates `experiment_results.csv` and `experiment_stats.csv`.*

2.  **Generate visualizations**:
    ```bash
    python Code/visualize_results.py
    ```
    *This populates the `plots/` directory with comparison charts.*

3.  **Perform outlier analysis**:
    ```bash
    python Code/analyze_outliers.py
    ```
    *This generates the `outlier_analysis/` folder with detailed reports and images.*

## User Guide

Explanations on how to analyze and verify the workflow, check [USER_GUIDE.md](USER_GUIDE.md).

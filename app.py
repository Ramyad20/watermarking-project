import streamlit as st
import pandas as pd
import os
import sys
import io
import contextlib
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Watermarking Experiment Dashboard",
    page_icon="🖼️",
    layout="wide"
)

# Custom context manager to capture stdout for the UI
class StreamToStreamlit:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.buffer = io.StringIO()

    def write(self, data):
        self.buffer.write(data)
        self.placeholder.code(self.buffer.getvalue())

    def flush(self):
        pass

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Run Pipeline", "Overall Results", "Outlier Analysis"])

def run_full_pipeline(log_placeholder):
    st.info("Starting the full experiment pipeline. This may take a few minutes...")
    
    # Redirect stdout to the placeholder
    with contextlib.redirect_stdout(StreamToStreamlit(log_placeholder)):
        # Run Experiment
        print("--- PHASE 1: EMBEDDING & ATTACKS ---")
        try:
            # Adding Code directory to sys.path to import modules
            if os.path.join(os.getcwd(), 'Code') not in sys.path:
                sys.path.append(os.path.join(os.getcwd(), 'Code'))
            from run_full_experiment import run_experiment
            run_experiment()
            print("\n--- PHASE 1 COMPLETE ---\n")
        except Exception as e:
            st.error(f"Error during experiment: {e}")
            return

        # Run Visualizations
        print("--- PHASE 2: GENERATING VISUALIZATIONS ---")
        try:
            from visualize_results import generate_visualizations
            generate_visualizations()
            print("\n--- PHASE 2 COMPLETE ---\n")
        except Exception as e:
            st.error(f"Error during visualization: {e}")
            return

        # Run Outlier Analysis
        print("--- PHASE 3: ANALYZING OUTLIERS ---")
        try:
            from analyze_outliers import analyze_specific_outliers
            analyze_specific_outliers()
            print("\n--- PHASE 3 COMPLETE ---\n")
        except Exception as e:
            st.error(f"Error during outlier analysis: {e}")
            return

    st.success("Full pipeline executed successfully!")

if page == "Run Pipeline":
    st.title("Run Experiment Pipeline")
    st.markdown("""
    #### This section executes the entire watermarking evaluation pipeline:
                
    
    * ##### **Phase 1.** **Embedding & Attacks**: Processes 101 images from Caltech-101 using LSB, DFT, and Hybrid methods.

    * ##### **Phase 2.** **Visualization**: Generates boxplots and bar charts comparing the performance.
    
    * ##### **Phase 3.** **Outlier Analysis**: Identifies categories with high failure rates and generates detailed reports.
    """)
    
    if st.button("Run Full Experiment", type="primary"):
        st.subheader("Process Logs")
        log_placeholder = st.empty()
        run_full_pipeline(log_placeholder)

elif page == "Overall Results":
    st.title("Overall Performance Results")
    
    if os.path.exists('experiment_stats.csv'):
        st.subheader("Summary Statistics")
        stats_df = pd.read_csv('experiment_stats.csv')
        st.dataframe(stats_df.style.highlight_max(axis=1, subset=[col for col in stats_df.columns if 'Mean' in col], color='grey'))
        
        st.divider()
        
        st.subheader("Comparison Visualizations")
        plot_dir = 'plots'
        if os.path.exists(plot_dir):
            plots = [f for f in os.listdir(plot_dir) if f.endswith('.png')]
            cols = st.columns(2)
            for i, plot_file in enumerate(plots):
                with cols[i % 2]:
                    st.image(os.path.join(plot_dir, plot_file), caption=plot_file.replace('_', ' ').replace('.png', '').title())
        else:
            st.warning("No plots found. Please run the pipeline first.")
    else:
        st.warning("No results found. Please run the pipeline in the 'Run Pipeline' tab.")

elif page == "Outlier Analysis":
    st.title("Outlier Deep Dive")
    
    outlier_dir = 'outlier_analysis'
    if os.path.exists(outlier_dir):
        # Find all categories by looking at _orig.png files
        categories = sorted(list(set([f.split('_orig.png')[0] for f in os.listdir(outlier_dir) if f.endswith('_orig.png')])))
        
        if categories:
            selected_cat = st.selectbox("Select an Outlier Category", categories)
            
            # Display Images
            st.subheader(f"Visual Analysis: {selected_cat.replace('_', ' ').title()}")
            img_cols = st.columns(4)
            
            image_types = [
                ("_orig.png", "Original Image"),
                ("_watermarked.png", "Watermarked (Hybrid)"),
                ("_attack_jpeg.png", "After JPEG Attack"),
                ("_attack_resize.png", "After Resize Attack")
            ]
            
            for col, (suffix, title) in zip(img_cols, image_types):
                img_path = os.path.join(outlier_dir, f"{selected_cat}{suffix}")
                if os.path.exists(img_path):
                    col.image(img_path, caption=title, width="stretch")
            
            st.divider()
            
            # Parse Analysis.md for this category
            analysis_path = os.path.join(outlier_dir, 'ANALYSIS.md')
            if os.path.exists(analysis_path):
                with open(analysis_path, 'r') as f:
                    content = f.read()
                
                # Simple extraction of the category section
                sections = content.split('## Category: ')
                for section in sections:
                    if section.startswith(selected_cat):
                        st.markdown(f"## Metrics & Findings From Deep Dive Outlier Analysis")
                        # Skip the first line which is the category name
                        clean_section = '\n'.join(section.split('\n')[1:])
                        st.markdown(clean_section)
                        break
            
            st.divider()

            # Global Insights
            st.header("Global Insights & Conclusions")
            col1, col2 = st.columns(2)

            with col1:
                if os.path.exists(os.path.join(outlier_dir, 'CORRELATIONS.md')):
                    with open(os.path.join(outlier_dir, 'CORRELATIONS.md'), 'r') as f:
                        st.markdown(f.read())

            with col2:
                if os.path.exists(os.path.join(outlier_dir, 'CONCLUSION.md')):
                    with open(os.path.join(outlier_dir, 'CONCLUSION.md'), 'r') as f:
                        st.markdown(f.read())

        else:
            st.warning("No outlier data found. Please run the pipeline first.")
    else:
        st.warning("Outlier analysis directory not found. Please run the pipeline.")

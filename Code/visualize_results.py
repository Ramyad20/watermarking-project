import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_visualizations(results_csv='experiment_results.csv', output_dir='plots'):
    if not os.path.exists(results_csv):
        print(f"Error: {results_csv} not found. Please run the experiment first.")
        return

    # Clear existing plots
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            if f.endswith('.png'):
                os.remove(os.path.join(output_dir, f))
    else:
        os.makedirs(output_dir)

    df = pd.read_csv(results_csv)

    # Set aesthetic style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 12})

    metrics = [
        ('SSIM', 'SSIM_LSB', 'SSIM_DFT', 'SSIM_Hybrid'),
        ('NC_JPEG', 'NC_JPEG_LSB', 'NC_JPEG_DFT', 'NC_JPEG_Hybrid'),
        ('NC_Resize', 'NC_Resize_LSB', 'NC_Resize_DFT', 'NC_Resize_Hybrid')
    ]

    for title, lsb_col, dft_col, hyb_col in metrics:
        plt.figure(figsize=(12, 7))
        
        # Melt the dataframe for Seaborn boxplot
        plot_df = df[[lsb_col, dft_col, hyb_col]].melt(var_name='Algorithm', value_name=title)
        plot_df['Algorithm'] = plot_df['Algorithm'].map({
            lsb_col: 'Spatial (LSB)', 
            dft_col: 'Frequency (DFT)',
            hyb_col: 'Hybrid (LSB+DFT)'
        })

        sns.boxplot(x='Algorithm', y=title, data=plot_df, palette='Set2', width=0.5)
        sns.stripplot(x='Algorithm', y=title, data=plot_df, color=".3", alpha=0.4)
        
        plt.title(f'Comparison of {title}: Spatial vs Frequency vs Hybrid', fontweight='bold')
        plt.ylabel(f'{title} Score')
        plt.xlabel('Algorithm Type')
        
        # Save plot
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{title.lower()}_comparison.png', dpi=300)
        plt.close()
        print(f"Generated {title} comparison plot in '{output_dir}/'.")

    # Generate a summary bar chart for means from experiment_stats.csv if it exists
    stats_csv = 'experiment_stats.csv'
    if os.path.exists(stats_csv):
        stats_df = pd.read_csv(stats_csv)
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 7))
        
        # Prepare data for plotting
        bar_data = []
        for _, row in stats_df.iterrows():
            bar_data.append({'Metric': row['Metric'], 'Score': row['Mean_LSB'], 'Algorithm': 'Spatial (LSB)'})
            bar_data.append({'Metric': row['Metric'], 'Score': row['Mean_DFT'], 'Algorithm': 'Frequency (DFT)'})
            bar_data.append({'Metric': row['Metric'], 'Score': row['Mean_Hybrid'], 'Algorithm': 'Hybrid (LSB+DFT)'})
        
        summary_df = pd.DataFrame(bar_data)
        
        sns.barplot(x='Metric', y='Score', hue='Algorithm', data=summary_df, palette='Set2')
        
        plt.title('Average Performance Metrics Comparison', fontweight='bold')
        plt.ylim(0, 1.1)
        plt.ylabel('Mean Score')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Modern and reliable way to label bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.3f', padding=3)

        plt.tight_layout()
        plt.savefig(f'{output_dir}/summary_metrics_comparison.png', dpi=300)
        plt.close()
        print(f"Generated summary metrics bar chart in '{output_dir}/'.")

if __name__ == "__main__":
    generate_visualizations()

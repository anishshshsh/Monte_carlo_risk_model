from src.risk_model import load_risks, compute_scores 
from src.visualizations import plot_heatmap, plot_top_risks
import os

def run():
    """
    Main entry point for the risk modeling tool.
    """
    base = os.path.dirname(__file__) 
    csv = os.path.join(base, 'data', 'risks.csv')
    out = os.path.join(base, 'outputs')
    os.makedirs(out, exist_ok=True)  # Create output directory if it doesn't exist
    df = load_risks(csv)
    df_scored = compute_scores(df)
    df_scored.to_csv(os.path.join(out, 'risks_scored.csv'), index=False)
    plot_heatmap(df_scored, os.path.join(out, 'risk_heatmap.png'))
    plot_top_risks(df_scored, os.path.join(out, 'top_risks.png'))
    print('Done. Outputs in', out)
    return df_scored

if __name__ == '__main__':
    run()

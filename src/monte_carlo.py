import numpy as np
import pandas as pd

def run_monte_carlo(df, trials=10000, base_exposure=1_000_000, random_seed=42):
    '''
    df must have columns: Category, Description, Probability (1-5), Impact (1-5)
    Interpretation:
      - probability = Probability / 5
      - impact factor = Impact / 5 (fraction of base_exposure lost if the risk occurs)
      - severity_multiplier ~ LogNormal( mean=1, sigma=0.5 ) to add randomness to impact size
    Returns:
      - losses: np.array of total loss per trial
      - summary dict with mean, median, percentiles, VaR95, ES95 (expected shortfall)
    '''
    np.random.seed(random_seed)  # Set random seed for reproducibility
    probs = (df['Probability'].astype(float) / 5.0).values
    impacts = (df['Impact'].astype(float) / 5.0).values
    n_risks = len(df)
    losses = np.zeros(trials)  # Initialize losses array
    for i in range(trials):  # Loop over each trial
        occurs = np.random.rand(n_risks) < probs
        severity = np.random.lognormal(mean=0.0, sigma=0.6, size=n_risks)
        loss_per_risk = occurs * (impacts * base_exposure * severity)
        losses[i] = loss_per_risk.sum()
    summary = {
        'trials': int(trials),
        'mean_loss': float(np.mean(losses)),
        'median_loss': float(np.median(losses)),
        'std_loss': float(np.std(losses)),
        'percentiles': {p: float(np.percentile(losses, p)) for p in [50, 75, 90, 95, 99]},
        'VaR_95': float(np.percentile(losses, 95)),
        'ES_95': float(np.mean(losses[losses >= np.percentile(losses, 95)]))
    }
    return losses, summary

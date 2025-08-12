import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(df, outpath):
    """
    Plot a heatmap of risk scores.
    """
    scores = df['Score'].values
    labels = (df['Category'] + ' - ' + df['Description']).values
    y = np.arange(len(scores))  # Create a range for the y-axis
    fig, ax = plt.subplots(figsize=(8, max(3, len(scores)*0.3)))  # Create a horizontal bar chart
    bars = ax.barh(y, scores)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('Score')
    ax.set_title('Risk Scores Heatmap-like View')
    for bar, score in zip(bars, scores):  # Color bars based on score
        if score >= 15:
            bar.set_color((0.8,0.1,0.1))
        elif score >= 9:
            bar.set_color((0.95,0.5,0.1))
        elif score >= 5:
            bar.set_color((0.95,0.85,0.1))
        else:
            bar.set_color((0.3,0.7,0.3))
    plt.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

def plot_top_risks(df, outpath, top_n=8):
    """
    Plot the top N risks based on their scores.
    """
    df_top = df.head(top_n)  # Select top N risks
    x = df_top['Score'].values[::-1]
    labels = (df_top['Category'] + ' - ' + df_top['Description']).values[::-1]  # Reverse labels for top N
    fig, ax = plt.subplots(figsize=(7, max(3, len(x)*0.45)))
    y = range(len(x))
    ax.barh(y, x)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('Score')
    ax.set_title(f'Top {top_n} Risks')
    plt.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

import matplotlib.pyplot as plt

def GK_vol(df, ax):
    ax.plot(df.index.get_level_values('date'), df['GK_vol'], marker=',', color='red', linestyle='-')
    ax.set_ylabel('GK volatility', color='black')
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_xlabel('')
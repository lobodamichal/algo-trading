import matplotlib.pyplot as plt

def GK_vol(df, ax):
    ax.plot(df.index.get_level_values('date'), df['GK_vol'], marker=',', color='red', linestyle='-',linewidth=.5)
    ax.set_ylabel('GK volatility', color='red')
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_xlabel('')

def B_bands(df, ax):
    ax.plot(df.index.get_level_values('date'), df['BB_lower'], marker=',', color='blue', linestyle='-', linewidth=.5)
    ax.plot(df.index.get_level_values('date'), df['BB_middle'], marker=',', color='blue', linestyle='-', linewidth=.2)
    ax.plot(df.index.get_level_values('date'), df['BB_upper'], marker=',', color='blue', linestyle='-', linewidth=.5)

def RSI(df, ax):
    ax2 = ax.twinx()
    ax2.plot(df.index.get_level_values('date'), df['RSI'], marker=',', color='blue', linestyle='-', linewidth=.5)
    ax2.set_ylabel('RSI', color='blue')
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.set_ticks_position('right')
    ax2.set_xticks([])
    ax2.set_xticklabels([])
    ax2.set_xlabel('')
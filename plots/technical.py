def B_bands(df, ax):
    ax.plot(df.index.get_level_values('date'), df['BB_lower'], marker=',', color='blue', linestyle='-', linewidth=.5)
    ax.plot(df.index.get_level_values('date'), df['BB_middle'], marker=',', color='blue', linestyle='-', linewidth=.2)
    ax.plot(df.index.get_level_values('date'), df['BB_upper'], marker=',', color='blue', linestyle='-', linewidth=.5)

def technical_secondary(indicator, color, df, ax, side='left'):
    if side == 'left':
        ax2 = ax
    else:
        ax2 = ax.twinx()

    ax2.yaxis.set_label_position(side)
    ax2.yaxis.set_ticks_position(side)
    ax2.plot(df.index.get_level_values('date'), df[indicator], marker=',', color=color, linestyle='-',linewidth=.5)
    ax2.set_ylabel(indicator, color=color)
    ax2.set_xticks([])
    ax2.set_xticklabels([])
    ax2.set_xlabel('')
import matplotlib.pyplot as plt
from plots import candle, technical

def plot(df, label):
    fig, axs = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]})

    axs[0].set_title(label=label, loc='center')

    candle.candle(df, axs[0])
    technical.B_bands(df, axs[0])

    technical.technical_secondary('GK_vol', 'red', df, axs[1])
    technical.technical_secondary('RSI', 'blue', df, axs[1], side='right')

    technical.technical_secondary('ATR', 'red', df, axs[2], side='left')
    technical.technical_secondary('MACD', 'blue', df, axs[2], side='right')

    plt.show()
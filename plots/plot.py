import matplotlib.pyplot as plt
from plots import candle, technical

def plot(df):
    fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

    candle.candle(df, axs[0])
    technical.B_bands(df, axs[0])
    technical.GK_vol(df, axs[1])
    technical.RSI(df, axs[1])
    plt.show()
import matplotlib.pyplot as plt

def candle(df):
    plt.figure()

    df.reset_index(inplace=True)
    df.set_index('date', inplace=True)

    width_candle = .6
    width_knot = .2

    up_candle = df[df.close >= df.open]
    down_candle = df[df.close < df.open]

    color_up = 'green'
    color_down = 'red'

    # Bullish candle
    plt.bar(
            up_candle.index, 
            up_candle.close - up_candle.open, 
            width=width_candle, 
            bottom=up_candle.open, 
            color=color_up
            )
    
    plt.bar(
            up_candle.index, 
            up_candle.high - up_candle.close, 
            width=width_knot, 
            bottom=up_candle.close, 
            color=color_up
            )
    
    plt.bar(
            up_candle.index, 
            up_candle.low - up_candle.open, 
            width=width_knot, 
            bottom=up_candle.open, 
            color=color_up
            )
    
    # Bearish candle
    plt.bar(
            down_candle.index, 
            down_candle.close - down_candle.open, 
            width=width_candle, 
            bottom=down_candle.open, 
            color=color_down
            )
    
    plt.bar(
            down_candle.index, 
            down_candle.high - down_candle.open, 
            width=width_knot, 
            bottom=down_candle.open, 
            color=color_down
            )
    
    plt.bar(
            down_candle.index, 
            down_candle.low - down_candle.close, 
            width=width_knot, 
            bottom=down_candle.close, 
            color=color_down
            )
    
    plt.ylabel('price', color='black')
    plt.xlabel('Date')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.show()
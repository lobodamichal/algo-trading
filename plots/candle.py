import matplotlib.pyplot as plt

def candle(df, ax):
    df.reset_index(inplace=True)
    dates_list = df['date'].tolist()

    df.set_index('date', inplace=True)

    width_candle = .6
    width_knot = .2

    up_candle = df[df.close >= df.open]
    down_candle = df[df.close < df.open]

    color_up = 'green'
    color_down = 'red'

    # Bullish candle
    ax.bar(
            up_candle.index, 
            up_candle.close - up_candle.open, 
            width=width_candle, 
            bottom=up_candle.open, 
            color=color_up
            )
    
    ax.bar(
            up_candle.index, 
            up_candle.high - up_candle.close, 
            width=width_knot, 
            bottom=up_candle.close, 
            color=color_up
            )
    
    ax.bar(
            up_candle.index, 
            up_candle.low - up_candle.open, 
            width=width_knot, 
            bottom=up_candle.open, 
            color=color_up
            )
    
    # Bearish candle
    ax.bar(
            down_candle.index, 
            down_candle.close - down_candle.open, 
            width=width_candle, 
            bottom=down_candle.open, 
            color=color_down
            )
    
    ax.bar(
            down_candle.index, 
            down_candle.high - down_candle.open, 
            width=width_knot, 
            bottom=down_candle.open, 
            color=color_down
            )
    
    ax.bar(
            down_candle.index, 
            down_candle.low - down_candle.close, 
            width=width_knot, 
            bottom=down_candle.close, 
            color=color_down
            )
    
    ax.set_ylabel('price', color='black')
    ax.set_xlabel('Date')
    ax.set_xticks(dates_list, [date.strftime('%d.%m') for date in dates_list], rotation=90, ha='center', fontsize=6)
    ax.grid(True)
    
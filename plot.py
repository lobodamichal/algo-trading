import matplotlib.pyplot as plt
from stock import Stock

class Plot():

    @staticmethod
    def candle(stock: Stock, ax) -> None:
        stock.history.reset_index(inplace=True)
        dates_list = stock.history['date'].tolist()

        stock.history.set_index('date', inplace=True)

        width_candle = .6
        width_knot = .2

        up_candle = stock.history[stock.history.close >= stock.history.open]
        down_candle = stock.history[stock.history.close < stock.history.open]

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
        ax.set_xticks(dates_list, [date.strftime('%d.%m') for date in dates_list], rotation=90, ha='center', fontsize=6)
        ax.grid(True)

    @staticmethod
    def B_bands(stock: Stock, ax) -> None:
        ax.plot(stock.history.index.get_level_values('date'), stock.history['BB_lower'], marker=',', color='blue', linestyle='-', linewidth=.5)
        ax.plot(stock.history.index.get_level_values('date'), stock.history['BB_middle'], marker=',', color='blue', linestyle='-', linewidth=.2)
        ax.plot(stock.history.index.get_level_values('date'), stock.history['BB_upper'], marker=',', color='blue', linestyle='-', linewidth=.5)

    @staticmethod
    def technical_secondary(stock: Stock, indicator, color: str, ax, side: str = 'left') -> None:
        if side == 'left':
            ax2 = ax
        else:
            ax2 = ax.twinx()

        ax2.yaxis.set_label_position(side)
        ax2.yaxis.set_ticks_position(side)
        ax2.plot(stock.history.index.get_level_values('date'), stock.history[indicator], marker=',', color=color, linestyle='-',linewidth=.5)
        ax2.set_ylabel(indicator, color=color)
        ax2.set_xticks([])
        ax2.set_xticklabels([])
        ax2.set_xlabel('')
        
    @staticmethod
    def plot(stock: Stock) -> None:
        _, axs = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]})

        axs[0].set_title(label=stock.ticker, loc='center')

        Plot.candle(stock, axs[0])
        Plot.B_bands(stock, axs[0])

        Plot.technical_secondary(stock, 'GK_vol', 'red', axs[1])
        Plot.technical_secondary(stock, 'RSI', 'blue', axs[1], side='right')

        Plot.technical_secondary( stock, 'ATR', 'red', axs[2], side='left')
        Plot.technical_secondary(stock, 'MACD', 'blue', axs[2], side='right')

        plt.show()
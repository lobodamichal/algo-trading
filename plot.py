import matplotlib.pyplot as plt
import pandas as pd
from stock import Stock

class Plot():

    @staticmethod
    def candle(financial_data: pd.DataFrame, ax) -> None:
        financial_data.reset_index(inplace=True)
        dates_list = financial_data['date'].tolist()

        financial_data.set_index('date', inplace=True)

        width_candle = .6
        width_knot = .2

        up_candle = financial_data[financial_data.close >= financial_data.open]
        down_candle = financial_data[financial_data.close < financial_data.open]

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
    def B_bands(financial_data: pd.DataFrame, ax) -> None:
        ax.plot(financial_data.index.get_level_values('date'), financial_data['BB_lower'], marker=',', color='blue', linestyle='-', linewidth=.5)
        ax.plot(financial_data.index.get_level_values('date'), financial_data['BB_middle'], marker=',', color='blue', linestyle='-', linewidth=.2)
        ax.plot(financial_data.index.get_level_values('date'), financial_data['BB_upper'], marker=',', color='blue', linestyle='-', linewidth=.5)

    @staticmethod
    def technical_secondary(financial_data: pd.DataFrame, indicator, color: str, ax, side: str = 'left') -> None:
        if side == 'left':
            ax2 = ax
        else:
            ax2 = ax.twinx()

        ax2.yaxis.set_label_position(side)
        ax2.yaxis.set_ticks_position(side)
        ax2.plot(financial_data.index.get_level_values('date'), financial_data[indicator], marker=',', color=color, linestyle='-',linewidth=.5)
        ax2.set_ylabel(indicator, color=color)
        ax2.set_xticks([])
        ax2.set_xticklabels([])
        ax2.set_xlabel('')

    @staticmethod
    def volume(financial_data: pd.DataFrame, ax) -> None:
        financial_data.reset_index(inplace=True)
        dates_list = financial_data['date'].tolist()
        financial_data.set_index('date', inplace=True)
        ax.bar(financial_data.index.get_level_values('date'), financial_data['volume'])
        ax.set_xticks(dates_list, [date.strftime('%d.%m') for date in dates_list], rotation=90, ha='center', fontsize=6)
        ax.set_ylabel('volume', color='black')

    @staticmethod
    def plot(stock: Stock, days: int) -> None:
        _, axs = plt.subplots(4, 1, gridspec_kw={'height_ratios': [3, 1, 1, 1]})

        axs[0].set_title(label=stock.ticker, loc='center')

        financial_data = stock.financial_data.iloc[-days:]

        Plot.candle(financial_data, axs[0])
        Plot.B_bands(financial_data, axs[0])

        Plot.technical_secondary(financial_data, 'GK_vol', 'red', axs[1])
        Plot.technical_secondary(financial_data, 'RSI', 'blue', axs[1], side='right')

        Plot.technical_secondary(financial_data, 'ATR', 'red', axs[2], side='left')
        Plot.technical_secondary(financial_data, 'MACD', 'blue', axs[2], side='right')

        Plot.volume(financial_data, axs[3])

        plt.show()
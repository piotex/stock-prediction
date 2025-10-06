import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from calculate_rsi import calculate_rsi
from simulate_strategy import buy_threshold, sell_threshold
from values import *
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import datetime
from datetime import datetime

alpha_v = 0.4

# ========================================================================
def print_prices(dates, vals_list, stock_name, ax1):
    ax1.plot(dates, vals_list, label=f'{stock_name}', color='blue')
    ax1.set_title(f'Kurs {stock_name}')
    ax1.set_ylabel('Cena [PLN]')
    ax1.grid(True)
    ax1.legend()
    # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=90))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))


def print_tendencies_reports(tendencies, stock_name, ax4):
    text = f"TENDENCJE {stock_name}"
    trend_text_list = [text+t for t in tendencies.split(text) if t.strip() != ""]
    color = "green" if "POZYTYWNE" in trend_text_list[0] else "red"
    ax4.text(0.5, 0.5, trend_text_list[0], fontsize=16, fontweight='bold', ha='right', va='center', color=color)
    if len(trend_text_list) > 1:
        color = "green" if "POZYTYWNE" in trend_text_list[1] else "red"
        ax4.text(0.5, 0.5, trend_text_list[1], fontsize=16, fontweight='bold', ha='left', va='center', color=color)
    ax4.axis('off')


def print_reports_chart(financial_data, stock_name, ax1):
    categories = list(financial_data.keys())
    values = list(financial_data.values())
    data = []

    # 1. Przygotowanie danych do wyświetlenia (formatowanie)
    for i in range(len(categories)):
        formatted_values = []
        for val in values[i]:
            try:
                # Formatowanie liczbowe
                if isinstance(val, (int, float)):
                    if abs(val) >= 1000:
                        if isinstance(val, int) or val == int(val):
                            formatted_val = f"{int(val):,}".replace(",", " ")
                        else:
                            formatted_val = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
                    else:
                        if isinstance(val, int) or val == int(val):
                            formatted_val = str(int(val))
                        else:
                            # Użycie f"{val:g}" dla zwięzłego formatowania float
                            formatted_val = f"{val:g}"
                else:
                    formatted_val = str(val)
            except:
                formatted_val = str(val)
            formatted_values.append(formatted_val)
        # data[i] zawiera nagłówek kategorii + sformatowane dane
        data.append([categories[i]] + formatted_values)

    num_rows = len(data)
    num_cols = len(data[0])

    # 2. Utworzenie tabeli i podstawowe ustawienia
    table = ax1.table(cellText=data,
                      loc='center',
                      cellLoc='center')

    ax1.set_title(f'Dane Finansowe: {stock_name}', y=1.05)
    ax1.axis('off')

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    light_gray = '#f0f0f0'

    num_data_cols = num_cols - 1
    category_width_ratio = 0.25
    data_width_ratio = (1.0 - category_width_ratio) / num_data_cols

    for i in range(num_rows):  # i to indeks wiersza w tabeli
        if i >= 1 and i % 2 == 0:
            for j in range(num_cols):
                cell = table[(i, j)]
                cell.set_facecolor(light_gray)

        for j in range(num_cols):
            cell = table[(i, j)]
            if i == 0:
                cell.set_text_props(fontweight='bold')
                cell.set_facecolor('#cccccc')
            if j == 0:
                cell.set_width(category_width_ratio)
                cell.set_text_props(fontweight='bold')
            else:
                cell.set_width(data_width_ratio)

        if i >= 1 and len(values[i - 1]) >= 2:  # i - wiersze
            original_row_data = values[i]
            for j in range(2, num_cols):        # j - kolumny
                try:
                    current_value = float(original_row_data[j-1])
                    previous_value = float(original_row_data[j-2])
                except (ValueError, TypeError):
                    continue

                cell = table[(i, j)]
                if current_value > previous_value:
                    cell.set_facecolor('lightgreen')
                elif current_value < previous_value:
                    cell.set_facecolor('lightcoral')

                if j == num_cols - 1:
                    cell = table[(i, 0)]
                    if current_value > previous_value:
                        cell.set_facecolor('lightgreen')
                    elif current_value < previous_value:
                        cell.set_facecolor('lightcoral')


    return table


def print_stock_data(stock_name: str,
                     dates: List[datetime.date],
                     prices: List[float],
                     tendencies: str,
                     quarterly_data: Dict[str, List[Any]],
                     ):

    fig, ax_list = plt.subplots(
        3, 1,
        figsize=(25, 16),
        gridspec_kw={'height_ratios': [2, 1, 1]}
    )

    if print_stock_prices:
        print_prices(dates, prices, stock_name, ax_list[0])

    # if print_rsi_chart:
    #     print_rsi(dates, prices, stock_name, ax_list[1])

    if print_tendencies_reports:
        print_tendencies_reports(tendencies, stock_name, ax_list[1])

    if print_quarterly_reports:
        print_reports_chart(quarterly_data, stock_name, ax_list[2])

    # fig.autofmt_xdate()
    plt.tight_layout(pad=2.0)
    plt.show()



















# def print_prices(dates, vals_list, stock_name, buy_vals, sell_vals, ax1):
#     # 1. Wykres ceny
#     ax1.plot(dates, vals_list, label=f'{stock_name}', color='blue')
#     ax1.set_title(f'Kurs {stock_name}')
#     ax1.set_ylabel('Cena [PLN]')
#     ax1.grid(True)
#     ax1.legend()
#
#     for d, buy, sell in zip(dates, buy_vals, sell_vals):
#         if buy == 1:
#             ax1.axvline(x=d, color='green', linestyle='--', alpha=alpha_v+0.2)
#         if sell == 1:
#             ax1.axvline(x=d, color='red', linestyle='--', alpha=alpha_v)
#     ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

def print_rsi(dates, rsi_vals, buy_vals, sell_vals, ax2):
    # 2. Wykres RSI
    ax2.plot(dates, rsi_vals, label='RSI (14)', color='purple')
    ax2.axhline(70, color='red', linestyle='-', alpha=0.7)
    ax2.axhline(30, color='green', linestyle='-', alpha=0.7)
    ax2.set_title('RSI (14)')
    ax2.set_ylabel('RSI')
    ax2.grid(True)
    ax2.legend()

    for d, buy, sell in zip(dates, buy_vals, sell_vals):
        if buy == 1:
            ax2.axvline(x=d, color='green', linestyle='--', alpha=alpha_v+0.2)
        if sell == 1:
            ax2.axvline(x=d, color='red', linestyle='--', alpha=alpha_v)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.set_ylim(0, 100)                          # od 0 do 100
    ax2.set_yticks([10, 30, 50, 70, 90])          # pokazuj tylko te wartości

def print_portfel_vals(dates, portfolio_values, ax3):
    # 3. Wartość portfela
    ax3.plot(dates, portfolio_values, label='Wartość portfela [PLN]', color='black')
    ax3.set_title('Wartość portfela')
    ax3.set_ylabel('PLN')
    ax3.grid(True)
    ax3.legend()

    # ax3.axhline(y=initial_cash+initial_stock_value, color='red', linestyle='--', alpha=0.8, label='Poziom 20k PLN')
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.8, label='Poziom 20k PLN')
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# def print_tendencje(trend_text, ax4):
#     # 4. Tekst – nowy wykres
#     text = "TENDENCJE"
#     trend_text_list = [text+t for t in trend_text.split(text) if t.strip() != ""]
#     color = "green" if "POZYTYWNE" in trend_text_list[0] else "red"
#     ax4.text(0.5, 0.5, trend_text_list[0], fontsize=16, fontweight='bold', ha='right', va='center', color=color)
#     if len(trend_text_list) > 1:
#         color = "green" if "POZYTYWNE" in trend_text_list[1] else "red"
#         ax4.text(0.5, 0.5, trend_text_list[1], fontsize=16, fontweight='bold', ha='left', va='center', color=color)
#     ax4.axis('off')

def calc_buy_sell(rsi_vals):
    buy_vals = []
    sell_vals = []
    for val in rsi_vals:
        if val is None:
            buy_vals.append(2)
            sell_vals.append(0)
            continue

        if val < buy_threshold:
            buy_vals.append(1)
        else:
            buy_vals.append(0)

        if val > sell_threshold:
            sell_vals.append(1)
        else:
            sell_vals.append(0)
    return buy_vals, sell_vals

def plot_charts_rsi_trend_br(stock_name, date_vals, vals_list, portfolio_values, trend_text):
    rsi_vals = calculate_rsi(vals_list, period=rsi_period)
    buy_vals, sell_vals = calc_buy_sell(rsi_vals)
    dates = [datetime.datetime.strptime(d, "%Y%m%d") for d in date_vals]

    # dates = date_vals
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        4, 1,
        figsize=(20, 16),
        gridspec_kw={'height_ratios': [2, 1, 1, 1]}
    )

    print_prices(dates, vals_list, stock_name, buy_vals, sell_vals, ax1)
    print_tendencje(trend_text, ax2)
    print_rsi(dates, rsi_vals, buy_vals, sell_vals, ax3)
    print_portfel_vals(dates, portfolio_values, ax4)


    plt.tight_layout()
    plt.tight_layout(pad=2.0)
    plt.show()














def plot_charts_rsi(stock_name, date_vals, vals_list, portfolio_values):
    rsi_vals = calculate_rsi(vals_list, period=rsi_period)

    buy_vals = []
    sell_vals = []
    for val in rsi_vals:
        if val is None:
            buy_vals.append(2)
            sell_vals.append(0)
            continue

        if val < buy_threshold:
            buy_vals.append(1)
        else:
            buy_vals.append(0)

        if val > sell_threshold:
            sell_vals.append(1)
        else:
            sell_vals.append(0)

    dates = [datetime.datetime.strptime(d, "%Y%m%d") for d in date_vals]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # 1. Wykres ceny
    ax1.plot(dates, vals_list, label=f'{stock_name}', color='blue')
    ax1.set_title(f'Kurs {stock_name}')
    ax1.set_ylabel('Cena [PLN]')
    ax1.grid(True)
    ax1.legend()

    for d, buy, sell in zip(dates, buy_vals, sell_vals):
        if buy == 1:
            ax1.axvline(x=d, color='green', linestyle='solid', alpha=alpha_v)
        if sell == 1:
            ax1.axvline(x=d, color='red', linestyle='solid', alpha=alpha_v)

    # 2. Wykres RSI
    ax2.plot(dates, rsi_vals, label='RSI (14)', color='purple')
    ax2.axhline(70, color='red', linestyle='--', alpha=0.7)
    ax2.axhline(30, color='green', linestyle='--', alpha=0.7)
    ax2.set_title('RSI (14)')
    ax2.set_ylabel('RSI')
    ax2.grid(True)
    ax2.legend()

    for d, buy, sell in zip(dates, buy_vals, sell_vals):
        if buy == 1:
            ax2.axvline(x=d, color='green', linestyle='-', alpha=alpha_v)
        if sell == 1:
            ax2.axvline(x=d, color='red', linestyle='-', alpha=alpha_v)

    # 3. Wartość portfela
    ax3.plot(dates, portfolio_values, label='Wartość portfela [PLN]', color='black')
    ax3.set_title('Wartość portfela')
    ax3.set_ylabel('PLN')
    ax3.grid(True)
    ax3.legend()

    ax3.axhline(y=20000, color='red', linestyle='--', alpha=0.8, label='Poziom 20k PLN')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()


def plot_charts(date_vals, vals_list, portfolio_values):
    dates = [datetime.datetime.strptime(d, "%Y%m%d") for d in date_vals]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(dates, vals_list, label='', color='blue')
    ax1.set_title('Kurs')
    ax1.set_ylabel('Cena [PLN]')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(dates, portfolio_values, label='Wartość portfela [PLN]', color='orange')
    ax2.set_title('Wartość portfela')
    ax2.set_ylabel('PLN')
    ax2.set_xlabel('Data')
    ax2.grid(True)
    ax2.legend()

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()

import numpy as np
from matplotlib import pyplot as plt

from rsi import *
from wallet import get_wallet_values_in_time, get_wallet_values_from_histogram_in_time


def plot_chart(x_val, y_val):
    plt.rcParams["figure.figsize"] = (30, 5)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    major_ticks = np.arange(0, len(x_val) + 1, 100)
    minor_ticks = np.arange(0, len(x_val) + 1, 5)
    major_ticks = np.append(major_ticks, len(x_val)-1)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=0.1)
    ax.grid(which='major', alpha=0.7)

    # plt.text(x_val[-1], y_val[-1], x_val[-1], ha='center', va='bottom')

    plt.plot(x_val, y_val, c="b")
    plt.grid(True)
    plt.show()


def plot_chart_stock_rsi(x_val, y_val):
    major_ticks = np.arange(0, len(x_val) + 1, 100)
    minor_ticks = np.arange(0, len(x_val) + 1, 5)
    major_ticks = np.append(major_ticks, len(x_val)-1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 10), height_ratios=[2, 1])
    plt.grid(True)

    ax1.set_xticks(major_ticks)
    ax1.set_xticks(minor_ticks, minor=True)
    ax1.grid(which='minor', alpha=0.1)
    ax1.grid(which='major', alpha=0.7)
    ax1.plot(x_val, y_val, c="b")

    period = 14
    rsi_values = calculate_rsi(y_val, period)
    rsi_operations = get_rsi_operations(y_val, period)

    ax2.set_xticks(major_ticks)
    ax2.set_xticks(minor_ticks, minor=True)
    ax2.grid(which='minor', alpha=0.1)
    ax2.grid(which='major', alpha=0.7)
    ax2.plot(x_val, rsi_values, c="#FFAA00")

    ax2.axhline(y=high_threshold, color='red', linestyle='--')
    ax2.axhline(y=low_threshold, color='green', linestyle='--')

    opacity = 0.17
    color = "pink"
    for operation in rsi_operations:
        if operation[2] == "buy":
            color = "green"
        if operation[2] == "sell":
            color = "red"
        ax1.axvspan(operation[0], operation[1], color=color, alpha=opacity)
        ax2.axvspan(operation[0], operation[1], color=color, alpha=opacity)
    plt.show()


def plot_chart_stock_rsi_wallet(x_val, y_val, period, initial_capital=10000, percent_buy=0.1, percent_sell=0.25):
    major_ticks = np.arange(0, len(x_val) + 1, 100)
    minor_ticks = np.arange(0, len(x_val) + 1, 5)
    major_ticks = np.append(major_ticks, len(x_val)-1)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(30, 15), height_ratios=[2, 1, 1])
    plt.grid(True)

    ax1.set_title("Cena akcji w czasie", fontsize=15)
    ax1.set_xticks(major_ticks)
    ax1.set_xticks(minor_ticks, minor=True)
    ax1.grid(which='minor', alpha=0.1)
    ax1.grid(which='major', alpha=0.7)
    ax1.plot(x_val, y_val, c="b")
    ax1.text(x_val[-1], y_val[-1], str(y_val[-1]), ha='center', va='bottom')

    rsi_values = calculate_rsi(y_val, period)
    rsi_operations = get_rsi_operations(y_val, period)
    ax2.set_title("RSI", fontsize=15)
    ax2.set_xticks(major_ticks)
    ax2.set_xticks(minor_ticks, minor=True)
    ax2.grid(which='minor', alpha=0.1)
    ax2.grid(which='major', alpha=0.7)
    ax2.plot(x_val, rsi_values, c="#FFAA00")
    ax2.axhline(y=high_threshold, color='red', linestyle='--')
    ax2.axhline(y=low_threshold, color='green', linestyle='--')
    ax2.text(x_val[-1], rsi_values[-1], round(rsi_values[-1], 1), ha='center', va='bottom')

    wallet_in_time = get_wallet_values_in_time(y_val, period, initial_capital, percent_buy, percent_sell)
    ax3.set_title("Wartość portfela w czasie", fontsize=15)
    ax3.set_xticks(major_ticks)
    ax3.set_xticks(minor_ticks, minor=True)
    ax3.grid(which='minor', alpha=0.1)
    ax3.grid(which='major', alpha=0.7)
    ax3.plot(x_val, wallet_in_time, c="green")
    ax3.axhline(y=10000, color='red', linestyle='--')
    ax3.text(x_val[-1], wallet_in_time[-1], round(wallet_in_time[-1], 1), ha='center', va='bottom')

    opacity = 0.17
    color = "pink"
    for operation in rsi_operations:
        if operation[2] == "buy":
            color = "green"
        if operation[2] == "sell":
            color = "red"
        ax1.axvspan(operation[0], operation[1], color=color, alpha=opacity)
        ax2.axvspan(operation[0], operation[1], color=color, alpha=opacity)
        ax3.axvspan(operation[0], operation[1], color=color, alpha=opacity)

    plt.show()


# def plot_multichart_stock_rsi_wallet(x_val, y_val, period, initial_capital=10000, percent_buy=0.1, percent_sell=0.25):
#     major_ticks = np.arange(0, len(x_val) + 1, 100)
#     minor_ticks = np.arange(0, len(x_val) + 1, 5)
#     major_ticks = np.append(major_ticks, len(x_val)-1)
#
#     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(30, 15), height_ratios=[2, 1, 1])
#     plt.grid(True)
#
#     ax1.set_title("Cena akcji w czasie", fontsize=15)
#     ax1.set_xticks(major_ticks)
#     ax1.set_xticks(minor_ticks, minor=True)
#     ax1.grid(which='minor', alpha=0.1)
#     ax1.grid(which='major', alpha=0.7)
#     ax1.plot(x_val, y_val, c="b")
#     ax1.text(x_val[-1], y_val[-1], str(y_val[-1]), ha='center', va='bottom')
#
#     for period in range(3,30):
#         rsi_values = calculate_rsi(y_val, period)
#         rsi_operations = get_rsi_operations(y_val, period)
#         ax2.set_title("RSI", fontsize=15)
#         ax2.set_xticks(major_ticks)
#         ax2.set_xticks(minor_ticks, minor=True)
#         ax2.grid(which='minor', alpha=0.1)
#         ax2.grid(which='major', alpha=0.7)
#         ax2.plot(x_val, rsi_values, c="#FFAA00")
#         ax2.axhline(y=high_threshold, color='red', linestyle='--')
#         ax2.axhline(y=low_threshold, color='green', linestyle='--')
#         ax2.text(x_val[-1], rsi_values[-1], round(rsi_values[-1], 1), ha='center', va='bottom')
#
#         wallet_in_time = get_wallet_values_in_time(y_val, period, initial_capital, percent_buy, percent_sell)
#         ax3.set_title("Wartość portfela w czasie", fontsize=15)
#         ax3.set_xticks(major_ticks)
#         ax3.set_xticks(minor_ticks, minor=True)
#         ax3.grid(which='minor', alpha=0.1)
#         ax3.grid(which='major', alpha=0.7)
#         ax3.plot(x_val, wallet_in_time, c="green")
#         ax3.axhline(y=10000, color='red', linestyle='--')
#         ax3.text(x_val[-1], wallet_in_time[-1], round(wallet_in_time[-1], 1), ha='center', va='bottom')
#
#         opacity = 0.1
#         color = "pink"
#         for operation in rsi_operations:
#             if operation[2] == "buy":
#                 color = "green"
#             if operation[2] == "sell":
#                 color = "red"
#             ax1.axvspan(operation[0], operation[1], color=color, alpha=opacity)
#             ax2.axvspan(operation[0], operation[1], color=color, alpha=opacity)
#             ax3.axvspan(operation[0], operation[1], color=color, alpha=opacity)
#
#     plt.show()


def plot_chart_stock_rsi_histogram(x_val, y_val):
    major_ticks = np.arange(0, len(x_val) + 1, 100)
    minor_ticks = np.arange(0, len(x_val) + 1, 5)
    major_ticks = np.append(major_ticks, len(x_val)-1)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(30, 15), height_ratios=[2, 1, 1])
    plt.grid(True)

    ax1.set_title("Cena akcji w czasie", fontsize=15)
    ax1.set_xticks(major_ticks)
    ax1.set_xticks(minor_ticks, minor=True)
    ax1.grid(which='minor', alpha=0.1)
    ax1.grid(which='major', alpha=0.7)
    ax1.plot(x_val, y_val, c="b")
    ax1.text(x_val[-1], y_val[-1], str(y_val[-1]), ha='center', va='bottom')

    for period in range(3,32):
        rsi_values = calculate_rsi(y_val, period)
        rsi_operations = get_rsi_operations(y_val, period)
        ax2.set_title("RSI", fontsize=15)
        ax2.set_xticks(major_ticks)
        ax2.set_xticks(minor_ticks, minor=True)
        ax2.grid(which='minor', alpha=0.1)
        ax2.grid(which='major', alpha=0.7)
        ax2.plot(x_val, rsi_values, c="#FFAA00", alpha=0.2)
    ax2.axhline(y=high_threshold, color='red', linestyle='--')
    ax2.axhline(y=low_threshold, color='green', linestyle='--')

    histogram = get_rsi_histogram_operations(y_val)
    ax3.set_title("Wartość portfela w czasie", fontsize=15)
    ax3.set_xticks(major_ticks)
    ax3.set_xticks(minor_ticks, minor=True)
    ax3.grid(which='minor', alpha=0.1)
    ax3.grid(which='major', alpha=0.7)
    ax3.plot(x_val, histogram, c="blue")
    # ax3.axhline(y=10000, color='red', linestyle='--')

    # opacity = 0.17
    # color = "pink"
    # for operation in rsi_operations:
    #     if operation[2] == "buy":
    #         color = "green"
    #     if operation[2] == "sell":
    #         color = "red"
    #     ax1.axvspan(operation[0], operation[1], color=color, alpha=opacity)
    #     ax2.axvspan(operation[0], operation[1], color=color, alpha=opacity)
    #     ax3.axvspan(operation[0], operation[1], color=color, alpha=opacity)

    plt.show()




def plot_chart_stock_rsi_histogram_wallet(x_val, y_val):
    major_ticks = np.arange(0, len(x_val) + 1, 100)
    minor_ticks = np.arange(0, len(x_val) + 1, 5)
    major_ticks = np.append(major_ticks, len(x_val)-1)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(30, 15), height_ratios=[2, 1, 1])
    plt.grid(True)

    ax1.set_title("Cena akcji w czasie", fontsize=15)
    ax1.set_xticks(major_ticks)
    ax1.set_xticks(minor_ticks, minor=True)
    ax1.grid(which='minor', alpha=0.1)
    ax1.grid(which='major', alpha=0.7)
    ax1.plot(x_val, y_val, c="b")
    ax1.text(x_val[-1], y_val[-1], str(y_val[-1]),
        ha='center',
        va='bottom',
        fontsize=11,
        color='white',
        bbox=dict(facecolor=(0, 0, 0, 0.5), edgecolor='none', boxstyle='round,pad=0.15')
    )

    for period in range(3,32):
        rsi_values = calculate_rsi(y_val, period)
        ax2.set_title("RSI", fontsize=15)
        ax2.set_xticks(major_ticks)
        ax2.set_xticks(minor_ticks, minor=True)
        ax2.grid(which='minor', alpha=0.1)
        ax2.grid(which='major', alpha=0.7)
        ax2.plot(x_val, rsi_values, c="#FFAA00", alpha=0.2)
    ax2.axhline(y=high_threshold, color='red', linestyle='--')
    ax2.axhline(y=low_threshold, color='green', linestyle='--')

    walles = get_wallet_values_from_histogram_in_time(y_val)
    ax3.set_title("Wartość portfela w czasie", fontsize=15)
    ax3.set_xticks(major_ticks)
    ax3.set_xticks(minor_ticks, minor=True)
    ax3.grid(which='minor', alpha=0.1)
    ax3.grid(which='major', alpha=0.7)
    ax3.plot(x_val, walles, c="blue")
    ax3.axhline(y=10000, color='red', linestyle='--')
    # ax3.text(x_val[-1], walles[-1], round(walles[-1], 1), ha='center', va='bottom', fontsize=12, color='white')
    ax3.text(
        x_val[-1],
        walles[-1],
        round(walles[-1], 1),
        ha='center',
        va='bottom',
        fontsize=11,
        color='white',
        bbox=dict(facecolor=(0, 0, 0, 0.5), edgecolor='none', boxstyle='round,pad=0.15')
    )

    threshold = 5
    histogram_values = get_rsi_histogram_operations(y_val)
    for i, histogram in enumerate(histogram_values):
        if histogram > threshold:
            color = "green"
            opacity = histogram/30
            ax1.axvspan(i, i+1, color=color, alpha=opacity)
            ax2.axvspan(i, i+1, color=color, alpha=opacity)
            ax3.axvspan(i, i+1, color=color, alpha=opacity)
        if histogram < -threshold:
            color = "red"
            opacity = -histogram/30
            ax1.axvspan(i, i+1, color=color, alpha=opacity)
            ax2.axvspan(i, i+1, color=color, alpha=opacity)
            ax3.axvspan(i, i+1, color=color, alpha=opacity)

    plt.show()





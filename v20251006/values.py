







# === CLEAN ======================================
clean_all_folders = False

# === DOWNLOAD DATA ======================================
download_from_stooq = False
download_from_bizradar_tendencies = False
download_from_bankier_financial_data = False
print_results = True


print_stock_prices = True
print_tendencies_reports = False
print_quarterly_reports = True





show_all_charts_not_only_selected_by_rsi = False
rows_to_show_in_wyniki = 12

initial_cash = 1_000_000_000
initial_stock_value = 0
buy_amount_pln = 1500
sell_amount_pln = buy_amount_pln

dates_to_parse = -360
loss_that_is_ok = (-1*dates_to_parse) * buy_amount_pln * 0.01 * (-1)
gain_that_must_be = (-1*dates_to_parse) * buy_amount_pln * 0.01

rsi_period = 14
rsi_critical_period = 5
interval = "d"  # "240"=4h     "d"


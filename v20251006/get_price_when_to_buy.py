import math
import json
from typing import Dict, List, Any

# --- STAŁE WYCENY ---
# Współczynnik dla formuły Grahama (22.5 to iloczyn max P/E=15 i max P/B=1.5)
GRAHAM_FACTOR = 22.5
# Sugerowany margines bezpieczeństwa, np. 25%
MARGIN_OF_SAFETY = 0.75  # Oznacza, że cena zakupu to 75% Wartości Wewnętrznej


# --- ISTNIEJĄCE FUNKCJE POMOCNICZE ---

def get_eps_value(indicator_list, index=-1):
    if not indicator_list:
        return None
    try:
        # Format: '0,62r/r +255.15%k/k -4.54%'
        raw_value = str(indicator_list[index]).split('r/r')[0].replace(',', '.')
        return float(raw_value)
    except (IndexError, ValueError, TypeError):
        return None


def get_change(indicator_list, index=-1, change_type='r/r'):
    """
    Ekstrahuje zmianę r/r (rok do roku) lub k/k (kwartał do kwartału)
    dla wskaźników formatu 'wartość~branża...'. Zwraca None w przypadku braku.
    """
    if not indicator_list:
        return None

    try:
        raw_string = str(indicator_list[index])

        if change_type == 'r/r':
            start_marker = 'r/r '
        elif change_type == 'k/k':
            start_marker = 'k/k '
        else:
            return None

        if start_marker not in raw_string:
            return None

        # Wyszukiwanie zmiany dla Spółki, ignorując zmianę dla branży
        parts = raw_string.split('~')

        # Iteracja po częściach (poza samą wartością) w poszukiwaniu r/r lub k/k
        # Używamy pierwszej części (bez ~) bo dane kwartalne nie mają branży

        # Sprawdzamy, czy w głównej części (przed ~) jest r/r lub k/k
        main_part = parts[0]
        if start_marker in main_part:
            start_index = main_part.find(start_marker) + len(start_marker)
            end_index = main_part.find('%', start_index)

            if end_index != -1:
                change_value = main_part[start_index:end_index].replace(',', '.')
                return float(change_value) / 100

    except Exception:
        return None

    return None


def get_value(indicator_list, index=-1):
    if not indicator_list:
        return None
    try:
        raw_value = str(indicator_list[index]).split('~')[0].replace(',', '.')
        # Sprawdzamy i usuwamy 'r/r...' jeśli jest (jak w finansowych z bankiera)
        if 'r/r' in raw_value:
            raw_value = raw_value.split('r/r')[0]

        return float(raw_value)
    except (IndexError, ValueError, TypeError):
        return None


# --- NOWA FUNKCJA OKREŚLAJĄCA CENĘ ZAKUPU ---

def calculate_graham_intrinsic_value(eps: float, bvps: float) -> float:
    """
    Oblicza wartość wewnętrzną akcji na podstawie zmodyfikowanej formuły Grahama:
    V = pierwiastek(22.5 * ZyskNaAkcje * WartośćKsięgowaNaAkcję)
    """
    if eps <= 0 or bvps <= 0:
        # Zero lub ujemna wartość oznacza brak sensownej wyceny tą metodą
        return 0.0

    intrinsic_value = math.sqrt(GRAHAM_FACTOR * eps * bvps)
    return intrinsic_value


def determine_recommended_purchase_price(stock_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Określa zalecaną cenę zakupu, wykorzystując istniejącą strukturę danych
    i wskaźniki EPS oraz BVPS.
    """
    results = {
        "latest_close_price": 0.0,
        "eps_ttm": 0.0,
        "bvps": 0.0,
        "intrinsic_value_graham": 0.0,
        "recommended_purchase_price": 0.0
    }

    try:
        # Pobranie wskaźników finansowych z sekcji `financial_data` (dane z Bankier.pl)
        # Używamy get_value/get_eps_value, które ekstrahują wartość numeryczną

        # Wartość księgowa na akcję (BVPS) - bierzemy ostatnią dostępną wartość
        bvps = get_value(stock_data["financial_data"].get("Wartość księgowa na akcję (zł)", []), -1)
        results["bvps"] = bvps if bvps is not None else 0.0

        # Zysk na akcję (EPS) TTM - bierzemy ostatnią dostępną wartość
        eps = get_value(stock_data["financial_data"].get("Zysk na akcję (zł)", []), -1)
        results["eps_ttm"] = eps if eps is not None else 0.0

        # Ostatnia cena zamknięcia
        latest_close_price = float(stock_data["Close"][-1])
        results["latest_close_price"] = latest_close_price

        # Obliczenie wartości wewnętrznej
        if eps is not None and bvps is not None:
            intrinsic_value = calculate_graham_intrinsic_value(eps, bvps)
            results["intrinsic_value_graham"] = intrinsic_value

            # Określenie zalecanej ceny zakupu (Intrinsic Value * Margines Bezpieczeństwa)
            if intrinsic_value > 0:
                recommended_purchase_price = intrinsic_value * MARGIN_OF_SAFETY
                results["recommended_purchase_price"] = recommended_purchase_price

    except Exception as e:
        print(f"Błąd podczas określania ceny zakupu: {e}")

    return results









#
#
# # Dodanie kluczy 'financial_data' i 'indicators' dla zgodności z Twoim skryptem
# # Uwaga: Twoje funkcje get_value/get_eps_value są zaprojektowane dla danych z financial_data lub indicators
#
# # =========================================================================================
#
# # PRZYKŁADOWY KROK ANALIZY
# stock_to_analyze = mbk_data
#
# # 1. Sprawdzenie, czy spółka jest warta uwagi, używając Twojej logiki
# if is_stock_worth_interest(stock_to_analyze):
#     print(f"Spółka {stock_to_analyze['stock_name']} jest **WARTA INWESTYCJI** (spełnia kryteria fundamentalne).")
#
#     # 2. Określenie zalecanej ceny zakupu
#
#     print("\n--- ANALIZA CENOWA (Metoda Grahama) ---")
#     for key, value in price_analysis.items():
#         print(f"{key.replace('_', ' ').title()}: {value:.2f} PLN")
#
#     # 3. Wniosek końcowy
#     rec_price = price_analysis["recommended_purchase_price"]
#     current_price = price_analysis["latest_close_price"]
#     intrinsic_value = price_analysis["intrinsic_value_graham"]
#
#     if rec_price > 0:
#         print(f"\nPORÓWNANIE:")
#         print(f"Wartość Wewnętrzna (Intrinsic Value): {intrinsic_value:.2f} PLN")
#
#         if rec_price >= current_price:
#             print(
#                 f"Cena rynkowa ({current_price:.2f} PLN) jest PONIŻEJ lub równa zalecanej cenie zakupu ({rec_price:.2f} PLN). Zakup **ZALECANY**. ✅")
#         else:
#             print(
#                 f"Cena rynkowa ({current_price:.2f} PLN) jest WYŻSZA niż zalecana cena zakupu ({rec_price:.2f} PLN). Zakup **NIEZALECANY** ze względu na brak marginesu bezpieczeństwa. ❌")
#
# else:
#     print(
#         f"Spółka {stock_to_analyze['stock_name']} **NIE JEST WARTA INWESTYCJI** (nie spełnia kryteriów fundamentalnych/wzrostowych).")
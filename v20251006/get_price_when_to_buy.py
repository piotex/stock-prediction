import math
from typing import Dict, List, Any

# --- STAŁE WYCENY ---
# Współczynnik Grahama dla P/E * P/BV
GRAHAM_FACTOR = 22.5
# Sugerowany margines bezpieczeństwa (cena zakupu to 75% Wartości Wewnętrznej)
MARGIN_OF_SAFETY = 0.75
# Minimalna konserwatywna średnia P/E, używana do wyceny
CONSERVATIVE_AVG_PE = 15.0


# --- FUNKCJE POMOCNICZE (BEZ ZMIAN) ---

def get_value(indicator_list: List[str], index: int = -1) -> float | None:
    """Ekstrahuje wartość numeryczną (float) z uproszczonego formatu listy wskaźników."""
    if not indicator_list:
        return None
    try:
        raw_value = str(indicator_list[index]).strip().replace(' ', '').replace(',', '.')
        return float(raw_value)
    except (IndexError, ValueError):
        return None


# --- METODA 1: WARTOŚĆ GRAHAMA (Konserwatywna wartość minimalna) ---

def calculate_graham_intrinsic_value(eps: float | None, bvps: float | None) -> tuple[float, str]:
    """
    Oblicza konserwatywną wartość wewnętrzną na podstawie P/E i P/BV.
    Wymaga, by EPS i BVPS były dodatnie.
    """
    if eps is None or bvps is None:
        return 0.0, "Brak danych EPS lub BVPS"

    if eps <= 0:
        return 0.0, f"EPS (Zysk na akcję) jest ujemny/zerowy ({eps:.2f})"

    if bvps <= 0:
        return 0.0, f"BVPS (Wartość księgowa) jest ujemna/zerowa ({bvps:.2f})"

    try:
        # V = pierwiastek(22.5 * EPS * BVPS)
        intrinsic_value = math.sqrt(GRAHAM_FACTOR * eps * bvps)
        return intrinsic_value, "Graham (P/E * P/BV)"
    except ValueError:
        return 0.0, "Błąd obliczenia pierwiastka"


# --- METODA 2: WARTOŚĆ P/E (Wycena Zysków) ---

def calculate_pe_based_value(eps: float | None, pe_ratios: List[str]) -> tuple[float, str]:
    """
    Oblicza wartość docelową na podstawie średniego historycznego P/E i bieżącego EPS.
    Używa konserwatywnego limitu P/E.
    """
    if eps is None or eps <= 0:
        return 0.0, "EPS ujemny/zerowy. Nie można wycenić zysków."
    if not pe_ratios:
        return 0.0, "Brak danych historycznych P/E."

    try:
        # 1. Oblicz średni historyczny P/E
        historic_pe_values = [get_value([r]) for r in pe_ratios if get_value([r]) is not None and get_value([r]) > 0]

        if not historic_pe_values:
            return 0.0, "Brak pozytywnych historycznych P/E."

        # Używamy najniższego z: średnia historyczna lub konserwatywny limit 15.0
        avg_pe_ratio = sum(historic_pe_values) / len(historic_pe_values)
        target_pe = min(avg_pe_ratio, CONSERVATIVE_AVG_PE)

        # 2. Wycena = Docelowy P/E * Aktualny EPS
        value = target_pe * eps
        return value, f"P/E (Średnia historyczna {avg_pe_ratio:.2f})"

    except Exception:
        return 0.0, "Błąd obliczenia P/E."


# --- METODA 3: WARTOŚĆ P/S (Wycena Przychodu) ---

def calculate_sales_revenue_based_value(ps_ratios: List[str], sales_per_share: float | None) -> tuple[float, str]:
    """
    Oblicza wartość docelową na podstawie średniego historycznego P/S (Price/Sales)
    i bieżących przychodów na akcję (Sales Per Share - SPS).
    """
    if sales_per_share is None or sales_per_share <= 0:
        return 0.0, "SPS ujemny/zerowy. Nie można wycenić przychodów."
    if not ps_ratios:
        return 0.0, "Brak danych historycznych P/S."

    try:
        # 1. Oblicz średni historyczny wskaźnik P/S
        historic_ps_values = [get_value([r]) for r in ps_ratios if get_value([r]) is not None and get_value([r]) > 0]

        if not historic_ps_values:
            return 0.0, "Brak pozytywnych historycznych P/S."

        # Używamy średniej historycznej P/S jako 'sprawiedliwego' mnożnika
        avg_ps_ratio = sum(historic_ps_values) / len(historic_ps_values)

        # 2. Wycena = Średni P/S * Aktualne SPS
        value = avg_ps_ratio * sales_per_share
        return value, f"P/S (Średnia historyczna {avg_ps_ratio:.2f})"

    except Exception:
        return 0.0, "Błąd obliczenia P/S."


# --- GŁÓWNA FUNKCJA WYZNACZANIA CENY (AGREGATOR) ---

def determine_recommended_purchase_price(stock_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agreguje wyniki z trzech metod wyceny: Grahama, P/E oraz P/S,
    aby wyznaczyć ostateczną, wyważoną cenę zakupu.
    """
    indicators = stock_data.get("indicators", {})
    results = {
        # Dane Wejściowe
        "latest_close_price": 0.0,
        "eps_ttm": 0.0,
        "bvps": 0.0,
        "sales_per_share": 0.0,

        # Wyceny Poszczególnymi Metodami
        "value_graham": {"value": 0.0, "reason": "N/A"},
        "value_pe": {"value": 0.0, "reason": "N/A"},
        "value_ps": {"value": 0.0, "reason": "N/A"},

        # Wynik Końcowy
        "final_intrinsic_value": 0.0,
        "recommended_purchase_price": 0.0,
        "final_valuation_method": "Brak Zgodnych Wycen"
    }

    try:
        # 1. Pobieranie podstawowych danych i wskaźników historycznych
        bvps = get_value(indicators.get("Wartość księgowa na akcję", []), -1)
        eps = get_value(indicators.get("Zysk na akcję", []), -1)
        latest_close_price = get_value(indicators.get("Kurs", []), -1)
        sales_per_share = get_value(indicators.get("Przychody ze sprzedaży na akcję", []), -1)
        pe_ratios = indicators.get('Cena / Zysk', [])
        ps_ratios = indicators.get('Cena / Przychody ze sprzedaży', [])

        results["bvps"] = bvps if bvps is not None else 0.0
        results["eps_ttm"] = eps if eps is not None else 0.0
        results["latest_close_price"] = latest_close_price if latest_close_price is not None else 0.0
        results["sales_per_share"] = sales_per_share if sales_per_share is not None else 0.0

        # 2. Obliczenia poszczególnymi metodami
        v_graham, r_graham = calculate_graham_intrinsic_value(eps, bvps)
        results["value_graham"] = {"value": v_graham, "reason": r_graham}

        v_pe, r_pe = calculate_pe_based_value(eps, pe_ratios)
        results["value_pe"] = {"value": v_pe, "reason": r_pe}

        v_ps, r_ps = calculate_sales_revenue_based_value(ps_ratios, sales_per_share)
        results["value_ps"] = {"value": v_ps, "reason": r_ps}

        # 3. Agregacja (Uśrednianie)

        valid_valuations = []
        if v_graham > 0:
            valid_valuations.append(v_graham)
        if v_pe > 0:
            valid_valuations.append(v_pe)
        if v_ps > 0:
            valid_valuations.append(v_ps)

        if not valid_valuations:
            # Żadna z metod nie dała sensownej wyceny
            results["recommended_purchase_price"] = 0.0
            results["final_valuation_method"] = "Brak Metod (>0)"
        else:
            # Używamy średniej arytmetycznej z valid_valuations jako wyważonej wartości wewnętrznej
            final_intrinsic_value = sum(valid_valuations) / len(valid_valuations)

            # Wprowadzamy ostatni margines bezpieczeństwa
            results["final_intrinsic_value"] = final_intrinsic_value
            results["recommended_purchase_price"] = final_intrinsic_value * MARGIN_OF_SAFETY
            results["final_valuation_method"] = f"Średnia z {len(valid_valuations)} Metod"

    except Exception as e:
        results["final_valuation_method"] = f"Błąd końcowy: {e}"

    return results
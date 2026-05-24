"""
Build merged dataset: World Bank + WUI
=======================================
Output: merged_dataset.csv
Columns:
    country_iso3, year, region, income_group,
    gdp_per_capita_usd, 
    life_expectancy, health_spend_pct_gdp,
    education_spend_pct_gdp, rd_spend_pct_gdp,
    wui, wui_volatility, govt_effectiveness, researchers_per_million

Requirements:
    pip install pandas requests openpyxl
    WUI_Data.xlsx must be in the same folder as this script
"""

import re
import time
import requests
import pandas as pd
import numpy as np
from pathlib import Path

# ── Settings ──────────────────────────────────────────────
START_YEAR = 1995
END_YEAR   = 2024

NATIONS = [
    "USA","GBR","FRA","DEU","ITA","ESP","NLD","BEL","SWE","NOR",
    "DNK","FIN","AUT","CHE","PRT","IRL","CAN","AUS","NZL","JPN",
    "KOR","ISR","SAU","ARE","QAT","KWT","CHN","BRA","MEX","ARG",
    "ZAF","TUR","POL","HUN","CZE","ROU","MYS","THA","COL","PER",
    "IND","IDN","PAK","EGY","MAR","NGA","KEN","UKR","RUS","IRQ",
    "IRN","GRC",
]

REGION_MAP = {
    "USA":"North America","CAN":"North America",
    "GBR":"Europe","FRA":"Europe","DEU":"Europe","ITA":"Europe",
    "ESP":"Europe","NLD":"Europe","BEL":"Europe","SWE":"Europe",
    "NOR":"Europe","DNK":"Europe","FIN":"Europe","AUT":"Europe",
    "CHE":"Europe","PRT":"Europe","IRL":"Europe","POL":"Europe",
    "HUN":"Europe","CZE":"Europe","ROU":"Europe","GRC":"Europe",
    "UKR":"Europe","RUS":"Europe","TUR":"Europe",
    "JPN":"Asia-Pacific","KOR":"Asia-Pacific","AUS":"Asia-Pacific",
    "NZL":"Asia-Pacific","CHN":"Asia-Pacific","IND":"Asia-Pacific",
    "IDN":"Asia-Pacific","MYS":"Asia-Pacific","THA":"Asia-Pacific",
    "PAK":"Asia-Pacific",
    "SAU":"Middle East","ARE":"Middle East","QAT":"Middle East",
    "KWT":"Middle East","IRQ":"Middle East","IRN":"Middle East",
    "ISR":"Middle East","EGY":"Middle East","MAR":"Middle East",
    "BRA":"Latin America","MEX":"Latin America","ARG":"Latin America",
    "COL":"Latin America","PER":"Latin America",
    "ZAF":"Africa","NGA":"Africa","KEN":"Africa",
}

INCOME_MAP = {
    "USA":"High","GBR":"High","FRA":"High","DEU":"High","ITA":"High",
    "ESP":"High","NLD":"High","BEL":"High","SWE":"High","NOR":"High",
    "DNK":"High","FIN":"High","AUT":"High","CHE":"High","PRT":"High",
    "IRL":"High","CAN":"High","AUS":"High","NZL":"High","JPN":"High",
    "KOR":"High","ISR":"High","SAU":"High","ARE":"High","QAT":"High",
    "KWT":"High","GRC":"High",
    "CHN":"Upper-middle","BRA":"Upper-middle","MEX":"Upper-middle",
    "ARG":"Upper-middle","ZAF":"Upper-middle","TUR":"Upper-middle",
    "POL":"Upper-middle","HUN":"Upper-middle","CZE":"Upper-middle",
    "ROU":"Upper-middle","MYS":"Upper-middle","THA":"Upper-middle",
    "COL":"Upper-middle","PER":"Upper-middle","RUS":"Upper-middle",
    "IRN":"Upper-middle",
    "IND":"Lower-middle","IDN":"Lower-middle","PAK":"Lower-middle",
    "EGY":"Lower-middle","MAR":"Lower-middle","NGA":"Lower-middle",
    "KEN":"Lower-middle","UKR":"Lower-middle","IRQ":"Lower-middle",
}


# ══════════════════════════════════════════════════════════
# STEP 1 — WORLD BANK  (WDI + WGI in separate fetch loops)
# ══════════════════════════════════════════════════════════

# Standard WDI indicators — default source, no extra param needed
WB_WDI = {
    "NY.GDP.PCAP.CD":     "gdp_per_capita_usd",
    "SP.DYN.LE00.IN":     "life_expectancy",
    "SH.XPD.CHEX.GD.ZS":  "health_spend_pct_gdp",
    "SE.XPD.TOTL.GD.ZS":  "education_spend_pct_gdp",
    "GB.XPD.RSDV.GD.ZS":  "rd_spend_pct_gdp",
    "SP.POP.SCIE.RD.P6":  "researchers_per_million",}

# WGI indicators — live in source=3, will fail without it
WB_WGI = {
    "GE.EST": "govt_effectiveness",}

def fetch_wb_indicator(iso, wb_code, col_name, source_param=""):
    """Fetch one indicator for one country. source_param e.g. '&source=3'."""
    url = (
        f"https://api.worldbank.org/v2/country/{iso}"
        f"/indicator/{wb_code}"
        f"?format=json&per_page=500&date={START_YEAR}:{END_YEAR}{source_param}"
    )
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            break
        except Exception:
            time.sleep(2 ** attempt)
    else:
        return []

    rows = []
    try:
        payload = resp.json()
        if len(payload) >= 2 and payload[1]:
            for rec in payload[1]:
                yr  = rec.get("date")
                val = rec.get("value")
                if yr and val is not None:
                    rows.append({
                        "country_iso3": iso,
                        "year":         int(yr),
                        "indicator":    col_name,
                        "value":        float(val),
                    })
    except Exception:
        pass
    return rows


wb_rows = []
total = len(NATIONS) * (len(WB_WDI) + len(WB_WGI))
done  = 0

print("Fetching World Bank WDI indicators...")
for iso in NATIONS:
    for wb_code, col_name in WB_WDI.items():
        wb_rows.extend(fetch_wb_indicator(iso, wb_code, col_name, source_param=""))
        done += 1
        if done % 50 == 0:
            print(f"  {done}/{total} done...")

print("Fetching World Bank WGI indicators (source=75)...")
for iso in NATIONS:
    for wb_code, col_name in WB_WGI.items():
        wb_rows.extend(fetch_wb_indicator(iso, wb_code, col_name, source_param="&source=75"))
        done += 1
        if done % 20 == 0:
            print(f"  {done}/{total} done...")

# ── Pivot long → wide ────────────────────────────────────
wb_long = pd.DataFrame(wb_rows)
wb = wb_long.pivot_table(
    index=["country_iso3", "year"],
    columns="indicator",
    values="value",
    aggfunc="first",
).reset_index()
wb.columns.name = None

# ── Within-country imputation for slow-moving variables ──
IMPUTE_COLS = ["researchers_per_million", "govt_effectiveness"]
wb = wb.sort_values(["country_iso3", "year"])

for col in IMPUTE_COLS:
    if col in wb.columns:
        wb[f"{col}_imputed"] = wb[col].isna()

wb[IMPUTE_COLS] = (
    wb.groupby("country_iso3")[IMPUTE_COLS]
    .transform(lambda s: s.ffill().bfill())
)

# ── Coverage report ───────────────────────────────────────
all_cols = list(WB_WDI.values()) + list(WB_WGI.values())
print(f"\nWorld Bank done: {len(wb)} rows, {wb['country_iso3'].nunique()} nations")
print("\nNull counts after imputation:")
null_report = wb[all_cols].isnull().sum().rename("nulls").to_frame()
null_report["pct_null"] = (null_report["nulls"] / len(wb) * 100).round(1)
print(null_report.to_string())

# ══════════════════════════════════════════════════════════
# STEP 2 — WUI  (from local WUI_Data.xlsx, sheet T2)
# ══════════════════════════════════════════════════════════

PROJECT_DIR = Path("/home/raulginomiranda/MyProjects/FINAL PROJECT")

wui_file = PROJECT_DIR / "WUI_Data.xlsx"

print("\nReading WUI_Data.xlsx ...")

if not wui_file.exists():
    print(f"  Looked here: {wui_file.resolve()}")   # <-- add this line
    print("  ERROR: WUI_Data.xlsx not found in this folder.")
    print("  Download from worlduncertaintyindex.com/data/ and re-run.")
    wui = pd.DataFrame(columns=["country_iso3","year","wui","wui_volatility"])
else:
    # Sheet T2: rows = quarters ("1990q1"), columns = ISO-3 codes
    raw = pd.read_excel(wui_file, sheet_name="T2", header=0, index_col=0)
    print(f"  T2 shape: {raw.shape}")

    wui_rows = []
    for idx_val, row in raw.iterrows():
        # Parse quarter index e.g. "1995q1"
        m = re.search(r"([0-9]{4})[^0-9]?[qQ]([0-9])", str(idx_val))
        if not m:
            continue
        year = int(m.group(1))
        qtr  = int(m.group(2))
        if year < START_YEAR or year > END_YEAR:
            continue
        for col_name, val in row.items():
            iso3 = str(col_name).strip().upper()
            if iso3 not in NATIONS:
                continue
            try:
                vf = float(val)
                if not np.isnan(vf):
                    wui_rows.append({
                        "country_iso3": iso3,
                        "year":         year,
                        "quarter":      qtr,
                        "wui_q":        vf,
                    })
            except (TypeError, ValueError):
                continue

    wui_long = pd.DataFrame(wui_rows)

    # Annualize: mean = annual WUI, std = within-year volatility
    wui_mean = (wui_long.groupby(["country_iso3","year"])["wui_q"]
                        .mean().reset_index()
                        .rename(columns={"wui_q":"wui"}))
    wui_std  = (wui_long.groupby(["country_iso3","year"])["wui_q"]
                        .std().reset_index()
                        .rename(columns={"wui_q":"wui_volatility"}))
    wui = wui_mean.merge(wui_std, on=["country_iso3","year"], how="left")
    print(f"  WUI done: {len(wui)} rows, {wui['country_iso3'].nunique()} nations")


# ══════════════════════════════════════════════════════════
# STEP 3 — MERGE
# ══════════════════════════════════════════════════════════

print("\nMerging...")

# Base grid: every nation x every year
grid = pd.DataFrame(
    [(iso, yr) for iso in NATIONS for yr in range(START_YEAR, END_YEAR + 1)],
    columns=["country_iso3", "year"]
)

# Add metadata
grid["region"]       = grid["country_iso3"].map(REGION_MAP)
grid["income_group"] = grid["country_iso3"].map(INCOME_MAP)

# Merge World Bank
df = grid.merge(wb, on=["country_iso3","year"], how="left")

# Merge WUI
df = df.merge(wui, on=["country_iso3","year"], how="left")

# Forward/back fill minor gaps within country (interpolate, don't extrapolate)
fill_cols = ["gdp_per_capita_usd","life_expectancy",
                 "education_spend_pct_gdp","health_spend_pct_gdp",
                 "rd_spend_pct_gdp","wui","wui_volatility", "researchers_per_million", "govt_effectiveness"]
df = df.sort_values(["country_iso3","year"])
for col in fill_cols:
    if col in df.columns:
        df[col] = (df.groupby("country_iso3")[col]
                     .transform(lambda s: s.interpolate(method="linear")
                                           .ffill().bfill())) 

# Final column order
col_order = [
    "country_iso3", "year", "region", "income_group",
    "gdp_per_capita_usd", 
    "life_expectancy", "health_spend_pct_gdp",
    "education_spend_pct_gdp", "rd_spend_pct_gdp","researchers_per_million", "govt_effectiveness",
    "wui", "wui_volatility",
]
df = df[[c for c in col_order if c in df.columns]]
df = df.sort_values(["country_iso3","year"]).reset_index(drop=True)


# ══════════════════════════════════════════════════════════
# STEP 4 — SAVE
# ══════════════════════════════════════════════════════════

wb.to_csv(PROJECT_DIR/"worldbank.csv", index=False)
wui.to_csv(PROJECT_DIR/"wuncertindex.csv", index=False)
df.to_csv(PROJECT_DIR/"merged_dataset.csv", index=False)
print(f"\nSaved: worldbank.csv")
print(f"\nSaved: wuncertindex.csv")
print(f"\nSaved: merged_dataset.csv")
print(f"  Rows:    {len(df)}")
print(f"  Columns: {list(df.columns)}")
print(f"\nMissing values per column:")
for col in df.columns:
    n = df[col].isna().sum()
    if n > 0:
        print(f"  {col:<30} {n:>4} missing  ({100*n/len(df):.1f}%)")
print("\nDone.")

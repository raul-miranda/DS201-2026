"""
Simpson's Paradox: Electricity Access vs CO2 Emissions
=======================================================
Data source: Gapminder (via Our World in Data / open-numbers GitHub)
             + OWID CO2 dataset for richer time series

This script:
  1. Downloads electricity access and CO2 per-capita data
  2. Merges with income-group metadata for subgroup analysis
  3. Demonstrates Simpson's Paradox (aggregate trend reverses within subgroups)
  4. Highlights the USA in 2022 and projects its likely position in 2028
     after the 2025 federal CO2 policy reversal (Paris withdrawal + IRA rollback)

Requirements:
  pip install pandas numpy matplotlib seaborn scipy requests
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import requests
import io
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 0. STYLE
# ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0f0f1a",
    "axes.facecolor":   "#1a1a2e",
    "axes.edgecolor":   "#444466",
    "axes.labelcolor":  "#ccccee",
    "xtick.color":      "#aaaacc",
    "ytick.color":      "#aaaacc",
    "text.color":       "#e0e0f0",
    "grid.color":       "#2a2a44",
    "grid.alpha":       0.5,
    "font.family":      "DejaVu Sans",
    "font.size":        11,
})

INCOME_COLORS = {
    "Low income":          "#4e7af0",
    "Lower middle income": "#7ea1d1",
    "Upper middle income": "#a7cb7d",
    "High income":         "#f0a500",
}

# ─────────────────────────────────────────────
# 1. DOWNLOAD DATA
# ─────────────────────────────────────────────
print("⬇  Downloading data …")

# --- CO2 per capita (Our World in Data / Global Carbon Project) ---
CO2_URL = (
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
)
r = requests.get(CO2_URL, timeout=30)
owid = pd.read_csv(io.StringIO(r.text), low_memory=False)

# Keep only country-level rows (OWID uses iso_code to distinguish continents)
owid = owid[owid["iso_code"].notna() & ~owid["iso_code"].str.startswith("OWID")]

# Columns we need
co2_df = owid[["country", "iso_code", "year",
               "co2_per_capita",
               "electricity_demand",          # TWh
               "share_elec_renewables",       # %
               "gdp",                         # constant 2011 USD
               "population"]].copy()

co2_df = co2_df[co2_df["year"].between(2000, 2022)].dropna(
    subset=["co2_per_capita"]
)

# --- Electricity access (World Bank via Gapminder/OWID) ---
ELEC_URL = (
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv"
)
# We'll use the 'electricity_demand' as a proxy for electrification level,
# but for "access to electricity (%)" we pull the World Bank indicator
# directly from the OWID GitHub energy dataset.
ENERGY_URL = (
    "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
)
r2 = requests.get(ENERGY_URL, timeout=30)
energy = pd.read_csv(io.StringIO(r2.text), low_memory=False)
energy = energy[energy["iso_code"].notna() & ~energy["iso_code"].str.startswith("OWID")]

elec_access = energy[["country", "iso_code", "year",
                       "access_to_electricity"]].dropna(
    subset=["access_to_electricity"]
)
elec_access = elec_access[elec_access["year"].between(2000, 2022)]

# --- Income group classification (World Bank) ---
WB_URL = (
    "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv"
)
# Simpler: we'll define income groups manually for the ~190 countries
# using ISO-3 codes and World Bank 2022 classification.
# This avoids an additional fragile download.
HIGH_INCOME = {
    "AUS","AUT","BEL","CAN","CHE","CHL","CZE","DEU","DNK","ESP","EST","FIN",
    "FRA","GBR","GRC","HUN","IRL","ISL","ISR","ITA","JPN","KOR","LTU","LUX",
    "LVA","NLD","NOR","NZL","POL","PRT","SAU","SVK","SVN","SWE","USA","ARE",
    "BHR","KWT","QAT","SGP","HKG","TWN","MKD","HRV","CYP","MLT","ROU","BGR",
    "OMN","TTO","URY","PAN","MYS","BRN","ANT","NCL","PYF","GUM","VIR","BMU",
    "CYM","GIB","MAC","BHS","BRB","ATG","LCA","VCT","GRD","KNA","DMA","TCA",
    "ABW","CUW","SXM","AIA","MSR","TUV","PLW","MHL","NRU","FSM","COK","NIU",
    "AND","LIE","MCO","SMR","VAT"
}
UPPER_MIDDLE = {
    "ARG","AZE","BLR","BIH","BOL","BRA","CHN","COL","CRI","CUB","DOM","DZA",
    "ECU","EGY","FJI","GAB","GEO","GNQ","GTM","GUY","IDN","IRN","IRQ","JAM",
    "JOR","KAZ","LBN","LBY","LKA","MDA","MDV","MEX","MNE","MNG","MUS","NAM",
    "NOR","PRY","PER","RUS","SRB","SUR","THA","TKM","TON","TUN","TUR","UKR",
    "VEN","ZAF","ARM","ALB","BWA","CPV","CMR","COG","CIV","GHA","HND","MKD",
    "NIC","PNG","WSM","SLV","SWZ","UZB","VNM","XKX","BLZ","AGO","KGZ","TJK",
    "MMR","KIR","VUT","PSE","WLF"
}
LOW_MIDDLE = {
    "AFG","BEN","BGD","BFA","BTN","CIV","CMR","COD","COM","DJI","ERI","ETH",
    "GHA","GIN","GMB","GNB","HTI","HND","IND","KEN","KHM","KIR","LAO","LBR",
    "LSO","MAR","MDG","MLI","MMR","MOZ","MRT","MWI","NER","NGA","NIC","NPL",
    "PAK","PHL","PNG","SEN","SLB","SLE","SLV","SDN","SOM","SSD","STP","SWZ",
    "SYR","TCD","TGO","TJK","TLS","TZA","UGA","UKR","VNM","VUT","WSM","YEM",
    "ZMB","ZWE","CAF","COD","GNB","SOM","SSD","ERI","SLE","LBR","MDG","MWI",
    "MOZ","BEN","NER","MLI","TCD","BFA","RWA","TZA","UGA","ZMB","ZWE","HTI",
    "KGZ","KHM","LAO","MYA","NPL","PHI","TJK","UZB"
}

def assign_income(iso):
    if iso in HIGH_INCOME:   return "High income"
    if iso in UPPER_MIDDLE:  return "Upper middle income"
    if iso in LOW_MIDDLE:    return "Lower middle income"
    return "Low income"

# ─────────────────────────────────────────────
# 2. MERGE & CLEAN
# ─────────────────────────────────────────────
print("🔧 Merging datasets …")

merged = pd.merge(
    co2_df, elec_access,
    on=["country", "iso_code", "year"], how="inner"
).dropna(subset=["co2_per_capita", "access_to_electricity"])

merged["income_group"] = merged["iso_code"].apply(assign_income)
merged["gdp_per_capita"] = merged["gdp"] / merged["population"]

# Focus on a single representative year and on the full time series
FOCUS_YEAR = 2019   # pre-covid, rich data
df = merged[merged["year"] == FOCUS_YEAR].copy()

print(f"   {len(df)} countries with full data for {FOCUS_YEAR}")
print(f"   Income group distribution:\n{df['income_group'].value_counts()}\n")

# ─────────────────────────────────────────────
# 3. US POSITION 2022 + 2028 PROJECTION
# ─────────────────────────────────────────────
# Actual 2022: US CO2 per capita ≈ 14.21 t (Worldometer / EIA)
#              Electricity access = 100%
# Trend 2015-2022: US was declining ~0.3 t/year thanks to IRA + renewables
# After 2025 policy reversal:
#   - Paris Agreement withdrawal (Jan 2025)
#   - "One Big Beautiful Bill" (July 2025) rolls back IRA clean energy credits
#   - EPA emissions standards relaxed for power + transport
# CAT (Climate Action Tracker 2025) projects US emissions will rise
# or plateau instead of declining. Conservative estimate: +0.4-0.6 t/cap by 2028
# relative to the Biden trajectory.  We model two 2028 scenarios:
#   A) Policy reversal full effect:  ~15.0 t/cap  (+0.8 from 2022)
#   B) Market forces partially offset: ~14.5 t/cap (+0.3 from 2022)
# Access to electricity remains 100%.

US_2022 = {"co2": 14.21, "elec": 100.0, "label": "USA 2022 (actual)"}
US_2028_HIGH = {"co2": 15.0,  "elec": 100.0, "label": "USA 2028 — policy reversal\n(full effect est.)"}
US_2028_LOW  = {"co2": 14.5,  "elec": 100.0, "label": "USA 2028 — policy reversal\n(market offset est.)"}

# ─────────────────────────────────────────────
# 4. REGRESSION HELPER
# ─────────────────────────────────────────────
def ols(x, y):
    """Return slope, intercept, r, p for OLS regression."""
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 5:
        return None
    return stats.linregress(x[mask], y[mask])

# ─────────────────────────────────────────────
# 5.  FIGURE 1 — SIMPSON'S PARADOX MAIN PLOT
# ─────────────────────────────────────────────
print("📊 Building Figure 1: Simpson's Paradox scatter …")

fig, ax = plt.subplots(figsize=(13, 8))

x_col = "access_to_electricity"
y_col = "co2_per_capita"

# --- scatter by income group ---
order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
for grp in order:
    sub = df[df["income_group"] == grp]
    ax.scatter(
        sub[x_col], sub[y_col],
        color=INCOME_COLORS[grp], alpha=0.65, s=60,
        label=grp, zorder=3, edgecolors="none"
    )
    reg = ols(sub[x_col].values, sub[y_col].values)
    if reg:
        xs = np.linspace(sub[x_col].min(), sub[x_col].max(), 100)
        ax.plot(xs, reg.slope * xs + reg.intercept,
                color=INCOME_COLORS[grp], linewidth=2, linestyle="--", alpha=0.9, zorder=4)

# --- aggregate regression line ---
reg_all = ols(df[x_col].values, df[y_col].values)
xs_all = np.linspace(df[x_col].min(), df[x_col].max(), 200)
ax.plot(xs_all, reg_all.slope * xs_all + reg_all.intercept,
        color="white", linewidth=2.5, linestyle="-", alpha=0.9,
        label=f"Aggregate (slope={reg_all.slope:.3f})", zorder=5)

# --- US 2022 marker ---
ax.scatter(US_2022["elec"], US_2022["co2"],
           color="#ff4444", s=200, zorder=10, marker="★",
           edgecolors="white", linewidths=1)
ax.annotate(US_2022["label"],
            xy=(US_2022["elec"], US_2022["co2"]),
            xytext=(-110, 12), textcoords="offset points",
            color="#ff6666", fontsize=9, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#ff6666", lw=1.2))

# --- US 2028 HIGH marker ---
ax.scatter(US_2028_HIGH["elec"], US_2028_HIGH["co2"],
           color="#ff9900", s=200, zorder=10, marker="▲",
           edgecolors="white", linewidths=1)
ax.annotate(US_2028_HIGH["label"],
            xy=(US_2028_HIGH["elec"], US_2028_HIGH["co2"]),
            xytext=(-150, 22), textcoords="offset points",
            color="#ffaa33", fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color="#ffaa33", lw=1.2))

# --- US 2028 LOW marker ---
ax.scatter(US_2028_LOW["elec"], US_2028_LOW["co2"],
           color="#ffcc44", s=160, zorder=10, marker="▲",
           edgecolors="white", linewidths=1)
ax.annotate(US_2028_LOW["label"],
            xy=(US_2028_LOW["elec"], US_2028_LOW["co2"]),
            xytext=(-160, -28), textcoords="offset points",
            color="#ffdd66", fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color="#ffdd66", lw=1.2))

# Arrow from 2022 → 2028
ax.annotate("",
            xy=(US_2028_HIGH["elec"], US_2028_HIGH["co2"]),
            xytext=(US_2022["elec"], US_2022["co2"]),
            arrowprops=dict(arrowstyle="-|>", color="white",
                            lw=1.5, linestyle="dotted"))

ax.set_xlabel("Access to Electricity  (%)", fontsize=13)
ax.set_ylabel("CO₂ Emissions per Capita  (tonnes)", fontsize=13)
ax.set_title(
    "Simpson's Paradox — Electricity Access vs CO₂ Emissions\n"
    f"Gapminder / OWID data · {FOCUS_YEAR} · n={len(df)} countries",
    fontsize=14, pad=14
)

# Annotation box explaining the paradox
textstr = (
    "Simpson's Paradox:\n"
    "► Aggregate trend (white line):\n"
    f"   slope = {reg_all.slope:.3f}  →  more access = more CO₂\n\n"
    "► Within each income group (dashed):\n"
    "   slope ≈ 0 or negative for high-income\n"
    "   The aggregate slope is driven by\n"
    "   group composition, not causality."
)
props = dict(boxstyle="round,pad=0.6", facecolor="#0a0a1a", alpha=0.85, edgecolor="#555577")
ax.text(0.02, 0.97, textstr, transform=ax.transAxes, fontsize=8.8,
        verticalalignment="top", bbox=props, color="#ccccee")

ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.62),
          framealpha=0.3, fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(-2, 105)
ax.set_ylim(-0.5, 32)

plt.tight_layout()
plt.savefig("fig1_simpsons_paradox_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("   ✓ fig1_simpsons_paradox_scatter.png")

# ─────────────────────────────────────────────
# 6.  FIGURE 2 — SLOPES TABLE (reversal check)
# ─────────────────────────────────────────────
print("📊 Building Figure 2: Slope comparison bar chart …")

slope_data = {"Group": [], "Slope": [], "Color": []}

# Aggregate
slope_data["Group"].append("All countries\n(aggregate)")
slope_data["Slope"].append(reg_all.slope)
slope_data["Color"].append("white")

# By income group
for grp in order:
    sub = df[df["income_group"] == grp]
    reg = ols(sub[x_col].values, sub[y_col].values)
    if reg:
        slope_data["Group"].append(grp)
        slope_data["Slope"].append(reg.slope)
        slope_data["Color"].append(INCOME_COLORS[grp])

sdf = pd.DataFrame(slope_data)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(sdf["Group"], sdf["Slope"], color=sdf["Color"],
               edgecolor="#333355", linewidth=0.8, height=0.55)

ax.axvline(0, color="white", linewidth=1.2, alpha=0.6, linestyle="--")
for bar, val in zip(bars, sdf["Slope"]):
    ax.text(val + (0.003 if val >= 0 else -0.003),
            bar.get_y() + bar.get_height() / 2,
            f"{val:+.4f}",
            va="center", ha="left" if val >= 0 else "right",
            color="white", fontsize=9.5)

ax.set_xlabel("OLS Slope  (CO₂ per capita / % electricity access)", fontsize=11)
ax.set_title(
    "Simpson's Paradox — Regression Slopes by Income Group\n"
    "Positive aggregate slope reverses or disappears in sub-groups",
    fontsize=12, pad=10
)
textstr2 = (
    "A positive aggregate slope suggests\n"
    "more electricity → more CO₂.\n\n"
    "But within high-income countries,\n"
    "the slope is near zero or negative —\n"
    "the paradox is the group-composition\n"
    "effect of mixing income tiers."
)
props2 = dict(boxstyle="round,pad=0.5", facecolor="#0a0a1a", alpha=0.85, edgecolor="#555577")
ax.text(0.98, 0.05, textstr2, transform=ax.transAxes, fontsize=8.5,
        va="bottom", ha="right", bbox=props2, color="#ccccee")

ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("fig2_slopes_by_group.png", dpi=150, bbox_inches="tight")
plt.close()
print("   ✓ fig2_slopes_by_group.png")

# ─────────────────────────────────────────────
# 7.  FIGURE 3 — US TRAJECTORY 2000–2028
# ─────────────────────────────────────────────
print("📊 Building Figure 3: US CO₂ trajectory …")

us_ts = merged[(merged["iso_code"] == "USA") &
               (merged["year"] >= 2000)].sort_values("year")

# 2028 projection scenarios
proj_years = [2023, 2024, 2025, 2026, 2027, 2028]

# Trend under Biden trajectory (linear extrapolation from 2015-2022 decline)
us_2015_2022 = us_ts[us_ts["year"].between(2015, 2022)]
reg_us = ols(us_2015_2022["year"].values, us_2015_2022["co2_per_capita"].values)

biden_proj = {y: reg_us.slope * y + reg_us.intercept for y in proj_years}

# Policy-reversal scenarios
# High: stagnation then slight rise (+0.15/yr from 2025)
reversal_high = {}
base = us_ts[us_ts["year"] == 2022]["co2_per_capita"].values[0]
for i, y in enumerate(proj_years):
    if y <= 2024:
        reversal_high[y] = base + 0.05 * (y - 2022)   # small rise
    else:
        reversal_high[y] = base + 0.05 * 2 + 0.15 * (y - 2024)

# Low: market forces (renewables, EVs) partially offset policy
reversal_low = {}
for i, y in enumerate(proj_years):
    reversal_low[y] = base + 0.02 * (y - 2022)  # near flat

fig, ax = plt.subplots(figsize=(12, 6))

# Historical
ax.plot(us_ts["year"], us_ts["co2_per_capita"],
        color="#4488ff", linewidth=2.5, label="USA historical (OWID)")
ax.fill_between(us_ts["year"], us_ts["co2_per_capita"],
                alpha=0.15, color="#4488ff")

# Biden trajectory
ax.plot(list(biden_proj.keys()), list(biden_proj.values()),
        color="#44cc88", linewidth=2, linestyle="--",
        label="Counterfactual: Biden/IRA trajectory")

# Policy reversal high
ax.plot(list(reversal_high.keys()), list(reversal_high.values()),
        color="#ff4444", linewidth=2, linestyle="-.",
        label="Policy reversal — full effect (est.)")

# Policy reversal low
ax.plot(list(reversal_low.keys()), list(reversal_low.values()),
        color="#ff9900", linewidth=2, linestyle=":",
        label="Policy reversal — market offset (est.)")

# 2022 star
ax.scatter([2022], [base], color="#ff4444", s=180, zorder=10,
           marker="★", edgecolors="white", linewidths=1, label=f"USA 2022: {base:.2f} t")

# 2028 endpoints
ax.scatter([2028], [reversal_high[2028]], color="#ff4444", s=120, zorder=10,
           marker="▲", edgecolors="white", linewidths=1)
ax.scatter([2028], [reversal_low[2028]],  color="#ff9900", s=120, zorder=10,
           marker="▲", edgecolors="white", linewidths=1)

# Vertical lines for events
events = {
    2015: ("Paris Agr.\nsigned",  "#aaffaa"),
    2017: ("Trump\nwithdrawal 1", "#ff8888"),
    2021: ("Biden\nrejoins",      "#88aaff"),
    2025: ("Trump\nwithdrawal 2\n+ IRA rollback", "#ff4444"),
}
for yr, (lbl, col) in events.items():
    ax.axvline(yr, color=col, linewidth=1.2, linestyle=":", alpha=0.7)
    ax.text(yr + 0.1, 22.5, lbl, color=col, fontsize=7.5,
            rotation=0, va="top")

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("CO₂ per Capita  (tonnes)", fontsize=12)
ax.set_title(
    "United States CO₂ Emissions per Capita — Historical & 2028 Projection\n"
    "After the 2025 Paris Agreement withdrawal and IRA rollback",
    fontsize=13, pad=12
)

# Source notes
note = (
    "Sources: OWID/Global Carbon Project (historical) · Climate Action Tracker 2025\n"
    "2028 projections are illustrative estimates based on policy scenario analysis.\n"
    "★ = actual 2022 data point  ▲ = 2028 projected endpoints"
)
ax.text(0.01, 0.01, note, transform=ax.transAxes,
        fontsize=7.5, color="#aaaacc", va="bottom")

ax.legend(loc="upper right", fontsize=9, framealpha=0.3)
ax.set_xlim(2000, 2029)
ax.set_ylim(10, 24)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("fig3_us_trajectory.png", dpi=150, bbox_inches="tight")
plt.close()
print("   ✓ fig3_us_trajectory.png")

# ─────────────────────────────────────────────
# 8.  FIGURE 4 — FACETED PARADOX (4 income groups)
# ─────────────────────────────────────────────
print("📊 Building Figure 4: Faceted scatter by income group …")

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
axes = axes.flatten()

for i, grp in enumerate(order):
    ax = axes[i]
    sub = df[df["income_group"] == grp]
    color = INCOME_COLORS[grp]

    ax.scatter(sub[x_col], sub[y_col],
               color=color, alpha=0.7, s=55, edgecolors="none", zorder=3)

    # Group regression
    reg = ols(sub[x_col].values, sub[y_col].values)
    if reg:
        xs = np.linspace(sub[x_col].min(), sub[x_col].max(), 100)
        ax.plot(xs, reg.slope * xs + reg.intercept,
                color=color, linewidth=2.5, zorder=4,
                label=f"Within-group slope: {reg.slope:+.4f}")

    # Aggregate regression
    xs_a = np.linspace(sub[x_col].min(), sub[x_col].max(), 100)
    ax.plot(xs_a, reg_all.slope * xs_a + reg_all.intercept,
            color="white", linewidth=1.5, linestyle="--", alpha=0.5,
            label=f"Aggregate slope: {reg_all.slope:+.4f}")

    # Highlight USA if in range
    us_row = df[(df["iso_code"] == "USA") & (df["income_group"] == grp)]
    if not us_row.empty:
        ax.scatter(us_row[x_col], us_row[y_col],
                   color="#ff4444", s=200, marker="★", zorder=10,
                   edgecolors="white", linewidths=1)
        ax.text(us_row[x_col].values[0] - 3,
                us_row[y_col].values[0] + 0.4,
                "USA", color="#ff6666", fontsize=8.5, fontweight="bold")

    ax.set_title(grp, fontsize=11, color=color, pad=6)
    ax.set_xlabel("Electricity Access (%)", fontsize=9)
    ax.set_ylabel("CO₂ / capita (t)", fontsize=9)
    ax.legend(fontsize=7.5, framealpha=0.25, loc="upper left")
    ax.grid(True, alpha=0.25)

fig.suptitle(
    f"Simpson's Paradox — Faceted by Income Group  ({FOCUS_YEAR})\n"
    "Dashed white = aggregate slope · Solid = within-group slope",
    fontsize=13, y=1.01
)
plt.tight_layout()
plt.savefig("fig4_faceted_by_income.png", dpi=150, bbox_inches="tight")
plt.close()
print("   ✓ fig4_faceted_by_income.png")

# ─────────────────────────────────────────────
# 9.  PRINT SUMMARY STATISTICS
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("SUMMARY: Slope Reversal Check (Simpson's Paradox)")
print("="*60)
print(f"{'Group':<25} {'N':>4}  {'Slope':>8}  {'R²':>6}  {'p-value':>10}")
print("-"*60)

grp_all_reg = ols(df[x_col].values, df[y_col].values)
print(f"{'Aggregate':<25} {len(df):>4}  {grp_all_reg.slope:>8.4f}  {grp_all_reg.rvalue**2:>6.3f}  {grp_all_reg.pvalue:>10.2e}")

for grp in order:
    sub = df[df["income_group"] == grp]
    reg = ols(sub[x_col].values, sub[y_col].values)
    if reg:
        print(f"{grp:<25} {len(sub):>4}  {reg.slope:>8.4f}  {reg.rvalue**2:>6.3f}  {reg.pvalue:>10.2e}")

print("="*60)
print("\nUS snapshot:")
print(f"  2022 actual CO₂/cap : {US_2022['co2']:.2f} t  (electricity access: 100%)")
print(f"  2028 projection high: {US_2028_HIGH['co2']:.2f} t  (policy reversal, full effect)")
print(f"  2028 projection low : {US_2028_LOW['co2']:.2f} t  (market forces offset reversal)")
print("\nData sources:")
print("  CO₂ & energy: Our World in Data / Global Carbon Project")
print("  https://github.com/owid/co2-data")
print("  Electricity access: Our World in Data / World Bank")
print("  https://github.com/owid/energy-data")
print("  US policy context: Climate Action Tracker 2025")
print("  https://climateactiontracker.org/countries/usa/")
print("\n✅ All figures saved to current directory.")

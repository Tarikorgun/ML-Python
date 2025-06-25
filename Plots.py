import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# CSV laden
df = pd.read_csv("grow_attributes.csv", delimiter=';', low_memory=False)

# Jahr extrahieren für Zeitvergleich
df['starting_year'] = pd.to_datetime(df['starting_date']).dt.year
df['ending_year'] = pd.to_datetime(df['ending_date']).dt.year

# Filter-Kriterien
df['over_30_years'] = df['length_years'] >= 30
df['gap_free'] = df['gap_fraction'] == 0.0
df['monthly'] = df['interval'] == 'MS'
df['ends_2023_or_later'] = df['ending_year'] >= 2023


# Scatterplot der Messstellen auf Weltkarte
if {'latitude', 'longitude'}.issubset(df.columns):
    plt.figure(figsize=(12, 6))
    plt.scatter(df['longitude'], df['latitude'], s=1, alpha=0.4, c='red')
    plt.title("Verteilung der Grundwassermessstellen (Scatter)")
    plt.xlabel("Längengrad")
    plt.ylabel("Breitengrad")
    plt.tight_layout()
    plt.savefig("karte_messstellen_scatter.png", dpi=300)
    plt.show()

# Top 10 Länder mit den meisten Messstellen
plt.figure(figsize=(12,6))
df['country'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Länder nach Anzahl der Messstellen")
plt.xlabel("Land")
plt.ylabel("Anzahl")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("barplot_laender.png", dpi=300)
plt.show()

# Anteil Messreihen ≥30 Jahre
plt.figure(figsize=(12, 6))
ax = df.groupby('country')['over_30_years'].mean().sort_values(ascending=False).plot(kind='bar', color='mediumseagreen')
plt.title("Anteil Messreihen ≥30 Jahre pro Land")
plt.ylabel("Anteil")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("vergleich_messdauer_all_countries.png", dpi=300)
plt.show()

# Anteil gap-freier Reihen
plt.figure(figsize=(12, 6))
ax = df.groupby('country')['gap_free'].mean().sort_values(ascending=False).plot(kind='bar', color='salmon')
plt.title("Anteil gap-freier Reihen pro Land (gap_fraction = 0.0)")
plt.ylabel("Anteil")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("vergleich_gap_free_all_countries.png", dpi=300)
plt.show()

# Anteil Reihen mit Endjahr ≥2023
plt.figure(figsize=(12, 6))
ax = df.groupby('country')['ends_2023_or_later'].mean().sort_values(ascending=False).plot(kind='bar', color='darkorange')
plt.title("Anteil aktueller Reihen (Endjahr ≥2023)")
plt.ylabel("Anteil")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("vergleich_aktualitaet_all_countries.png", dpi=300)
plt.show()

# Anteil Monatsintervall (MS)
plt.figure(figsize=(12, 6))
ax = df.groupby('country')['monthly'].mean().sort_values(ascending=False).plot(kind='bar', color='cornflowerblue')
plt.title("Anteil Monatsintervall (MS) pro Land")
plt.ylabel("Anteil")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("vergleich_intervall_all_countries.png", dpi=300)
plt.show()


# Fehlende Werte pro Spalte
missing = df.isnull().sum().sort_values(ascending=False)
missing = missing[missing > 0]

if not missing.empty:
    plt.figure(figsize=(12,6))
    sns.barplot(x=missing.values, y=missing.index, palette='Reds_r')
    plt.title("Fehlende Werte pro Spalte")
    plt.xlabel("Anzahl fehlender Werte")
    plt.ylabel("Spalte")
    plt.tight_layout()
    plt.savefig("fehlende_werte.png", dpi=300)
    plt.show()

# Höhenlage nach Land
if 'surface_elevation_m_asl' in df.columns:
    plt.figure(figsize=(14,6))
    sns.boxplot(x="country", y="surface_elevation_m_asl", data=df)
    plt.title("Verteilung der Höhenlage pro Land")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("boxplot_hoehenlage.png", dpi=300)
    plt.show()

# Histogramm Höhenlage allgemein
if 'surface_elevation_m_asl' in df.columns:
    df['surface_elevation_m_asl'].dropna().hist(bins=50, color='green', figsize=(10,6))
    plt.title("Verteilung der Höhenlage aller Messstellen")
    plt.xlabel("Höhe (m ü. NN)")
    plt.ylabel("Anzahl")
    plt.tight_layout()
    plt.savefig("histogramm_hoehenlage.png", dpi=300)
    plt.show()

# Landnutzung
if 'main_landuse' in df.columns:
    df['main_landuse'].value_counts().head(10).plot(kind='bar', color='peru', figsize=(10,5))
    plt.title("Häufigste Landnutzungsarten")
    plt.xlabel("Landnutzung")
    plt.ylabel("Anzahl")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("barplot_landnutzung.png", dpi=300)
    plt.show()

# Korrelationsmatrix numerischer Werte
numeric_df = df.select_dtypes(include=['float64', 'int64'])
if not numeric_df.empty:
    corr = numeric_df.corr()
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=False, cmap="coolwarm", fmt=".2f")
    plt.title("Korrelationsmatrix numerischer Variablen")
    plt.tight_layout()
    plt.savefig("korrelationsmatrix.png", dpi=300)
    plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

df = pd.read_csv("grow_attributes.csv", delimiter=';', low_memory=False)

df_cz = df[df["country"] == "CZE"].copy()

df_cz['starting_year'] = pd.to_datetime(df_cz['starting_date']).dt.year
df_cz['ending_year'] = pd.to_datetime(df_cz['ending_date']).dt.year

print(f"Anzahl der Messstellen in Tschechien (CZE): {len(df_cz)}")

if df_cz.empty:
    raise ValueError("Keine Daten für Tschechien (CZE) gefunden. Bitte prüfen Sie die Eingabedatei und den Ländercode.")

plt.figure(figsize=(10, 6))
df_cz['length_years'].dropna().hist(bins=50, color='purple', edgecolor='black')
plt.title("Verteilung der Länge der Messreihen in Tschechien (Jahre)")
plt.xlabel("Länge der Messreihe (Jahre)")
plt.ylabel("Anzahl der Messstellen")
plt.tight_layout()
plt.savefig("CZ_histogramm_length_years.png", dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
df_cz['gap_fraction'].dropna().hist(bins=50, color='teal', edgecolor='black')
plt.title("Verteilung des Anteils fehlender Werte in Tschechien (gap_fraction)")
plt.xlabel("Anteil fehlender Werte")
plt.ylabel("Anzahl der Messstellen (log-Skala)")
plt.yscale('log')
plt.tight_layout()
plt.savefig("CZ_histogramm_gap_fraction_log_y.png", dpi=300)
plt.show()

plt.figure(figsize=(12, 6))
df_cz['starting_year'].value_counts().sort_index().plot(kind='bar', color='darkblue')
plt.title("Anzahl der Messstellen in Tschechien pro Startjahr")
plt.xlabel("Startjahr")
plt.ylabel("Anzahl der Messstellen")
plt.xticks(rotation=90, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig("CZ_barplot_starting_year.png", dpi=300)
plt.show()

plt.figure(figsize=(12, 8))
plt.hexbin(df_cz['length_years'], df_cz['gap_fraction'], gridsize=50, cmap='Blues', mincnt=1)
plt.colorbar(label='Anzahl der Messstellen')
plt.title("Dichte der Messstellen (Länge vs. Lückenanteil) in Tschechien")
plt.xlabel("Länge der Messreihe (Jahre)")
plt.ylabel("Anteil fehlender Werte (gap_fraction)")
plt.tight_layout()
plt.savefig("CZ_hexbin_length_vs_gap.png", dpi=300)
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(y=df_cz['length_years'].dropna(), color='lightgreen')
plt.title("Verteilung der Messreihenlänge in Tschechien")
plt.ylabel("Länge der Messreihe (Jahre)")
plt.xticks([])
plt.tight_layout()
plt.savefig("CZ_boxplot_length_years.png", dpi=300)
plt.show()

if 'main_landuse' in df_cz.columns and not df_cz['main_landuse'].dropna().empty:
    plt.figure(figsize=(10, 5))
    df_cz['main_landuse'].value_counts().head(10).plot(kind='bar', color='peru')
    plt.title("Häufigste Landnutzungsarten in Tschechien")
    plt.xlabel("Landnutzung")
    plt.ylabel("Anzahl")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("CZ_barplot_landnutzung.png", dpi=300)
    plt.show()
else:
    print("Spalte 'main_landuse' ist nicht vorhanden oder leer für Tschechien. Der Plot wird übersprungen.")

if 'surface_elevation_m_asl' in df_cz.columns and not df_cz['surface_elevation_m_asl'].dropna().empty:
    plt.figure(figsize=(10, 6))
    df_cz['surface_elevation_m_asl'].dropna().hist(bins=50, color='olive', edgecolor='black')
    plt.title("Verteilung der Höhenlage der Messstellen in Tschechien")
    plt.xlabel("Höhe (m ü. NN)")
    plt.ylabel("Anzahl")
    plt.tight_layout()
    plt.savefig("CZ_histogramm_hoehenlage.png", dpi=300)
    plt.show()
else:
    print("Spalte 'surface_elevation_m_asl' ist nicht vorhanden oder leer für Tschechien. Der Plot wird übersprungen.")

numeric_df_cz = df_cz.select_dtypes(include=['float64', 'int64'])
if not numeric_df_cz.empty and len(numeric_df_cz.columns) > 1:
    corr_cz = numeric_df_cz.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_cz, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
    plt.title("Korrelationsmatrix numerischer Variablen in Tschechien")
    plt.tight_layout()
    plt.savefig("CZ_korrelationsmatrix.png", dpi=300)
    plt.show()
elif len(numeric_df_cz.columns) <= 1:
    print("Nicht genügend numerische Spalten für eine Korrelationsmatrix in Tschechien vorhanden (mindestens 2 benötigt).")
else:
    print("Keine numerischen Spalten für eine Korrelationsmatrix in Tschechien gefunden.")

print("Alle ausgewählten Plots für Tschechien wurden generiert und im aktuellen Verzeichnis gespeichert.")
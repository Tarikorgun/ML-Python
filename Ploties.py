import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # Für np.nan und mögliche numerische Operationen
import matplotlib.ticker as mtick # Für mögliche Achsenformatierung

# CSV laden
df = pd.read_csv("grow_attributes.csv", sep=";", low_memory=False)

# --- Filterung auf Daten von Tschechien (CZE) ---
df_cz = df[df["country"] == "CZE"].copy()

# Optional: Überprüfen, ob Daten für CZE gefunden wurden
if df_cz.empty:
    print("Keine Daten für das Land 'CZE' gefunden. Bitte überprüfen Sie die 'country'-Spalte und den Ländercode.")
    exit()

print(f"Anzahl der Messstellen in Tschechien (CZE): {len(df_cz)}")

# Überblick: Fehlende Werte (jetzt nur für CZE-Daten)
print("\nFehlende Werte für Tschechien (CZE) Daten:")
print(df_cz.isnull().sum())


# 1. Histogramme numerischer Merkmale (für CZE)

numeric_cols_cz = df_cz.select_dtypes(include='number').columns
if not numeric_cols_cz.empty:
    numeric_cols_with_data = [col for col in numeric_cols_cz if df_cz[col].dropna().nunique() > 1]
    
    if numeric_cols_with_data:
        #  figsize vergrößern für bessere Lesbarkeit der Achsen
        df_cz[numeric_cols_with_data].hist(bins=30, figsize=(18, 12)) 
        plt.suptitle("Histogramme numerischer Merkmale (Tschechien)", fontsize=16) # Titel-Schriftgröße anpassen
        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # rect anpassen, um Platz für suptitle zu lassen
        plt.show()
    else:
        print("Nicht genügend diverse numerische Spalten für Histogramme in den CZE-Daten gefunden.")
else:
    print("Keine numerischen Spalten für Histogramme in den CZE-Daten gefunden.")



# 2. Boxplots zur Ausreißer-Erkennung (für CZE)

if not numeric_cols_cz.empty:
    for col in numeric_cols_cz:
        if df_cz[col].dropna().nunique() > 1:
            # figsize anpassen (hier nicht so kritisch für x, aber für y könnte es sein)
            plt.figure(figsize=(10, 3)) # Leicht breiter und höher für Boxplots
            sns.boxplot(x=df_cz[col].dropna())
            plt.title(f'Boxplot von {col} (Tschechien)')
            plt.tight_layout()
            plt.show()
        else:
            print(f"Überspringe Boxplot für '{col}' (Tschechien): Nicht genügend diverse oder keine nicht-fehlenden Werte.")
else:
    print("Keine numerischen Spalten für Boxplots in den CZE-Daten gefunden.")



# 3. Balkendiagramme für kategoriale Features (für CZE)

categorical_cols_cz = df_cz.select_dtypes(include='object').columns
if not categorical_cols_cz.empty:
    for col in categorical_cols_cz:
        all_categories = df[col].dropna().unique()
        cz_value_counts = df_cz[col].value_counts()
        cz_value_counts_full = cz_value_counts.reindex(all_categories, fill_value=0).sort_index()

        if cz_value_counts_full.empty:
            print(f"Spalte '{col}' in CZE-Daten ist leer nach Entfernung fehlender Werte. Überspringe Balkendiagramm.")
            continue

        # Prüfen, ob die Anzahl der Kategorien sinnvoll ist (Schwellenwert kann angepasst werden)
        if len(cz_value_counts_full) < 35: # Etwas höherer Schwellenwert, da wir die Lesbarkeit verbessern
            #  figsize dynamisch an Anzahl der Kategorien anpassen, wenn viele Kategorien
            fig_width = max(10, len(cz_value_counts_full) * 0.6) # Min. 10, dann 0.6 Einheiten pro Kategorie
            plt.figure(figsize=(fig_width, 6)) # Breite basierend auf Anzahl der Kategorien, feste Höhe

            cz_value_counts_full.plot(kind='bar')
            plt.title(f'Häufigkeiten der Kategorie: {col} (Tschechien - inkl. 0-Werte)')
            plt.xlabel(col)
            plt.ylabel('Anzahl')
            # **ANPASSUNG:** Rotation und Ausrichtung
            plt.xticks(rotation=60, ha='right', fontsize=9) # Stärkere Rotation, kleinere Schrift
            plt.tight_layout()
            plt.show()
        else:
            print(f"Spalte '{col}' in CZE-Daten hat nach Reindexing zu viele einzigartige Werte ({len(cz_value_counts_full)}) für ein Balkendiagramm. Bitte Top N Kategorien betrachten oder horizontalen Balkenplot erwägen.")
else:
    print("Keine kategorialen Spalten für Balkendiagramme in den CZE-Daten gefunden.")



# 4. Korrelationsmatrix (nur numerisch, für CZE)

if len(numeric_cols_cz) > 1:
    corr_matrix_cz = df_cz[numeric_cols_cz].corr()
    
    if not corr_matrix_cz.empty:
        #  figsize vergrößert für bessere Lesbarkeit der Zahlen und Labels
        plt.figure(figsize=(14, 12)) 
        sns.heatmap(corr_matrix_cz, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8}) # Schriftgröße der Anmerkungen
        plt.title("Korrelationsmatrix numerischer Features (Tschechien)", fontsize=16)
        plt.xticks(rotation=45, ha='right', fontsize=10) # Achsenbeschriftung der Korrelation
        plt.yticks(rotation=0, ha='right', fontsize=10)
        plt.tight_layout()
        plt.show()
    else:
        print("Korrelationsmatrix für CZE konnte nicht erstellt werden (möglicherweise zu viele fehlende Werte).")
elif len(numeric_cols_cz) <= 1:
    print("Nicht genügend numerische Spalten in den CZE-Daten vorhanden (mindestens 2 benötigt) für eine Korrelationsmatrix.")
else:
    print("Keine numerischen Spalten für eine Korrelationsmatrix in den CZE-Daten gefunden.")
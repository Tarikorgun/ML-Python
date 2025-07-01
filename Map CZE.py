import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load the data
df = pd.read_csv("grow_attributes.csv", delimiter=';', low_memory=False)

# Ensure 'latitude' and 'longitude' columns exist
if {'latitude', 'longitude'}.issubset(df.columns):
    plt.figure(figsize=(10, 8)) # Adjust figure size for a more focused view

    # Filter data for only the Czech Republic
    df_cz = df[df["country"] == "CZE"]

    # Plot Czech Republic stations
    plt.scatter(df_cz['longitude'], df_cz['latitude'],
                s=20,          # Marker size
                alpha=0.7,     # Transparency
                color='red',   # Color for Czech Republic stations
                label='Czech Republic (CZE) Stations')

    plt.title("Distribution of Groundwater Monitoring Stations in the Czech Republic")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Set more appropriate limits for the Czech Republic
    # These values are approximate bounding box coordinates for the Czech Republic
    plt.xlim(12.0, 19.0)
    plt.ylim(48.5, 51.5)

    # Add a grid for better spatial orientation
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.legend(markerscale=2) # Show legend
    plt.tight_layout()
    plt.savefig("karte_messstellen_scatterplot_czech_republic.png", dpi=300)
    plt.show()
else:
    print("Columns 'latitude' and 'longitude' not found in the DataFrame. Skipping map plot.")
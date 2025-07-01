import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # Although not strictly needed for this simplified map, kept for consistency

# Load the data
df = pd.read_csv("grow_attributes.csv", delimiter=';', low_memory=False)

# Ensure 'latitude' and 'longitude' columns exist
if {'latitude', 'longitude'}.issubset(df.columns):
    plt.figure(figsize=(15, 8)) # Adjust figure size

    # Separate Czech Republic data from the rest
    df_cz = df[df["country"] == "CZE"]
    df_other = df[df["country"] != "CZE"]

    # Plot non-Czech Republic stations in one color
    plt.scatter(df_other['longitude'], df_other['latitude'],
                s=1,           # Marker size
                alpha=0.2,     # Transparency
                color='blue',  # Color for other countries
                label='Other Countries')

    # Plot Czech Republic stations in a different color on top
    plt.scatter(df_cz['longitude'], df_cz['latitude'],
                s=1,          # Slightly larger marker size for emphasis
                alpha=0.7,     # Less transparent for visibility
                color='red',   # Distinct color for Czech Republic
                label='Czech Republic (CZE)')

    plt.title("Distribution of Groundwater Monitoring Stations Worldwide")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Set approximate world map limits for better visualization
    # These values cover most of the Earth's surface
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)

    # Add a grid for better spatial orientation (optional)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.legend(markerscale=2) # Show legend to differentiate colors, adjust marker size in legend
    plt.tight_layout()
    plt.savefig("karte_messstellen_scatterplot_simple_world.png", dpi=300)
    plt.show()
else:
    print("Columns 'latitude' and 'longitude' not found in the DataFrame. Skipping map plot.")
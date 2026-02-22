import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


# =========================
# Crear carpeta si no existe
# =========================
def create_graphs_folder():
    os.makedirs("graphs", exist_ok=True)


# =========================
# Histograma y Heatmaps
# =========================
def plot_histogram(df):

    plt.figure(figsize=(10,5))
    sns.histplot(df["rating_per_euro"], bins=50, kde=False, color="skyblue")
    plt.title("Distribución de Rating por Euro")
    plt.xlabel("Rating / €")
    plt.ylabel("Cantidad de vinos")
    plt.savefig("graphs/histogram.png")
    plt.close()

def plot_style_region_heatmaps(df):

    top_regions = df['region'].value_counts().head(20).index
    df_filtered = df[df['region'].isin(top_regions)]

    exclude_styles = [
        "Ribera del Duero Tinto", "Montsant Tinto", "Rioja Blanco",
        "Rioja Tinto", "Spanish Rosé", "Spanish White", "Tinto"
    ]

    df_filtered = df_filtered[~df_filtered['style'].isin(exclude_styles)]

    count_matrix = df_filtered.pivot_table(
        index='style',
        columns='region',
        values='wine_id',
        aggfunc='count',
        fill_value=0
    )

    weighted_matrix = df_filtered.pivot_table(
        index='style',
        columns='region',
        values='rating',
        aggfunc=lambda x: np.average(
            x,
            weights=df_filtered.loc[x.index, 'num_reviews']
        ),
        fill_value=np.nan
    )

    # Heatmap 1
    plt.figure(figsize=(16, 12))
    sns.heatmap(count_matrix, cmap='YlGnBu')
    plt.title("Cantidad de vinos por estilo y top 20 regiones")
    plt.tight_layout()
    plt.savefig("graphs/heatmap_count.png")
    plt.close()

    # Heatmap 2
    plt.figure(figsize=(16, 12))
    sns.heatmap(weighted_matrix, cmap='coolwarm')
    plt.title("Rating promedio ponderado por estilo y top 20 regiones")
    plt.tight_layout()
    plt.savefig("graphs/heatmap_weighted.png")
    plt.close()


# =========================
# Scatter: Year Analysis
# =========================
def plot_year_analysis(df):

    year_stats = (
        df.groupby("year")
        .agg(
            avg_rating=("rating", "mean"),
            total_reviews=("num_reviews", "sum"),
            n_wines=("wine_id", "count")
        )
        .reset_index()
    )

    year_stats = year_stats[year_stats["n_wines"] >= 5]

    # Scatter rating
    plt.figure(figsize=(10, 6))
    sns.regplot(data=year_stats, x="year", y="avg_rating")
    plt.title("Rating promedio por año")
    plt.tight_layout()
    plt.savefig("graphs/year_rating.png")
    plt.close()

    # Scatter reviews
    plt.figure(figsize=(10, 6))
    sns.regplot(data=year_stats, x="year", y="total_reviews")
    plt.title("Total reviews por año")
    plt.tight_layout()
    plt.savefig("graphs/year_reviews.png")
    plt.close()


# =========================
# Sankey
# =========================
def plot_sankey(df):

    wine_colors = {
        "Red": "#8B0000",
        "Rose": "#FF69B4",
        "Dessert": "#32CD32",
        "White": "#FFD700",
        "Fortified": "#19138B",
        "Sparkling": "#FFA500"
    }

    flow_df = (
        df.groupby(["wine_type", "wine_category"])
        .size()
        .reset_index(name="count")
    )

    wine_types = flow_df["wine_type"].unique().tolist()
    wine_categories = flow_df["wine_category"].unique().tolist()

    labels = wine_types + wine_categories
    label_index = {label: i for i, label in enumerate(labels)}

    source = []
    target = []
    value = []

    for _, row in flow_df.iterrows():
        source.append(label_index[row["wine_type"]])
        target.append(label_index[row["wine_category"]])
        value.append(row["count"])

    node_colors = [wine_colors.get(w, "#CCCCCC") for w in wine_types] + ["#AAAAAA"]*len(wine_categories)

    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels, color=node_colors),
        link=dict(source=source, target=target, value=value)
    )])

    fig.update_layout(title_text="Distribución tipo de vino por categoría")

    fig.write_html("graphs/sankey.html")  # guardamos interactivo
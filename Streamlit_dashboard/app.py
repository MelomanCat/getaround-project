import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import seaborn as sns

### Config
st.set_page_config(
    page_title="Getaround Rental Delay Analysis",
    page_icon="car",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

RENTAL_FILE_ID = "1aos7aPFI2nnE4A_S-DACZINCTm6eMzQd"
RENTAL_DATA_URL = f"https://drive.google.com/uc?export=download&id={RENTAL_FILE_ID}"


PRICING_FILE_ID = "1JVd1ZD6PK1nMrcoVTFwMl4swCd337fyK"
PRICING_DATA_URL = f"https://drive.google.com/uc?export=download&id={PRICING_FILE_ID}"


### App
st.title("Analyse de Getaround")

# Use `st.cache` when loading data is extremly useful
# because it will cache your data so that your app 
# won't have to reload it each time you refresh your app

### === Raw data ===

@st.cache_data
def load_df_pricing():
    df_pricing = pd.read_csv(PRICING_DATA_URL, sep=",")
    df_pricing.drop(df_pricing.columns[0], axis=1, inplace = True)
    return df_pricing

@st.cache_data
def load_df():
    df = pd.read_excel(RENTAL_DATA_URL)
    return df

st.header("Charger et afficher les données")


data_load_state = st.text('Chargement des données...')
df = load_df()
df_pricing = load_df_pricing()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked 
if st.checkbox('Afficher les données brutes'):
    st.subheader('Données brutes des locations')
    st.write(df) 
    st.write("*"*100)
    st.subheader('Données brutes des tarifs')
    st.write(df_pricing)

st.divider()

### Connected cars vs non-connected 
st.header("Voitures Connect vs non-Connect")

## Create two columns
col1, spacer, col2 = st.columns([1, 0.2, 1])

with col1:
    st.subheader("1️⃣ Proportion de voitures Connect vs non-Connect")
    st.markdown("""
    ##### Les voitures Connect, légèrement moins nombreuses (2230 vs 2613), 
    ##### génèrent pourtant des revenus comparables aux non-Connect.                 
        
    """)
    st.markdown(" ")
    # Get revenue sum per group of cars
    revenue_by_connect = df_pricing.groupby("has_getaround_connect")['rental_price_per_day'].sum().reset_index()
    
    # Create a dictionary for displaying labels
    connect_labels = {
        True: "Connect",
        False: "Non-Connect",
        
    }
    revenue_by_connect['connection_type'] = revenue_by_connect['has_getaround_connect'].map(connect_labels)
    
    
    fig = px.pie(
    revenue_by_connect,
    names="connection_type",
    values="rental_price_per_day",
    title="Répartition des revenus : Connect vs non-Connect",
    hole=0.3,  # make dohnut
    labels={False: "Non-Connect", True: "Connect"},
)

    # Add sums as hoverinfo
    fig.update_traces(textinfo="percent+label", hoverinfo="label+value")

    # Show graph with Streamlit
    st.plotly_chart(fig)

with col2:
    st.subheader("2️⃣ Répartition des prix de location")
    st.markdown("""
                ##### Explication : les tarifs moyens des locations dans la catégorie Connect sont légèrement supérieurs :
                ##### 132 EUR/jour contre 111 EUR/jour pour les voitures non-Connect.
                
                """)

    # Create boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='has_getaround_connect', y='rental_price_per_day', data=df_pricing, ax=ax)
    ax.set_title('Répartition des prix de location selon le type de connexion')
    ax.set_xlabel('Avec Getaround Connect')
    ax.set_ylabel('Prix de location par jour')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Non-Connect', 'Connect'])

    # Show plot in Streamlit
    st.pyplot(fig)

st.markdown(" ")
st.divider()

### === conflict cases analysis ===

st.header("Analyse des retards de restitution et des cas de conflits")

# Filtering data
df_valid = df[
    df["delay_at_checkout_in_minutes"].notna() & 
    df["time_delta_with_previous_rental_in_minutes"].notna()
].copy()

# Share of rentals with delay
delayed_rentals = df_valid[df_valid["delay_at_checkout_in_minutes"] > 0]
total_delayed = delayed_rentals.shape[0]
total_rentals = df_valid.shape[0]
delay_share = total_delayed / total_rentals

# Conflict cases (delay greater than buffer)
conflicts = delayed_rentals[
    delayed_rentals["delay_at_checkout_in_minutes"] > 
    delayed_rentals["time_delta_with_previous_rental_in_minutes"]
]
total_conflicts = conflicts.shape[0]
conflict_share = total_conflicts / total_delayed

# Metrics
st.subheader("📌 Indicateurs clés")
st.markdown(" ")

col1, col2, col3 = st.columns(3)
col1.metric("Locations avec retard", f"{total_delayed}", f"{delay_share:.1%} of total")
col2.metric("Conflits avec la location suivante", f"{total_conflicts}", f"{conflict_share:.1%} of delayed")
col3.metric("Total des locations valides", f"{total_rentals}")

st.markdown(" ")

st.markdown("""
##### Parmi les 1515 locations valides, 802 (environ 53 %) ont enregistré un retard lors du retour du véhicule.

##### Parmi ces locations retardées, 270 cas (environ 34 %) ont provoqué un conflit avec une location ultérieure, ce qui a pu nuire au conducteur suivant.

##### 🔍 Cela signifie qu'un retard sur trois crée un risque d'échec de la location suivante, ce qui peut dégrader l'expérience client et potentiellement réduire la confiance envers la plateforme.
            """)
st.markdown("<div style='margin-top: 120px', 'margin-bottom: 120px'> </div>", unsafe_allow_html=True )


# Create two columns
col1, spacer, col2 = st.columns([1, 0.2, 1])

with col1:
    # Pie chart: rentals with delay ratio
    st.subheader("📊 Part des locations avec retard")

    delay_labels = ["Avec retard", "Sans retard"]
    delay_counts = [total_delayed, total_rentals - total_delayed]

    fig1, ax1 = plt.subplots()
    ax1.pie(delay_counts, labels=delay_labels, autopct='%1.1f%%', startangle=90, colors=["#8661C1", "#97D8B2"])
    ax1.axis('equal')
    st.pyplot(fig1)

with col2:
    # Pie chart: delays with conflicts
    st.subheader("⚠️ Part des retards entraînant un conflit")

    conflict_labels = ["Conflict", "Pas de conflict"]
    conflict_counts = [total_conflicts, total_delayed - total_conflicts]

    fig2, ax2 = plt.subplots()
    ax2.pie(conflict_counts, labels=conflict_labels, autopct='%1.1f%%', startangle=90, colors=["#8661C1", "#97D8B2"])
    ax2.axis('equal')
    st.pyplot(fig2)

st.markdown("<div style='margin-top: 120px', 'margin-bottom: 120px'> </div>", unsafe_allow_html=True )

st.divider()

# === Delay statistics with outlier filtering  ===

# IQR filtering function
def filter_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Section title
st.header("⏱️ Statistique des retards")

# Checkbox for filtering
apply_filter = st.checkbox("Exclure les valeurs aberrantes extrêmes des statistiques de retard (basé sur l'IQR)")

# Filter data
if apply_filter:
    delayed_data = filter_outliers_iqr(delayed_rentals, "delay_at_checkout_in_minutes")
    st.markdown("✅ *Valeurs abérantes exclues à l'aide de la méthode IQR*")
else:
    delayed_data = delayed_rentals
    st.markdown("⚠️ *Données brutes avec valeurs aberrantes*")

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
# Horizontal layout for metrics
col1, col2, col3 = st.columns(3)
col1.metric("Délai moyen", f"{delayed_data['delay_at_checkout_in_minutes'].mean():.1f} min")
col2.metric("Délai médian", f"{delayed_data['delay_at_checkout_in_minutes'].median():.1f} min")
col3.metric("Délai maximal", f"{delayed_data['delay_at_checkout_in_minutes'].max():.1f} min")

# Text with insights below
st.markdown("""
<div class="insights">
    <h3 class="insights-title">📌 Insights</h3>
    <ul class="insights-list">
        <li class="insight-item">Plus de la moitié des locations (<strong>52.9%</strong>) sont retournées avec un retard.</li>
        <li class="insight-item">Seulement environ <strong>33.7%</strong> des retards entraînent des conflits avec les locations suivantes, ce qui signifie que la plupart des retards n'impactent pas le client suivant.</li>
        <li class="insight-item">Le <strong>délai moyen</strong> est d'environ <strong>160 minutes</strong>, tandis que la <strong>médiane</strong> est autour de <strong>50 minutes</strong>, ce qui montre que quelques retards importants (jusqu'à <strong>{:.0f} minutes</strong>) faussent la moyenne.</li>
    </ul>
</div>
""".format(delayed_data['delay_at_checkout_in_minutes'].max()), unsafe_allow_html=True)

# === Expandable histogram section ===

with st.expander("📈 Afficher l'histogramme de la distribution des retards"): 
    

    # Radio button inside expander for the histogram
    hist_filter_option = st.radio(
        "Choisissez les données à afficher :",
        ("Inclure les valeurs aberrantes", "Exclure les valeurs aberrantes (filtrage IQR)"),
        horizontal=True
    )

    # Apply selected filter
    if hist_filter_option == "Exclure les valeurs aberrantes (filtrage IQR)":
        data_for_hist = filter_outliers_iqr(delayed_rentals, "delay_at_checkout_in_minutes")
        st.markdown("✅ *Histogramme sans valeurs aberrantes*")
    else:
        data_for_hist = delayed_rentals
        st.markdown("⚠️ *Histogramme avec retards extrêmes*")

    # Draw histogram
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(
        data_for_hist["delay_at_checkout_in_minutes"],
        bins=60,
        kde=True,
        color="mediumpurple",
        edgecolor="black",
        ax=ax
    )
    ax.set_title("Distribution des retards (en minutes)")
    ax.set_xlabel("Délai de restitution (minutes)")
    ax.set_ylabel("Nombre de locations")
    st.pyplot(fig)
st.markdown("<div style='margin-top: 120px', 'margin-bottom: 120px'> </div>", unsafe_allow_html=True )

st.divider()

### === Efficiency vs revenue losses ===

# List of threshold
thresholds = [30, 60, 90, 120, 180]

# Calculate mean rental prices
pricing_stats = df_pricing.groupby("has_getaround_connect")["rental_price_per_day"].mean()
price_connect = pricing_stats[True]
price_non_connect = pricing_stats[False]

# Filtering data
df_valid = df[
    df["previous_ended_rental_id"].notna() & 
    df["time_delta_with_previous_rental_in_minutes"].notna() &
    df["delay_at_checkout_in_minutes"].notna()
].copy()
st.markdown(" ")

# Section subheader
st.header("Efficacité vs pertes de revenus selon le seuil")

# Threshold selection (in min) 
threshold = st.selectbox("Sélectionnez le seuil (en minutes)", thresholds, index=0)


# Create 2 columns
col1, col2 = st.columns(2)

# Define function for calculation statistics for both scopes
def calculate_scope_data(scope, threshold):
    if scope == "Toutes les voitures":
        scope_df = df_valid.copy()
        valeur_moyenne = 120.7
    else:
        scope_df = df_valid[df_valid["checkin_type"] == "connect"]
        valeur_moyenne = 132

    total_rentals = scope_df.shape[0]
    total_connect = scope_df[scope_df["checkin_type"] == "connect"].shape[0]
    total_non_connect = scope_df[scope_df["checkin_type"] != "connect"].shape[0]
    total_revenue = (total_connect * price_connect) + (total_non_connect * price_non_connect)

    # Affected rentals
    affected = scope_df[scope_df["time_delta_with_previous_rental_in_minutes"] < threshold]
    affected_connect = affected[affected["checkin_type"] == "connect"].shape[0]
    affected_non_connect = affected[affected["checkin_type"] != "connect"].shape[0]
    affected_total = affected.shape[0]
    affected_revenue = (affected_connect * price_connect) + (affected_non_connect * price_non_connect)
    revenue_share = affected_revenue / total_revenue if total_revenue > 0 else 0

    # Saved rentals
    conflict_cases = scope_df[
        scope_df["delay_at_checkout_in_minutes"] > scope_df["time_delta_with_previous_rental_in_minutes"]
    ]
    saved = conflict_cases[conflict_cases["time_delta_with_previous_rental_in_minutes"] < threshold]
    saved_count = saved.shape[0]
    saved_pct = saved_count / affected_total * 100 if affected_total > 0 else 0

    # Efficiency
    estimated_benefit = saved_count * valeur_moyenne
    cost_benefit_score = (estimated_benefit / affected_revenue)*100 if affected_revenue > 0 else 0

    return {
        "Locations impactées": affected_total,
        "Locations sauvées": saved_count,
        "Locations sauvées (%)": round(saved_pct, 1),
        "Perte de revenu (%)": round(revenue_share * 100, 1),
        "Perte de revenu (€)": round(affected_revenue, 2),
        "Efficacité": round(cost_benefit_score, 1)
        
    }

# Calculate results for both scopes
results_all_cars = calculate_scope_data("Toutes les voitures", threshold)
results_connect_only = calculate_scope_data("Connect uniquement", threshold)

# Display two dataframes
df_all_cars = pd.DataFrame([results_all_cars])
df_connect_only = pd.DataFrame([results_connect_only])

# Visualization in two columns
with col1:
    st.subheader(f"Résultats pour toutes les voitures (seuil = {threshold} min)")
    st.write(df_all_cars)

    # Plot for all cars
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    ax1.bar(["Perte de revenu (%)", "Locations sauvées (%)", "Efficacité"], 
            [results_all_cars["Perte de revenu (%)"], results_all_cars["Locations sauvées (%)"], results_all_cars["Efficacité"]])
    for i, v in enumerate([results_all_cars["Perte de revenu (%)"], results_all_cars["Locations sauvées (%)"], results_all_cars["Efficacité"]]):
        ax1.text(i, v + 1, f'{v}', ha='center', va='bottom', fontsize=10)  # add notation
    ax1.set_title("Analyse d'impact pour toutes les voitures")

    # Define common scale for Y axis (max for all the data)
    y_max = max([results_all_cars["Perte de revenu (%)"], results_all_cars["Locations sauvées (%)"], results_all_cars["Efficacité"], 
                 results_connect_only["Perte de revenu (%)"], results_connect_only["Locations sauvées (%)"], results_connect_only["Efficacité"]]) + 10
    ax1.set_ylim(0, y_max)
    st.pyplot(fig1)

with col2:
    st.subheader(f"Résultats pour Connect uniquement (seuil = {threshold} min)")
    st.write(df_connect_only)

    # Plot for connect only
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))
    ax2.bar(["Perte de revenu (%)", "Locations sauvées (%)", "Efficacité"], 
            [results_connect_only["Perte de revenu (%)"], results_connect_only["Locations sauvées (%)"], results_connect_only["Efficacité"]])
    for i, v in enumerate([results_connect_only["Perte de revenu (%)"], results_connect_only["Locations sauvées (%)"], results_connect_only["Efficacité"]]):
        ax2.text(i, v + 1, f'{v}', ha='center', va='bottom', fontsize=10)  # add notation
    ax2.set_title("Analyse d'impact pour Connect uniquement")

    # Define common scale for Y axis 
    ax2.set_ylim(0, y_max)
    st.pyplot(fig2)

### === Conclusions ===

st.markdown("""
<div class="conclusions">
    <h3 class="conclusions-title">📌 Conclusions</h3>
    <ul class="conclusions-list">
        <li class="conclusions-item">Seuils courts (<strong>30-60 minutes</strong>) sont les plus efficaces</li>
        <br>
        <li class="conclusions-item">Lorsque le seuil augmente, l'efficacité diminue et les pertes augmentent</li>
        <br>
        <li class="conclusions-item"><strong>Limiter aux voitures Connect</strong> permet de réduire les pertes des revenus, car ces voitures génèrent plus de valeur. </li>       
    </ul>
</div>
""" , unsafe_allow_html=True)
st.divider()

### ===Recommendations ===

st.header("✅ Recommendations")

st.markdown ("#### 🛡️ Option prudente :")
st.markdown("""
<div class="recommendations">
    <ul class="recommendations-list">
            <li class="recommendations-item">Seuil : <strong>30 minutes</strong></li>
            <li class="recommendations-item">Scope : <strong>Connect uniquement</strong></li>
            <li class="recommendations-item">Efficacité : <strong>49.2%</strong> et pertes faibles (<strong>~14000 €</strong>)</li>                                  
    </ul>
</div>
""" , unsafe_allow_html=True)

st.markdown ("#### 🎯 Option équilibrée :")
st.markdown("""
<div class="recommendations">            
    <ul class="recommendations-list">
            <li class="recommendations-item">Seuil : <strong>30 minutes</strong></li>
            <li class="recommendations-item">Scope : <strong>Toutes les voitures</strong></li>
            <li class="recommendations-item">Efficacité : <strong>59.6%</strong>, pertes plus élevées (<strong>~27500 €</strong>)</li>                                    
    </ul>
</div>
""" , unsafe_allow_html=True)


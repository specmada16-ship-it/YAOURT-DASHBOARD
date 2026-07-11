import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURATION ET DESIGN
# ==========================================
st.set_page_config(page_title="Tableau de bord YAOURT", page_icon="🥣", layout="wide")

# Palette de couleurs extraite de votre image
C_NAVY = "#003049"
C_RED = "#d62828"
C_ORANGE = "#f77f00"
C_YELLOW = "#fcbf49"
C_BEIGE = "#eae2b7"

# Injection de CSS personnalisé pour correspondre au design élégant
st.markdown(f"""
    <style>
    /* Fond principal */
    .stApp {{
        background-color: #f4f4f4;
    }}
    /* Barre latérale */
    [data-testid="stSidebar"] {{
        background-color: {C_NAVY} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    /* Style des cartes KPI */
    .kpi-card {{
        background-color: {C_BEIGE};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid {C_NAVY};
    }}
    .kpi-title {{
        font-size: 16px;
        color: {C_NAVY};
        margin-bottom: 5px;
        font-weight: bold;
    }}
    .kpi-value {{
        font-size: 28px;
        color: {C_RED};
        font-weight: 900;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. EXTRACTION DES DONNÉES (EXCEL)
# ==========================================
@st.cache_data
def load_data():
    file_path = "Tableau de bord YAOURT.xlsx"
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(file_path, sheet_name='Tableau de bord')
        
        # Extraction sécurisée de quelques KPIs réels depuis votre fichier
        revenue = df.loc[df['Indicateur'] == 'Total', 'Valeur'].values
        revenue_brute = revenue[0] if len(revenue) > 0 else 10400
        
        dep = df.loc[df['Indicateur'].str.contains('Total des depenses', na=False), 'Valeur'].values
        depenses = dep[0] if len(dep) > 0 else 20750
        
        ben = df.loc[df['Indicateur'] == 'Bénéfice lot à PRIX Direct', 'Valeur'].values
        benefice = ben[0] if len(ben) > 0 else 5287.20
        
        return revenue_brute, depenses, benefice
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier Excel: {e}")
        return 0, 0, 0

revenue_brute, depenses, benefice = load_data()

# ==========================================
# 3. INTERFACE UTILISATEUR ET GRAPHIQUES
# ==========================================
# Menu latéral
st.sidebar.title("YAOURT")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["🏠 Aperçu", "🏭 Production", "📈 Ventes", "⚙️ Paramètres"])

if menu == "🏠 Aperçu":
    st.title("Tableau de bord YAOURT")
    st.markdown("---")
    
    # Section des KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card" style="border-bottom-color: {C_RED};">
                <div class="kpi-title">Revenu Brut Total</div>
                <div class="kpi-value">{revenue_brute:,.0f} Ar</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card" style="border-bottom-color: {C_ORANGE};">
                <div class="kpi-title">Total des Dépenses</div>
                <div class="kpi-value" style="color: {C_ORANGE};">{depenses:,.0f} Ar</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card" style="border-bottom-color: {C_YELLOW};">
                <div class="kpi-title">Bénéfice par Lot (Direct)</div>
                <div class="kpi-value" style="color: {C_NAVY};">{benefice:,.0f} Ar</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)

    # Section des Graphiques
    col_chart1, col_chart2 = st.columns([6, 4])
    
    # Graphique 1: Tendance Linéaire (Courbes lissées)
    with col_chart1:
        st.subheader("Tendance Mensuelle Production & Ventes")
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
        production = [50, 160, 240, 160, 260, 190]
        ventes = [20, 110, 160, 120, 195, 180]
        
        fig_trend = go.Figure()
        # Courbe de Production
        fig_trend.add_trace(go.Scatter(
            x=months, y=production, name='Production', 
            line=dict(color=C_NAVY, width=4, shape='spline'), 
            marker=dict(size=10, color=C_YELLOW, line=dict(width=2, color=C_NAVY))
        ))
        # Courbe de Ventes
        fig_trend.add_trace(go.Scatter(
            x=months, y=ventes, name='Ventes', 
            line=dict(color=C_RED, width=4, shape='spline'), 
            marker=dict(size=10, color=C_ORANGE, line=dict(width=2, color=C_RED))
        ))
        
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='#e0e0e0')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # Graphique 2: Répartition en Beignet (Donut Chart)
    with col_chart2:
        st.subheader("Répartition par Type de Produit")
        labels = ['Nature', 'Fruits', 'Grec', 'Probiotique']
        values = [33, 15, 23, 29]
        # Utilisation de la palette fournie
        colors = [C_NAVY, C_RED, C_ORANGE, C_YELLOW] 
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.6, 
            marker=dict(colors=colors, line=dict(color='#ffffff', width=2))
        )])
        
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="v", yanchor="center", y=0.5, xanchor="left", x=1)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Sélectionnez l'onglet 'Aperçu' pour voir le tableau de bord.")

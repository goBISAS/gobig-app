import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="GoBIG Intelligence", page_icon="🚀", layout="wide")

# Estilos CSS para el modo oscuro profesional
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #4caf50; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🚀 GoBIG Consulting | 2025")
st.markdown("Visión estratégica financiera y operativa")
st.markdown("---")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Enlace oficial de tu hoja [DATA_APP]
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQt8Ty41wMm8mpw5dZi59aEeRs19iJgb0E56CPzBNWWLt6p_fI3Nzh7Pqa8JI7X0f7_NOYmv7IEJ1xu/pub?gid=1196271650&single=true&output=csv"
    
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- CALCULADORAS ---
    total_rev = df['Revenue'].sum()
    total_cost = df['Cost_Total'].sum()
    total_margin = df['Margin_Net'].sum()
    
    if total_rev > 0:
        margin_pct_global = total_margin / total_rev
    else:
        margin_pct_global = 0
        
    # Encontrar Cliente MVP (Mayor margen neto)
    try:
        best_client_row = df.loc[df['Margin_Net'].idxmax()]
        mvp_name = best_client_row['Client']
    except:
        mvp_name = "N/A"

    # --- TARJETAS SUPERIORES (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facturación Total", f"${total_rev/1000000:.1f}M", "2025")
    with col2:
        st.metric("Utilidad Neta", f"${total_margin/1000000:.1f}M", "Cash")
    with col3:
        st.metric("Eficiencia Global", f"{margin_pct_global:.1%}", "Margen %")
    with col4:
        st.metric("Cliente MVP", mvp_name, "Top Ingresos")

    st.markdown("---")

    # --- GRÁFICOS ---
    
    col_chart_1, col_chart_2 = st.columns(2)

    with col_chart_1:
        # 1. TREEMAP (Mapa de Calor)
        st.subheader("Mapa de Rentabilidad (Treemap)")
        fig_treemap = px.treemap(
            df, 
            path=['Client'], 
            values='Revenue',
            color='Margin_Pct',
            color_continuous_scale=['#FF4B4B', '#1c1c1c', '#2bd972'], # Rojo -> Negro -> Verde
            range_color=[-0.5, 1],
            custom_data=['Margin_Net']
        )
        fig_treemap.update_traces(
            textinfo="label+value+percent entry",
            hovertemplate='<b>%{label}</b><br>Facturación: $%{value}<br>Margen: %{color:.1%}'
        )
        fig_treemap.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_treemap, use_container_width=True)

    with col_chart_2:
        # 2. COMPARATIVA BARRAS
        st.subheader("Ingresos vs Utilidad Real")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df['Client'], y=df['Revenue'], name='Ingresos', marker_color='#4a4e69'))
        fig_bar.add_trace(go.Bar(x=df['Client'], y=df['Margin_Net'], name='Utilidad', marker_color='#2bd972'))
        fig_bar.update_layout(barmode='overlay', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 3. TABLA DE DATOS
    with st.expander("Ver Datos Detallados"):
        st.dataframe(df[['Client', 'Revenue', 'Cost_Total', 'Margin_Net', 'Margin_Pct']].sort_values(by='Revenue', ascending=False))

else:
    st.info("Conectando con Google Sheets... Si esto tarda, verifica que la hoja [DATA_APP] tenga datos.")

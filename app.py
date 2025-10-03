import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

@st.cache_data
def load_data():
    return pd.read_csv("salud_pacientes.csv")

df = load_data()

# Sidebar
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Contexto", "Análisis descriptivo", "Georreferenciación"])

# ---------------- Página 1 ----------------
if page == "Contexto":
    st.title("Contexto de los datos de salud")
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=120)

    st.write("""
    Este dataset contiene información de pacientes en Colombia, incluyendo variables como 
    **Departamento, Sexo, Edad, Latitud y Longitud**. 
    El objetivo es analizar la distribución de pacientes y visualizar los datos en mapas interactivos.
    """)
    
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    st.subheader("Descripción estadística")
    st.write(df.describe())

# ---------------- Página 2 ----------------
elif page == "Análisis descriptivo":
    st.title("Análisis descriptivo de los pacientes")

    st.subheader("Pacientes por departamento")
    dept_counts = df["Departamento"].value_counts()
    fig, ax = plt.subplots()
    dept_counts.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Distribución por Genero")
    sex_counts = df["Genero"].value_counts()
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    st.subheader("Tabla dinámica de pacientes")
    dept_filter = st.selectbox("Selecciona un departamento:", df["Departamento"].unique())
    st.dataframe(df[df["Departamento"] == dept_filter])

# ---------------- Página 3 ----------------
elif page == "Georreferenciación":
    st.title("Mapa de pacientes por departamento")

    dept_filter = st.selectbox("Selecciona un departamento:", ["Todos"] + list(df["Departamento"].unique()))

    if dept_filter != "Todos":
        df_filtered = df[df["Departamento"] == dept_filter]
    else:
        df_filtered = df

    # Crear mapa centrado en Colombia
    m = folium.Map(location=[4.6, -74.1], zoom_start=6, tiles="CartoDB positron")

    # Clúster de puntos para no saturar el mapa
    from folium.plugins import MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_filtered.iterrows():
        popup_text = f"""
        <b>Departamento:</b> {row['Departamento']}<br>
        <b>Genero:</b> {row['Genero']}<br>
        <b>Edad:</b> {row['Edad']}
        """
        folium.CircleMarker(
            location=[row["Latitud"], row["Longitud"]],
            radius=6,
            color="navy",
            fill=True,
            fill_color="cyan",
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=250)
        ).add_to(marker_cluster)

    # Mostrar en Streamlit
    st_folium(m, width=800, height=600)


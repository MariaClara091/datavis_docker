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
    st.title("Contexto de los datos de salud - María Clara Ávila")
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

    # Comentario 2
    st.info("""En el gráfico de distribución geográfica por departamentos vemos que la distribución de pacientes abarca nueve departamentos: 
    **Cundinamarca, Bolívar y Valle del Cauca** los que encabezan la lista, seguidos por **Nariño, Bogotá D.C., Santander, Córdoba, Magdalena y Atlántico**, 
    siendo una cobertura amplia a nivel nacional, lo cual puede reflejar la ubicación de centros de atención.""")

    st.subheader("Distribución por Genero")
    sex_counts = df["Genero"].value_counts()
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    # Comentario 3
    st.info("""En la gráfica de distribución por género vemos que predomina el sexo **masculino con un 37.5%**, 
    el **sexo femenino con un 33.5%**, y la categoría **"Otro" con un 29.0%**, reflejando una inclusión de categorías no binarias 
    dentro de la población de pacientes encuestados para una salud inclusiva.""")

    st.subheader("Tabla dinámica de pacientes")
    dept_filter = st.selectbox("Selecciona un departamento:", df["Departamento"].unique())
    st.dataframe(df[df["Departamento"] == dept_filter])

    # Comentario 1
    st.info("""Analizando este descriptivo de la base de datos “Salud_Pacientes” con 200 registros de dichos encuestados, 
    se vio que las coordenadas geográficas de los datos están cercanas a una latitud promedio de **6.47** y una longitud promedio de **-75.17**,  
    siendo típica de la zona tropical de Colombia, pero la desviación estándar de **3.07** es mayor que en longitud de **1.21**, 
    lo que pudiera decir que esta variabilidad geográfica se encuentra en una dirección norte-sur del país y menos en dirección este-oeste.  

    En la variable edad los pacientes tienen un rango desde **0 hasta 99 años**. El promedio de todos es de **45.99 años**, es decir, de 45 a 46 años.  
    La mitad de la población tiene **44 años o menos**, mientras que el 25% más joven tiene **20 años o menos**, 
    y el 25% de mayor edad supera los **72.5 años**.  

    En cuanto a la frecuencia de visitas vemos un promedio de **5.52 visitas por paciente** y una mediana de **6**, 
    lo que indica que el 50% de los individuos realiza entre **3 y 8 visitas**, y casos extremos de hasta **11 visitas**.""")

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
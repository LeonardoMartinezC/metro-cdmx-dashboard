# 🚇 Dashboard Afluencia Metro CDMX

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyecto integral de Ciencia de Datos enfocado en el análisis de la **Afluencia Diaria Desglosada** del Sistema de Transporte Colectivo (Metro) de la Ciudad de México. El objetivo de esta aplicación interactiva es explorar el comportamiento de los pasajeros, agrupar estaciones con patrones similares, detectar anomalías operativas (o eventos atípicos) y proyectar tendencias a futuro.

## ✨ Características Principales

El proyecto cuenta con un diseño estético "Dark Mode" y se divide en las siguientes secciones funcionales:

1. 📊 **KPIs y Resumen Ejecutivo:** Tarjetas de impacto con información acumulada, estaciones top y un **mapa interactivo geolocalizado** (Plotly Mapbox) que muestra el volumen de pasajeros de todas las estaciones de la red.
2. 🔍 **Análisis Exploratorio (EDA):** Gráficas de tendencias históricas, mapas de calor mensual-semanal, treemaps y distribución por líneas y tipos de pago (Boleto vs Tarjeta).
3. 🤖 **Clustering K-Means (100% NumPy):** Segmentación automática de las estaciones según su perfil de uso diario y método de pago. El algoritmo de K-Means y la reducción de dimensionalidad (PCA) están implementados desde cero en NumPy, eliminando la dependencia de librerías externas de Machine Learning como Scikit-Learn.
4. 📈 **Pronóstico de Series de Tiempo:** Proyección a futuro de la afluencia agregada utilizando el modelo de Suavizamiento Exponencial Triple (Holt-Winters), visualizando intervalos de confianza y evaluando errores (MAE, RMSE, MAPE).
5. 🚨 **Detección de Anomalías:** Identificación de días atípicos mediante un análisis de Z-Score Móvil, cruzando visualmente descensos drásticos de afluencia con eventos históricos conocidos (Semana Santa, inicio de la pandemia, días festivos).

## 🛠️ Tecnologías y Librerías

- **Python** como lenguaje principal.
- **[Streamlit](https://streamlit.io/):** Creación del front-end interactivo y la interfaz gráfica.
- **[Pandas](https://pandas.pydata.org/):** Limpieza, transformación y manipulación masiva de datos estructurados.
- **[NumPy](https://numpy.org/):** Operaciones matriciales, implementación nativa de K-Means y PCA.
- **[Plotly](https://plotly.com/python/):** Visualizaciones interactivas de alto nivel (mapas geolocalizados, treemaps, gráficos de series temporales con intervalos de confianza).
- **[Statsmodels](https://www.statsmodels.org/):** Ajuste de modelos de series de tiempo (Holt-Winters) para pronósticos.

## ⚙️ Estructura del Proyecto

```bash
├── afluenciastc_desglosado_06_2026.csv  # Base de datos principal (no incluida en el repo si es muy grande)
├── app.py                               # Script principal de la aplicación Streamlit
├── mapping.json                         # Mapeo de nombres de estaciones y coordenadas geográficas (Lat/Lon)
└── README.md                            # Documentación del proyecto
```

## 🚀 Cómo ejecutar localmente

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/Afluencia_Metro_CDMX.git
   cd Afluencia_Metro_CDMX
   ```

2. **Crea un entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias necesarias:**
   ```bash
   pip install streamlit pandas numpy plotly statsmodels
   ```

4. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```
   La aplicación se abrirá automáticamente en tu navegador predeterminado, generalmente en la dirección `http://localhost:8501`.

## 📌 Datos Utilizados
Los datos originales proceden del **[Portal de Datos Abiertos de la CDMX](https://datos.cdmx.gob.mx/)**. 
Para garantizar la precisión de los nombres y resolver problemas de codificación de caracteres en los datos de origen, el proyecto utiliza un diccionario puente (`mapping.json`) construido a medida que también inyecta coordenadas geográficas (Latitud/Longitud) para los análisis espaciales.

## ✒️ Licencia
Este proyecto es de código abierto y está disponible bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

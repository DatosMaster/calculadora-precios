import streamlit as st  
import pandas as pd  
from PIL import Image  
  
logo_path = 'logo_petroplastic.jpg'

try:  
    logo = Image.open(logo_path)  
    logo = logo.resize((100, 100))
except FileNotFoundError:  
    st.error("⚠️ No se pudo cargar el logo. Verifica que la imagen esté en la carpeta correcta.")  

# Factores por país  
factores = {  
    "Guatemala": 0.0622,  
    "El Salvador": 0.0745,  
    "Honduras": 0.0548,  
    "Nicaragua": 0.0341,  
    "Costa Rica": 0.0646,  
    "Panamá": 0.0432,  
}  

# Tipo de cambio por país  
tipo_cambio = {  
    "Guatemala": 8.03,  
    "El Salvador": 1,  
    "Honduras": 26,  
    "Nicaragua": 37,  
    "Costa Rica": 525,  
    "Panamá": 1,  
}  

# Símbolos de moneda local  
moneda_local = {  
    "Guatemala": "Q",  
    "El Salvador": "USD",  
    "Honduras": "L.",  
    "Nicaragua": "C$",  
    "Costa Rica": "₡",  
    "Panamá": "USD",  
}  

# Comisión por país  
comision_pais = {  
    "Guatemala": 1.01,  
    "El Salvador": 1.011,  
    "Honduras": 1.0111,  
    "Nicaragua": 1.0123,  
    "Costa Rica": 1.01,  
    "Panamá": 1.0125,  
}  

# Diseño del encabezado  
col1, col2 = st.columns([1, 4])  
with col1:  
    st.image(logo)  # Mostrar el logo  
with col2:  
    st.markdown("<h1 style='text-align: left; color: black;'>Petroplastic</h1>", unsafe_allow_html=True)  

st.title("📊 Calculadora de Precios de Venta")  

# Entrada de datos  
pais = st.selectbox("🌍 Selecciona el país:", list(factores.keys()))  
costo = st.number_input("💰 Ingresa el costo por kilo (USD):", min_value=0.00, format="%.2f")  
margen_minimo = st.number_input("📈 Margen mínimo de ganancia (%)", min_value=1, max_value=90, value=10, step=1)  

if st.button("🔍 Calcular Precio de Venta"):  
    if costo == 0:  
        st.error("⚠️ No se puede generar el precio sin antes ingresar el costo del producto.")  
    else:  
        factor = factores[pais]  
        comision = comision_pais[pais]  
        costo_total = costo + (costo * factor) * comision  
        
        precios = {}  
        for incremento in [0, 5, 10]:  
            margen = margen_minimo + incremento  
            precio_venta = costo_total / (1 - (margen / 100))  
            precio_local = precio_venta * tipo_cambio[pais]  
            simbolo_moneda = moneda_local[pais]  
            precios[f"Margen {margen}%"] = f"${precio_venta:.2f} / {simbolo_moneda}{precio_local:.2f}" if tipo_cambio[pais] != 1 else f"${precio_venta:.2f}"  

        st.subheader("💰 Precios de Venta Calculados:")  
        for key, value in precios.items():  
            st.markdown(f'<div style="text-align: center; font-size: 20px; font-weight: bold; padding: 15px; border-radius: 10px; margin-bottom: 10px;">{key}: {value}</div>', unsafe_allow_html=True)  
        
        # Mostrar precios en otros países en tabla  
        data = []  
        for p, f in factores.items():  
            comision_otro = comision_pais[p]  
            costo_otro = costo + (costo * f) * comision_otro  
            precio_otro = costo_otro / (1 - (margen_minimo / 100))  
            precio_otro_local = precio_otro * tipo_cambio[p]  
            simbolo_moneda_otro = moneda_local[p]  
            data.append({"País": p, "Precio de Venta (USD)": f"${precio_otro:.2f}", "Precio en Moneda Local": f"{simbolo_moneda_otro} {precio_otro_local:.2f}"})  
        
        df = pd.DataFrame(data)  
        st.subheader("🌎 Precios Mínimos en Otros Países:")  
        st.table(df)
import streamlit as st
import pandas as pd

# Definición de datos
datos_paises = {
    "Guatemala": {"factor": 0.0622, "tipo_cambio": 8.03, "moneda": "Q", "comision": 1.01},
    "El Salvador": {"factor": 0.0745, "tipo_cambio": 1, "moneda": "USD", "comision": 1.011},
    "Honduras": {"factor": 0.0548, "tipo_cambio": 26, "moneda": "L.", "comision": 1.0111},
    "Nicaragua": {"factor": 0.0341, "tipo_cambio": 37, "moneda": "C$", "comision": 1.0123},
    "Costa Rica": {"factor": 0.0646, "tipo_cambio": 525, "moneda": "₡", "comision": 1.01},
    "Panamá": {"factor": 0.0432, "tipo_cambio": 1, "moneda": "USD", "comision": 1.0125},
}

# Función de cálculo
def calcular_precio_venta(costo, pais, margen_minimo):
    datos = datos_paises[pais]
    costo_total = costo + (costo * datos["factor"]) * datos["comision"]
    precios = {}
    
    for incremento in [0, 5, 10]:
        margen = margen_minimo + incremento
        precio_venta = costo_total / (1 - (margen / 100))
        precio_local = precio_venta * datos["tipo_cambio"]
        simbolo_moneda = datos["moneda"]
        precios[f"Margen {margen}%"] = {
            "venta": f"${precio_venta:.2f}",
            "local": f"{simbolo_moneda}{precio_local:.2f}" if datos["tipo_cambio"] != 1 else f"${precio_venta:.2f}"
        }
    return precios

# Generar precios en otros países
def precios_en_otros_paises(costo, margen_minimo):
    data = [
        {"País": p, **calcular_precio_venta(costo, p, margen_minimo)[f"Margen {margen_minimo}%"]}
        for p in datos_paises.keys()
    ]
    return pd.DataFrame(data)

# Interfaz de usuario
st.title("📊 Calculadora de Precios de Venta")

pais = st.selectbox("🌍 Selecciona el país:", list(datos_paises.keys()))
costo = st.number_input("💰 Ingresa el costo por unidad (USD):", min_value=0.00, format="%.2f")
margen_minimo = st.number_input("📈 Margen mínimo de ganancia (%):", min_value=1, max_value=90, value=10, step=1)

if st.button("🔍 Calcular Precio de Venta"):
    if costo == 0:
        st.error("⚠️ No se puede generar el precio sin antes ingresar el costo del producto.")
    else:
        precios = calcular_precio_venta(costo, pais, margen_minimo)
        
        st.subheader("💰 Precios de Venta Calculados:")
        for key, value in precios.items():
            st.markdown(
                f'<div style="text-align: center; font-size: 20px; font-weight: bold; padding: 15px; border-radius: 10px; margin-bottom: 10px;">{key}: {value["venta"]} / {value["local"]}</div>',
                unsafe_allow_html=True
            )
        
        # Mostrar precios en otros países en tabla
        df = precios_en_otros_paises(costo, margen_minimo)
        st.subheader("🌎 Precios Mínimos en Otros Países:")
        st.table(df)
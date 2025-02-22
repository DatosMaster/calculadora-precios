import streamlit as st
import pandas as pd

# Factores por país
factores = {
    "Guatemala": 0.0622,
    "El Salvador": 0.0745,
    "Honduras": 0.0548,
    "Nicaragua": 0.0341,
    "Costa Rica": 0.0646,
    "Panamá": 0.0432,
}

# Tipo de cambio por país (1 si es USD)
tipo_cambio = {
    "Guatemala": 8.03,
    "El Salvador": 1,
    "Honduras": 24.5,
    "Nicaragua": 36.0,
    "Costa Rica": 530,
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

# Detectar modo oscuro del sistema
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = "dark" if st.get_option("theme.base") == "dark" else "light"

st.title("📊 Calculadora de Precios de Venta")

# Modo claro/oscuro automático con opción de cambio
modo = st.radio("🎨 Modo de pantalla:", ["Claro", "Oscuro"], index=0 if st.session_state.modo_oscuro == "light" else 1, horizontal=True)

if modo == "Oscuro":
    st.session_state.modo_oscuro = "dark"
    st.markdown(
        """
        <style>
            body { background-color: #333; color: white; }
            .stButton>button { background-color: white; color: black; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.session_state.modo_oscuro = "light"

# Entrada de datos
pais = st.selectbox("🌍 Selecciona el país:", list(factores.keys()))
cantidad = st.number_input("⚖️ Cantidad en kilos:", min_value=1, value=1, step=1)
costo = st.number_input("💰 Ingresa el costo por kilo (USD):", min_value=0.00, format="%.2f")
margen = st.slider("📈 Margen de ganancia (%)", min_value=1, max_value=100, value=30)

if "historial" not in st.session_state:
    st.session_state.historial = []

if st.button("🔍 Calcular Precio de Venta"):
    if costo == 0:
        st.error("⚠️ No se puede generar el precio sin antes ingresar el costo del producto.")
    else:
        factor = factores[pais]
        costo_total = (costo * cantidad) + (costo * factor * cantidad) + (costo * 0.01 * cantidad)
        precio_venta = costo_total / (1 - (margen / 100)) + 0.015 * cantidad

        # Convertir precio a moneda local
        precio_local = precio_venta * tipo_cambio[pais]
        simbolo_moneda = moneda_local[pais]
        precio_final = f"💰 Precio en {pais}: ${precio_venta:.2f}"
        if tipo_cambio[pais] != 1:
            precio_final += f" / {simbolo_moneda}{precio_local:.2f}"

        # Mostrar precio centrado
        st.markdown(f'<div style="text-align: center; font-size: 24px; font-weight: bold; background-color: #f4f4f4; padding: 10px; border-radius: 10px;">{precio_final}</div>', unsafe_allow_html=True)

        # Guardar en historial
        st.session_state.historial.append(precio_final)

        # Mostrar precios en otros países en tabla
        data = []
        for p, f in factores.items():
            costo_otro = (costo * cantidad) + (costo * f * cantidad) + (costo * 0.01 * cantidad)
            precio_otro = costo_otro / (1 - (margen / 100)) + 0.015 * cantidad
            precio_otro_local = precio_otro * tipo_cambio[p]
            simbolo_moneda_otro = moneda_local[p]
            data.append({"País": p, "Precio de Venta (USD)": f"${precio_otro:.2f}", "Precio en Moneda Local": f"{simbolo_moneda_otro}{precio_otro_local:.2f}"})

        df = pd.DataFrame(data)
        st.subheader("🌎 Precios en otros países:")
        st.table(df)

# Historial de cálculos
if st.session_state.historial:
    st.subheader("📜 Historial de cálculos")
    for item in st.session_state.historial:
        st.write(item)

# Botón de reinicio
if st.button("🔄 Reiniciar"):
    st.session_state.historial = []
    st.experimental_rerun()

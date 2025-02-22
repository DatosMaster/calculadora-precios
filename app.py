import streamlit as st

# Factores por país
factores = {
    "Guatemala": 0.0622,
    "El Salvador": 0.0745,
    "Honduras": 0.0548,
    "Nicaragua": 0.0341,
    "Costa Rica": 0.0646,
    "Panamá": 0.0432,
}

st.title("📊 Calculadora de Precios de Venta")

# Entrada de datos
pais = st.selectbox("🌍 Selecciona el país:", list(factores.keys()))
costo = st.number_input("💰 Ingresa el costo producto:", min_value=0.00, format="%.2f")
margen = st.slider("📈 Margen de ganancia (%)", min_value=1, max_value=100, value=30)

if st.button("🔍 Calcular Precio de Venta"):
    if costo == 0:
        st.error("⚠️ Por favor, ingresa un costo válido para el producto antes de calcular.")
    else:
        factor = factores[pais]
        costo_venta = costo + (costo * factor) + (costo * 0.01)
        precio_venta = costo_venta / (1 - (margen / 100)) + 0.015

        # Precio de venta centrado y en negrita
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 24px;">
                💰 <b>Precio de venta en {pais}: ${precio_venta:.2f}</b>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.subheader("🌎 Precios en otros países:")
        for p, f in factores.items():
            if p != pais:
                costo_otro = costo + (costo * f) + (costo * 0.01)
                precio_otro = costo_otro / (1 - (margen / 100)) + 0.015
                st.write(f"📍 {p}: **${precio_otro:.2f}**")

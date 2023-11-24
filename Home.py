import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = ''
)

image = Image.open( 'Icon.png' )
st.sidebar.image( image, width = 120 )

st.sidebar.markdown('<div style="text-align: center; font-size:30px; font-weight: 600;"><i>InFood</i></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">The Best Delivery</div>', unsafe_allow_html=True)
st.sidebar.markdown("""---""")

st.markdown('<div style="text-align: center; font-size:50px; font-weight: 600;"><i>InFood</i> Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    """
        Esse Dashboard foi construído para acompanhar as métricas de crescimento da empresa especializada em Delivery de comida na India, onde será apresentada a visão da Empresa, Entregadores e Restaurantes.
        ### Como utilizar esse Growth Dashboard?
        - Visão Empresa:
            - Visão Gerencial: Métricas gerais de comportamento.
            - Visão Tática: Indicadores semanais de crescimento.
            - Visão Geográfica: Insights de geolocalização.
        - Visão Entregador:
            - Acompanhamento dos indicadores semanais de crescimento.
        - Visão Restaurante:
            - Indicadores semanais de crescimento dos restaurantes.
""" )

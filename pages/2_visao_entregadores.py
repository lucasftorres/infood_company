# Libraries
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import pandas as pd
import datetime
import streamlit as st
import re
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

# --------------------------------
# Funções
# --------------------------------


def top_delivers(df1, top_asc):
    df2 =  (df1.loc[:, ['Delivery_person_ID','City', 'Time_taken(min)']]
                .groupby(['City', 'Delivery_person_ID'])
                .max()
                .sort_values(['City', 'Time_taken(min)'], ascending = top_asc)
                .reset_index())

    df3 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df4 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df5 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    
    df6 = pd.concat([df3, df4, df5]).reset_index( drop = True)

    return df6



def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe

    Tipos de limpeza:
    1. Remoção de dados NaN
    2. Mudança do tipo de Coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo ( remoção do texto da variável numérica )

    Input: Dataframe
    Output: Dataframe

    """
    
    # 1. Remoção das Linhas que possuam NaN
    # Remove as linhas da coluna Delivery_person_Age que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['Delivery_person_Age'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'Road_traffic_density' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['Road_traffic_density'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'City' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['City'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'Develivery_person_Age' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['Festival'] != 'NaN' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna Weatherconditions que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['Weatherconditions'] != 'NaN' ) 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linha da coluna multiple_deliveries  que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    
     # 2.
    # Conversão de texto/categoria/string para numeros float utilizando o método astype()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 3.
    # Conversão de texto para data utilizando o método to_datetime() onde em format= o ano sempre será marcado com Y maíusculo
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    
    # 4.
    # O método strip() irá remover os espaços vazios da string
    # Substituindo as colunas por novas sem os espaços na string
    
    
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # O método reset_index irá fazer uma atualização do DataFrame após a remoção das linhas que tinham o 'NaN '
    df1 = df1.reset_index(drop=True)
    
    # Comando para remover o texto de números
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split(' ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1


# ------------------------------ Início da Estrutura Lógica do Código


# ===================
# Import dataset
# ===================
df = pd.read_csv( 'dataset/train.csv' )
df1 = df.copy()

df1 = clean_code( df )


# ==============================
# Barra Lateral
# ==============================

st.markdown('<div style="text-align: center; font-size:50px; font-weight: 600;">Marketplace - Visão Entregadores</div>', unsafe_allow_html=True)

image = Image.open( 'Icon.png' )
st.sidebar.image( image, width = 120 )

st.sidebar.markdown('<div style="text-align: center; font-size:30px; font-weight: 600;"><i>InFood</i></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">The Best Delivery</div>', unsafe_allow_html=True)
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = datetime.date( 2022, 4 , 13 ),
    min_value = datetime.date( 2022, 2, 11 ),
    max_value = datetime.date( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown("""---""")
print(type(date_slider))
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

# Filtro de data
linhas_selecionadas = ( df1['Order_Date'].dt.date < date_slider )
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = ( df1['Road_traffic_density'].isin(traffic_options) )
df1 = df1.loc[linhas_selecionadas, :]

# ==============================
# Layout no Streamlit
# ==============================

tab1, tab2, tab3 = st.tabs( [ 'Visão Gerencial', '-', '-'] )

with tab1:
    with st.container():
        st.markdown('<div style="text-align: center; font-size:40px; font-weight: 600;padding-bottom: 35px;">Overall  Metrics</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns( 4, gap = 'large')
        
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior idade', maior_idade )
            
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric( 'Menor idade', menor_idade )
            
        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor Condicao', melhor_condicao)
            
        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior Condicao', pior_condicao)

    with st.container():
        st.markdown( """----""" )        
        st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600; padding-bottom: 20px">Avaliações</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">Avaliação Media por entregador</div>', unsafe_allow_html=True)
            column = ['Delivery_person_ID', 'Delivery_person_Ratings']
            avg_ratings  = ( df1.loc[:, column]
                                .groupby('Delivery_person_ID')
                                .mean()
                                .reset_index() )
            
            st.dataframe( avg_ratings, use_container_width = True, height = 482)
            
        with col2:
            st.markdown('<div style="text-align: center; font-size: 20px; font-weight: 600;">Avaliação Media por Transito</div>', unsafe_allow_html=True)
            columns = ['Delivery_person_Ratings', 'Road_traffic_density']
            df2 = ( df1.loc[:, columns].groupby('Road_traffic_density')
                    .agg({'Delivery_person_Ratings': ['mean', 'std']}) )

            df2.columns = ['Delivery_mean', 'Delivery_std']
            df2.reset_index()
            st.dataframe(df2, use_container_width = True)
            
            st.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">Avaliação Media por Clima</div>', unsafe_allow_html=True)
            columns = ['Delivery_person_Ratings', 'Weatherconditions']
            df2 = (df1.loc[:, columns].groupby('Weatherconditions')
            .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            df2.columns = ['Mean_Weathercondition', 'Std_Weathercondition']
            df2.reset_index()
            st.dataframe(df2, use_container_width = True)
            
    with st.container():
        st.markdown( """----""" )
        st.markdown('<div style="text-align: center; font-size: 35px; font-weight: 700, padding-bottom: 20px;">Velocidade de Entrega</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns( 2 )
        
        with col1:
            st.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">Top entregador mais Rapido</div>', unsafe_allow_html=True)
            df6 = top_delivers( df1, top_asc = True )
            st.dataframe( df6 )
            
        with col2:
            st.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">Top entregador mais Lento</div>', unsafe_allow_html=True)
            df6 = top_delivers( df1, top_asc = False )
            st.dataframe( df6 )
            
            
        
            
        
        
        
        
        
        
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


## Função para criar um mapa com a mediana dos lcais de entrega por cidade e por densidade de tráfego
def country_maps(df1):            
    df2 = ( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                .groupby(['City', 'Road_traffic_density'])
                .median()
                .reset_index() )
    
    map = folium.Map()
    for (index, location_info) in df2.iterrows():
         folium.Marker( [location_info['Delivery_location_latitude'],
                         location_info['Delivery_location_longitude']],
                         popup = location_info[['City', 'Road_traffic_density']]).add_to(map)
                           
    folium_static( map, width = 1024, height = 600 )


## Função para mostrar a quantidade de entregas por semana por entregador unico
def order_share_by_week(df1): 
    df2 = df1.loc[:, ['ID', 'Week_of_the_year']].groupby('Week_of_the_year').count().reset_index()
    df3 = ( df1.loc[:, ['Delivery_person_ID', 'Week_of_the_year']]
                .groupby('Week_of_the_year')
                .nunique()
                .reset_index() )
        
    df4 = pd.merge(df2, df3, how = 'inner', on = 'Week_of_the_year')
    df4['Order_by_delivery'] = df4['ID'] / df4['Delivery_person_ID']
    fig = px.line(df4, x='Week_of_the_year', y='Order_by_delivery')

    return fig


## Função para mostrar a quantidade de entregas por semana
def order_by_week(df1):
    df1['Week_of_the_year'] = df1['Order_Date'].dt.strftime('%U')
    df2 = df1.loc[:, ['ID', 'Week_of_the_year']].groupby('Week_of_the_year').count().reset_index()
    fig = px.line(df2, x='Week_of_the_year', y='ID')

    return fig 


## Função para mostrar a quantidade de entregas por cidade e por densidade de tráfego
def traffic_order_city(df1):
    df2 = ( df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
               .groupby(['City', 'Road_traffic_density'])
               .count()
               .reset_index() )
                    
    fig = px.scatter(df2, x = 'City', y='Road_traffic_density', size = 'ID', color = 'City')

    return fig


## Função para mostrar a quantidade de entregas por densidade de tráfego
def traffic_order_share(df1):                       
    df2 = ( df1.loc[:, ['ID', 'Road_traffic_density']]
               .groupby('Road_traffic_density')
               .count()
               .reset_index() )
    
    df2['perc_ID'] = 100 * (df2['ID'] / df2['ID'].sum())  
    fig =  px.pie( df2, values = 'perc_ID', names = 'Road_traffic_density')

    return fig


## Função para mostrar a quantidade de entregas por dia
def order_metric( df1 ):
    #Selecção de Linhas
    df2 = df1.loc[:,['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()            
    df2.columns = ['order_date', 'qtd_entregas']
    
    ## Desenhando gráfico
    fig = px.bar(df2 , x='order_date', y='qtd_entregas')

    return fig



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

st.markdown('<div style="text-align: center; font-size:50px; font-weight: 600;">Marketplace - Visão Cliente</div>', unsafe_allow_html=True)

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


tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        fig = order_metric( df1 )
        st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Orders by Day</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width = True)

    with st.container():       
        col1, col2 = st.columns( 2 )
        
        with col1:
            st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Traffic Order Share</div>', unsafe_allow_html=True)
            fig = traffic_order_share( df1 )
            st.plotly_chart( fig, use_container_width = True )
            
            
        with col2:
            st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Traffic Order City</div>', unsafe_allow_html=True)
            fig = traffic_order_city( df1 )
            st.plotly_chart( fig, use_container_width = True )
            


with tab2:
    with st.container():
        st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Order by Week</div>', unsafe_allow_html=True)
        fig  = order_by_week(df1)
        st.plotly_chart( fig, use_container_width = True )
        
         
    with st.container():
        st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Order Share by Week</div>', unsafe_allow_html=True)
        fig = order_share_by_week(df1)
        st.plotly_chart( fig, use_container_width = True )
        
        

with tab3:
        col1, col2, col3 = st.columns([1, 10, 1])
        with col2:
            st.markdown('<div style="text-align: center; font-size:35px; font-weight: 600;">Country Maps</div>', unsafe_allow_html=True)
            country_maps( df1 )





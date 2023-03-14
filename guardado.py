import pandas as pd
import streamlit as st
import codecs as co
import matplotlib.pyplot as plt
import plotly.express as px
st.title("Comics of marvel")
DATA_URL =co.open('Marvel_Comics.csv', 'rU', 'latin1')


#--------------------------------------------sidebar-----------------------------------------------
#side bar
sidebar = st.sidebar


#--------------------------------------------cargar 500 registros--------------------------------------

@st.cache
def load_data(nrows):
    
    data=pd.read_csv(DATA_URL, nrows=nrows)
    return data

data_load_state =st.text('Load data...')
data=load_data(500)
data_load_state.text("Done! (using st.cache)")

st.dataframe(data)
#-------------------------------------------Busqueda por nombre------------------------------------
@st.cache
def load_data_byname(name):
    data =pd.read_csv(DATA_URL)
    filtered_data_byname =data[data["comic_name"].str.contains(name, case=False)]
    return filtered_data_byname

name = sidebar.text_input("Titulo")
btnbuscar = sidebar.button('Buscar comic')

if(btnbuscar):
    filterbyname = load_data_byname(name)
    count_row = filterbyname.shape[0]

    st.title(":blue[Resultado de busqueda]")
    st.write("total names: {count_row}")
    st.dataframe(filterbyname)


#-------------------------------------Histograma------------------------------------------------
fig, ax=plt.subplots()
ax.hist(load_data(500).Price)
st.header("Precio de los comics")
st.pyplot(fig)

#::::::::::: histograma :::::::::::
datasave=load_data(500)
sidebar.title("Graficas:")
st.header("Histograma")
agree = sidebar.checkbox("Clic para ver histograma")
if agree:
  fig_genre=px.bar(datasave,
                    x=datasave.Price,
                    y=datasave.index, #index es para que cuente la cantidad total
                    orientation="v",
                    title="Cantidad de canciones que hay por genero",
                    labels=dict(name_employee="Employee Name", 
performance_score="Performance Score"),
                    color_discrete_sequence=["#7ECBB4"],
                    template="plotly_white")
  st.plotly_chart(fig_genre)

#---------------------------------------grafica de barras---------------------------------------

fig2, ax2=plt.subplots()
x_pos= load_data(100)['Price']
y_pos= load_data(100)['cover_artist']
ax2.barh(y_pos,x_pos)
ax2.set_ylabel("precio")
ax2.set_xlabel("cover_artist")
ax2.set_title("relacion precios-autor")

st.header("Grafica de barras")
st.pyplot(fig2)

#::::::::::: grafica de barras :::::::::::

agree = sidebar.checkbox("Clic para ver grafica de barras")
if agree:
   price=load_data(100)['Price']
   cover=load_data(100)['cover_artist']
   st.header("Grafica de barras")
   fig_barra=px.bar(data,
                    x=cover,
                    y=price,
                    orientation="v",
                    title="Relación Artistas precios",
                    labels=dict(price="Price", cover="Cover_artist"),
                    color_discrete_sequence=["#7ECBB4"],
                    template="plotly_white")
   st.plotly_chart(fig_barra)
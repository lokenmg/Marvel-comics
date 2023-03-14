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
#--------------------------------------------logo---------------------------------------------------
st.sidebar.image("marvel_logo.jpg")
st.sidebar.markdown("##")
st.sidebar.title("Autor")
st.sidebar.text("Rodrigo Mencias Gonzalez")

#--------------------------------------------cargar 500 registros--------------------------------------

@st.cache
def load_data(nrows):
    
    data=pd.read_csv(DATA_URL, nrows=nrows)
    return data

st.title("_Registros_")
data_load_state =st.text('Load data...')
data=load_data(500)
data_load_state.text("Done! (using st.cache)")

st.dataframe(data)

st.sidebar.title("Filtros de busqueda")
#-------------------------------------------Busqueda por nombre------------------------------------
@st.cache
def load_data_byname(name):
    data =pd.read_csv(DATA_URL)
    filtered_data_byname =data[data["comic_name"].str.contains(name, case=False)]
    return filtered_data_byname

name = sidebar.text_input("Buscar titulo")
btnbuscar = sidebar.button('Buscar')

if(btnbuscar):
    filterbyname = load_data_byname(name)
    count_row = filterbyname.shape[0]

    st.title("_Resultado de busqueda_")
    st.write("total names: {count_row}")
    st.dataframe(filterbyname)

#-----------------------------------multiselect----------------------------------------------------
Price = st.sidebar.multiselect("Seleccionar precios",
                                options=data['Price'].unique(),
                                default=data['Price'].unique())

st.title("_Filtrado por precios_")
df_selection=data.query("Price == @Price")
st.write("Origen seleccionado", df_selection)

#Select
data=load_data(500)
selected_type = sidebar.radio("Selecciona la imprenta",
data['Imprint'].unique())

st.title("_Filtrado por imprentas_")
st.write("Imprenta seleccionada: ", selected_type)
st.write(data.query(f"""Imprint==@selected_type"""))
st.markdown("_")


#-------------------------------------Histograma------------------------------------------------
st.sidebar.title("Controles de graficas de barras")

fig, ax=plt.subplots()
ax.hist(load_data(500).Price)
agree = sidebar.checkbox("Clic para ver histograma")
if agree:
    st.header("Precio de los comics")
    st.pyplot(fig)
    st.markdown("En este histograma podemos ver la variación de los precios que tienen los comics,\
                 precios que van desde los comics gratis hasta comics de $7.99. los comics que vemos\
                 son los mas comunes de ver son los que están entre los precios de 3.99 y 2.99, seguidos\
                 de los comics gratis.")
#---------------------------------------grafica de barras---------------------------------------

data=load_data(500)
fig2, ax2=plt.subplots()
x_pos= data['Price']
y_pos= data['cover_artist']
ax2.barh(y_pos,x_pos)
ax2.set_ylabel("precio")
ax2.set_xlabel("cover_artist")
ax2.set_title("relacion precios-autor")

agree = sidebar.checkbox("Clic para ver grafica de barras")

df_selection=data.query("Price == @Price")
if agree:
    Precio=data['Price']
    Clasificacion=data['Rating']
    st.header("Grafica de barras")
    fig_barra=px.bar(data,
                        x=Clasificacion,
                        y=Precio,
                        orientation="v",
                        title="Relación precios-clasificación",
                        labels=dict(price="precio", cover="clasificacion"),
                        color_discrete_sequence=["#7ECBB4"],
                        template="plotly_white")
    st.plotly_chart(fig_barra)


    st.markdown("En esta grafica de barras podemos ver los precios de los comics en la relación con su\
             clasificación, también podemos ver que las clasificaciones con mayor número de comics\
             de diferentes precios son los comics que no se encuentran registrados en ninguna \
             clasificación.")

#---------------------------------------Grafica scatter --------------------------------------------
data=load_data(1000)

agree = sidebar.checkbox("Clic para ver grafica scatter")
if agree:
    imprint=data['Imprint']
    years=data['active_years']
    rating=data['Rating']
    fig_age=px.scatter(data,
                   x=imprint,
                   y=rating,
                   color=years, 
                   title="Relación de los años activos de los comics con la imprenta y la imprenta de los comics",
                   labels=dict(Imprenta="imprint", years="years", print="Print"),
                   template="plotly_white")
    st.header("Grafica Scatter")
    st.plotly_chart(fig_age)
    st.markdown("En esta grafica podemos ver la relación entre la clasificación y la imprenta\
                 relacionada con los años activos de cada comic, vemos que los comics de la impr\
                 enta Marvel Universe tiene mas variedad de clasificación de comics con distinto\
                 s años de publicación activos.")
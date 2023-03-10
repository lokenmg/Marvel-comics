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
    st.markdown("En este histograma podemos ver la variaci??n de los precios que tienen los comics,\
                 precios que van desde los comics gratis hasta comics de 7.99 los comics  mas \
                 comunes de ver son los que est??n entre los precios de 3.99 y los gratis, seguidos\
                 de los comics de 2.99")
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
                        title="Relaci??n precios-clasificaci??n",
                        labels=dict(price="precio", cover="clasificacion"),
                        color_discrete_sequence=["#7ECBB4"],
                        template="plotly_white")
    st.plotly_chart(fig_barra)


    st.markdown("En esta grafica de barras podemos ver los precios de los comics en la relaci??n con su\
             clasificaci??n, tambi??n podemos ver que las clasificaciones con mayor n??mero de comics\
             de diferentes precios son los comics que no se encuentran registrados en ninguna \
             clasificaci??n.")

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
                   title="Relaci??n de los a??os activos de los comics con la imprenta y la imprenta de los comics",
                   labels=dict(Imprenta="imprint", years="years", print="Print"),
                   template="plotly_white")
    st.header("Grafica Scatter")
    st.plotly_chart(fig_age)
    st.markdown("En esta grafica podemos ver la relaci??n entre la clasificaci??n y la imprenta\
                 relacionada con los a??os activos de cada comic, vemos que los comics de la impr\
                 enta Marvel Universe tiene mas variedad de clasificaci??n de comics con distinto\
                 s a??os de publicaci??n activos.")
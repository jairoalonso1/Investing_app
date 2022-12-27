import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go



countries = ['united states', 'spain', 'chile','brazil','Luxembourg']
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(112)
end_date = datetime.today()

@st.cache(allow_output_mutation=True)
def consultar_etf (fund, country, from_date, to_date, interval):
    df = ip.get_fund_historical_data(
        fund=fund, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df



def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)



def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }


    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig



# CREANDO UNA BARRA LATERAL
st.sidebar.title ('Frontera Eficiente')
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Seleccione un país:", countries)
funds = ip.get_funds_list(country=country_select)
stock_select = st.sidebar.selectbox("Seleccione un fondo:", funds)
from_date = st.sidebar.date_input('Fecha Inicial:', start_date)
to_date = st.sidebar.date_input('Fecha Final:', end_date)
interval_select = st.sidebar.selectbox("Seleccione el intervalo:", intervals)
cargar_datos = st.sidebar.checkbox('Cargar datos')


grafico_line = st.empty()
grafico_candle = st.empty()

# elementos centrais da página
st.title('ETF Monitor')

st.header('ETF´s')

st.subheader('Plot')

if from_date > to_date:
    st.sidebar.error('Fecha de ínicio mayor que la fecha final')
else:
    df = consultar_etf(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.area_chart(df.Close)
        if cargar_datos:
            st.subheader('Datos')
            datos = st.dataframe(df)
            stock_select = st.sidebar.selectbox          
    except Exception as e:
        st.error(e)

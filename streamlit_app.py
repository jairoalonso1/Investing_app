import datetime
import streamlit as st
import cufflinks as cf
import yfinance as yf

APP_NAME = "Frontera Eficiente!"

# Page Configuration
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add some markdown
st.sidebar.markdown("Grado de Inversion Funds")
st.sidebar.markdown("# :chart_with_upwards_trend:")

# Add app title
st.sidebar.title(APP_NAME)

# List of tickers
TICKERS = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']

# Select ticker
ticker = st.sidebar.text_input('STOCK OR ETF', 'AAPL')
tickerData = yf.Ticker(ticker)

# Set start and end point to fetch data
start_date = st.sidebar.date_input('Start date', datetime.datetime(2021, 1, 1))
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

# Fetch the data for specified ticker e.g. AAPL from yahoo finance
df_ticker = tickerData.history(period='1d', start=start_date, end=end_date)

st.header(f'{ticker} Stock Price')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df_ticker)

# Interactive data visualizations using cufflinks
# Create candlestick chart
qf = cf.QuantFig(df_ticker, legend='top', name=ticker)


# Technical Analysis Studies can be added on demand
# Add Relative Strength Indicator (RSI) study to QuantFigure.studies
qf.add_rsi(periods=20, color='java')

# Add Bollinger Bands (BOLL) study to QuantFigure.studies
qf.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)

# Add 'volume' study to QuantFigure.studies
qf.add_volume()

fig = qf.iplot(asFigure=True, dimensions=(800, 600))

# Render plot using plotly_chart
st.plotly_chart(fig)

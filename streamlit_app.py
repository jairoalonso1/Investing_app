import streamlit as st
import quantstats as qs

# Seleccionar los fondos a comparar
fund1 = st.selectbox("Seleccione el primer fondo", ["IVV", "EEM", "AGG", "LQD"])
fund2 = st.selectbox("Seleccione el segundo fondo", ["IVV", "EEM", "AGG", "LQD"])

# Crear un widget de fecha para ingresar las fechas de inicio y fin
fecha_inicio = st.date_input("Ingrese la fecha de inicio")
fecha_fin = st.date_input("Ingrese la fecha de fin")

# Descargar los datos de los fondos seleccionados en el rango de fechas seleccionado
fund1_data = qs.utils.download_returns(fund1, start=fecha_inicio, end=fecha_fin)
fund2_data = qs.utils.download_returns(fund2, start=fecha_inicio, end=fecha_fin)

# Calcular las métricas de rendimiento de los fondos
fund1_performance = qs.Performance(fund1_data)
fund2_performance = qs.Performance(fund2_data)

# Crear una tabla con las principales métricas de los fondos
metrics = ["Rendimiento Anualizado", "Tasa de Ganancia", "Volatilidad", "Drawdown"]
values1 = [fund1_performance.annual_return, fund1_performance.winning_percentage, fund1_performance.volatility, fund1_performance.drawdown]
values2 = [fund2_performance.annual_return, fund2_performance.winning_percentage, fund2_performance.volatility, fund2_performance.drawdown]

# Grafico de Earnings comparativo
st.subheader("Gráfico de Earnings comparativo")
qs.plt.earnings_plot(fund1_performance, label=fund1)
qs.plt.earnings_plot(fund2_performance, label=fund2)
st.pyplot()

# Crear cuatro tabs:
st.header("Análisis de fondos")
tab = st.selectbox("Seleccione una pestaña",["Performance","Métricas", "Drawdown", "Rollings"])

if tab == "Performance":
  st.subheader("Gráfico de Earnings comparativo")
  qs.plt.earnings_plot(fund1_performance, label=fund1)
  qs.plt.earnings_plot(fund2_performance, label=fund2)
  st.pyplot()
  st.write("Características del fondo {}:".format(fund1))
  st.write(fund1_performance.characteristics)
  st.write("Características del fondo {}:".format(fund2))
  st.write(fund2_performance.characteristics)

elif tab == "Métricas":
  st.table(metrics, values1, values2)

elif tab == "Drawdown":
  st.subheader("Gráfico de Drawdown comparativo")
  qs.plt.drawdown_plot(fund1_performance, label=fund1)
  qs.plt.drawdown_plot(fund2_performance, label=fund2)
  st.pyplot()
  st.write("5 mayores Drawdowns del fondo {}:".format(fund1))
  st.write(fund1_performance.top_drawdowns(5))
  st.write("5 mayores Drawdowns del fondo {}:".format(fund2))
  st.write(fund2_performance.top_drawdowns(5))

elif tab == "Rollings":
  st.write("Rolling volatility del fondo {}:".format(fund1))
  st.write(fund1_performance.rolling_volatility())
  st.write("Rolling sharpe del fondo {}:".format(fund1))
  st.write(fund1_performance.rolling_sharpe())
  st.write("Rolling volatility del fondo {}:".format(fund2))
  st.write(fund2_performance.rolling_volatility())
  st.write("Rolling sharpe del fondo {}:".format(fund2))
  st.write(fund2_performance.rolling_sharpe())

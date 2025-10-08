import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Investimentos", page_icon="💰")
st.title("Simulador de Investimento Ambicioso")
st.write("Aplicação que utiliza um **algoritmo guloso (Fractional Knapsack)** para montar uma carteira com o **melhor retorno possível sem ultrapassar o risco total permitido.**")

DATA_PATH = "ETFs.csv"

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("Arquivo CSV não encontrado em 'ETFs.csv'.")
    st.stop()

df = df[[
    'fund_symbol',
    'fund_short_name',
    'fund_mean_annual_return_3years',
    'fund_stdev_3years'
]].dropna()

df['eficiencia'] = df['fund_mean_annual_return_3years'] / df['fund_stdev_3years']

st.sidebar.header("Configurações")
limite_risco = st.sidebar.slider("Limite máximo de risco total (%)", 1, 100, 15)

df = df.sort_values(by='eficiencia', ascending=False)

risco_total = 0.0
retorno_total = 0.0
carteira = []

for _, row in df.iterrows():
    risco_item = row['fund_stdev_3years'] * 100  # percentual
    retorno_item = row['fund_mean_annual_return_3years'] * 100

    if risco_total + risco_item <= limite_risco:
        carteira.append(row)
        risco_total += risco_item
        retorno_total += retorno_item
    else:
        fracao_disponivel = max(0, (limite_risco - risco_total) / risco_item)
        if fracao_disponivel > 0:
            risco_total += risco_item * fracao_disponivel
            retorno_total += retorno_item * fracao_disponivel
            row_copy = row.copy()
            row_copy['fund_short_name'] += f" (fração {fracao_disponivel:.2f})"
            carteira.append(row_copy)
        break  # limite atingido

carteira_df = pd.DataFrame(carteira)

st.subheader("📊 Carteira Selecionada")
st.dataframe(
    carteira_df[['fund_short_name', 'fund_mean_annual_return_3years', 'fund_stdev_3years', 'eficiencia']]
    .rename(columns={
        'fund_short_name': 'Investimento',
        'fund_mean_annual_return_3years': 'Retorno (3y)',
        'fund_stdev_3years': 'Risco (3y)',
        'eficiencia': 'Eficiência'
    })
)

col1, col2 = st.columns(2)
col1.metric("📉 Risco total", f"{risco_total:.2f}%")
col2.metric("📈 Retorno estimado", f"{retorno_total:.2f}%")

st.subheader("📈 Retorno dos Investimentos Selecionados")
st.bar_chart(carteira_df.set_index('fund_short_name')['fund_mean_annual_return_3years'])

st.caption("💡O algoritmo guloso seleciona sempre o investimento com melhor relação **retorno/risco** até atingir o limite máximo de risco permitido (estratégia semelhante ao *Fractional Knapsack*).")
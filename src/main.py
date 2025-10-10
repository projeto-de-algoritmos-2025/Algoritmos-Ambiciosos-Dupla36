import pandas as pd
import streamlit as st

st.set_page_config(page_title="Simulador de Investimentos", page_icon="💰")
st.title("Simulador de Investimento Ambicioso")
st.write("Aplicação que utiliza um **algoritmo guloso (Fractional Knapsack)** para montar uma carteira com o **melhor retorno possível sem ultrapassar o risco total permitido.**")

DATA_PATH = "ETFs.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df = df[[
        'fund_symbol',
        'fund_short_name',
        'fund_mean_annual_return_3years',
        'fund_stdev_3years'
    ]].dropna()
    df['eficiencia'] = df['fund_mean_annual_return_3years'] / (df['fund_stdev_3years'] + 1e-9)
    return df

try:
    df_original = load_data(DATA_PATH)
except FileNotFoundError:
    st.error("Arquivo CSV não encontrado em 'ETFs.csv'.")
    st.stop()

st.sidebar.header("Configurações")
limite_risco = st.sidebar.slider("Limite máximo de risco total (%)", 1, 100, 15)

df_sorted = df_original.sort_values(by='eficiencia', ascending=False)

risco_total = 0.0
retorno_total = 0.0
carteira = []

for _, row in df_sorted.iterrows():
    risco_item = row['fund_stdev_3years']
    retorno_item = row['fund_mean_annual_return_3years']

    row_copy = row.copy()

    if risco_total + risco_item <= limite_risco:
        risco_total += risco_item
        retorno_total += retorno_item
        row_copy['alocacao'] = 1.0
        carteira.append(row_copy)
    else:
        fracao_disponivel = max(0, (limite_risco - risco_total) / risco_item)
        if fracao_disponivel > 0:
            risco_total += risco_item * fracao_disponivel
            retorno_total += retorno_item * fracao_disponivel
            row_copy['alocacao'] = fracao_disponivel
            row_copy['fund_short_name'] += f" ({fracao_disponivel:.2f} da alocação)"
            carteira.append(row_copy)
        break  # limite atingido

st.subheader("📊 Carteira Selecionada")

if not carteira:
    st.warning("Nenhum ativo pôde ser adicionadao à carteira com os critérios atuais.")
else:
    carteira_df = pd.DataFrame(carteira)
    carteira_df['retorno_ponderado'] = carteira_df['fund_mean_annual_return_3years'] * carteira_df['alocacao']
    st.dataframe(
        carteira_df[['fund_short_name', 'fund_mean_annual_return_3years', 'fund_stdev_3years', 'eficiencia', 'alocacao']]
        .rename(columns={
            'fund_short_name': 'Investimento',
            'fund_mean_annual_return_3years': 'Retorno Anual (3a)',
            'fund_stdev_3years': 'Risco (3a)',
            'eficiencia': 'Eficiência',
            'alocacao': 'Fração Alocada'
        }),
        column_config={
            "Retorno Anual (3a)": st.column_config.NumberColumn(format="%.2f%%"),
            "Risco (3a)": st.column_config.NumberColumn(format="%.2f%%"),
            "Fração Alocada": st.column_config.ProgressColumn(
                "Fração Alocada",
                format="%.2f",
                min_value=0,
                max_value=1,
            ),
        }
    )


col1, col2 = st.columns(2)
col1.metric("📉 Risco total da carteira", f"{risco_total:.2f}%")
col2.metric("📈 Retorno estimado da carteira", f"{retorno_total:.2f}%")

st.subheader("📈 Contribuição de Retorno por Ativo na Carteira")

st.bar_chart(carteira_df.set_index('fund_short_name')['retorno_ponderado'])
st.caption("💡O algoritmo guloso seleciona sempre o investimento com melhor relação **retorno/risco** até atingir o limite máximo de risco permitido (estratégia semelhante ao *Fractional Knapsack*).")
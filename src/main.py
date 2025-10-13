import pandas as pd
import streamlit as st

st.set_page_config(page_title="Simulador de Investimentos", page_icon="💰")
st.title("Simulador de Investimento Ambicioso")

tab1, tab2 = st.tabs([
    "Seleção por Capital Disponível",
    "Seleção com Limite de Risco"
])


# == carregar os datasets
DATA_PATH_ETFS = "../data/ETFs.csv"
DATA_PATH_ETFS_PRICE = "../data/ETF prices.csv" 

@st.cache_data
def load_data(funds_path, prices_path):
    # dados gerais
    df_funds = pd.read_csv(funds_path)
    df_funds = df_funds[[
        'fund_symbol',
        'fund_short_name',
        'fund_mean_annual_return_3years',
        'fund_stdev_3years',
        'fund_return_1year',
        'fund_return_3years',
        'fund_return_5years'
    ]].dropna()

    # dados de preços
    df_prices = pd.read_csv(prices_path)
    df_prices = df_prices[['fund_symbol', 'adj_close', 'price_date']]

    # pegar o último preço de cada fundo
    df_last_prices = df_prices.sort_values('price_date').groupby('fund_symbol').tail(1)

    # merge para unir preço aos dados gerais
    df_merged = pd.merge(df_funds, df_last_prices[['fund_symbol','adj_close']],
                        on='fund_symbol', how='left')
    return df_merged
try:
    df_original = load_data(DATA_PATH_ETFS, DATA_PATH_ETFS_PRICE)
except FileNotFoundError:
    st.error("Arquivo CSV não encontrado no PATH especificado.")
    st.stop()




with tab1:
    # ======= nova versão para considerar capital disponível para investir =======
    st.header("Seleção de Carteira por Capital Disponível")
    st.write("Nesta aba, o algoritmo utiliza uma abordagem semelhante ao Fractional Knapsack clássico. O “peso” é o preço de cada ETF, e o “valor” é o retorno anual esperado. " \
    "O objetivo é montar a carteira com o maior retorno possível sem ultrapassar o capital disponível, podendo investir frações de ETFs quando necessário. Ideal para demonstrar a relação valor/peso aplicada a investimentos.")

    # == configurações do usuário
    st.sidebar.header("Configurações")

    capital_total = st.sidebar.number_input(
        "Capital disponível para investir (R$)", min_value=10, value=150, step=10
    )

    risco_prioridade = st.sidebar.selectbox(
        "Prioridade de risco",
        options=["Maior risco", "Menor risco"],
        index=0
    )

    # == calcular eficiência (razão valor/peso) conforme prioridade
    if risco_prioridade == "Menor risco":
        df_original['eficiencia'] = df_original['fund_mean_annual_return_3years'] / (df_original['fund_stdev_3years'] + 1e-9)
    else:
        df_original['eficiencia'] = df_original['fund_mean_annual_return_3years'] * df_original['fund_stdev_3years']

    # ordenar por eficiência decrescente
    df_sorted = df_original.sort_values(by='eficiencia', ascending=False)

    # == Algoritmo Fractional Knapsack
    capital_usado = 0.0
    retorno_total = 0.0
    carteira = []

    for _, row in df_sorted.iterrows():
        row_copy = row.copy()
        preco_unitario = row['adj_close']
        capital_restante = capital_total - capital_usado

        if capital_restante >= preco_unitario:
            # compra inteira
            row_copy['alocacao'] = preco_unitario
            capital_usado += preco_unitario
            retorno_total += (row['fund_mean_annual_return_3years'] / 100) * preco_unitario
            carteira.append(row_copy)
        else:
            # compra fracionária
            fracao_disponivel = capital_restante
            if fracao_disponivel > 0:
                row_copy['alocacao'] = fracao_disponivel
                row_copy['fund_short_name'] += f" ({fracao_disponivel:.2f} R$)"
                capital_usado += fracao_disponivel
                retorno_total += (row['fund_mean_annual_return_3years'] / 100) * fracao_disponivel
                carteira.append(row_copy)
            break


    st.subheader("📊 Carteira Selecionada")

    if not carteira:
        st.warning("Nenhum ativo pôde ser adicionado à carteira com os critérios atuais.")
    else:
        carteira_df = pd.DataFrame(carteira)
        carteira_df['capital_investido'] = carteira_df['alocacao']  # valor em R$
        carteira_df['retorno_real'] = carteira_df['fund_mean_annual_return_3years'] * carteira_df['alocacao']
        carteira_df['retorno_ponderado'] = carteira_df['fund_mean_annual_return_3years'] * carteira_df['alocacao']

        st.dataframe(
            carteira_df[[
                'fund_short_name',
                'adj_close',
                'fund_mean_annual_return_3years',
                'fund_stdev_3years',
                'eficiencia',
                'alocacao',
                'capital_investido',
                'retorno_real'
            ]].rename(columns={
                'fund_short_name': 'Investimento',
                'adj_close': 'Preço Unitário (R$)',
                'fund_mean_annual_return_3years': 'Retorno Anual (%)',
                'fund_stdev_3years': 'Risco (%)',
                'eficiencia': 'Eficiência',
                'alocacao': 'Unidades (ou fração)',
                'capital_investido': 'Capital Alocado (R$)',
                'retorno_real': 'Retorno Estimado (R$)'
            }),
            column_config={
                "Retorno Anual (%)": st.column_config.NumberColumn(format="%.2f%%"),
                "Risco (%)": st.column_config.NumberColumn(format="%.2f%%"),
                "Unidades (ou fração)": st.column_config.NumberColumn(format="%.2f"),
                "Capital Alocado (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
                "Retorno Estimado (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
            }
        )


    col1, col2 = st.columns(2)

    col1.metric("💸 Capital usado", f"R${capital_usado:.2f}")
    col2.metric("📈 Retorno estimado da carteira ao ano (base 3 anos)", f"{retorno_total:.2f}%")

    st.subheader("📈 Contribuição de Retorno por Ativo na Carteira")

    st.bar_chart(carteira_df.set_index('fund_short_name')['retorno_ponderado'])
    st.caption("💡O algoritmo guloso seleciona sempre o investimento com melhor relação **retorno/risco** até atingir o limite máximo de risco permitido (estratégia semelhante ao *Fractional Knapsack*).")

with tab2:
    # ======= versão original com limite de risco =======
    st.header("Seleção de Carteira com Limite de Risco")
    st.write("Nesta aba, o “peso” é o risco de cada ETF, e o “valor” continua sendo o retorno anual. O objetivo é maximizar o retorno da carteira sem ultrapassar um limite máximo de risco definido pelo investidor. " \
    "Essa adaptação mostra como o Knapsack pode ser aplicado a restrições diferentes, como controle de risco, e ainda permite frações de investimentos para otimizar a alocação.")

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
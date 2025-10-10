# 📊 Simulador de Investimentos Ambicioso — ETFs e Fundos

**Número da Lista**: 36
**Conteúdo da Disciplina**: FGA0124 - PROJETO DE ALGORITMOS - T01

## 👩‍💻 Alunos

<div align="center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/danielle-soaress"><img style="border-radius: 50%;" src="https://github.com/danielle-soaress.png" width="190;" alt=""/><br /><sub><b>Danielle Soares</b></sub></a></td>
    <td align="center"><a href="https://github.com/Leticia-Arisa-K-Higa"><img style="border-radius: 50%;" src="https://github.com/Leticia-Arisa-K-Higa.png" width="190px;" alt=""/><br /><sub><b>Leticia Arisa</b></sub></a></td>
  </tr>
</table>

| Matrícula  | Aluno                        |
| ---------- | ---------------------------- |
| 23/1012058 | Danielle Soares da Silva     |
| 23/1012272 | Leticia Arisa Kobayashi Higa |

</div>

## 🎬 Apresentação do Projeto

<div align="center">
<a href=""><img src="" width="50%"></a>
</div>

Autores: [Danielle Soares](https://github.com/danielle-soaress) e [Leticia Arisa](https://github.com/Leticia-Arisa-K-Higa).

## 🎯 Objetivo

Desenvolver uma aplicação interativa para analisar e visualizar dados de investimentos (ETFs e Fundos Mútuos), permitindo:

* Exibição de indicadores de desempenho, como *retorno anual*, *Sharpe ratio*, *beta*, etc.;
* Visualização interativa de métricas de fundos por categoria, tipo de ativo ou rentabilidade;
* Auxílio na tomada de decisão de investimentos através de gráficos e filtros dinâmicos.


## 🔧 Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas:**
  * `pandas` → leitura e manipulação de dados CSV
  * `streamlit` → criação da interface web interativa

## 🧩 Estrutura do Projeto

```
📁 Algoritmos-Ambiciosos-Dupla36
 ┣ 📂 data
 ┃ ┗ ETFs.csv
 ┣ 📂 src
 ┃ ┗ main.py
 ┣ 📜 LICENSE
 ┣ 📜 requirements.txt
 ┣ 📜 README.md
```

* `data/` → contém o dataset com as informações dos fundos e ETFs.
* `src/main.py` → script principal do Streamlit que faz a leitura e visualização dos dados.
* `requirements.txt` → dependências necessárias para executar o projeto.

## 🧠 Funcionalidades

1. **Visualização de Indicadores**

   * Exibe métricas financeiras como retorno, volatilidade, Sharpe Ratio, e total de ativos sob gestão.

2. **Filtros Dinâmicos**

   * Permite selecionar regiões, categorias e famílias de fundos.

3. **Gráficos Interativos**

   * Mostra comparações de performance ao longo do tempo com `Plotly`.

4. **Análise Exploratória**

   * Calcula médias e correlações entre indicadores financeiros.


## 🚀 Como Executar

1. **Clonar o repositório**

```bash
git clone https://github.com/projeto-de-algoritmos-2025/Algoritmos-Ambiciosos-Dupla36.git
```

2. **Entrar na pasta do projeto**

```bash
cd Algoritmos-Ambiciosos-Dupla36
```

3. **Instalar dependências**

```bash
pip install -r requirements.txt
```

4. **Executar o programa**

```bash
cd src
streamlit run main.py
```

5. **Abrir no navegador**

O Streamlit abrirá automaticamente (geralmente em [http://localhost:8501](http://localhost:8501)).


## 💡 Observações

* O dataset utilizado foi extraído da plataforma Kaggle (neste [link](https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs?select=ETF+prices.csv)), contendo informações históricas sobre ETFs e Fundos Mútuos dos EUA.

* Projeto desenvolvido para a disciplina **Projeto de Algoritmos (FGA0124)** da **Universidade de Brasília — FCTE**.


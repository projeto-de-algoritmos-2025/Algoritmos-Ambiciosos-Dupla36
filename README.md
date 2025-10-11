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

Desenvolver uma aplicação interativa que analisa e simula estratégias de alocação de investimentos em ETFs, utilizando algoritmos ambiciosos (guloso).

O sistema permite montar carteiras automaticamente a partir de dados reais de desempenho de ETFs, considerando diferentes restrições de otimização, como capital disponível ou limite de risco.

O projeto visa ilustrar a aplicação prática de algoritmos ambiciosos em problemas reais de otimização financeira.


## 🧠 Funcionalidades

A aplicação apresenta duas abas, cada uma implementando uma variação do problema do Knapsack Fracionário:

### 💼 1. Seleção de Carteira por Capital Disponível

> (Inspirado no Fractional Knapsack clássico)

Nesta aba, o algoritmo seleciona automaticamente os ETFs que maximizam o retorno esperado, respeitando o capital total disponível informado pelo investidor.

* O “peso” de cada ETF é o preço unitário (adj_close);
* O “valor” é o retorno médio anual dos últimos 3 anos;
* A eficiência é calculada como a razão entre retorno e risco (ou o produto entre eles, dependendo da prioridade do usuário).
* O investidor pode escolher se deseja priorizar menor risco ou maior retorno.

**Saídas exibidas na tela:**

* Tabela com os ETFs selecionados, preço, retorno, risco e fração alocada;
* Cálculo do capital total investido e retorno estimado da carteira;
* Gráfico de barras mostrando a contribuição de retorno por ativo.

### ⚖️ 2. Seleção de Carteira com Limite de Risco

> Inspirado no Knapsack com restrição de capacidade

Nesta aba, o algoritmo seleciona os ETFs que maximizam o retorno total, respeitando um limite máximo de risco total definido pelo investidor.

* O “peso” é o risco (desvio-padrão em 3 anos);
* O “valor” é o retorno médio anual;
* Os ETFs são escolhidos na ordem de maior eficiência (retorno/risco) até que o risco total atinja o limite.

**Saídas exibidas na tela:**

* Tabela com os ETFs escolhidos e a fração de alocação;
* Exibição do risco total da carteira e retorno estimado;
* Gráfico de barras mostrando a contribuição percentual de cada ativo.

## 🧮 Algoritmos Ambiciosos aplicados

Ambas as estratégias implementam versões do algoritmo ambicioso (guloso), baseadas no problema do Knapsack:

| Versão                 | Restrição               | Característica Principal                                                  |
| ---------------------- | ----------------------  | ------------------------------------------------------------------------- |
| **Capital Disponível** | Capital máximo (em R$)      | Escolhe ativos com melhor retorno relativo até esgotar o capital          |
| **Limite de Risco**    | Risco máximo (%)            | Escolhe ativos com melhor eficiência (retorno/risco) até atingir o limite |

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

* `data/` → contém um dos datasets necessários (ETFs.csv) com as informações dos fundos e ETFs.

   ⚠️ O dataset ETF_prices.csv não está incluído no repositório devido ao tamanho. Baixe-o manualmente em: https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs

* `src/main.py` → script principal do Streamlit que faz a leitura e visualização dos dados.
* `requirements.txt` → dependências necessárias para executar o projeto.

## 🚀 Como Executar

⚠️ **Observação importante:**  

O arquivo `data/ETF_prices.csv` (≈188 MB) não está incluído neste repositório devido ao limite de tamanho do GitHub. Você pode baixá-lo manualmente no [Kaggle](https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs?select=ETF+prices.csv) e colocá-lo dentro da pasta `data/` antes de executar o projeto.

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



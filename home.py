import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Layout para a página Home
def home_layout():
    return dbc.Container([
        html.Br(),
      

dbc.Card([
     dbc.CardHeader(
            html.H1("Bem-vindo ao Painel OncoPed", className="text-center mb-4")
        ),
        dbc.CardBody(
            dcc.Markdown('''
**PainelOncoped** é uma iniciativa voltada para compreender melhor os dados sobre a **oncologia pediátrica** no **Rio Grande do Sul** e no **Brasil**.

Este painel integra dados de diferentes fontes, como:
- **Painel Oncológico do DATASUS**
- **Tabulador do INCA**
- **Sistema de Mortalidade do DATASUS**
- **Complexo Regulador da Prefeitura de Porto Alegre**

A partir dessas bases, foram desenvolvidos **quatro painéis interativos e dinâmicos**, com o objetivo de apoiar **profissionais da saúde** e **gestores públicos** na **tomada de decisões** e no **entendimento da oncologia pediátrica**.

Abaixo você encontra **cards explicativos sobre cada painel**.  
Para navegar entre eles, utilize as **abas** localizadas na parte superior da tela.
                         
**O painelOncoped pode apresentar instabilidade ou travamento. Se isso ocorrer, atualize a página.**
''')
        ),
        ], className="mb-4 shadow"),
        # Seção: Relatório de todos os painéis

        dbc.Card([
            dbc.CardHeader(html.H4("Painel Oncológico Pediátrico (Dados DATASUS)", className="mb-0")),
            dbc.CardBody(dcc.Markdown(r'''
**Visão geral**

Este painel apresenta informações sobre casos de câncer infantil e juvenil extraídos do **DATASUS**, atualizados a cada três meses. O objetivo é fornecer uma visão rápida e dinâmica dos diagnósticos e tratamentos realizados, permitindo comparações por ano, região e características dos pacientes.

**Fonte de dados**
- **Origem:** Sistema de Informações de Saúde do DATASUS (Ministério da Saúde)
- **Atualização:** dados consolidados trimestralmente (a cada 3 meses)
- **Âmbito geográfico:** todo o Brasil, com filtros por região e estado.

**Filtros principais**
1. **Diagnóstico (CID-10)**
2. **Grupo de doenças**
   - Tumores Malignos (CID iniciados em “C”)
   - Tumores Benignos (CID iniciados em “D”)
3. **Anos de diagnóstico/tratamento** (seleção múltipla)
4. **Faixa etária** (“Menos de 1 ano” até 19 anos)
5. **Região e Estado**

**Indicadores de topo**
- **Pacientes Diagnosticados:** Total de crianças e adolescentes que receberam diagnóstico oncológico.
- **Pacientes Iniciaram Tratamento:** Total de pacientes que iniciaram tratamento registrado.

**Serviços habilitados (quando se escolhe um estado)**
- **Proporção de Serviços Habilitados vs Não Habilitados:** Pizza indicando quantos estabelecimentos estão credenciados.
- **Detalhes do Estabelecimento:** Tabela com nome, tipo de habilitação, forma de gestão e número de pacientes atendidos.

**Gráficos de acompanhamento**
- **Pacientes Diagnosticados vs Tratados por Ano**: barras comparando casos diagnosticados vs tratados.
- **Top 10 Doenças diagnosticadas**: donut com 10 CIDs mais frequentes.
- **Top 10 Doenças tratadas**: donut com 10 tratamentos mais comuns.
- **Casos por Diagnóstico e Tempo de Tratamento**: sunburst detalhando faixas de dias até tratamento.
- **Casos por Diagnóstico e Primeiro Tratamento**: sunburst mostrando modalidade de primeiro tratamento.
- **Distribuição do Primeiro Tratamento Registrado**: donut com modalidades de tratamento.
- **Categorias Paralelas: Diagnóstico vs Tempo**: gráfico paralelo relacionando CID e categoria de tempo.

**Como usar**
- Monitore evolução anual, lacunas de habilitação, priorização de intervenções e logística.

**Vantagens**
- Dados atualizados trimestralmente.
- Filtros flexíveis.
- Interface amigável com pop-ups informativos.
- Visão integrada de diagnóstico, tratamento e capacidade de atendimento.
'''))
        ], className="mb-4 shadow"),

        # Painel RHC-INCA
        dbc.Card([
            dbc.CardHeader(html.H4("Painel Oncológico Pediátrico (Dados RHC-INCA)", className="mb-0")),
            dbc.CardBody(dcc.Markdown(r'''
**Visão geral**

O Painel RHC-INCA consolida dados de registros hospitalares do cancer (RHC) do INCA, permitindo explorar o perfil de atendimento de crianças e adolescentes.

**Fonte de dados**
- **Origem:** Registros RHC do INCA.
- **Campos principais:** diagnóstico, tipo histológico, topografia tumoral, histórico familiar, idade, sexo, data da primeira consulta e CNES.

**Filtros disponíveis**
- **Região e Estado:** Norte, Nordeste, Centro-Oeste, Sudeste, Sul ou “Todas”.
- **Estabelecimento (CNES):** selecione um hospital ou “Todos”.
- **Ano da Primeira Consulta:** escolha um ou vários anos.
- **Idade:** “Menos de 1 ano” ou anos completos (1–19).
- **Diagnóstico, Morfologia e Topografia**.
- **Modo Daltonismo:** adapta cores para daltonismo.

**Indicador de topo**
- **Total de Pacientes:** número de registros filtrados.

**Gráficos**
- **Pacientes por Ano:** evolução do número de pacientes.
- **Top 10 Diagnósticos:** donut com 10 tumores mais frequentes.
- **Base para Diagnóstico:** donut mostrando examen confirmatório (“BASMAIMP”).
- **Diagnóstico/Trat. Anteriores:** donut de registros pré-existentes.
- **Histórico Familiar:** donut com proporção de histórico familiar.
- **Estado após 1º Tratamento:** donut do status após primeiro tratamento.
- **Registros por Sexo:** barras comparando por sexo.

**Como usar**
1. Monitorar tendências.
2. Avaliar perfil tumoral.
3. Mapear fatores de risco.
4. Planejar serviços.
5. Ativar modo daltonismo.

**Benefícios**
- Interface intuitiva sem programação.
- Visão abrangente multidimensional.
- Suporte à decisão e acessibilidade.
'''))
        ], className="mb-4 shadow"),

        # Painel Mortalidade SIM
        dbc.Card([
            dbc.CardHeader(html.H4("Painel Mortalidade Oncológica Pediátrica (Dados SIM)", className="mb-0")),
            dbc.CardBody(dcc.Markdown(r'''
**Visão geral**

Este painel exibe registros de óbitos por câncer em crianças/adolescentes (0–19 anos) em todo o Brasil, com detalhamento por estado e municípios do RS.

**Fonte de dados**
- **Origem:** DATASUS – SIM.
- **Atualização:** conforme último processamento.

**Filtros disponíveis**
1. **Estado (UF):** qualquer ou em branco.
2. **Ano do Óbito:** seleção de anos.
3. **Idade do Óbito:** faixas 0 a 19 anos.
4. **Modo Daltonismo:** paletas adaptadas.

**Indicador principal**
- **Quantidade de Óbitos:** total filtrado.

**Gráficos principais**
- **Óbitos por Ano:** barras anuais.
- **Top 10 Causas Básicas de Óbito:** donut com 10 CIDs.
- **Locais de Ocorrência do Óbito:** donut de local.
- **Top 10 Causas por Sexo:** barras por sexo.
- **Mapa de Óbitos por Município (RS):** coroplético se UF=RS.

**Como usar**
- Analisar tendências.
- Identificar causas principais.
- Avaliar distribuição espacial no RS.
- Comparar por gênero.

**Por que é útil**
- Dados oficiais completos e filtráveis.
- Interface acessível.
- Apoio à gestão e cuidado.
'''))
        ], className="mb-4 shadow"),

        # Painel SMSPOA
        dbc.Card([
            dbc.CardHeader(html.H4("Painel Sistemas Regulador SMSPOA", className="mb-0")),
            dbc.CardBody(dcc.Markdown(r'''


## Visão geral

Este painel interativo reúne informações sobre pacientes pediátricos oncológicos atendidos pela Prefeitura de Porto Alegre, extraídas dos sistemas reguladores Gerint (internações hospitalares), Gercon (consultas) e Gerapc (atenção primária), todos mantidos pela Procempa. O objetivo é oferecer, de forma visual e dinâmica, indicadores e gráficos que ajudem a entender o perfil desses atendimentos.

---

## Fonte de dados

* **Origem:** Sitemas do Complexo Regulador
* **Sistemas:**

  * **Gerint:** Gerenciamento de internações hospitalares
  * **Gercon:** Gerenciamento de consultas
  * **Gerapc:** Gestão de atendimentos na atenção primária


---

## Filtros disponíveis

Antes de tudo, você pode refinar a visualização escolhendo:

* **Ano de cadastro** (único ou múltiplos)
* **Idade do paciente** (anos completos)
* **CID principal** (código de classificação de doenças)
* **Unidade executante** (hospital ou ambulatório responsável pelo tratamento)

Esses filtros permitem ver apenas o subconjunto de pacientes que interessam ao seu estudo ou à sua gestão.

---

## Principais indicadores 

1. **Quantidade Total de Pacientes**  
   Número de pacientes únicos após aplicação dos filtros.
2. **Mediana entre Diagnóstico e Tratamento**  
   Tempo central (em dias) entre a data do laudo anatomopatológico e o início do primeiro tratamento oncológico.

   * Para o Hospital de Clínicas, considera dados a partir de 2019  
   * Para demais unidades, considera a partir de 2023
3. **Mediana de Quilômetros Percorridos**  
   Distância mediana (em km) entre a residência do paciente e a unidade onde foi atendido.
4. **Média de Procedimentos Realizados**  
   Quantidade média de procedimentos (exames, terapias, etc.) realizados por paciente no conjunto filtrado.

Cada indicador traz um ícone de informação que explica o cálculo por trás do número.

---

## Principais gráficos

| Gráfico                                           | O que mostra                                                                                                     |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Distribuição de Diagnósticos por CID**          | Pizza (donut) com os 10 CIDs mais frequentes e agrupamento “Outros” para o restante.                             |
| **Distribuição dos Grupos de Procedimentos**      | Barra mostrando quantos procedimentos de cada grupo (quimioterapia, radioterapia etc.) foram realizados.         |
| **Distribuição por Local de Residência**          | Pizza com os 10 municípios de residência mais comuns entre os pacientes.                                         |
| **Origem do Paciente (Protocolo)**                | Pizza que mostra a proporção de entradas pelo Gerint, Gercon, Gerapc ou sem informação.                          |
| **Primeiro Procedimento Registrado (Top 10)**     | Pizza com os 10 primeiros procedimentos feitos por paciente, agrupando o restante como “Outros”.                 |
| **Tempo diagnóstico→tratamento por faixa etária** | Barras com a mediana de dias entre diagnóstico e tratamento, separadas em faixas etárias (0–4, 5–10 etc.).       |
| **Caminho do Paciente (Sankey)**                  | Diagrama de fluxo que ilustra o caminho de cada paciente, desde o protocolo de entrada até a unidade executante. |

Em cada gráfico você também encontra um “i” de informações que, ao clicar, explica brevemente o que está sendo exibido e como interpretar os resultados.

---

## Como usar no dia a dia

1. **Investigar atrasos**  
   * Identifique em quais faixas etárias o tempo entre diagnóstico e tratamento é maior.
2. **Avaliar acesso geográfico**  
   * Veja se há distâncias excessivas que possam impactar o tratamento.
3. **Monitorar carga de procedimentos**  
   * Entenda quantos procedimentos, em média, cada paciente faz, para planejar recursos.
4. **Mapear perfil de diagnósticos**  
   * Ver quais CIDs predominam para orientar treinamento e estoques.

---


Com isso, o painel se torna uma ferramenta ágil para apoiar decisões, identificar gargalos e melhorar o cuidado às crianças e adolescentes com câncer em Porto Alegre.
'''))
        ], className="mb-4 shadow"),

        html.Br(),
    ], fluid=True)

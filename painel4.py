from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import State  # Já que vamos usar States também


# Carregando os dados para o painel
df2 = pd.read_excel("dados/gerpac_agrupado_com_grupos_publico.xlsx")
df2['datacadastro'] = pd.to_datetime(
    df2['datacadastro'],
    errors='coerce'   # valores inválidos viram NaT
)

def criar_filtro_combinado(df):
    idade_min = int(df['idade'].min())
    idade_max = int(df['idade'].max())
    return dbc.Card(
        
        
        dbc.CardBody([
             html.Label("Filtrar por Ano", className="form-label"),
             
           dcc.Dropdown(
                id="ano-filter",
                options=[
                    {'label': ano, 'value': ano}
                    for ano in sorted(
                        df['datacadastro']
                        .dropna()
                        .dt.year
                        .unique()
                    )
                ],
                value=None,
                multi=True,
                placeholder="Selecione o ano",
            ),

            html.Br(),
            html.Label("Filtrar por Idade (anos)", className="form-label"),
            dcc.Dropdown(
                id="idade-filter",
                options=[
                    {'label': str(age), 'value': age}
                    for age in sorted(df['idade'].dropna().unique())
                ],
                value=None,
                multi=True,
                placeholder="Selecione uma ou mais idades",
            ),

            html.Label("Filtrar por CID Principal", className="form-label"),
            dcc.Dropdown(
                id="cidprincipal-filter",
                options=[{'label': cid, 'value': cid} for cid in df['cidprincipal'].dropna().unique()],
                value=None,  # Valor inicial
                multi=True,  # Permitir múltiplos filtros
                placeholder="Selecione um CID",
            ),
            html.Br(),
            html.Label("Selecione o Grupo de Doenças", className="form-label"),
            dcc.Dropdown(
                id="grupo-doencas-filter",
                options=[
                    {"label": "Tumores Malignos (C…)", "value": "malignos"},
                    {"label": "Tumores Benignos (D…)",   "value": "benignos"},
                ],
                value=None,
                multi=False,
                placeholder="Todos os grupos",
            ),
            html.Br(),
            html.Label("Filtrar por Unidade Executante", className="form-label"),
            dcc.Dropdown(
                id="unidadeexecutante-filter",
                options=[{'label': unidade, 'value': unidade} for unidade in df['unidadeexecutantetratamento'].dropna().unique()],
                value=None,  # Valor inicial
                multi=True,  # Permitir múltiplos filtros
                placeholder="Selecione uma Unidade Executante",
            ),
            
            
            
        ]),
        className="mb-4",
    )

# Layout do painel
def painel4_layout():
    return dbc.Container([
        
        
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H1("Painel Sistemas Regulador SMSPOA", className="text-center mb-4"),
                    html.Img(src="assets/iconSMPOA.png", height="150px", className="d-block mx-auto"),
                ]),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Switch(
                        id="daltonismo-switch",
                        label="Modo Daltonismo",
                        value=False,           # estado inicial desligado
                        className="mb-3",
                    )
                ),
                width=3,
                className="mb-4",
            )
        ),
        dbc.Row(
            dbc.Col(criar_filtro_combinado(df2), width=12),
            className="mb-4",
        ),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                   html.Div([
                    html.H5("Quantidade Total de Pacientes",
                            className="card-title d-inline-block"),
                    dbc.Button(
                        html.I(className="bi bi-info-circle"),
                        id="popover-target-total-pacientes",
                        color="link",
                        className="p-0 ms-2",
                        n_clicks=0,
                    ),
                    dbc.Popover(
                        dbc.PopoverBody("Mostra o número total de pacientes após aplicação dos filtros."),
                        target="popover-target-total-pacientes",
                        trigger="click",
                        placement="bottom",
                    ),
                ], className="text-center mb-2"),

                html.H2(id="total-pacientes", className="text-center")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H5("Mediana entre Diagnóstico e Tratamento",
                                className="card-title d-inline-block"),
                        dbc.Button(html.I(className="bi bi-info-circle"),
                            id="popover-target-mediana-tempo",
                            color="link", className="p-0 ms-2"),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Exibe a mediana (dias) entre a data do anatomopatológico e o primeiro tratamento Oncologico,\nPara calcular a mediana, foram considerados apenas os pacientes com data de diagnóstico e data de tratamento disponíveis, \npara o Hospital de Clinicas de Porto Alegre foi considerado todos os pacientes apartir de 2019, para os demais apenas 2023, ano que iniciou a a implementação do Gerpac."
                            ),
                            target="popover-target-mediana-tempo",
                            trigger="click",
                            placement="bottom",
                        ),
                    ], className="text-center mb-2"),
                    html.H2(id="media-tempo", className="text-center")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                   html.Div([
                        html.H5("Mediana da distância(em KM) Percorridos pelos Pacientes",
                                className="card-title d-inline-block"),
                        dbc.Button(html.I(className="bi bi-info-circle"),
                            id="popover-target-mediana-km",
                            color="link", className="p-0 ms-2"),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Mostra a mediana da distância(em km) entre a residência e o local de atendimento,\ncalculado atraves da longitue latitude do hospital e do município residência do Paciente."
                            ),
                            target="popover-target-mediana-km",
                            trigger="click",
                            placement="bottom",
                        ),
                    ], className="text-center mb-2"),
                    html.H2(id="media-km", className="text-center")
                ])
            ]), width=3),

             dbc.Col(dbc.Card([
                dbc.CardBody([
                     html.H5("Média de Procedimentos Realizados",
                                className="card-title d-inline-block"),
                        dbc.Button(html.I(className="bi bi-info-circle"),
                            id="popover-target-media-procedimentos",
                            color="link", className="p-0 ms-2"),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Calcula a média de procedimentos realizados por paciente no conjunto filtrado."
                            ),
                            target="popover-target-media-procedimentos",
                            trigger="click",
                            placement="bottom",
                        ),
                    ], className="text-center mb-2"),
                    html.H2(id="media-procedimentos", className="text-center")
    
            ]), width=3),   
        ], className="mb-4"),
       
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Distribuição de Diagnósticos por CID"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-donut-info",
                            color="link",
                            className="p-0 ms-2",
                            n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Esse gráfico mostra a distribuição dos principais CID após aplicação dos filtros.'Outros' agrupa os CIDs restante."),
                            target="popover-donut-info",
                            trigger="click",
                            placement="bottom",
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-donut", config={'responsive': True},style={'height': '500px'}))
            ]), width=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Distribuição dos Grupos de Procedimentos Realizados"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-barras2-info",
                            color="link",
                            className="p-0 ms-2",
                            n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Detalha quantos procedimentos de cada grupo foram realizados."),
                            target="popover-barras2-info",
                            trigger="click",
                            placement="bottom",
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-barras2"))
            ]), width=6),
        ], className="mb-4"),
     
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Origem do Paciente"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-protocolo-info",
                            color="link", className="p-0 ms-2", n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Exibe a proporção de pacientes segundo o protocolo de entrada (GERINT, GERCON, etc)."),
                            target="popover-protocolo-info", trigger="click", placement="bottom"
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-pizza-protocolo"))
            ]), width=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Distribuição por Local de Residência"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-local-info",
                            color="link", className="p-0 ms-2", n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Mostra os 10 municípios de residência dos pacientes no conjunto filtrado."),
                            target="popover-local-info", trigger="click", placement="bottom"
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-local-residencia"))
            ]), width=6),
        ], className="mb-4"),

       dbc.Row([
            # Coluna 1: Primeiro Procedimento
            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Primeiro Procedimento Registrado (Top 10)"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-proc1-info",
                            color="link",
                            className="p-0 ms-2",
                            n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Top 10 dos primeiros procedimentos feitos por paciente."),
                            target="popover-proc1-info",
                            trigger="click",
                            placement="bottom"
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-pizza-procedimento1"))
            ]), width=6),

            # Coluna 2: Tempo diagnóstico→tratamento por faixa etária
            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Tempo diagnóstico-tratamento por faixa etária"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-idade-tempo-info",
                            color="link",
                            className="p-0 ms-2",
                            n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Mostra a mediana do número de dias entre a data do diagnóstico e o início do tratamento, agrupada por faixas etárias (0–4, 5–10, 11–15, 16–19 anos)."
                            ),
                            target="popover-idade-tempo-info",
                            trigger="click",
                            placement="bottom"
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody(dcc.Graph(id="grafico-idade-tempo"))
            ]), width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Caminho do Paciente"),
                        dbc.Button(
                            html.I(className="bi bi-info-circle"),
                            id="popover-sankey-info",
                            color="link", className="p-0 ms-2", n_clicks=0
                        ),
                        dbc.Popover(
                            dbc.PopoverBody("Representa o fluxo do paciente desde a origem até a unidade executante."),
                            target="popover-sankey-info", trigger="click", placement="bottom"
                        )
                    ], className="d-flex align-items-center justify-content-between")
                ),
                dbc.CardBody([
                    dcc.Graph(id="grafico-sankey"),
                    html.P(
                        "GERINT é Gerenciamento de internações hospitalares e GERCON é Gerenciamento de consultas",
                        className="mt-2"
                    )
                ])
            ]), width=12),
        ], className="mb-4"),
        # Toast flutuante com resumo dos filtros
        html.Div([
            dbc.Toast(
                id="filtro-toast",
                header="Filtros Ativos",
                children="Nenhum filtro aplicado",
                icon="info",
                is_open=True,  # Visível por padrão
                dismissable=False,  # Não pode ser fechado manualmente (só pelo botão flutuante)
                style={"position": "fixed", "bottom": "100px", "right": "30px", "width": 300, "zIndex": 9999},
            ),
            html.Div([
                dbc.Button("Filtros Ativos", id="toggle-toast", color="primary", className="btn-float"),
            ], style={"position": "fixed", "bottom": "30px", "right": "30px", "zIndex": 9999})
        ])

       
    ], fluid=True)

# Callback para atualizar os gráficos e informativos

def painel4_callbacks(app):
     # Callback para alternar a visibilidade do Toast
    @app.callback(
        Output("filtro-toast", "is_open"),
        Input("toggle-toast", "n_clicks"),
        State("filtro-toast", "is_open"),
        prevent_initial_call=True
    )
    def toggle_toast(n_clicks, is_open):
        return not is_open

    # Callback para atualizar o conteúdo do Toast com os filtros aplicados
    @app.callback(
        Output("filtro-toast", "children"),
        Input("grupo-doencas-filter",        "value"),
        Input("ano-filter",                  "value"),
        Input("idade-filter",                "value"),
        Input("cidprincipal-filter",         "value"),
        Input("unidadeexecutante-filter",    "value"),
    )
    def atualizar_conteudo_toast(grupo, ano, idade, cid, unidade):
        # 1) Texto para o grupo
        if grupo == "malignos":
            grupo_texto = "Grupo: Tumores Malignos"
        elif grupo == "benignos":
            grupo_texto = "Grupo: Tumores Benignos"
        else:
            grupo_texto = "Grupo: Todos"

        # 2) Os outros já estavam corretos
        ano_texto      = f"Ano(s): {', '.join(map(str, ano))}"         if ano     else "Ano(s): Todos"
        idade_texto    = f"Idade(s): {', '.join(map(str, idade))}"    if idade   else "Idade(s): Todas"
        cid_texto      = f"CID(s): {', '.join(cid)}"                  if cid     else "CID(s): Todos"
        unidade_texto  = f"Unidade(s): {', '.join(unidade)}"          if unidade else "Unidade(s): Todas"

        return html.Ul([
            html.Li(grupo_texto),
            html.Li(ano_texto),
            html.Li(idade_texto),
            html.Li(cid_texto),
            html.Li(unidade_texto)
        ])
       

    @app.callback(
        [
            Output("cidprincipal-filter", "options"),
            Output("unidadeexecutante-filter", "options"),
           
        ],
        [
            Input("ano-filter", "value"),
        ]
    )
    
    def atualizar_opcoes_filtros(ano_filter):
        df_filtered = df2.copy()
        
        if ano_filter:
            df_filtered = df_filtered[df_filtered['datacadastro'].dt.year.isin(ano_filter)]

        cid_options = [{'label': cid, 'value': cid} for cid in df_filtered['cidprincipal'].dropna().unique()]
        unidade_options = [{'label': unidade, 'value': unidade} for unidade in df_filtered['unidadeexecutantetratamento'].dropna().unique()]

        return cid_options, unidade_options
    @app.callback(
        [
            Output("grafico-donut", "figure"),
            Output("grafico-barras2", "figure"),
            Output("grafico-local-residencia", "figure"),
            Output("grafico-pizza-protocolo", "figure"),
            Output("grafico-pizza-procedimento1", "figure"),
            Output("grafico-idade-tempo", "figure"),
            Output("grafico-sankey", "figure"), 
            # Informativos
            Output("total-pacientes", "children"),
            Output("media-tempo", "children"),
            Output("media-km", "children"),
            Output("media-procedimentos", "children"),  
        ],
        [
            Input("grupo-doencas-filter",       "value"),
            Input("ano-filter",                  "value"),
            Input("idade-filter",                "value"),
            Input("cidprincipal-filter",         "value"),
            Input("unidadeexecutante-filter",    "value"),
            Input("daltonismo-switch",           "value"),
        ],
    )
    def atualizar_graficos(grupo,ano_filter,idade_filter,cidprincipal_filter, unidadeexecutante_filter,daltonismo):
        # Filtrar o dataframe por CID Principal
        df_filtered = df2
        if cidprincipal_filter:
            df_filtered = df_filtered[df_filtered['cidprincipal'].isin(cidprincipal_filter)]
        if unidadeexecutante_filter:
            df_filtered = df_filtered[df_filtered['unidadeexecutantetratamento'].isin(unidadeexecutante_filter)]
        if ano_filter :
            df_filtered = df_filtered[df_filtered['datacadastro'].dt.year.isin(ano_filter)]
        if idade_filter:
            df_filtered = df_filtered[df_filtered['idade'].isin(idade_filter)]
        # Calcular a média de procedimentos
        media_procedimentos = round(df_filtered['totalprocedimentos'].mean(), 2)

        df_filtered['tipoprotocoloorigem'] = df_filtered['tipoprotocoloorigem'].replace('[NULL]', "Sem informação").fillna("Sem informação")

    
        # Gráfico de Donut (CID Principal)
        top_cids = df_filtered['cidprincipal'].value_counts().head(10).index
        df_top_cids = df_filtered[df_filtered['cidprincipal'].isin(top_cids)]
        
        # Criar o grupo "Outros"
        df_outros_cids = df_filtered[~df_filtered['cidprincipal'].isin(top_cids)]
        df_outros_cids = pd.DataFrame({'cidprincipal': ['Outros'], 'count': [len(df_outros_cids)]})
        df_top_cids_count = df_top_cids['cidprincipal'].value_counts().reset_index()
        df_top_cids_count.columns = ['cidprincipal', 'count']
        
        # Usar pd.concat para adicionar o grupo "Outros"
        df_top_cids_count = pd.concat([df_top_cids_count, df_outros_cids], ignore_index=True)
        
        palette = px.colors.qualitative.Safe if daltonismo else None
        # Calcular a porcentagem
        total_cids = len(df_filtered)
        df_top_cids_count['percent'] = (df_top_cids_count['count'] / total_cids) * 100
        
        if grupo == "malignos":
            df_filtered = df_filtered[
                df_filtered['cidprincipal']
                        .str.upper()
                        .str.startswith('C', na=False)
        ]
        elif grupo == "benignos":
            df_filtered = df_filtered[
                df_filtered['cidprincipal']
                        .str.upper()
                        .str.startswith('D', na=False)
            ]

        # 2) Aplique seus outros filtros (CID, ano, idade, unidade) normalmente…
        if cidprincipal_filter:
            df_filtered = df_filtered[df_filtered['cidprincipal'].isin(cidprincipal_filter)]

        
        fig_donut = px.pie(
            df_top_cids_count, 
            names='cidprincipal', 
            values='count', 
            hole=0.5, 
            title=f"Total: {total_cids} Diagnósticos por CID Principal",
            labels={'cidprincipal': 'CID Principal'},
            hover_data=['count', 'percent'],
            color='cidprincipal',
            color_discrete_map={
                'Outros': 'lightgray',  # Cor para o grupo "Outros"
            },
            color_discrete_sequence=palette, 
        )
        fig_donut.update_layout(
            legend=dict(
            orientation="h",
            y=-0.2,           # empurra para baixo do gráfico
            x=0.5,
            xanchor="center"
        ),
    margin=dict(t=40, b=80))
                
        # Gráfico de Barras
        fig_barras_Grupo = px.bar(df_filtered, x='grupoprocedimento',color_discrete_sequence=palette, )

        # Gráfico de Donut (Local de Residência - Top 10)
        top_municipios = df_filtered['municipioresidencia'].value_counts().head(10).index
        df_top_municipios = df_filtered[df_filtered['municipioresidencia'].isin(top_municipios)]
        fig_local_residencia = px.pie(
            df_top_municipios,
            names='municipioresidencia',
            hole=0.3,
            color_discrete_sequence=palette, 
        )
        fig_local_residencia.update_traces(textinfo="label+percent+value" )

        # Gráfico de Pizza (Tipo de Protocolo de Origem)
        fig_pizza_protocolo = px.pie(
            df_filtered,
            names='tipoprotocoloorigem',
            
            color='tipoprotocoloorigem',
            color_discrete_map={
                'GERINT': 'lightgreen',  # Vermelho pastel
                'GERCON': 'lightblue',  # Azul pastel
            },color_discrete_sequence=palette, 
        )
        
        df_proc1_count = (
            df_filtered
            .groupby('DescricaoProcedimento1')
            .size()
            .reset_index(name='count')
            .rename(columns={'DescricaoProcedimento1': 'descricao'})
        )

        # 2) Pega Top-10 e agrupa o restante em "Outros"
        top_n = 10
        df_top = df_proc1_count.nlargest(top_n, 'count').copy()
        others = df_proc1_count['count'].sum() - df_top['count'].sum()

        # substitua df_top.append(...) por concat:
        df_top = pd.concat([
            df_top,
            pd.DataFrame([{'descricao': 'Outros', 'count': others}])
        ], ignore_index=True)

        # 3) Cria legenda curta (até 10 chars + '…')
        df_top['legenda_curta'] = (
            df_top['descricao']
            .str.slice(0, 50)
            .str.rstrip()
            + df_top['descricao'].str.len().gt(20).map({True: '…', False: ''})
        )

        # 4) Desenha o pie usando a legenda curta
        fig_pizza_proc1 = px.pie(
            df_top,
            names='legenda_curta',
            values='count',
            hole=0.3,
            labels={'legenda_curta': 'Procedimento'},
            color_discrete_sequence=palette, 
        )

        # 5) Ajustes de layout
        fig_pizza_proc1.update_traces(textinfo='percent+value')
        fig_pizza_proc1.update_layout(
            legend=dict(title='Procedimento', font=dict(size=10)),
            margin=dict(t=40, b=40, l=20, r=20)
        )
        # Gráfico de Barras (Tempo entre Diagnóstico e Tratamento por Faixa Etária)
        bins = [0, 5, 11, 16, 20]
        labels = ["0-4", "5-10", "11-15", "16-19"]
        df_filtered['faixa_idade'] = pd.cut(
            df_filtered['idade'],
            bins=bins,
            labels=labels,
            right=False
        )
        # Agrupa e calcula mediana de tempoDiasDiagTrat_grafico
        df_age = (
            df_filtered
            .dropna(subset=['faixa_idade', 'tempoDiasDiagTrat_grafico'])
            .groupby('faixa_idade')['tempoDiasDiagTrat_grafico']
            .median()
            .reset_index()
        )
        fig_idade_tempo = px.bar(
            df_age,
            x='faixa_idade',
            y='tempoDiasDiagTrat_grafico',
            labels={
                'faixa_idade': 'Faixa etária (anos)',
                'tempoDiasDiagTrat_grafico': 'Mediana (dias)'
            },
            color_discrete_sequence=palette, 
        )

        ### fig caminho paciente ####
        
            # 1) Cria lista de todos os nós (origem, subgrupos e unidade)
        # 1) Liste dinamicamente todas as colunas de “DescricaoProcedimentoX”
        proc_cols = [c for c in df_filtered.columns if c.startswith('grupoDescricaoProcedimento')]

        # 2) Monte todos os rótulos e o mapping
       

       
        all_labels = pd.unique(
            df_filtered[
                ['tipoprotocoloorigem'] + proc_cols + ['unidadeexecutantetratamento']
            ].values.ravel()
        )
        all_labels = [lbl for lbl in all_labels if pd.notna(lbl)]
        short_labels = [
            lbl if len(lbl) <= 25 else lbl[:25].rstrip() + '…'
            for lbl in all_labels
        ]
        mapping_dict = {lbl: i for i, lbl in enumerate(all_labels)}

        # 3) Construa os links sem repetições por paciente
        links_list = []
        for _, row in df_filtered.iterrows():
            origem = row['tipoprotocoloorigem']
            unidade = row['hospital_base']
            seen = set()
            passos = []
            for col in proc_cols:
                val = row.get(col)
                if pd.notna(val) and val not in seen:
                    seen.add(val)
                    passos.append(val)
            sequence = [origem] + passos + [unidade]
            for src, tgt in zip(sequence, sequence[1:]):
                links_list.append({'source': src, 'target': tgt})

        # 4) Agregue ocorrências
        links_df = (
            pd.DataFrame(links_list)
            .groupby(['source','target'])
            .size()
            .reset_index(name='value')
        )

        # 5) Mapeie para índices
        link_sources = links_df['source'].map(mapping_dict)
        link_targets = links_df['target'].map(mapping_dict)
        link_values  = links_df['value']

        palette = px.colors.qualitative.Safe if daltonismo else px.colors.qualitative.Plotly
        node_colors = [ palette[i % len(palette)] for i in range(len(short_labels)) ]

        # 6) Crie o Sankey com cores padrão
        fig_sankey = go.Figure(go.Sankey(
           node=dict(
                pad=15,
                thickness=20,
                label=short_labels,
                color=node_colors, 
            ),
            link=dict(
                source=link_sources,
                target=link_targets,
                value=link_values
            ),
        ))


        


       

        # Informativos
        total_pacientes = len(df_filtered)
        mediana_tempo = df_filtered['tempoDiasDiagTrat_grafico'].median()
        mediaana_km = int(df_filtered['distancia_km'].median()) if not df_filtered['distancia_km'].isna().all() else 0

        return fig_donut, fig_barras_Grupo,  fig_local_residencia, fig_pizza_protocolo,fig_pizza_proc1,fig_idade_tempo, fig_sankey, total_pacientes, f"{mediana_tempo:.2f} dias", f"{mediaana_km} km",f"{media_procedimentos}"


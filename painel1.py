from dash import dcc,dash_table, html, Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import locale

# Configurar o locale para formato brasileiro
try:
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
except locale.Error:
    # fallback para C ou pt_BR sem encoding
    locale.setlocale(locale.LC_ALL, "")

# Carregando os dados para o painel
df1 = pd.read_csv("dados/painel oncologico Datasus/painel_Final_.csv")  # Substitua pelo caminho correto do seu CSV

# Ordenar os diagnósticos do C00 ao D48
df1 = df1.sort_values(
    by="DIAG_DETH", 
    key=lambda col: col.str.extract(r'(\d+)')[0].astype(int), 
    ignore_index=True
)

# Filtros de Idade
idades_disponiveis = list(range(20))

# Substituir a opção "0 anos" por "Menos de 1 ano" para exibição
idades_disponiveis_display = ['Menos de 1 ano'] + \
    [str(i) for i in idades_disponiveis[1:]]

def criar_botao_flutuante():
    return html.Div([
        dbc.Button(
            "Filtros Ativos",
            id="btn-filtros",
            color="primary",
            className="btn-float",
            n_clicks=0
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader("Filtros Ativos", style={"font-weight": "bold"}),
                dbc.PopoverBody(id="popover-filtros-conteudo"),
            ],
            target="btn-filtros",
            trigger="legacy",   # legacy faz toggle no clique E fecha ao clicar fora
            placement="top",
        ),
    ], style={"position": "fixed", "bottom": "20px", "right": "20px", "zIndex": 1000})



def criar_filtros(df):
    grupos = []
    for diag in df["DIAG_DETH"].unique():
        if str(diag).startswith("C"):
            grupos.append("Tumores Malignos")
        elif str(diag).startswith("D"):
            grupos.append("Tumores Benignos")
    grupos = list(set(grupos))

    # Lista de anos disponíveis no dataset
    anos = sorted(df["ANO_DIAGN"].unique())
    
    # Lista de estados únicos
    estados_unicos = sorted(df["UF_DIAGN"].unique())

    return dbc.Card([
        dbc.CardHeader(html.H4("Filtros", className="card-title", style={"text-align": "center"})),
        dbc.Row([
            dbc.Col([
                html.Label("Selecione o Diagnóstico:"),
                dcc.Dropdown(
                    id="diagnostico-filter",
                    options=[{"label": diag, "value": diag} for diag in df["DIAG_DETH"].unique()] + [{"label": "Todos", "value": "Todos"}],
                    value="Todos",
                )
            ], md=6),
           dbc.Col([
                html.Label("Selecione o Grupo de Doenças:"),
                dcc.Dropdown(
                    id="grupo-filter",
                    options=[{"label": "Todos os Grupos", "value": "Todos"}] + 
                            [{"label": grupo, "value": grupo} for grupo in grupos],
                    value="Todos",  # Valor padrão atualizado
                )
            ], md=6),
            dbc.Col([
                html.Label("Selecione os Anos:"),
                dcc.Dropdown(
                    id="ano-filter",
                    options=[{"label": str(ano), "value": ano} for ano in anos],
                    value=anos,  # Valor inicial sendo todos os anos
                    multi=True,  # Permite múltiplas seleções
                )
            ], md=12, style={"margin-top": "20px"}),
            dbc.Col([
                html.Label("Selecione a Idade:"),
                dcc.Dropdown(
                    id="idade-filter",
                    options=[{"label": idade, "value": idade} for idade in idades_disponiveis_display],
                    value=idades_disponiveis_display,  # Valor inicial sendo todas as idades
                    multi=True,  # Permite múltiplas seleções
                )
            ], md=12, style={"margin-top": "20px"}),
            dbc.Col([
                html.Label("Selecione a Região:"),
                dcc.Dropdown(
                    id="regiao-filter",
                    options=[
                        {"label": "Todas", "value": "Todas"},
                        {"label": "Norte", "value": "Norte"},
                        {"label": "Nordeste", "value": "Nordeste"},
                        {"label": "Centro-Oeste", "value": "Centro-Oeste"},
                        {"label": "Sudeste", "value": "Sudeste"},
                        {"label": "Sul", "value": "Sul"}
                    ],
                    value="Todas"
                )
            ], md=6,style={"margin-top": "20px"}),
            dbc.Col([
                html.Label("Selecione o Estado:"),
                dcc.Dropdown(
                    id="estado-filter",
                    options=[{"label": estado, "value": estado} for estado in estados_unicos] + [{"label": "Todos", "value": "Todos"}],
                    value="Todos"
                )
            ], md=6,style={"margin-top": "20px"}),
        ], style={"margin-bottom": "20px", "margin-top": "20px", "margin-left":"20px", "margin-right":"20px"})
    ])

# Layout do Painel 1
def painel1_layout():
    return html.Div([
        html.Div([
            html.H1("Painel Oncológico Pediátrico (Dados DATASUS)", style={'marginRight': '20px'}),
            html.Img(src="assets/logodatasus.png", style={'height': '150px'})
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'flexWrap': 'wrap',
            'marginBottom': '20px'
        }),

        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Switch(
                        id="switch-daltonismo",
                        label="Modo Daltonismo",
                        value=False,           # estado inicial desligado
                        className="mb-3",
                    )
                ),
                width=3,
                className="mb-4",
            )
        ),

        criar_filtros(df1),
        criar_botao_flutuante(),

        # Totais de pacientes
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Pacientes Diagnosticados", style={"text-align": "center"}),
                    html.Div(id="pacientes-diagnosticados", style={"text-align": "center", "font-size": "20px"}),
                ], style={"padding": "10px"}),
                xs=12, sm=12, md=6
            ),
            dbc.Col(
                html.Div([
                    html.H5("Pacientes Iniciaram Tratamento", style={"text-align": "center"}),
                    html.Div(id="pacientes-tratados", style={"text-align": "center", "font-size": "20px"}),
                ], style={"padding": "10px"}),
                xs=12, sm=12, md=6
            ),
        ], style={"margin-top": "20px"}),
        # 1) Collapse de Estabelecimentos
dbc.Collapse(
    id="collapse-estabs",
    is_open=False,
    children=[
        dbc.Row([
            # 1.1) Serviços Habilitados vs Não Habilitados
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Serviços Habilitados vs Não Habilitados", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                   id="info-grafico-habilitacao",
                                   style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Gráfico de pizza mostrando a proporção de serviços habilitados e não habilitados em oncologia pediátrica para o estado selecionado.",
                                target="info-grafico-habilitacao",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(id="grafico-habilitacao", config={'responsive': True})
                    )
                ]),
                xs=12, sm=12, md=6, style={"padding": "10px"}
            ),
            # 1.2) Detalhes do Estabelecimento
            dbc.Col(
                dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.Span("Detalhes do Estabelecimento", className="me-2"),
                                    html.I(className="bi bi-info-circle",
                                        id="info-tabela-estabelecimento",
                                        style={"cursor": "pointer", "fontSize": "1.2rem"}),
                                    dbc.Tooltip(
                                        "Tabela com informações de habilitação, gestão e quantidade de pacientes por estabelecimento.",
                                        target="info-tabela-estabelecimento",
                                        placement="top",
                                        style={"fontSize": "0.9rem"}
                                    ),
                                ], className="d-flex justify-content-center align-items-center")
                            ),
                            dbc.CardBody(
                                dash_table.DataTable(
                                    id="tabela-estabelecimento",
                                    columns=[{"name": c, "id": c} for c in ["Estabelecimento", "Habilitação", "Gestão", "Pacientes"]],
                                    data=[],
                                    style_table={"overflowX": "auto"},
                                    page_size=10
                                )
                            )
                        ]),
                        xs=12, sm=12, md=6, style={"padding": "10px"}
                    ),
                ])
            ]
        ),

        # 2) Pacientes Diagnosticados vs Tratados por Ano
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Pacientes Diagnosticados vs Tratados por Ano", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-barras",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Este gráfico compara o número de pacientes diagnosticados e tratados em cada ano.",
                                target="info-grafico-barras",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-barras",
                            config={'responsive': True},
                            style={'height': '500px'}
                        )
                    )
                ], color="light", outline=True),
                md=12
            ),
        ], style={"margin-bottom": "20px"}),

        # 3) 10 Doenças diagnosticadas
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("10 Doenças diagnosticadas", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-diagnosticos",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Gráfico de pizza dos 10 diagnósticos mais frequentes; 'Outros' agrupa o restante dos diagnósticos.",
                                target="info-grafico-diagnosticos",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-diagnosticos",
                            config={'responsive': True},
                            style={'height': '600px'}   # de
                        )

                    ),
                ]),
                xs=12, sm=12, md=6,
                style={"padding": "10px"}
            ),
            # 4) 10 Doenças tratadas
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("10 Doenças tratadas", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-tratamentos",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Gráfico de pizza dos 10 tratamentos mais frequentes; 'Outros' agrupa os CIDs restante.",
                                target="info-grafico-tratamentos",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-tratamentos",
                            config={'responsive': True},
                            style={'height': '600px'}   # de
                        )

                    ),
                ]),
                xs=12, sm=12, md=6,
                style={"padding": "10px"}
            ),
        ], style={"margin-bottom": "20px"}),

        # 5) Sunburst – Tempo de Tratamento
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Casos por Diagnóstico e Tempo de Tratamento (Top 10)", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-sunburst1",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Sunburst mostrando, para os 10 diagnósticos mais frequentes, a distribuição de tempo até o tratamento em faixas de dias.",
                                target="info-grafico-sunburst1",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-sunburst1",
                            config={'responsive': True},
                            style={'height': '500px'}
                        )
                    ),
                ]),
                xs=12, sm=12, md=6,
                style={"padding": "10px"}
            ),
            # 6) Sunburst – Primeiro Tratamento
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Casos por Diagnóstico e Primeiro Tratamento (Top 10)", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-sunburst2",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Sunburst mostrando, para os 10 diagnósticos mais frequentes, o primeiro tratamento registrado.",
                                target="info-grafico-sunburst2",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-sunburst2",
                            config={'responsive': True},
                            style={'height': '500px'}
                        )
                    ),
                ]),
                xs=12, sm=12, md=6,
                style={"padding": "10px"}
            ),
        ], style={"margin-bottom": "20px"}),

        # 7) Distribuição do Primeiro Tratamento Registrado
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Distribuição do Primeiro Tratamento Registrado", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-modalidade",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Gráfico de pizza com a distribuição das modalidades de tratamento seguidas pelos pacientes.",
                                target="info-grafico-modalidade",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-modalidade",
                            config={'responsive': True},
                            style={'height': '500px'}
                        )
                    ),
                ]),
                xs=12, sm=12, md=6,
                style={"padding": "10px"}
            ),
        ], style={"margin-bottom": "20px"}),

        # 8) Gráfico de Categorias Paralelas
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Categorias Paralelas: Diagnóstico vs Tempo até Tratamento", className="me-2"),
                            html.I(className="bi bi-info-circle",
                                id="info-grafico-parallel",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}),
                            dbc.Tooltip(
                                "Gráfico de categorias paralelas comparando diagnóstico (3 chars) e faixas de tempo até o tratamento.",
                                target="info-grafico-parallel",
                                placement="top",
                                style={"fontSize": "0.9rem"}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="grafico-parallel",
                            config={'responsive': True},
                            style={'height': '500px'}
                        )
                    ),
                ]),
                xs=12, sm=12, md=12,
                style={"padding": "10px"}
            ),
        ]),
        
    ])




regioes_estados = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MS", "MT"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"]
}

# Função para retornar os estados de uma região
def get_estados_por_regiao(regiao):
    return regioes_estados.get(regiao, sorted(df1["UF_DIAGN"].unique()))

# Função para retornar diagnósticos por grupo
def get_diagnosticos_por_grupo(grupo):
    if grupo == "Tumores Malignos":
        return sorted(df1[df1["DIAG_DETH"].str.startswith("C")]["DIAG_DETH"].unique())
    elif grupo == "Tumores Benignos":
        return sorted(df1[df1["DIAG_DETH"].str.startswith("D")]["DIAG_DETH"].unique())
    else:
        return sorted(df1["DIAG_DETH"].unique())

# Callback para atualizar os filtros de estado e diagnóstico dinamicamente
def painel1_callbacks(app):

    @app.callback(
        Output("collapse-estabs", "is_open"),
        Input("estado-filter", "value")
    )
    def mostrar_estabs(estado):
        # abre o collapse apenas se um estado específico foi selecionado
        return estado != "Todos"

    @app.callback(
        Output("estado-filter", "options"),
        Input("regiao-filter", "value")
    )
    def atualizar_estados(regiao):
        estados = get_estados_por_regiao(regiao)
        return [{"label": estado, "value": estado} for estado in estados] + [{"label": "Todos", "value": "Todos"}]

    @app.callback(
        Output("diagnostico-filter", "options"),
        Input("grupo-filter", "value")
    )
    def atualizar_diagnosticos(grupo):
        diagnosticos = get_diagnosticos_por_grupo(grupo)
        return [{"label": diag, "value": diag} for diag in diagnosticos] + [{"label": "Todos", "value": "Todos"}]

    @app.callback(
        Output("grupo-filter", "value"),
        Input("diagnostico-filter", "value")
    )
    def atualizar_grupo(diagnostico):
        if diagnostico.startswith("C"):
            return "Tumores Malignos"
        elif diagnostico.startswith("D"):
            return "Tumores Benignos"
        else:
            return "Todos os Grupos"
    
    @app.callback(
        Output("popover-filtros", "is_open"),
        Input("btn-filtros", "n_clicks"),
        State("popover-filtros", "is_open")
    )
    def toggle_popover(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
   

    # Callback para atualizar o conteúdo do popover com os filtros ativos
    @app.callback(
        Output("popover-filtros-conteudo", "children"),
        [
            Input("regiao-filter", "value"),
            Input("estado-filter", "value"),
            Input("diagnostico-filter", "value"),
            Input("grupo-filter", "value"),
            Input("ano-filter", "value"),
            Input("idade-filter", "value"),
        ]
    )
    def atualizar_filtros_ativos(regiao, estado, diagnostico, grupo, anos, idades):
        # Montar a lista de filtros
        filtros = [
            f"Região: {regiao}" if regiao != "Todas" else "Região: Todas",
            f"Estado: {estado}" if estado != "Todos" else "Estado: Todos",
            f"Diagnóstico: {diagnostico}" if diagnostico != "Todos" else "Diagnóstico: Todos",
            f"Grupo: {grupo}" if grupo != "Todos os Grupos" else "Grupo: Todos os Grupos",
            f"Anos: {', '.join(map(str, anos))}" if anos else "Anos: Todos",
            f"Idades: {', '.join(map(str, idades))}" if idades else "Idades: Todas"
        ]
        return html.Ul([html.Li(f) for f in filtros])
    @app.callback(
        [
            
            Output("grafico-barras", "figure"),
            Output("grafico-habilitacao", "figure"),
            Output("tabela-estabelecimento", "data"),
            Output("pacientes-diagnosticados", "children"),
            Output("pacientes-tratados", "children"),
            Output("grafico-diagnosticos", "figure"),
            Output("grafico-tratamentos", "figure"),
            Output("grafico-sunburst1", "figure"),
            Output("grafico-sunburst2", "figure"),
            Output("grafico-modalidade", "figure"),
            Output("grafico-parallel", "figure")
        ],
        [
            Input("switch-daltonismo", "value"), 
            Input("regiao-filter", "value"),
            Input("estado-filter", "value"),
            Input("diagnostico-filter", "value"),
            Input("grupo-filter", "value"),
            Input("ano-filter", "value"),
            Input("idade-filter", "value"),
        ]
    )
    def atualizar_graficos(daltonismo,regiao, estado, diagnostico, grupo, anos_selecionados, idades_selecionadas):
        
        # Criar cópias para filtragem separada
        diagnosticados_df = df1.copy()
        tratados_df = df1.copy()
        if daltonismo:
            cat_palette = px.colors.qualitative.Plotly    # paleta categórica
            seq_palette = px.colors.sequential.Viridis        # paleta sequencial
            bar_colors  = [cat_palette[0], cat_palette[1]]
        else:
            cat_palette = px.colors.qualitative.Alphabet
            seq_palette = px.colors.sequential.Plasma
            bar_colors  = ['lightblue', 'salmon']
        
        # Aplicar filtro por região
        # Filtrar por Região
        if regiao and regiao != "Todas":
            estados = get_estados_por_regiao(regiao)
            diagnosticados_df = diagnosticados_df[diagnosticados_df["UF_DIAGN"].isin(estados)]
            tratados_df = tratados_df[tratados_df["UF_TRATAM"].isin(estados)]


        # Filtrar por Estado
        if estado and estado != "Todos":
            diagnosticados_df = diagnosticados_df[diagnosticados_df["UF_DIAGN"] == estado]
            tratados_df = tratados_df[tratados_df["UF_TRATAM"] == estado]

        # Filtrar por Grupo
        if grupo == "Tumores Malignos":
            diagnosticados_df = diagnosticados_df[diagnosticados_df["DIAG_DETH"].str.startswith("C")]
            tratados_df = tratados_df[tratados_df["DIAG_DETH"].str.startswith("C")]
        elif grupo == "Tumores Benignos":
            diagnosticados_df = diagnosticados_df[diagnosticados_df["DIAG_DETH"].str.startswith("D")]
            tratados_df = tratados_df[tratados_df["DIAG_DETH"].str.startswith("D")]

        # Filtrar por Diagnóstico
        if diagnostico and diagnostico != "Todos":
            diagnosticados_df = diagnosticados_df[diagnosticados_df["DIAG_DETH"] == diagnostico]
            tratados_df = tratados_df[tratados_df["DIAG_DETH"] == diagnostico]

        # Filtrar por Anos
        if anos_selecionados:
            diagnosticados_df = diagnosticados_df[diagnosticados_df["ANO_DIAGN"].isin(anos_selecionados)]
            tratados_df = tratados_df[tratados_df["ANO_TRATAM"].isin(anos_selecionados)]
        # Filtrar por Idades
        if idades_selecionadas:
            if 'Menos de 1 ano' in idades_selecionadas:
                idades_selecionadas.remove('Menos de 1 ano')
                idades_selecionadas.append(0)
            idades_selecionadas = [int(idade) for idade in idades_selecionadas]
            diagnosticados_df = diagnosticados_df[diagnosticados_df["IDADE"].isin(idades_selecionadas)]
            tratados_df = tratados_df[tratados_df["IDADE"].isin(idades_selecionadas)]


        # Agregar os dados por ano para diagnóstico e tratamento
        quanti_paciente_Diag_ANO = diagnosticados_df.groupby('ANO_DIAGN')['UF_DIAGN'].count().reset_index()
        quanti_paciente_Diag_ANO.rename(columns={
            'ANO_DIAGN': 'Ano Diagnóstico', 
            'UF_DIAGN': 'Quantidade de Pacientes'
        }, inplace=True)

        quanti_paciente_Trat_ANO = tratados_df.groupby('ANO_TRATAM')['UF_TRATAM'].count().reset_index()
        quanti_paciente_Trat_ANO.rename(columns={
            'ANO_TRATAM': 'Ano Tratamento', 
            'UF_TRATAM': 'Quantidade de Pacientes'
        }, inplace=True)

        # Calcular os totais de pacientes diagnosticados e tratados
        total_diagnosticados = quanti_paciente_Diag_ANO['Quantidade de Pacientes'].sum()
        total_tratados = quanti_paciente_Trat_ANO['Quantidade de Pacientes'].sum()

        if estado == "Todos":
            fig_hab = go.Figure()               # gráfico de habilitação vazio
            dados_estab = []                    # tabela vazia
            fig_diagnosticos = go.Figure()      # gráfico de diagnósticos vazio
        else:
            # === cálculo normal do fig_hab ===
            filt = tratados_df
            hab = filt[filt['SGRUPHAB'].str[:4].isin(['1709','1713','1711'])]
            nao = filt[filt['SGRUPHAB']=='Sem Habilitação em Oncologia Pediátrica']
            fig_hab = px.pie(
                names=['Habilitados','Não Habilitados'],
                values=[len(hab), len(nao)],
                hole=0.3,
                title='Serviços Habilitados vs Não Habilitados',
                color_discrete_sequence=cat_palette,
            )
            fig_hab.update_traces(textinfo='percent+label+value')
            
            # === cálculo normal da tabela de estabelecimento ===
            grp = filt.groupby(['CNES_TRAT','SGRUPHAB','TPGESTAO'])\
                      .size().reset_index(name='Pacientes')
            grp = grp.rename(columns={
                'CNES_TRAT':'Estabelecimento',
                'SGRUPHAB':'Habilitação',
                'TPGESTAO':'Gestão'
            })
            dados_estab = grp.to_dict('records')
            
            # === cálculo normal do gráfico de diagnósticos ===
            diagnosticos_mais_frequentes = diagnosticados_df['DIAG_DETH'].value_counts().head(10)
            outros_diagnosticos = diagnosticados_df['DIAG_DETH'].value_counts().iloc[10:].sum()
            df_diagnosticos = pd.DataFrame({
                'diagnóstico': list(diagnosticos_mais_frequentes.index) + ['Outros'],
                'valor': list(diagnosticos_mais_frequentes.values) + [outros_diagnosticos]
            })
            fig_diagnosticos = px.pie(
                df_diagnosticos,
                names='diagnóstico',
                values='valor',
                hole=0.3,
                labels={'diagnóstico': 'Diagnóstico'},
                 color_discrete_sequence=cat_palette,
            )


   
           
        

       
        # Criar o gráfico de barras
        Graf_barras_ano = go.Figure(data=[
            go.Bar(
                x=quanti_paciente_Diag_ANO['Ano Diagnóstico'], 
                y=quanti_paciente_Diag_ANO['Quantidade de Pacientes'],
                name="Diagnosticados",
                marker_color=bar_colors[0],
                text=quanti_paciente_Diag_ANO['Quantidade de Pacientes'],
                textposition='auto'
            ),
            go.Bar(
                x=quanti_paciente_Trat_ANO['Ano Tratamento'], 
                y=quanti_paciente_Trat_ANO['Quantidade de Pacientes'],
                name="Tratados",
                marker_color=bar_colors[1],
                text=quanti_paciente_Trat_ANO['Quantidade de Pacientes'],
                textposition='auto'
            )
        ])

        # Customizar o layout do gráfico
        Graf_barras_ano.update_layout(
            title="Pacientes Diagnosticados vs Tratados por Ano",
            xaxis_title="Ano",
            yaxis_title="Quantidade de Pacientes",
            autosize=True
        )
            
        # Diagnósticos mais frequentes
        diagnosticos_mais_frequentes = diagnosticados_df['DIAG_DETH'].value_counts().head(10)
        outros_diagnosticos = diagnosticados_df['DIAG_DETH'].value_counts().iloc[10:].sum()

        # Tratamentos mais frequentes
        tratamentos_mais_frequentes = tratados_df['DIAG_DETH'].value_counts().head(10)
        outros_tratamentos = tratados_df['DIAG_DETH'].value_counts().iloc[10:].sum()

        # Combinar rótulos para garantir consistência de cores
        combined_labels = list(set(diagnosticos_mais_frequentes.index).union(set(tratamentos_mais_frequentes.index)))
        colors = px.colors.qualitative.Alphabet
        label_to_color = {}

        # Mapear cores de maneira consistente para ambos os gráficos
        for idx, label in enumerate(sorted(combined_labels)):
            label_to_color[label] = colors[idx % len(colors)]
        label_to_color['Outros'] = '#CCCCCC'

        # DataFrame de Diagnósticos incluindo 'Outros'
        df_diagnosticos = pd.DataFrame({
            'diagnóstico': list(diagnosticos_mais_frequentes.index) + ['Outros'],
            'valor': list(diagnosticos_mais_frequentes.values) + [outros_diagnosticos]
        })

        fig_diagnosticos = px.pie(
            df_diagnosticos,
            names='diagnóstico',
            values='valor',
            hole=0.3,
            labels={'diagnóstico': 'Diagnóstico'},
            hover_data=['valor'],
            color='diagnóstico',
            color_discrete_map=label_to_color,
            color_discrete_sequence=cat_palette,
        )
        fig_diagnosticos.update_layout(
            legend=dict(
                orientation="h",
                y=-0.2,           # empurra para baixo do gráfico
                x=0.5,
                xanchor="center"
            ),
            margin=dict(t=40, b=80)  # topo menor, espaço maior em baixo
        )

        # DataFrame de Tratamentos incluindo 'Outros'
        df_tratamentos = pd.DataFrame({
            'tratamento': list(tratamentos_mais_frequentes.index) + ['Outros'],
            'valor': list(tratamentos_mais_frequentes.values) + [outros_tratamentos]
        })

        fig_tratamentos = px.pie(
            df_tratamentos,
            names='tratamento',
            values='valor',
            hole=0.3,
            labels={'tratamento': 'Tratamento'},
            hover_data=['valor'],
            color='tratamento',
            color_discrete_map=label_to_color,
            color_discrete_sequence=cat_palette,
        )
        fig_tratamentos.update_layout(
            legend=dict(
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center"
            ),
            margin=dict(t=40, b=80)
        )
                

        bins_tempo_tratamento = [-900, -61, -31, -1, 0, 10, 20, 30,
                             40, 50, 60, 90, 120, 300, 365, 730, 9999, float('inf')]

        # Defina as categorias de tempo de tratamento
        categorias_tempo_tratamento = ['-90 dias a -61 dias', '-60 dias a -31 dias', '-30 dias a -1 dia', 'mesmo dia (tempo 0 dia)',
                                    '1 a 10 dias', '11 a 20 dias', '21 a 30 dias', '31 a 40 dias', '41 a 50 dias', '51 a 60 dias',
                                    '61 a 90 dias', '91 a 120 dias', '121 dias a 300 dias', '301 dias a 365 dias', '366 a 730 dias',
                                    'mais de dois anos', 'Sem Informação']

        # Criar a coluna 'Categorias Tempo Tratamento' com base nos bins definidos
        diagnosticados_df['Categorias Tempo Tratamento'] = pd.cut(
            diagnosticados_df['TEMPO_TRAT'], bins=bins_tempo_tratamento, labels=categorias_tempo_tratamento
        )

        # Agrupar os dados por diagnóstico e categorias de tempo de tratamento
        tabela_contagem = diagnosticados_df.groupby(['DIAG_DETH', 'Categorias Tempo Tratamento']).size().reset_index(name='value')

        # Obter os 10 diagnósticos mais frequentes
        top_10_diagnosticos = diagnosticados_df['DIAG_DETH'].value_counts().head(10).index

        # Filtrar o DataFrame para incluir apenas os 10 diagnósticos mais frequentes
        diagnosticados_df_top10 = diagnosticados_df[diagnosticados_df['DIAG_DETH'].isin(top_10_diagnosticos)]

        # Criar a coluna 'Categorias Tempo Tratamento' com base nos bins definidos
        diagnosticados_df_top10['Categorias Tempo Tratamento'] = pd.cut(
            diagnosticados_df_top10['TEMPO_TRAT'], bins=bins_tempo_tratamento, labels=categorias_tempo_tratamento
        )

        # Agrupar os dados por diagnóstico e categorias de tempo de tratamento
        tabela_contagem = diagnosticados_df_top10.groupby(['DIAG_DETH', 'Categorias Tempo Tratamento']).size().reset_index(name='value')

        # Criar o gráfico Sunburst para os 10 primeiros diagnósticos
        Temp_diagnostico = px.sunburst(
            tabela_contagem,
            path=['DIAG_DETH', 'Categorias Tempo Tratamento'],
            values='value',
           
            color_discrete_sequence=cat_palette,
        )

        

        Temp_diagnostico.update_traces(
            textinfo="label+value",
            insidetextfont=dict(size=24),
        )

        # Criar a tabela de contagem para o gráfico Sunburst 2
        tabela_contagem_grafico2_aux = pd.crosstab(
            diagnosticados_df_top10['DIAG_DETH'], diagnosticados_df_top10['TRATAMENTO'], margins=True, margins_name="Total"
        )

        # Excluir a coluna "Total" da tabela de contagem
        tabela_contagem_grafico2_aux = tabela_contagem_grafico2_aux.iloc[:-1, :-1]

        # Reorganizar a tabela para o gráfico Sunburst
        tabela_contagem_grafico2_aux.reset_index(inplace=True)
        tabela_contagem_melted2 = tabela_contagem_grafico2_aux.melt(
            id_vars=['DIAG_DETH'], value_vars=tabela_contagem_grafico2_aux.columns[1:]
        )

        # Criar o gráfico Sunburst para o primeiro tratamento dos 10 diagnósticos mais frequentes
        fig_primeiro_TRAT = px.sunburst(
            tabela_contagem_melted2,
            path=['DIAG_DETH', 'TRATAMENTO'],
            values='value',
            
            color_discrete_sequence=cat_palette,
        )

       

        fig_primeiro_TRAT.update_traces(
            textinfo="label+value",
            insidetextfont=dict(size=18),
        )

        variavelauxmodalidade = diagnosticados_df['TRATAMENTO'].value_counts()
        if not variavelauxmodalidade.empty:
            # Aqui, variavelauxmodalidade não está vazia, então você pode usá-la.
            variavelauxmodalidade = diagnosticados_df['TRATAMENTO'].value_counts()
        else:
            # Caso contrário, use data2 para calcular os valores.
            variavelauxmodalidade = tratados_df['TRATAMENTO'].value_counts()

        # Crie um gráfico Plotly Pie separadamente
        fig_modalidade = go.Figure(data=[go.Pie(
            labels=variavelauxmodalidade.index,
            values=variavelauxmodalidade.values,
            marker=dict(colors=cat_palette),
            textinfo='percent+value'
        )])
        fig_modalidade.update_layout(
            
            legend=dict(
                orientation='v',
                font=dict(size=18),

            ),
           
            font=dict(size=18),
        )
        
     
       

        top_30 = diagnosticados_df['DIAG_DETH'].value_counts().nlargest(35).index

        # filtra o DataFrame original
        df_parallel = diagnosticados_df[
            diagnosticados_df['DIAG_DETH'].isin(top_30)
        ].copy()

        

        # categoriza o tempo de tratamento
        df_parallel['TEMPO_TRAT_CAT'] = pd.cut(
            df_parallel['TEMPO_TRAT'],
            bins=bins_tempo_tratamento,
            labels=categorias_tempo_tratamento
        )

        # cria coluna com só os 3 primeiros caracteres de DIAG_DETH
        df_parallel['DIAG_DETH_3'] = df_parallel['DIAG_DETH'].astype(str).str.slice(0, 3)

        # Gráfico de categorias paralelas usando a coluna truncada
        fig_parallel = px.parallel_categories(
            df_parallel,
            dimensions=["DIAG_DETH_3", "TEMPO_TRAT_CAT"],
            labels={
                "DIAG_DETH_3": "Diagnóstico (3 chars)",
                "TEMPO_TRAT_CAT": "Tempo até Tratamento"
            }
        )



      


        

        return (
            Graf_barras_ano,                 # 1. grafico-barras
            fig_hab,                         # 2. grafico-habilitacao
            dados_estab,                     # 3. tabela-estabelecimento
            f"{total_diagnosticados} Pacientes",  # 4. pacientes-diagnosticados
            f"{total_tratados} Pacientes",        # 5. pacientes-tratados
            fig_diagnosticos,               # 6. grafico-diagnosticos
            fig_tratamentos,                # 7. grafico-tratamentos
            Temp_diagnostico,               # 8. grafico-sunburst1
            fig_primeiro_TRAT,              # 9. grafico-sunburst2
            fig_modalidade,                 # 10. grafico-modalidade
            fig_parallel                    # 11. grafico-parallel
        )





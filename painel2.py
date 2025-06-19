import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Carrega dados
df2 = pd.read_csv('dados/rhc/Painel_RHC_Final2.csv', encoding='utf-8')
for col in ['diagnostico', 'TIPOHIST', 'LOCTUPRI', 'BASMAIMP', 'DIAGANT',
            'HISTFAMC', 'ESTDFIMT', 'UFUH', 'CNES', 'IDADE', 'DTPRICON', 'SEXO']:
    if col in df2.columns:
        df2[col] = df2[col].astype(str)

# Paletas de cor
DEFAULT_COLOR_MAP = {
    'Masculino': '#0072B2',  # você pode ajustar
    'Feminino':  '#D55E00',
    'Outro':     '#999999'
}
# Para gráficos com múltiplos slices (pies, barras de categorias):
COLORBLIND_SAFE = px.colors.qualitative.Safe

def painel2_layout():
    header = html.Div([
        html.H1("Painel Oncológico RHC-INCA", style={'marginRight': '20px'}),
        html.Img(src="assets/logodatasus.png", style={'height': '150px'}),
        
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'flexWrap': 'wrap',
        'marginBottom': '20px'
    })

    botao_flutuante = html.Div([
        dbc.Button("Filtros Ativos", id="btn-filtros-rhc", color="primary", className="btn-float"),
        dbc.Popover([
            dbc.PopoverHeader("Filtros Ativos"),
            dbc.PopoverBody(id="popover-filtros-rhc-conteudo"),
        ], id="popover-filtros-rhc", target="btn-filtros-rhc", trigger="click")
    ], style={"position": "fixed", "bottom": "20px", "right": "20px", "zIndex": 1000})

    filtros = dbc.Card([
        dbc.CardHeader("Filtros"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([html.Label("Região"), dcc.Dropdown(
                    ['Todas','Norte','Nordeste','Centro-Oeste','Sudeste','Sul'],
                    'Todas', id='region-filter'
                )], md=3),
                dbc.Col([html.Label("Estado"), dcc.Dropdown(
                    ['Todas'] + sorted(df2['UFUH'].unique()), 'Todas', id='state-filter'
                )], md=3),
                dbc.Col([html.Label("Estabelecimento"), dcc.Dropdown(
                    ['Todos'] + sorted(df2['CNES'].unique()), 'Todos', id='estab-filter'
                )], md=3),
                dbc.Col([html.Label("Ano Primeira Consulta"), dcc.Dropdown(
                    ['Todos'] + sorted(df2['DTPRICON'].unique()), sorted(df2['DTPRICON'].unique()),
                    id='year-filter', multi=True
                )], md=3),
                dbc.Col([html.Label("Idade"), dcc.Dropdown(
                    ['Menos de 1 ano'] + [str(i) for i in range(1,20)],
                    ['Menos de 1 ano'] + [str(i) for i in range(1,20)],
                    id='age-filter', multi=True
                )], md=3),
                dbc.Col([html.Label("Diagnóstico"), dcc.Dropdown(
                    ['Todos'] + sorted(df2['diagnostico'].unique()), 'Todos', id='diag-filter'
                )], md=3),
                dbc.Col([html.Label("Morfologia"), dcc.Dropdown(
                    ['Todos'] + sorted(df2['TIPOHIST'].unique()), 'Todos', id='morph-filter'
                )], md=3),
                dbc.Col([html.Label("Topografia"), dcc.Dropdown(
                    ['Todos'] + sorted(df2['LOCTUPRI'].unique()), 'Todos', id='topo-filter'
                )], md=3),
                dbc.Switch(
                    id="switch-daltonismo",
                    label="Modo Daltonismo",
                    value=False,
                    className="ms-4 align-self-center"
                )
            ], className='g-3'),
           
        ])
    ], className='mb-4')

    metric_card = dbc.Col(dbc.Card([
        dbc.CardHeader( html.Div([
                        html.Span("Total de Pacientes"),
                       
                    ], className="d-flex align-items-center justify-content-between")),
        dbc.CardBody(html.Div(id='metric-total-patients', style={"fontSize":22, "textAlign":"center"}))
    ]), xs=12, md=6, className='mb-4')

    # 1) Defina seus gráficos com título + descrição:
    graph_infos = [
        {
            'id': 'graph-patients-year',
            'title': 'Pacientes por Ano',
            'desc': 'Este gráfico mostra a evolução do número de pacientes por ano de primeira consulta.'
        },
        {
            'id': 'graph-top10-diag',
            'title': 'Top 10 Diagnósticos',
            'desc': 'Pie chart dos 10 diagnósticos mais frequentes registrados no período.'
        },
        {
            'id': 'graph-base-diag',
            'title': 'Base para Diagnóstico',
            'desc': 'Distribuição das bases mais importantes utilizadas para confirmar o diagnóstico.'
        },
        {
            'id': 'graph-prev-treatment',
            'title': 'Diagnóstico/Trat. Anteriores',
            'desc': 'Percentual de pacientes que já tinham diagnóstico ou tratamento antes do registro atual.'
        },
        {
            'id': 'graph-hist-family',
            'title': 'Histórico Familiar',
            'desc': 'Proporção de pacientes com histórico familiar de câncer.'
        },
        {
            'id': 'graph-first-hosp',
            'title': 'Estado após Primeiro Trat.',
            'desc': 'Estado da doença no final do primeiro tratamento registrado.'
        },
        {
            'id': 'graph-sex',
            'title': 'Registros por Sexo',
            'desc': 'Quantidade de registros divididos por sexo do paciente.'
        },
    ]

    # 2) Gere os cards incluindo o parágrafo de descrição:
    graph_cards = [
        dbc.Col(
            [
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span(info['title'], className="me-2"),
                            html.I(
                                className="bi bi-info-circle",
                                id=f"info-{info['id']}",
                                style={"cursor": "pointer", "fontSize": "1.2rem"}
                            )
                        ], className="d-flex justify-content-center align-items-center")
                    ),
                    dbc.CardBody([
                        # descrição sempre visível
                        html.P(info['desc'], className="text-muted mb-2"),
                        # seu gráfico
                        dcc.Graph(id=info['id'], style={'height':'600px'})
                    ])
                ]),
                # Tooltip opcional com a mesma descrição
                dbc.Tooltip(
                    info['desc'],
                    target=f"info-{info['id']}",
                    placement="top"
                )
            ],
            xs=12, md=6, className='mb-4'
        )
        for info in graph_infos
    ]



    return html.Div([
        botao_flutuante,
        header,
        dbc.Container([filtros, dbc.Row([metric_card] + graph_cards, className='g-4')], fluid=True)
    ])

def painel2_callbacks(app: dash.Dash):
    @app.callback(
        Output('state-filter','options'),
        Output('state-filter','value'),
        Input('region-filter','value')
    )
    def upd_states(region):
        reg_map = {
            'Norte':['AC','AM','AP','PA','RO','RR','TO'],
            'Nordeste':['AL','BA','CE','MA','PB','PE','PI','RN','SE'],
            'Centro-Oeste':['DF','GO','MS','MT'],
            'Sudeste':['ES','MG','RJ','SP'],
            'Sul':['PR','RS','SC']
        }
        if region=='Todas':
            opts = sorted(df2['UFUH'].unique())
        else:
            opts = reg_map[region]
        return ([{'label':i,'value':i} for i in (['Todas']+opts)], 'Todas')

    @app.callback(
        Output('estab-filter','options'),
        Output('estab-filter','value'),
        Input('state-filter','value'),
        Input('region-filter','value')
    )
    def update_estabs_by_state(state, region):
        d = df2.copy()
        if region != 'Todas':
            mapping = {
                'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
                'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
                'Centro-Oeste': ['DF', 'GO', 'MS', 'MT'],
                'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
                'Sul': ['PR', 'RS', 'SC']
            }
            d = d[d['UFUH'].isin(mapping.get(region, []))]
        if state != 'Todas':
            d = d[d['UFUH'] == state]

        estabs = sorted(d['CNES'].dropna().unique())
        options = [{'label': 'Todos', 'value': 'Todos'}] + [{'label': cnes, 'value': cnes} for cnes in estabs]
        return options, 'Todos'

    @app.callback(
        Output('popover-filtros-rhc','is_open'),
        Input('btn-filtros-rhc','n_clicks'),
        State('popover-filtros-rhc','is_open')
    )
    def toggle(n, open_):
        return not open_ if n else open_

    @app.callback(
        Output('popover-filtros-rhc-conteudo','children'),
        [Input(f,'value') for f in
         ['region-filter','state-filter','estab-filter','year-filter',
          'age-filter','diag-filter','morph-filter','topo-filter']]
    )
    def popover(*vals):
        labels = ["Região","Estado","Estab.","Ano(s)","Idade(s)",
                  "Diagnóstico","Morfologia","Topografia"]
        return html.Ul([html.Li(f"{lab}: {val}") for lab,val in zip(labels,vals)])

    @app.callback(
        [
            Output('metric-total-patients','children'),
            Output('graph-patients-year','figure'),
            Output('graph-top10-diag','figure'),
            Output('graph-base-diag','figure'),
            Output('graph-prev-treatment','figure'),
            Output('graph-hist-family','figure'),
            Output('graph-first-hosp','figure'),
            Output('graph-sex','figure'),
        ],
        [
            Input('region-filter','value'),
            Input('state-filter','value'),
            Input('estab-filter','value'),
            Input('year-filter','value'),
            Input('age-filter','value'),
            Input('diag-filter','value'),
            Input('morph-filter','value'),
            Input('topo-filter','value'),
            Input('switch-daltonismo','value'),
        ]
    )
    def update_all(region, state, estab, years, ages, diag, morph, topo, dalto):
        d = df2.copy()
        # --- Aplica filtros (igual ao original) ---
        reg_map = {
            'Norte':['AC','AM','AP','PA','RO','RR','TO'],
            'Nordeste':['AL','BA','CE','MA','PB','PE','PI','RN','SE'],
            'Centro-Oeste':['DF','GO','MS','MT'],
            'Sudeste':['ES','MG','RJ','SP'],
            'Sul':['PR','RS','SC']
        }
        if region!='Todas': d=d[d['UFUH'].isin(reg_map[region])]
        if state!='Todas':  d=d[d['UFUH']==state]
        if estab!='Todos':  d=d[d['CNES']==estab]
        if isinstance(years,list) and years: d=d[d['DTPRICON'].isin(years)]
        if isinstance(ages,list)  and ages:
            real = [0 if a=='Menos de 1 ano' else int(a) for a in ages]
            d=d[d['IDADE'].astype(int).isin(real)]
        if diag!='Todos':  d=d[d['diagnostico']==diag]
        if morph!='Todos':d=d[d['TIPOHIST']==morph]
        if topo!='Todos': d=d[d['LOCTUPRI']==topo]

        # Métrica
        total = len(d)
        metric = f"{total:,}"

        # Escolhe paleta
        cmap_bar = COLORBLIND_SAFE if dalto else ['#D5E5ED']
        cmap_pie = COLORBLIND_SAFE if dalto else px.colors.qualitative.Plotly

        # 1) Pacientes por ano
        yc = d.groupby('DTPRICON').size().reset_index(name='count')
        fig1 = go.Figure(go.Bar(
            x=yc['DTPRICON'], y=yc['count'],
            marker_color=cmap_bar[0], text=yc['count'], textposition='auto'
        ))
        fig1.update_layout(xaxis_title='Ano', yaxis_title='Qtd.', showlegend=False)

        # 2) Top 10 Diagnósticos
        t10 = d['diagnostico'].value_counts().head(10)
        fig2 = go.Figure(go.Pie(
            labels=t10.index, values=t10.values, hole=0.5,
            marker_colors=cmap_pie
        ))
        fig2.update_layout(
            legend=dict(
            orientation="h",
            y=-0.2,           # empurra para baixo do gráfico
            x=0.5,
            xanchor="center"
        ),
    margin=dict(t=40, b=80) )

        # 3) Base mais importante
        bc = d['BASMAIMP'].value_counts(dropna=False)
        fig3 = go.Figure(go.Pie(
            labels=bc.index, values=bc.values, hole=0.5,
            marker_colors=cmap_pie
        ))
        
        # 4) Diagnóstico/Trat Anteriores
        pc = d['DIAGANT'].value_counts(dropna=False)
        fig4 = go.Figure(go.Pie(
            labels=pc.index, values=pc.values, hole=0.5,
            marker_colors=cmap_pie
        ))
        

        # 5) Histórico Familiar
        hf = d['HISTFAMC'].value_counts()
        fig5 = go.Figure(go.Pie(
            labels=hf.index, values=hf.values, hole=0.5,
            marker_colors=cmap_pie
        ))
        

        # 6) Estado ao fim do 1º tratamento
        ph = d['ESTDFIMT'].value_counts(dropna=False)
        fig6 = go.Figure(go.Pie(
            labels=ph.index, values=ph.values, hole=0.5,
            marker_colors=cmap_pie
        ))
      

        # 7) Sexo (barra colorblind-safe)
        mapping = {'1':'Masculino','2':'Feminino','M':'Masculino','F':'Feminino'}
        d['SEXO_LABEL'] = d['SEXO'].map(mapping).fillna('Outro')
        cnt = d['SEXO_LABEL'].value_counts()
        colors = [DEFAULT_COLOR_MAP[lbl] for lbl in cnt.index]
        if dalto:
            colors = [DEFAULT_COLOR_MAP[lbl] for lbl in cnt.index]  # já são daltônico-safe
        fig7 = go.Figure(go.Bar(
            x=cnt.index, y=cnt.values,
            marker_color=colors, text=cnt.values, textposition='auto'
        ))
        fig7.update_layout(title='Registros por Sexo', xaxis_title='Sexo', yaxis_title='Qtd.', showlegend=False)

        return metric, fig1, fig2, fig3, fig4, fig5, fig6, fig7


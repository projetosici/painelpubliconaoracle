import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import json
import geopandas as gpd
from urllib.request import urlopen

# Lista de UF dos estados brasileiros
ufs = [
    '', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
    'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

# Mapeamento dos caminhos dos arquivos CSV para cada UF
caminhos_csv = {
    'AC': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_AC_processado_modificado.csv',
    'AL': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_AL_processado_modificado.csv',
    'AP': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_AP_processado_modificado.csv',
    'AM': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_AM_processado_modificado.csv',
    'BA': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_BA_processado_modificado.csv',
    'CE': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_CE_processado_modificado.csv',
    'DF': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_DF_processado_modificado.csv',
    'ES': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_ES_processado_modificado.csv',
    'GO': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_GO_processado_modificado.csv',
    'MA': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_MA_processado_modificado.csv',
    'MT': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_MT_processado_modificado.csv',
    'MS': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_MS_processado_modificado.csv',
    'MG': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_MG_processado_modificado.csv',
    'PA': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_PA_processado_modificado.csv',
    'PB': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_PB_processado_modificado.csv',
    'PR': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_PR_processado_modificado.csv',
    'PE': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_PE_processado_modificado.csv',
    'PI': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_PI_processado_modificado.csv',
    'RJ': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_RJ_processado_modificado.csv',
    'RN': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_RN_processado_modificado.csv',
    'RS': 'dados/sim/Painel_Mortalidade_RS2.csv',
    'RO': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_RO_processado_modificado.csv',
    'RR': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_RR_processado_modificado.csv',
    'SC': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_SC_processado_modificado.csv',
    'SP': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_SP_processado_modificado.csv',
    'SE': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_SE_processado_modificado.csv',
    'TO': 'dados/sim/painel_final/Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_Painel_Mortalidade_neoplasias_0_19_TO_processado_modificado.csv'
}

# Instanciando o app com tema Litera
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Painel Mortalidade Oncológica"

# Layout do painel

def painel3_layout():
    layout = html.Div([
        html.Div([
            html.H1("Painel Mortalidade Oncológica Pediátrica", style={'marginRight': '20px'}),
            html.Img(src="assets/SIMlogo.png", style={'height': '150px'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'}),

        # Filtros
        dbc.Row([
            dbc.Col([html.Label("Selecione um estado:"), dcc.Dropdown(id='uf-selector', options=[{'label': uf, 'value': uf} for uf in ufs], value='', style={'width': '100%'})], md=4, style={'margin': '20px'}),
            dbc.Col([html.Label("Selecione os Anos:"), dcc.Dropdown(id='ano-filter', options=[], value=[], multi=True, style={'width': '100%'})], md=4, style={'margin': '20px'}),
            dbc.Col([html.Label("Selecione as Idades:"), dcc.Dropdown(id='idade-filter', options=[], value=[], multi=True, style={'width': '100%'})], md=4, style={'margin': '20px'}),
            dbc.Col(dbc.Switch(id='colorblind-switch', label='Modo Daltonismo', value=False, style={'marginLeft': '20px'}), width=2, style={'marginTop': '40px'}),
        ], style={'margin-bottom': '20px'}),

        # Quantidade de óbitos
        dbc.Row(dbc.Col(html.Div([html.H5("Quantidade de Óbitos", style={"text-align": "center"}), html.Div(id="quantidade-obitos", style={"text-align": "center", "font-size": "20px"})], style={"padding": "10px"})), style={"margin-bottom": "20px"}),

        # Gráficos principais com ícones de info
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader(html.Div([html.H4("Óbitos por Ano", style={"display": "inline-block", "marginRight": "5px"}), html.I(className="bi bi-info-circle", id="info-ano", style={"cursor": "pointer", "color": "#0d6efd"})])), dbc.CardBody(dcc.Graph(id="fig-obitos-ano", config={'responsive': True}))], color="light", outline=True), md=6),
            dbc.Col(dbc.Card([dbc.CardHeader(html.Div([html.H4("Top 10 Causas Básicas de Óbito", style={"display": "inline-block", "marginRight": "5px"}), html.I(className="bi bi-info-circle", id="info-top-causas", style={"cursor": "pointer", "color": "#0d6efd"})])), dbc.CardBody(dcc.Graph(id="fig-top-causas", config={'responsive': True}))], color="light", outline=True), md=6),
        ], style={"margin-bottom": "20px"}),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader(html.Div([html.H4("Locais de Ocorrência do Óbito", style={"display": "inline-block", "marginRight": "5px"}), html.I(className="bi bi-info-circle", id="info-local", style={"cursor": "pointer", "color": "#0d6efd"})])), dbc.CardBody(dcc.Graph(id="fig-local-ocorrencia", config={'responsive': True}))], color="light", outline=True), md=6),
            dbc.Col(dbc.Card([dbc.CardHeader(html.Div([html.H4("Top 10 Causas de Mortes por Sexo", style={"display": "inline-block", "marginRight": "5px"}), html.I(className="bi bi-info-circle", id="info-sexo", style={"cursor": "pointer", "color": "#0d6efd"})])), dbc.CardBody(dcc.Graph(id="fig-causas-sexo", config={'responsive': True}))], color="light", outline=True), md=6),
        ], style={"margin-bottom": "20px"}),

        # Mapa só para RS, dentro de Collapse
        dbc.Collapse(dbc.Row(dbc.Col(dbc.Card([dbc.CardHeader(html.Div([html.H4("Mapa de Óbitos por Município (RS)", style={"display": "inline-block", "marginRight": "5px"}), html.I(className="bi bi-info-circle", id="info-mapa", style={"cursor": "pointer", "color": "#0d6efd"})])), dbc.CardBody(dcc.Graph(id="fig-mapa-rs", config={'responsive': True}))], color="light", outline=True), md=12), style={"margin-bottom": "20px"}), id="collapse-mapa", is_open=False, style={"margin-top": "20px"}),

        # Tooltips explicativos
        dbc.Tooltip("Exibe o total de óbitos agrupados por ano.", target="info-ano", placement="top"),
        dbc.Tooltip("Mostra as 10 principais causas básicas de óbito em formato de donut.", target="info-top-causas", placement="top"),
        dbc.Tooltip("Distribuição dos locais onde ocorreram os óbitos.", target="info-local", placement="top"),
        dbc.Tooltip("Comparativo das mortes por sexo para as 10 causas principais.", target="info-sexo", placement="top"),
        dbc.Tooltip("Mapa geográfico dos óbitos por município para RS.", target="info-mapa", placement="top"),

        # Rodapé
        html.Div(html.P("Fonte: DATASUS - SIM", style={"text-align": "center"}))
    ])
    return layout

# Callback de atualização dos gráficos
def painel3_callbacks(app):
    @app.callback([
        Output('quantidade-obitos', 'children'),
        Output('fig-obitos-ano', 'figure'),
        Output('fig-top-causas', 'figure'),
        Output('fig-local-ocorrencia', 'figure'),
        Output('fig-causas-sexo', 'figure'),
        Output('fig-mapa-rs', 'figure'),
        Output('collapse-mapa', 'is_open'),
        Output('ano-filter', 'options'),
        Output('ano-filter', 'value'),
        Output('idade-filter', 'options'),
        Output('idade-filter', 'value'),
    ], [
        Input('uf-selector', 'value'),
        Input('ano-filter', 'value'),
        Input('idade-filter', 'value'),
        Input('colorblind-switch', 'value'),
    ])
    def update_dashboard(selected_uf, selected_anos, selected_idades, colorblind_mode):
        if not selected_uf or selected_uf not in caminhos_csv:
            return (
                "Selecione um estado para visualizar os dados.", {}, {}, {}, {}, {}, False,
                [], [], [], []
            )

        df = pd.read_csv(caminhos_csv[selected_uf], encoding='utf-8')
        anos_unicos = sorted(df['ANOOBITO'].unique())
        if not selected_anos:
            selected_anos = anos_unicos
        df_filtrado = df[df['ANOOBITO'].isin(selected_anos)]

        if not selected_idades:
            selected_idades = [str(i) for i in range(0, 20)]
        idades = [int(i) for i in selected_idades]
        df_filtrado = df_filtrado[df_filtrado['IDADEOBITO'].isin(idades)]

        quantidade_obitos = len(df_filtrado)

        dados_ano = df_filtrado.groupby('ANOOBITO').size().reset_index(name='Quantidade')
        top_causas = df_filtrado['CAUSABAS'].value_counts().nlargest(10)
        df_top_causas = pd.DataFrame({'Causa': top_causas.index, 'Quantidade': top_causas.values})
        top_locais = df_filtrado['LOCOCOR'].value_counts()
        df_locais = pd.DataFrame({'Local': top_locais.index, 'Quantidade': top_locais.values})
        sexo_ct = df_filtrado.groupby(['CAUSABAS','SEXO']).size().reset_index(name='Quantidade')
        top10 = sexo_ct.groupby('CAUSABAS')['Quantidade'].sum().nlargest(10).index
        sexo_ct = sexo_ct[sexo_ct['CAUSABAS'].isin(top10)]

        seq = px.colors.qualitative.Safe if colorblind_mode else None

        fig_ano = px.bar(dados_ano, x='ANOOBITO', y='Quantidade', title='Óbitos por Ano', color_discrete_sequence=seq)
        fig_causas = px.pie(df_top_causas, names='Causa', values='Quantidade', hole=0.3, title='Top 10 Causas Básicas de Óbito', color_discrete_sequence=seq)
        fig_causas.update_layout(legend_orientation='h', legend=dict(y=-0.3))
        fig_local = px.pie(df_locais, names='Local', values='Quantidade', hole=0.4, title='Locais de Ocorrência do Óbito', color_discrete_sequence=seq)
        fig_local.update_layout(legend_orientation='h', legend=dict(y=-0.3))

        if colorblind_mode:
            pal = px.colors.qualitative.Safe
            cmap = {'Masculino': pal[0], 'Feminina': pal[1]}
        else:
            cmap = {'Masculino': '#ADD8E6', 'Feminina': '#FFC0CB'}
        fig_sexo = px.bar(sexo_ct, x='Quantidade', y='CAUSABAS', color='SEXO', title='Top 10 Causas de Mortes por Sexo', color_discrete_map=cmap, barmode='group')

        abrir = (selected_uf == 'RS')
        fig_mapa = {}
        if abrir:
            with urlopen("https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-43-mun.json") as resp:
                geojson = json.load(resp)
            df['Contagem'] = df.groupby('CODMUNOCOR')['CODMUNOCOR'].transform('count')
            geo_df = gpd.GeoDataFrame.from_features(geojson['features']).merge(df, left_on='name', right_on='CODMUNOCOR', how='left')
            mn, mx = geo_df['Contagem'].min(), geo_df['Contagem'].max()
            fig_mapa = px.choropleth_mapbox(
                geo_df, geojson=geo_df.geometry, locations=geo_df.index, color='Contagem',
                color_continuous_scale=px.colors.sequential.Reds, center={"lat":-29.491010,"lon":-53.038245},
                mapbox_style="open-street-map", zoom=5, hover_name='name', custom_data=['name','Contagem'],
                range_color=(mn, mx), color_continuous_midpoint=mx/2
            )
            fig_mapa.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Óbitos: %{customdata[1]}')
            fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        anos_opts = [{'label': str(a), 'value': a} for a in anos_unicos]
        idades_opts = [{'label': f'{i} anos', 'value': str(i)} for i in range(0,20)]

        return (
            f"Quantidade de Óbitos: {quantidade_obitos}", fig_ano, fig_causas, fig_local, fig_sexo, fig_mapa, abrir,
            anos_opts, selected_anos, idades_opts, selected_idades
        )
    
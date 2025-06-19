import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os

# Importando os painéis de arquivos separados
from painel1 import painel1_callbacks, painel1_layout
from painel2 import painel2_callbacks, painel2_layout
from painel3 import painel3_callbacks, painel3_layout
from painel4 import painel4_callbacks, painel4_layout
from home     import home_layout

# Criando o aplicativo Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css",
    ],
)

server = app.server
# Definindo o título da página e incluindo o favicon
app.title = "Paineloncoped"
app._favicon = "logo.svg"  # Nome do arquivo do favicon no diretório "assets"

# Layout principal
app.layout = html.Div([
    dbc.Container([
        html.Div([
            html.Img(
                src='assets/logopaceiros.png',
                style={
                    "position": "absolute",
                    "top": "20px",
                    "left": "20px",
                    "width": "450px",
                    "height": "auto"
                }
            ),
            html.Div([
                html.Img(src='/assets/logo.svg', style={"height": "auto", "max-width": "300px", "display": "block", "margin": "0 auto"}),
                 html.A("Acesse o painel em inglês",
           href="https://paineloncopedenglish.up.railway.app/",
           target="_blank",
           style={
               "position": "absolute",
               "top": "40px",
               "right": "20px",
               "fontWeight": "bold",
               "color": "#0d6efd",
               "textDecoration": "none"
           })
            ], style={"textAlign": "center", "margin-top": "30px"})
        ], style={"position": "relative", "margin-bottom": "30px"}),

        # Definindo as abas de navegação
        dbc.Tabs([
            dbc.Tab(label="Home", tab_id="Home"),
            dbc.Tab(label="Painel Oncológico Pediátrico (Dados DATASUS)", tab_id="painel1"),
            dbc.Tab(label="Painel Oncológico Pediátrico (Dados do Tabulador RHC-INCA)", tab_id="painel2"),
            dbc.Tab(label="Painel Mortalidade Oncológica Pediátrica(Dados Sim)", tab_id="painel3"),
            dbc.Tab(label="Painel Sistemas Regulador SMSPOA", tab_id="painel4"),
            
        ], id="tabs", active_tab="Home"),

        html.Div(id="conteudo-painel")
    ], fluid=True)

])
# Callback para trocar de painel
@app.callback(
    Output("conteudo-painel", "children"),
    Input("tabs", "active_tab")
)
def renderizar_painel(tab_id):
    if tab_id == "Home":
        return home_layout()
    elif tab_id == "painel1":
        return painel1_layout()
    elif tab_id == "painel2":
        return painel2_layout()
    elif tab_id == "painel3":
        return painel3_layout()
    elif tab_id == "painel4":
        return painel4_layout()
    #    return painel4_layout()
    return "Selecione um painel."

# Registrando os callbacks de cada painel
painel1_callbacks(app)
painel2_callbacks(app)
painel3_callbacks(app)
painel4_callbacks(app)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

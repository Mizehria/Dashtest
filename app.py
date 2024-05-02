import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Lista de testes
testes = ['ABFW', 'TENA', 'PROLEC', 'TDE2', 'NEUPSILIM', 'PROVA DE CONSCIÊNCIA SINTÁTICA', 'PROVA DE CONSCIÊNCIA FONOLÓGICA']

# Dicionário para mapear os valores dos resultados
valores_resultados = {
    'Superior': 3,
    'Adequado': 2,
    'Inferior': 1
}

# Dicionário para mapear as cores
cores_resultados = {
    'Superior': 'rgba(76, 187, 23, 0.6)',  # Verde
    'Adequado': 'rgba(40, 116, 166, 0.6)',  # Azul
    'Inferior': 'rgba(219, 50, 54, 0.6)'  # Vermelho
}

# Layout do aplicativo Dash
app = dash.Dash(__name__)
sever = app.sever

app.layout = html.Div([
    html.Div(id='sidebar', className='sidebar', children=[
        html.H2('Opções de Resultados'),
        html.Button("Mostrar/Ocultar Opções", id="show-hide-button", n_clicks=0),
        html.Div(id='options-div', children=[
            html.Div([
                html.Label(teste),
                dcc.Dropdown(
                    id=f'{teste}-dropdown',
                    options=[
                        {'label': 'Superior', 'value': 'Superior'},
                        {'label': 'Adequado', 'value': 'Adequado'},
                        {'label': 'Inferior', 'value': 'Inferior'}
                    ],
                    value='Adequado'
                )
            ]) for teste in testes
        ])
    ]),
    
    html.Div(id='content', className='content', children=[
        html.H1("Dashboard de Desempenho de Paciente"),
        html.Div([
            dcc.Graph(id='radar-chart', className='six columns'),
            dcc.Graph(id='bar-chart', className='six columns')
        ], className='row')
    ])
])

@app.callback(
    Output('options-div', 'style'),
    [Input('show-hide-button', 'n_clicks')]
)
def toggle_options_div(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('radar-chart', 'figure'),
    [Input(f'{teste}-dropdown', 'value') for teste in testes]
)
def update_radar_chart(*values):
    valores = [valores_resultados[value] for value in values]
    
    # Adicionando valores "Adequado" para a sombra de fundo
    valores_shadow = [valores_resultados['Adequado']] * len(testes)
    
    data = [
        go.Scatterpolar(
            r=valores_shadow,
            theta=testes,
            fill='toself',
            fillcolor='rgba(0,0,0,0.1)',
            mode='none',
            showlegend=False
        ),
        go.Scatterpolar(
            r=valores,
            theta=testes,
            fill='toself',
            marker=dict(color=[cores_resultados[value] for value in values])
        )
    ]
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=False
            )
        ),
        showlegend=False
    )
    return {'data': data, 'layout': layout}

@app.callback(
    Output('bar-chart', 'figure'),
    [Input(f'{teste}-dropdown', 'value') for teste in testes]
)
def update_bar_chart(*values):
    valores = [valores_resultados[value] for value in values]
    
    # Adicionando uma linha horizontal para "Adequado"
    adequado_line = {'type': 'line',
                     'x0': testes[0], 'x1': testes[-1],
                     'y0': valores_resultados['Adequado'], 'y1': valores_resultados['Adequado'],
                     'line': {'color': 'black', 'width': 1, 'dash': 'dash'}}
    
    data = [
        go.Bar(
            x=testes,
            y=valores,
            marker=dict(color=[cores_resultados[value] for value in values])
        )
    ]
    layout = go.Layout(
        title='Resultados dos Testes',
        xaxis=dict(title='Testes', showticklabels=True, tickangle=45),
        yaxis=dict(showticklabels=False),  # Removendo valores numéricos do eixo Y
        showlegend=False,
        shapes=[adequado_line]  # Adicionando a linha horizontal
    )
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from datetime import datetime
from flask import Flask

dados_oficina_json = {
    "2023": {
        "Janeiro": {"receita": 15600.96, "despesas": 9140.9, "lucro": 6460.06},
        "Fevereiro": {"receita": 14306.85, "despesas": 8521.07, "lucro": 5785.78},
        "Março": {"receita": 6239.25, "despesas": 2194.52, "lucro": 4044.73},
        "Abril": {"receita": 3354.84, "despesas": 1882.22, "lucro": 1472.62},
        "Maio": {"receita": 14911.89, "despesas": 6106.07, "lucro": 8805.82},
        "Junho": {"receita": 11620.73, "despesas": 5054.68, "lucro": 6566.05},
        "Julho": {"receita": 9825.83, "despesas": 6885.68, "lucro": 2940.15},
        "Agosto": {"receita": 3664.21, "despesas": 1646.87, "lucro": 2017.34},
        "Setembro": {"receita": 6829.18, "despesas": 3939.14, "lucro": 2890.04},
        "Outubro": {"receita": 7948.74, "despesas": 5191.32, "lucro": 2757.42},
        "Novembro": {"receita": 9598.8, "despesas": 5657.86, "lucro": 3940.94},
        "Dezembro": {"receita": 10743.76, "despesas": 4540.9, "lucro": 6202.86}
    },
    "2024": {
        "Janeiro": {"receita": 14106.28, "despesas": 5292.41, "lucro": 8813.87},
        "Fevereiro": {"receita": 13418.1, "despesas": 6024.92, "lucro": 7393.18},
        "Março": {"receita": 8721.7, "despesas": 3137.77, "lucro": 5583.93},
        "Abril": {"receita": 3863.93, "despesas": 2762.96, "lucro": 1100.97},
        "Maio": {"receita": 13853.84, "despesas": 8749.91, "lucro": 5103.93},
        "Junho": {"receita": 10736.79, "despesas": 7504.59, "lucro": 3232.2},
        "Julho": {"receita": 4293.24, "despesas": 1549.77, "lucro": 2743.47},
        "Agosto": {"receita": 4113.87, "despesas": 2743.81, "lucro": 1370.06},
        "Setembro": {"receita": 4033.51, "despesas": 1940.3, "lucro": 2093.21},
        "Outubro": {"receita": 9679.79, "despesas": 5844.62, "lucro": 3835.17},
        "Novembro": {"receita": 8635.23, "despesas": 6197.2, "lucro": 2438.03},
        "Dezembro": {"receita": 12000.3, "despesas": 4647.11, "lucro": 7353.19}
    },
    "2025": {
        "Janeiro": {"receita": 11740.7, "despesas": 5488.78, "lucro": 6251.92},
        "Fevereiro": {"receita": 15397.16, "despesas": 5949.39, "lucro": 9447.77},
        "Março": {"receita": 7069.13, "despesas": 3112.66, "lucro": 3956.47},
        "Abril": {"receita": 8448.54, "despesas": 4232.29, "lucro": 4216.25},
        "Maio": {"receita": 15482.25, "despesas": 7223.45, "lucro": 8258.8},
        "Junho": {"receita": 14303.99, "despesas": 7300.8, "lucro": 7003.19},
        "Julho": {"receita": 9398.23, "despesas": 6035.47, "lucro": 3362.76}
    }
}

def json_para_dataframe(dados_json):
    rows = []
    for ano, meses in dados_json.items():
        for mes, valores in meses.items():
            mes_num = {
                'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
                'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
                'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
            }[mes]
            
            data = datetime(int(ano), mes_num, 1)
            
            rows.append({
                'data': data,
                'ano': int(ano),
                'mes': mes,
                'mes_num': mes_num,
                'mes_ano': f"{mes[:3]}/{ano}",
                'receita': valores['receita'],
                'despesas': valores['despesas'],
                'lucro': valores['lucro']
            })
    
    return pd.DataFrame(rows).sort_values('data')

def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df = json_para_dataframe(dados_oficina_json)

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

config_grafico = {
    'displayModeBar': False,
    'staticPlot': False,
    'scrollZoom': False,
    'doubleClick': False,
    'showTips': False,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
}

cores = {
    'background': '#fafafa',
    'surface': '#ffffff',
    'primary': '#2563eb',
    'secondary': '#dc2626',
    'success': '#16a34a',
    'text': '#1f2937',
    'muted': '#6b7280',
    'border': '#e5e7eb'
}

app.layout = html.Div(
    style={
        'backgroundColor': cores['background'],
        'color': cores['text'],
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'minHeight': '100vh',
        'padding': '0',
        'margin': '0'
    },
    children=[
        html.Div(
            style={
                'backgroundColor': cores['surface'],
                'padding': '32px 24px',
                'borderBottom': f'1px solid {cores["border"]}',
                'marginBottom': '32px'
            },
            children=[
                html.H1(
                    'Dashboard',
                    style={
                        'margin': '0',
                        'fontSize': '2rem',
                        'fontWeight': '600',
                        'color': cores['text'],
                        'textAlign': 'center'
                    }
                ),
                html.P(
                    'Dashboard Financeiro',
                    style={
                        'margin': '8px 0 0 0',
                        'fontSize': '1rem',
                        'color': cores['muted'],
                        'textAlign': 'center',
                        'fontWeight': '400'
                    }
                )
            ]
        ),
        
        html.Div(
            style={
                'maxWidth': '1200px', 
                'margin': '0 auto', 
                'padding': '0 24px'
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': cores['surface'],
                        'padding': '24px',
                        'borderRadius': '8px',
                        'border': f'1px solid {cores["border"]}',
                        'marginBottom': '24px',
                        'display': 'flex',
                        'gap': '16px',
                        'alignItems': 'center',
                        'flexWrap': 'wrap'
                    },
                    children=[
                        html.Label(
                            'Filtrar por Ano:',
                            style={
                                'fontWeight': '500',
                                'color': cores['text'],
                                'fontSize': '0.875rem'
                            }
                        ),
                        dcc.Dropdown(
                            id='filtro-ano',
                            options=[{'label': 'Todos os Anos', 'value': 'todos'}] + 
                                    [{'label': str(ano), 'value': ano} for ano in sorted(df['ano'].unique())],
                            value='todos',
                            style={
                                'width': '160px',
                                'fontSize': '0.875rem'
                            },
                            clearable=False
                        )
                    ]
                ),
                
                html.Div(
                    id='cards-metricas',
                    style={
                        'display': 'grid',
                        'gridTemplateColumns': 'repeat(auto-fit, minmax(240px, 1fr))',
                        'gap': '16px',
                        'marginBottom': '32px'
                    }
                ),
                
                html.Div(
                    style={
                        'backgroundColor': cores['surface'],
                        'padding': '24px',
                        'borderRadius': '8px',
                        'border': f'1px solid {cores["border"]}',
                        'marginBottom': '24px'
                    },
                    children=[
                        html.H3('Evolução Mensal', 
                                style={'margin': '0 0 24px 0', 'fontSize': '1.125rem', 'fontWeight': '600', 'color': cores['text']}),
                        dcc.Graph(
                            id='grafico-principal',
                            config=config_grafico,
                            style={'height': '400px'}
                        )
                    ]
                ),
                
                html.Div(
                    style={
                        'backgroundColor': cores['surface'],
                        'padding': '24px',
                        'borderRadius': '8px',
                        'border': f'1px solid {cores["border"]}',
                        'marginBottom': '24px'
                    },
                    children=[
                        html.H3('Comparativo Anual', 
                                style={'margin': '0 0 24px 0', 'fontSize': '1.125rem', 'fontWeight': '600', 'color': cores['text']}),
                        dcc.Graph(
                            id='grafico-anual',
                            config=config_grafico,
                            style={'height': '350px'}
                        )
                    ]
                ),
                
                html.Div(
                    style={
                        'backgroundColor': cores['surface'],
                        'padding': '24px',
                        'borderRadius': '8px',
                        'border': f'1px solid {cores["border"]}',
                        'marginBottom': '40px'
                    },
                    children=[
                        html.H3('Dados Detalhados', 
                                style={'margin': '0 0 24px 0', 'fontSize': '1.125rem', 'fontWeight': '600', 'color': cores['text']}),
                        dash_table.DataTable(
                            id='tabela-simples',
                            columns=[
                                {'name': 'Período', 'id': 'mes_ano'},
                                {'name': 'Receita', 'id': 'receita_formatada', 'type': 'text'},
                                {'name': 'Despesas', 'id': 'despesas_formatada', 'type': 'text'},
                                {'name': 'Lucro', 'id': 'lucro_formatado', 'type': 'text'},
                                {'name': 'Margem (%)', 'id': 'margem', 'type': 'numeric', 'format': {'specifier': '.1f'}}
                            ],
                            sort_action='native',
                            sort_mode='single',
                            style_cell={
                                'backgroundColor': cores['surface'],
                                'color': cores['text'],
                                'textAlign': 'center',
                                'padding': '12px',
                                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                                'fontSize': '14px',
                                'border': 'none',
                                'borderBottom': f'1px solid {cores["border"]}'
                            },
                            style_header={
                                'backgroundColor': cores['background'],
                                'color': cores['text'],
                                'fontWeight': '600',
                                'border': 'none',
                                'borderBottom': f'2px solid {cores["border"]}',
                                'cursor': 'pointer'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'filter_query': '{margem} > 50'},
                                    'color': cores['success'],
                                    'fontWeight': '500'
                                },
                                {
                                    'if': {'filter_query': '{margem} < 30'},
                                    'color': cores['secondary'],
                                    'fontWeight': '500'
                                }
                            ],
                            page_size=12,
                            style_table={'overflowX': 'auto'}
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [Output('cards-metricas', 'children'),
     Output('grafico-principal', 'figure'),
     Output('grafico-anual', 'figure'),
     Output('tabela-simples', 'data')],
    [Input('filtro-ano', 'value')]
)
def atualizar_dashboard(ano_selecionado):
    if ano_selecionado == 'todos':
        df_filtrado = df.copy()
        titulo_periodo = "Todos os Anos"
    else:
        df_filtrado = df[df['ano'] == ano_selecionado].copy()
        titulo_periodo = f"Ano {ano_selecionado}"
    
    receita_total = df_filtrado['receita'].sum()
    despesas_total = df_filtrado['despesas'].sum()
    lucro_total = df_filtrado['lucro'].sum()
    margem_media = (lucro_total / receita_total * 100) if receita_total > 0 else 0
    
    cards = [
        html.Div(
            style={
                'backgroundColor': cores['surface'],
                'padding': '24px',
                'borderRadius': '8px',
                'border': f'1px solid {cores["border"]}',
                'textAlign': 'center'
            },
            children=[
                html.P('Receita Total', style={'margin': '0 0 8px 0', 'fontSize': '0.875rem', 'color': cores['muted']}),
                html.H2(formatar_real(receita_total), 
                        style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '600', 'color': cores['success']})
            ]
        ),
        html.Div(
            style={
                'backgroundColor': cores['surface'],
                'padding': '24px',
                'borderRadius': '8px',
                'border': f'1px solid {cores["border"]}',
                'textAlign': 'center'
            },
            children=[
                html.P('Despesas Totais', style={'margin': '0 0 8px 0', 'fontSize': '0.875rem', 'color': cores['muted']}),
                html.H2(formatar_real(despesas_total), 
                        style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '600', 'color': cores['secondary']})
            ]
        ),
        html.Div(
            style={
                'backgroundColor': cores['surface'],
                'padding': '24px',
                'borderRadius': '8px',
                'border': f'1px solid {cores["border"]}',
                'textAlign': 'center'
            },
            children=[
                html.P('Lucro Total', style={'margin': '0 0 8px 0', 'fontSize': '0.875rem', 'color': cores['muted']}),
                html.H2(formatar_real(lucro_total), 
                        style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '600', 'color': cores['primary']})
            ]
        ),
        html.Div(
            style={
                'backgroundColor': cores['surface'],
                'padding': '24px',
                'borderRadius': '8px',
                'border': f'1px solid {cores["border"]}',
                'textAlign': 'center'
            },
            children=[
                html.P('Margem Média', style={'margin': '0 0 8px 0', 'fontSize': '0.875rem', 'color': cores['muted']}),
                html.H2(f'{margem_media:.1f}%', 
                        style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '600', 'color': cores['text']})
            ]
        )
    ]
    
    fig_principal = go.Figure()
    
    if not df_filtrado.empty:
        fig_principal.add_trace(go.Scatter(
            x=df_filtrado['data'],
            y=df_filtrado['receita'],
            mode='lines+markers',
            name='Receitas',
            line=dict(color=cores['success'], width=2),
            marker=dict(size=6, color=cores['success']),
            hovertemplate='<b>Receitas</b><br>%{x|%b/%Y}<br>%{y:$,.2f}<extra></extra>'
        ))
        
        fig_principal.add_trace(go.Scatter(
            x=df_filtrado['data'],
            y=df_filtrado['despesas'],
            mode='lines+markers',
            name='Despesas',
            line=dict(color=cores['secondary'], width=2),
            marker=dict(size=6, color=cores['secondary']),
            hovertemplate='<b>Despesas</b><br>%{x|%b/%Y}<br>%{y:$,.2f}<extra></extra>'
        ))
        
        fig_principal.add_trace(go.Scatter(
            x=df_filtrado['data'],
            y=df_filtrado['lucro'],
            mode='lines+markers',
            name='Lucro',
            line=dict(color=cores['primary'], width=2),
            marker=dict(size=6, color=cores['primary']),
            hovertemplate='<b>Lucro</b><br>%{x|%b/%Y}<br>%{y:$,.2f}<extra></extra>'
        ))
    
    fig_principal.update_layout(
        title=f'Evolução Mensal - {titulo_periodo}',
        title_font_size=16,
        title_font_color=cores['text'],
        paper_bgcolor='white',
        plot_bgcolor='white',
        font_color=cores['text'],
        font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            showline=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            showline=False,
            zeroline=False,
            tickformat='$,.0f'
        ),
        hovermode='x unified'
    )
    
    if ano_selecionado == 'todos':
        df_anual = df.groupby('ano').agg({
            'receita': 'sum',
            'despesas': 'sum',
            'lucro': 'sum'
        }).reset_index()
    else:
        df_anual = df_filtrado.groupby(['ano', 'mes_num', 'mes']).agg({
            'receita': 'sum',
            'despesas': 'sum',
            'lucro': 'sum'
        }).reset_index().sort_values('mes_num')
        df_anual['x_label'] = df_anual['mes'].apply(lambda x: x[:3])
    
    fig_anual = go.Figure()
    
    if ano_selecionado == 'todos':
        x_data = df_anual['ano']
        titulo_anual = 'Comparativo por Ano'
    else:
        x_data = df_anual['x_label']
        titulo_anual = f'Comparativo Mensal - {ano_selecionado}'
    
    fig_anual.add_trace(go.Bar(
        name='Receitas',
        x=x_data,
        y=df_anual['receita'],
        marker_color=cores['success'],
        hovertemplate='<b>Receitas</b><br>%{x}<br>%{y:$,.2f}<extra></extra>'
    ))
    fig_anual.add_trace(go.Bar(
        name='Despesas',
        x=x_data,
        y=df_anual['despesas'],
        marker_color=cores['secondary'],
        hovertemplate='<b>Despesas</b><br>%{x}<br>%{y:$,.2f}<extra></extra>'
    ))
    fig_anual.add_trace(go.Bar(
        name='Lucro',
        x=x_data,
        y=df_anual['lucro'],
        marker_color=cores['primary'],
        hovertemplate='<b>Lucro</b><br>%{x}<br>%{y:$,.2f}<extra></extra>'
    ))
    
    fig_anual.update_layout(
        title=titulo_anual,
        title_font_size=16,
        title_font_color=cores['text'],
        paper_bgcolor='white',
        plot_bgcolor='white',
        font_color=cores['text'],
        font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        margin=dict(l=20, r=20, t=40, b=20),
        barmode='group',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            type='category'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            showline=False,
            zeroline=False,
            tickformat='$,.0f'
        )
    )
    
    df_tabela = df_filtrado.copy()
    df_tabela['receita_formatada'] = df_tabela['receita'].apply(formatar_real)
    df_tabela['despesas_formatada'] = df_tabela['despesas'].apply(formatar_real)
    df_tabela['lucro_formatado'] = df_tabela['lucro'].apply(formatar_real)
    df_tabela['margem'] = (df_tabela['lucro'] / df_tabela['receita'] * 100).round(1)
    
    tabela_dados = df_tabela[['mes_ano', 'receita_formatada', 'despesas_formatada', 'lucro_formatado', 'margem']].to_dict('records')
    
    return cards, fig_principal, fig_anual, tabela_dados

@server.route("/")
def index():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: {cores['background']};
                color: {cores['text']};
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                text-align: center;
                max-width: 500px;
                padding: 48px 32px;
                background-color: {cores['surface']};
                border-radius: 12px;
                border: 1px solid {cores['border']};
                margin: 24px;
            }}
            h1 {{
                font-size: 2.25rem;
                font-weight: 700;
                margin-bottom: 8px;
                color: {cores['text']};
            }}
            p {{
                font-size: 1.125rem;
                margin-bottom: 32px;
                color: {cores['muted']};
            }}
            .btn {{
                background-color: {cores['primary']};
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                font-size: 1rem;
                font-weight: 500;
                display: inline-block;
                transition: background-color 0.2s;
            }}
            .btn:hover {{
                background-color: #1d4ed8;
            }}
            .stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin-top: 32px;
                text-align: center;
            }}
            .stat {{
                padding: 16px;
                background-color: {cores['background']};
                border-radius: 8px;
                border: 1px solid {cores['border']};
            }}
            .stat-value {{
                font-size: 1.25rem;
                font-weight: 600;
                color: {cores['primary']};
            }}
            .stat-label {{
                font-size: 0.875rem;
                color: {cores['muted']};
                margin-top: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dashboard</h1>
            <p>Dashboard Financeiro Simplificado</p>
            <a href="/dashboard/" class="btn">Acessar Dashboard</a>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{formatar_real(df['receita'].sum())}</div>
                    <div class="stat-label">Receita Total</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{formatar_real(df['lucro'].sum())}</div>
                    <div class="stat-label">Lucro Total</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(df)}</div>
                    <div class="stat-label">Meses</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{(df['lucro'].sum()/df['receita'].sum()*100):.1f}%</div>
                    <div class="stat-label">Margem</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Dashboard Financeiro - Servidor Iniciado")
    print("-" * 40)
    print(f"URL: http://127.0.0.1:5000/dashboard/")
    print("-" * 40)
    server.run(debug=True, port=5000)

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
        "Janeiro": {"receita": 4200.50, "despesas": 2480.30, "lucro": 1720.20},
        "Fevereiro": {"receita": 3850.40, "despesas": 2100.75, "lucro": 1749.65},
        "Março": {"receita": 2950.80, "despesas": 1420.35, "lucro": 1530.45},
        "Abril": {"receita": 2680.90, "despesas": 1315.60, "lucro": 1365.30},
        "Maio": {"receita": 5140.25, "despesas": 2785.70, "lucro": 2354.55},
        "Junho": {"receita": 4620.10, "despesas": 2295.45, "lucro": 2324.65},
        "Julho": {"receita": 3975.35, "despesas": 2460.90, "lucro": 1514.45},
        "Agosto": {"receita": 3100.60, "despesas": 1685.40, "lucro": 1415.20},
        "Setembro": {"receita": 3525.70, "despesas": 1940.25, "lucro": 1585.45},
        "Outubro": {"receita": 3890.85, "despesas": 2105.30, "lucro": 1785.55},
        "Novembro": {"receita": 4450.40, "despesas": 2570.75, "lucro": 1879.65},
        "Dezembro": {"receita": 4985.25, "despesas": 2430.10, "lucro": 2555.15}
    },
    "2024": {
        "Janeiro": {"receita": 4325.30, "despesas": 2275.20, "lucro": 2050.10},
        "Fevereiro": {"receita": 4180.60, "despesas": 2390.45, "lucro": 1790.15},
        "Março": {"receita": 3655.75, "despesas": 1870.35, "lucro": 1785.40},
        "Abril": {"receita": 2850.90, "despesas": 1510.70, "lucro": 1340.20},
        "Maio": {"receita": 4720.40, "despesas": 2885.30, "lucro": 1835.10},
        "Junho": {"receita": 3950.65, "despesas": 2165.55, "lucro": 1785.10},
        "Julho": {"receita": 3125.10, "despesas": 1540.25, "lucro": 1584.85},
        "Agosto": {"receita": 2980.35, "despesas": 1655.20, "lucro": 1325.15},
        "Setembro": {"receita": 3410.50, "despesas": 1725.35, "lucro": 1685.15},
        "Outubro": {"receita": 4280.70, "despesas": 2520.40, "lucro": 1760.30},
        "Novembro": {"receita": 3965.85, "despesas": 2365.20, "lucro": 1600.65},
        "Dezembro": {"receita": 5100.20, "despesas": 2620.30, "lucro": 2479.90}
    },
    "2025": {
        "Janeiro": {"receita": 3820.40, "despesas": 1920.30, "lucro": 1900.10},
        "Fevereiro": {"receita": 4590.25, "despesas": 2285.75, "lucro": 2304.50},
        "Março": {"receita": 3480.60, "despesas": 1795.40, "lucro": 1685.20},
        "Abril": {"receita": 3760.75, "despesas": 1985.35, "lucro": 1775.40},
        "Maio": {"receita": 5280.90, "despesas": 2710.40, "lucro": 2570.50},
        "Junho": {"receita": 4940.80, "despesas": 2490.35, "lucro": 2450.45},
        "Julho": {"receita": 4120.65, "despesas": 2135.30, "lucro": 1985.35}
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

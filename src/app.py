from dash import Dash, html, dcc, Input, Output # utilizado para implementação da biblioteca Dash (gerador de gráficos)
import plotly.express as px # utilizado para implementação do Protly (customizador de gráficos)
import pandas as pd # utilizado para implementação do Pandas (analisador de dados)
import os #utilizado para implementar o OS (rastreador de dados)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# inicialização da biblioteca Dash
app = Dash(__name__, external_stylesheets=external_stylesheets) # inicialização do projeto dash
app.config.suppress_callback_exceptions = True # configuração de certificação e validação do callback


# utilizado para dicrecionar os caminhos para os arquivos Excel que contêm os dados que serão analisados
file_path_turma = os.path.join(os.path.dirname(__file__), "data/tabela_desempenho_da_turma.xlsx")
file_path_estudante = os.path.join(os.path.dirname(__file__), "data/desempenho_estudante_turma.xlsx")
file_path_submissoes = os.path.join(os.path.dirname(__file__), "data/submissoes_por_dia.xlsx")
file_path_dificuldade = os.path.join(os.path.dirname(__file__), "data/tabela_de_desempnho_por_dificuldade.xlsx")
file_path_question = os.path.join(os.path.dirname(__file__), "data/questions_by_difficulty_with_title.xlsx")

# carrega os dados dos arquivos Excel
df_turma = pd.read_excel(file_path_turma)
df_estudante = pd.read_excel(file_path_estudante)
df_submissoes = pd.read_excel(file_path_submissoes)
df_dificuldade = pd.read_excel(file_path_dificuldade)
df_questions_difficulty = pd.read_excel(file_path_question)

# modifica o DataFrame reformulando os dados (desempenho estudante)
df_estudante_exp = df_estudante.explode(['expressoes', 'estrutura_de_decisao', 'repeticao_condicional', 'repeticao_contada', 'vetores'])
df_estudante_exp = df_estudante_exp.melt(id_vars='user_id', value_vars=['expressoes', 'estrutura_de_decisao', 'repeticao_condicional', 'repeticao_contada', 'vetores'])
df_estudante_exp.rename(columns={'variable': 'status'}, inplace=True)

# modifica o DataFrame reformulando os dados (desempenho turma)
df_turma_long = df_turma.melt(id_vars='list', value_vars=['hits', 'parcial', 'undone'])
df_turma_long['status'] = df_turma_long['variable'].map({'hits': 'Concluído', 'parcial': 'Incompleto', 'undone': 'Pendente'})

# usado para criar o gráfico de barras para mostrar o desempenho da turma por lista de exercícios
fig_turma = px.bar(df_turma_long, x="list", y="value",
                   color="status",
                   title="Desempenho da Turma por Lista",
                   labels={"list": "Lista de Exercícios", "value": "Número de Submissões", "status": "Status"},
                   template="plotly_dark")

# usado para criar o gráfico de linha para mostrar o número de submissões por dia
fig_submissoes = px.line(df_submissoes, x="data", y="qnt_de_submissoes",
                         title="Número de Submissões por Dia",
                         labels={"data": "Data", "qnt_de_submissoes": "Número de Submissões"},
                         template="plotly_dark")

# modifica o DataFrame reformulando os dados (desempenho por dificuldade) e renomeando colunas
df_dificuldade_exp = df_dificuldade.melt(id_vars='user_id', value_vars=['muito_faceis', 'faceis', 'medias', 'dificeis', 'muito_dificeis'])
df_dificuldade_exp.rename(columns={'variable': 'dificuldade', 'value': 'submissoes'}, inplace=True)
df_dificuldade_exp['submissoes'] = df_dificuldade_exp['submissoes'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df_dificuldade_exp[['Fácil', 'Médio', 'Difícil']] = pd.DataFrame(df_dificuldade_exp['submissoes'].tolist(), index=df_dificuldade_exp.index)
df_dificuldade_long = df_dificuldade_exp.melt(id_vars=['user_id', 'dificuldade'], value_vars=['Fácil', 'Médio', 'Difícil'])
df_dificuldade_long['dificuldade'] = df_dificuldade_long['dificuldade'].map({'muito_faceis': 'Muito Fáceis', 'faceis': 'Fáceis', 'medias': 'Médias', 'dificeis': 'Difíceis', 'muito_dificeis': 'Muito Difíceis'})


# usado para criar o gráfico de barras para mostrar o desempenho dos estudantes por nível de dificuldade
fig_dificuldade = px.histogram(df_dificuldade_long, x="dificuldade", y="value",
                        color="variable",
                        title="Desempenho dos Estudantes por Dificuldade",
                        labels={"dificuldade": "Nível de Dificuldade", "value": "Quantidade de Submissões", "variable": "Tipo"},
                        template="plotly_dark")



fig_questions_by_difficulty = px.bar(df_questions_difficulty, x='title', y='percentage',
                                     title='Percentual de acerto por questão',
                                     labels={"data": "Data", "percentage": "Percentual"},
                                     template="plotly_dark")

# utilizado para criar o layout de aplicação e criar diferentes abas para cada gráfico
app.layout = html.Div(children=[
    html.H1(children='DataViewer inPacta'),
    html.H2(children='Gráficos do Desempenho dos Estudantes'),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='grafico_desempenho_turma',
                figure=fig_turma
            )
        ], className='five columns'),

        html.Div([
            dcc.Graph(
                id='grafico_submissoes_dia',
                figure=fig_submissoes
            )
        ], className='five columns'),
            
        html.Div([
            
            dcc.Graph(
                id='grafico_desempenho_estudante'
            ),
            dcc.Dropdown(
                id='dropdown_estudante',
                options=[{'label': str(id), 'value': id} for id in df_estudante['user_id'].unique()],
                value=df_estudante['user_id'].unique()[0]  
            ),
            dcc.Dropdown(
                id='dropdown_assunto',
                options=[
                    {'label': 'Expressões', 'value': 'expressoes'},
                    {'label': 'Estrutura de Decisão', 'value': 'estrutura_de_decisao'},
                    {'label': 'Repetição Condicional', 'value': 'repeticao_condicional'},
                    {'label': 'Repetição Contada', 'value': 'repeticao_contada'},
                    {'label': 'Vetores', 'value': 'vetores'}
                ],
                value='expressoes'  # valor inicial do dropdown de assuntos
            )
        ], className='five columns'),

        html.Div([
            dcc.Graph(
                id='grafico_desempenho_dificuldade',
                figure=fig_dificuldade
            )
        ], className='five columns'),
        
        html.Div([
            dcc.Dropdown(
                id="dropdown_question",
                options=[
                    {'label': '0 - 25% (Taxa muito baixa de acertos)', 'value': 'first_quarter'},
                    {'label': '25 - 50% (Taxa baixa de acertos)', 'value': 'second_quarter'},
                    {'label': '50 - 75% (Taxa boa de acertos)', 'value': 'third_quarter'},
                    {'label': '75 - 100% (Taxa muito boa de acertos)', 'value': 'fourth_quarter'},
                ],
                value='first_quarter'
            ),
            dcc.Graph(
                id='question_difficulty',
                 figure=fig_questions_by_difficulty
            ),
            
        ], className='five columns'),
    
    ], className='custom-container'),
])

# Callback utilizada para atualizar o gráfico de desempenho por estudante selecionado
@app.callback(
    Output('grafico_desempenho_estudante', 'figure'),
    [Input('dropdown_estudante', 'value'),
     Input('dropdown_assunto', 'value')]
)


# modelos de filtragem
def update_estudante_graph(selected_user_id, selected_assunto):
    # filtragem de dados
    df_filtered = df_estudante_exp[(df_estudante_exp['user_id'] == selected_user_id) & (df_estudante_exp['status'] == selected_assunto)]
    
    # apresentação de valores
    df_filtered['value'] = df_filtered['value'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    
    # usado para adicionar colunas separadas para cada valor dentro dos colchetes
    df_filtered[['Concluído', 'Incompleto', 'Pendente']] = pd.DataFrame(df_filtered['value'].tolist(), index=df_filtered.index)
    
    # usado para preparar dados para o gráfico
    df_pivot = df_filtered.groupby('user_id')[['Concluído', 'Incompleto', 'Pendente']].sum().reset_index()
    
    # criação do gráfico
    fig = px.bar(df_pivot, x='user_id', y=['Concluído', 'Incompleto', 'Pendente'], 
                 title=f"Desempenho do Estudante {selected_user_id} em {selected_assunto}",
                 labels={"user_id": "ID do Estudante", "value": "Quantidade"},
                 text_auto=True,
                 template="plotly_dark")

    return fig

# @app.callback(
#     Output('dropdown_question', 'figure'),
#     Input('dropdown_question', 'value')
# )

def update_question_graph(selected_percentage):
    if selected_percentage == '0 - 25% (Taxa muito baixa de acertos)':
        print('teste')
        ...
    #return df_filtered



# execução do aplicativo

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

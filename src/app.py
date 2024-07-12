# ferramentas importadas
from dash import Dash, html, dcc, Input, Output  # importação do dash
import plotly.express as px # ferramenta especifica para personalização de gráficos
import pandas as pd # ferramenta para leitura de dados das planilhas
import os # ferramenta utilizada para auxílio de rastreamento dos arquivos .xlsx


#criador do servidor
app = Dash(__name__)


# utilizado especificamente para modificações no HTML (espeficamente usado nesse código para implementar a fonte)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>DataViewer inPacta</title>
        <link href="https://fonts.cdnfonts.com/css/florida-project" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# utilizado para rastrear os arquivos .xlsx
file_path_turma = os.path.join(os.path.dirname(__file__), "tabela_desempenho_da_turma.xlsx")
file_path_estudante = os.path.join(os.path.dirname(__file__), "desempenho_estudante_turma.xlsx")
#file_path_submissoes = os.path.join(os.path.dirname(__file__), "submissoes_por_dia.xlsx")


# utilizado para ler e carregar os dados das planilhas
df_turma = pd.read_excel(file_path_turma)
df_estudante = pd.read_excel(file_path_estudante)
#df_submissoes = pd.read_excel(file_path_submissoes)


# utilizado para criar o gráfico de BARRAS para desempenho da turma
fig_turma = px.bar(df_turma, x="list", y=["hits", "parcial", "undone"], # representação em plano cartesiano + filtro de seleção de amostra
                   barmode="group", title="Desempenho da Turma por Lista", #Título do gráfico
                   labels={"list": "Lista de Exercícios", "value": "Número de Submissões"}, #Variáveis lidas
                   template="plotly_white") # cor e modelo de template


# utilizado para criar o gráfico de PONTOS para desempenho dos estudantes filtrados
fig_estudante = px.scatter(df_estudante, x="user_id", y="expressoes", # representação em plano cartesiano
                           title="Desempenho dos Estudantes em Expressões", #Título do gráfico
                           labels={"user_id": "ID do Estudante", "expressoes": "Número de Acertos"}, #Variáveis lidas
                           template="plotly_white") # cor e modelo de template


# utilizado para criar o gráfico de LINHA para submissoes por dia

# fig_submissoes = px.line(df_submissoes, x="data", y="qnt_de_submissoes", # representação em plano cartesiano
#                          title="Número de Submissões por Dia", #Título do gráfico
#                          labels={"data": "Data", "qnt_de_submissoes": "Número de Submissões"}, #Variáveis lidas
#                          template="plotly_white") # cor e modelo de template


# opções para realizar o dropdown
opcoes = list(df_estudante['user_id'].unique())
opcoes.append("GERAL")


# utilizado para customização de alguns recursos HTML importados do próprio Dash
app.layout = html.Div(children=[
    html.H1(children='DataViewer inPacta: Desempenho dos Estudantes'),
    html.H2(children='Gráficos de Desempenho por Lista e por Estudante'),


    html.Div(children='''
        Obs: Os gráficos mostram o desempenho da turma e dos estudantes em diferentes listas de atividade estudantis.
    '''),


    # geradores e estilizadores HTML dos gráficos
    dcc.Tabs([
        dcc.Tab(label='Desempenho da Turma', children=[
            dcc.Graph(
                id='grafico_desempenho_turma',
                figure=fig_turma
            )
        ]),
        dcc.Tab(label='Desempenho por Estudantes', children=[
            dcc.Dropdown(opcoes, value='GERAL', id='lista_estudantes'),
            dcc.Graph(
                id='grafico_desempenho_estudantes',
                figure=fig_estudante
            )
        ]),
        # dcc.Tab(label='Submissões por Dia', children=[
        #     dcc.Graph(
        #         id='grafico_submissoes_dia',
        #         figure=fig_submissoes
        #     )
        #]),
    ])
], className='custom-container')


# utilizado para atualizar o gráfico de desempenho dos estudantes após tal função ser chamada
@app.callback(
    Output('grafico_desempenho_estudantes', 'figure'),
    Input('lista_estudantes', 'value')
)
# atualização após chamar a função GERAL ( onde ficará a amostra uma tabela de maneira geral de todos os dados), função essa já padrão.
def update_output(value):
    if value == "GERAL":
        fig = px.scatter(df_estudante, x="user_id", y="expressoes", # representação em plano cartesiano
                         title="Desempenho dos Estudantes em Expressões", #Título do gráfico
                         labels={"user_id": "ID do Estudante", "expressoes": "Número de Acertos"}, #Variáveis lidas
                         template="plotly_white") # cor e modelo de template
       
# atualização após chamar a função de filtrar e selecionar o estudante (abre lista por user_id [id]) onde é possível selecionar o estudante específico.
    else:
        tabela_filtrada = df_estudante.loc[df_estudante['user_id'] == value, :]
        fig = px.scatter(tabela_filtrada, x="user_id", y="expressoes", # representação em plano cartesiano
                         title=f"Desempenho do Estudante {value} em Expressões", #Título do gráfico
                         labels={"user_id": "ID do Estudante", "expressoes": "Número de Acertos"}, #Variáveis lidas
                         template="plotly_white") # cor e modelo de template
    return fig


# Inicialização do servidor
if __name__ == '__main__':
    app.run_server(debug=True)

# Desafio: Plataforma de Streaming com Python e SQL

## Cenário

Você é um analista de dados em uma plataforma de streaming. O banco de dados SQL possui as seguintes tabelas:

* **Filmes:** (id, titulo, genero, diretor, ano\_lancamento)
* **Series:** (id, titulo, genero, criador, ano\_lancamento, temporadas)
* **Usuarios:** (id, nome, idade, plano)
* **Visualizacoes:** (usuario\_id, conteudo\_id, tipo\_conteudo, data\_visualizacao)

## Seu Desafio

1.  **Conexão e Dados de Teste:**
    * Crie um banco de dados SQLite e as tabelas acima.
    * Insira dados de teste fictícios para filmes, séries, usuários e visualizações.
2.  **Análise de Dados:**
    * Escreva uma função que receba um gênero como entrada e retorne os 5 filmes mais populares desse gênero (mais visualizados).
    * Crie uma função que calcule a média de idade dos usuários que assistiram a séries de drama.
    * Implemente uma função que retorne os criadores de séries que lançaram mais de 2 séries no último ano.
    * Crie uma função que mostre o plano mais popular entre os usuarios.
3.  **Relatórios (Opcional):**
    * Gere um relatório em formato de texto ou CSV com as informações dos filmes e séries mais visualizados por gênero.

## Dicas

* Use a biblioteca `datetime` para trabalhar com datas nas consultas SQL.
* Considere o uso de subconsultas (subqueries) para consultas mais complexas.
* Use a função `COUNT` do SQL para contar o número de visualizações.
* Use a função `AVG` do SQL para calcular a média de idade.
* Use a função `MAX` do SQL para encontrar o plano mais popular.

## Exemplo de Consulta SQL

```sql
SELECT Filmes.titulo
FROM Filmes
JOIN Visualizacoes ON Filmes.id = Visualizacoes.conteudo_id
WHERE Filmes.genero = 'Ação' AND Visualizacoes.tipo_conteudo = 'Filme'
GROUP BY Filmes.titulo
ORDER BY COUNT(*) DESC
LIMIT 5;

SELECT AVG(Usuarios.idade)
FROM Usuarios
JOIN Visualizacoes ON Usuarios.id = Visualizacoes.usuario_id
JOIN Series ON Visualizacoes.conteudo_id = Series.id
WHERE Series.genero = 'Drama' AND Visualizacoes.tipo_conteudo = 'Serie';
"""

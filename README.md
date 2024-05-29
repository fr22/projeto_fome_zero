# 1. Problema de negócio
*	Neste projeto de ciência de dados foi feito um dashbord com métricas de uma empresa fictícia, a Fome Zero, baseados em dados da empresa Zomato disponíveis publicamente no Kaggle.
*	A Fome Zero é uma empresa do tipo Marketplace que diponibiliza de forma online informações sobre restaurantes em diversos países com o objetivo de conectar restaurantes e consumidores de comida. Isso possibilita que pessoas possam escolher um restaurante para ir, com base em informações tais como o tipo de culinária, a localização, o preço e a nota de avaliação.
*	A plataforma possui diferentes fontes de receita, cuja principal é publicidade. Surge então a necessidade de se analisar os dados gerados dentro da própria plataforma para se conhecer oportunidades de expansão do negócio.
*	As informações extraídas foram agrupadas de acordo com três visões diferentes: Visão Países, Visão Cidades e Visão Culinárias. E o usuário do dashbord –  CEO e pessoas de negócio da Fome Zero – podem filtrar as informações por diferentes parâmetros.

# 2. Premissas do negócio
  1. Análise realizada a partir de uma dataset que é atualizado semanalmente.
  2. O modelo de negócio assumido foi Marketplace.
  3. As três visões abordadas foram:  Visão Países, Visão Cidades e Visão Culinárias.
# 3. Estratégia da solução
  1. Primeiro foi feito um notebook no JupyterLab para prototipar a solução buscando responder questões levantadas pelo CEO e gerar gráficos que seriam usados no dashboard.
  2. Para cada visão o dashbord apresenta as seguintes métricas:
  1. Visão cidades:
      1. Top 10 cidades com mais restaurantes registrados
      2. Top 7 cidades com mais restaurantes cuja média de avaliação é acima de 4 
      3. Top 7 cidades com mais restaurantes cuja média de avaliação é abaixo de 2.5 
      4. Top 10 cidades com mais tipos de culinárias 
  2. Visão países:
      1. Quantidade de restaurantes registrados por país
      2. Quantidade de cidades registadas por país
      3. Média de avaliações por país
      4. Média de preço de prato de duas pessoas por país
  3. Visão culinárias
      1. Melhores Restaurantes dos Principais tipos Culinários 
      2. Top 5 restaurantes 
      3. Top 5 melhores culinárias 
      4. Top 5 piores culinárias
# 4. Top 3 insights de dados
  1. A culinária brasileira está entre as piores embora o Brasil possua restaurantes muito bem avaliados.
  2. A Índia possui a maior quantidade de restaurantes e cidades.
  3. São Paulo está entre as cidades com maior diversidade de culinárias.
# 5. O produto final do projeto
  1. Um painel disponível online contendo diversas métricas do negócio.
  2. O painel pode ser acessado pelo seguinte link: https://projetofomezero-dkqjhrzamivfkazeq66y2e.streamlit.app/
# 6. Conclusão
  1. O objetivo desse projeto foi gerar um dashbord hospedado em uma Cloud que pudesse ser utilizado por diferentes pessoas da empresa. O dashboard foi concluído.
  2. A zona de maior relevância para os negócios da empresa é a Índia.
# 7. Próximos passos
  1. Criar mais filtros.
  2. Gerar métricas de potencial de faturamento.

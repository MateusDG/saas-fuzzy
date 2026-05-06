# Selecao De Dataset Publico - Fase 5

## Objetivo

Definir criterio de selecao de dataset publico para avaliacao academica
reproduzivel do recomendador, sem depender de dados privados de clientes da
Kouzina.

## Principio Central

O catalogo da Kouzina e o dominio aplicado do projeto, mas sozinho nao basta
como base de avaliacao academica reproduzivel, porque:

- nao e um dataset publico padronizado;
- pode mudar com o tempo sem versionamento academico;
- nao possui, nesta fase, interacoes reais abertas para comparacao cientifica;
- depende de autorizacao comercial e contexto local.

Por isso, a avaliacao offline da Fase 5 deve usar dataset publico como base de
comparabilidade e reprodutibilidade.

## Criterios De Selecao

Um candidato deve atender, idealmente, aos itens abaixo:

1. licenca ou termos que permitam uso academico;
2. disponibilidade publica estavel;
3. interacoes usuario-item suficientes para top-k;
4. metadados de itens com categoria ou texto;
5. tamanho administravel para execucao local;
6. possibilidade de split temporal ou por usuario;
7. documentacao clara de colunas e formato;
8. aderencia razoavel a e-commerce de bens de consumo duraveis.

## Candidatos Sugeridos (Sem Download Automatico)

### 1) Amazon Reviews (subset por categoria)

Pros:

- grande volume de interacoes;
- metadados ricos de item;
- amplamente usado em literatura.

Contras:

- volume pode ser muito alto;
- limpeza e recorte exigem trabalho;
- dominio nem sempre alinhado com high-end de cozinha.

### 2) Retailrocket Recommender System Dataset

Pros:

- eventos implicitos de navegacao;
- foco de e-commerce;
- tamanho intermediario.

Contras:

- metadados de item podem ser limitados;
- mapeamento para categoria pode exigir processamento extra.

### 3) Yoochoose / RecSys Challenge (session-based)

Pros:

- benchmark conhecido;
- bom para avaliar recomendacao baseada em evento.

Contras:

- foco em sessao, nao perfil rico de item;
- menos aderente a atributos de produto high-end.

### 4) Instacart Market Basket

Pros:

- estrutura limpa de compra e co-ocorrencia;
- facil para baseline de popularidade/coocorrencia.

Contras:

- dominio alimentar, distante do caso Kouzina;
- baixa transferibilidade semantica para cozinha premium.

## Comparativo Resumido

| Dataset | Interacoes | Metadados De Item | Aderencia Ao Dominio Kouzina | Custo De Preparacao |
| --- | --- | --- | --- | --- |
| Amazon Reviews (subset) | Alta | Alta | Media | Alto |
| Retailrocket | Media/Alta | Media | Media | Medio |
| Yoochoose | Alta | Baixa/Media | Baixa/Media | Medio |
| Instacart | Alta | Media | Baixa | Baixo/Medio |

## Recomendacao Inicial Para Comecar

Recomendacao pragmatica da Fase 5:

- iniciar com um subset controlado de Amazon Reviews orientado a categorias de
  casa/cozinha ou eletrodomesticos;
- limitar tamanho para execucao local;
- documentar exatamente o recorte usado (`source`, filtros, versao, data).

Justificativa:

- oferece equilibrio entre comparabilidade academica e disponibilidade de
  metadados para baseline de conteudo/categoria;
- facilita evolucao futura para ontologia e fuzzy.

## Limitacoes De Adaptacao Para O Dominio Kouzina

- datasets publicos raramente refletem posicionamento high-end;
- campos tecnicos especificos (ex.: voltagem, instalacao) podem estar ausentes;
- sinal de preco/premium pode ser incompleto;
- comportamento de usuarios em datasets publicos pode divergir de publico
  premium consultivo.

Essas limitacoes devem ser declaradas explicitamente na analise de resultados.

## Governanca De Dados E LGPD

- nao usar dados reais de clientes da Kouzina sem autorizacao formal e base
  legal;
- nao coletar PII na fase de benchmark offline;
- manter dados publicos e dados locais privados separados;
- registrar origem e licenca de cada dataset usado.

## Decisao De Fase

Nesta fase, o projeto deve:

- documentar selecao;
- preparar estrutura local de dados publicos;
- executar baselines offline com recorte reproduzivel.

Nesta fase, o projeto nao deve:

- baixar dataset gigante automaticamente por script;
- assumir resultado definitivo sem comparacao transparente;
- misturar dados publicos com dados sensiveis de cliente.

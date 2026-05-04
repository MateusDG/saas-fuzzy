# Politica De Relacoes Do Recomendador

Este documento resume a politica pratica de relacoes para orientar a Fase 4.8
sem alterar o comportamento atual do sistema. Ele transforma a pesquisa de
`docs/PHASE_4_8_VALIDACAO_KOUZINA.md` em criterios de revisao comercial.

Esta politica nao implementa fuzzy, ontologia, CTR, painel, deploy ou mudanca
no ranking v0. Ela serve para conduzir a reuniao com a Kouzina e preparar
ajustes futuros.

## Objetivo

Separar quatro classes de relacao:

- relacoes universais de cozinha, gourmet e eletrodomesticos premium;
- relacoes contextuais, que dependem do projeto ou ambiente;
- relacoes especificas da Kouzina, ligadas ao catalogo e curadoria local;
- relacoes fracas ou proibidas, que devem ser vetadas ou restringidas.

## Relacoes Universais

Sao relacoes sustentadas por uso, funcao, instalacao ou compatibilidade tecnica.
Elas tendem a valer alem da loja-piloto.

Exemplos fortes:

- `Cooktop -> Coifa`: relacao tecnico-funcional de coccao e ventilacao.
- `Coifa -> Cooktop`: complemento natural, desde que largura, instalacao e uso
  facam sentido.
- `Cuba -> Misturador`: complementaridade estrutural e de uso.
- `Misturador -> Cuba`: complemento direto quando acabamento e instalacao
  forem coerentes.
- `Forno -> Cooktop`: composicao comum de cozinha planejada.
- `Cooktop -> Forno`: composicao de projeto e suite de coccao.
- `Lava-loucas -> Cuba/Misturador`: relacao funcional de area molhada, com
  cautela para instalacao e marcenaria.
- `Cafeteira embutida -> Forno/Micro-ondas da mesma linha`: relacao de suite
  visual em built-ins premium.

Pergunta de validacao: essa relacao continuaria fazendo sentido em outro
catalogo high-end semelhante?

## Relacoes Contextuais

Sao relacoes plausiveis em determinados ambientes ou projetos, mas nao devem
virar regra universal forte sem contexto.

Exemplos:

- `Adega -> Cervejeira/Frigobar`: faz sentido em estacao de bebidas.
- `Churrasqueira -> Adega/Cervejeira/Frigobar`: faz sentido em espaco gourmet,
  mas pode depender do tipo de projeto.
- `Churrasqueira -> Coifa/Cooktop`: pode fazer sentido em area gourmet coberta,
  mas deve ser revisado por contexto.
- `Forno de Pizza -> Churrasqueira/Adega/Cervejeira`: coerente em area gourmet,
  mas nao obrigatorio.
- `Maquina de Gelo -> Cervejeira/Frigobar/Adega`: coerente em bar, varanda ou
  espaco gourmet.
- `Refrigerador -> Freezer`: complemento de refrigeracao, dependente de
  espaco e projeto.

Pergunta de validacao: essa relacao depende de ambiente, projeto, instalacao,
marcenaria ou consultoria?

## Relacoes Especificas Da Kouzina

Sao relacoes que podem fazer sentido para a Kouzina por mix de catalogo,
posicionamento de marca, estoque, curadoria comercial ou objetivo editorial,
mas nao devem ser tratadas como conhecimento universal.

Exemplos possiveis:

- recomendar itens de uma marca especifica por linha comercial da Kouzina;
- promover uma categoria premium por estrategia editorial;
- aproximar produtos de uma mesma colecao quando a loja validou essa suite;
- priorizar produtos sob consulta quando a venda exige atendimento consultivo;
- destacar itens com maior relevancia comercial em reunioes de projeto.

Essas relacoes devem aparecer em `reviewer_comment` como "especifica Kouzina" e
precisam ser separadas das relacoes universais antes de qualquer ontologia
futura.

## Relacoes Fracas Ou Proibidas

Sao relacoes que devem ser removidas, restringidas ou cair muito no ranking
futuro. A Fase 4.8 deve procurar esses casos no HTML de revisao.

Sinais de alerta:

- mesmo ambiente sem complementaridade real;
- mesma marca puxando produto tecnicamente incompativel;
- faixa premium semelhante substituindo relacao funcional;
- produto decorativo puxando cuba, misturador ou marcenaria sem contexto;
- lavanderia puxando cozinha gourmet;
- refrigeracao puxando coccao sem projeto claro;
- item sob consulta aparecendo no topo sem motivo forte;
- reason generica demais para justificar a sugestao.

Exemplos citados pela pesquisa como fracos ou inadequados:

- acessorio de mesa decorativo puxando cuba, misturador ou painel de
  lava-loucas;
- lavadora ou secadora puxando adega, coifa, forno ou rangetop;
- dispenser de agua puxando churrasqueira ou adega como regra universal.

## Politica Inicial Para Produtos Sob Consulta

No catalogo atual, `Preco venda = 0.00` e tratado como `Sob consulta`.
Atualmente esses produtos:

- ficam com `price = null`;
- continuam disponiveis;
- nao pontuam por faixa de preco proxima;
- podem receber reason `Produto sob consulta.`

Politica de revisao para a Fase 4.8:

- permitir `Sob consulta` quando o produto for configuravel, consultivo, de
  projeto, dealer/showroom ou tecnicamente muito forte para o item atual;
- evitar `Sob consulta` como top-1 quando houver alternativa precificada e
  comercialmente equivalente;
- exigir comentario do especialista quando o item sem preco deve aparecer;
- registrar se o motivo e instalacao, configuracao, projeto, marcenaria ou
  consultoria;
- limitar excesso de itens sem preco no mesmo bloco de recomendacao.

Pergunta central: a ausencia de preco e aceitavel para este contexto de compra
ou reduz confianca na recomendacao?

## Criterios Atuais Do v0

Esta tabela nao muda o codigo. Ela orienta o que revisar na Fase 4.8 e o que
pode virar trabalho futuro.

| Criterio atual | Decisao de politica | Observacao |
| --- | --- | --- |
| Complementaridade de tipo | Manter | Deve continuar como eixo central e ser validada por especialista. |
| Disponibilidade | Manter e refinar futuramente | Separar `in_stock`, `backorder`, `quote_only` e `discontinued` em fase futura. |
| Mesma voltagem | Aumentar futuramente | Pode virar filtro duro em casos tecnicos, mas ainda nao nesta fase. |
| Faixa de preco proxima | Reduzir futuramente | Deve moderar coerencia, nao comandar recomendacao. |
| Mesma marca | Ajustar futuramente | Separar marca, colecao e design line quando houver dados. |
| Mesmo ambiente | Manter como auxiliar | Nao deve puxar item sem complementaridade funcional. |
| Faixa premium semelhante | Transformar em fuzzy futuramente | Util como nuance, fraco como regra binaria. |
| Exclusao do proprio produto | Manter | Regra correta e nao negociavel. |
| Penalizacao de indisponivel | Manter e refinar futuramente | Diferenciar indisponivel, descontinuado e sob consulta. |
| Reason textual | Manter e enriquecer futuramente | Deve ficar mais concreta: instalacao, voltagem, linha, medida e contexto. |

## Como Usar Na Reuniao

Para cada recomendacao revisada, registrar no comentario:

- `universal`, `contextual`, `especifica Kouzina` ou `proibida`;
- `complemento`, `alternativa`, `mesma suite` ou `editorial`;
- dependencia de medida, instalacao, marcenaria, voltagem, largura, acabamento
  ou consultoria;
- se produto sob consulta deve aparecer;
- se a reason esta clara ou precisa ser reescrita.

O resultado esperado nao e mudar o codigo imediatamente. O resultado esperado e
uma base de decisao para ajustes editoriais futuros, dataset de especialista e
preparacao das fases academicas posteriores.

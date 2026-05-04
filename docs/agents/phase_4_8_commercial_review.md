# Fase 4.8 - Revisao Do Consultor Comercial High-End

Este documento registra a avaliacao simulada do agente "Consultor Comercial
High-End da Kouzina" para a reuniao qualitativa da Fase 4.8.

Escopo desta avaliacao:

- atuar como especialista de dominio e venda consultiva, nao como programador;
- avaliar se as recomendacoes ajudam venda premium, projeto, cross-sell,
  upsell e percepcao de valor;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao baixar imagens;
- nao versionar `reports/*.html` ou `reports/*.csv`.

## Diagnostico Comercial

O recomendador v0 esta apto para uma reuniao comercial, mas ainda nao deve ser
tratado como curadoria final da Kouzina. Ele cria bons pontos de partida quando
recomenda itens que ajudam o cliente a fechar um projeto premium: coccao com
exaustao, cuba com misturador, rangetop com forno/coifa, adega com cervejeira
ou frigobar, e zona gourmet com churrasqueira e refrigeracao.

O risco comercial esta nos casos em que a recomendacao parece elevar ticket sem
resolver uma necessidade real do cliente. Em uma loja premium, um item caro nao
e automaticamente bom. A recomendacao precisa parecer consultiva: "isto melhora
seu projeto" e nao "isto tambem e caro".

No CSV de revisao ha 120 linhas. O HTML confirma o uso previsto: comparar
origem e recomendado, discutir score/reason e preencher `reviewer_rating` e
`reviewer_comment`. Tambem aparecem muitos itens `Sob consulta`: 48 linhas com
produto de origem sob consulta e 40 linhas com recomendado sob consulta. Isso
exige uma politica comercial clara antes de expor qualquer carousel real.

## Criterios Comerciais Para Aprovar Recomendacao

- Ajuda a fechar projeto: o item completa uma composicao de cozinha, gourmet,
  lavanderia ou refrigeracao.
- Complementa a jornada do cliente: reduz uma duvida natural do comprador ou
  antecipa um item que o consultor venderia junto.
- Defende ticket medio com valor percebido: o preco maior precisa vir com
  funcao, marca, suite, acabamento, capacidade ou consultoria.
- Nao substitui criterio tecnico por preco: preco deve moderar coerencia, nao
  comandar a recomendacao.
- Marca pesa quando ha linha, suite, colecao ou linguagem visual. Marca pura
  nao deve empurrar produto incompatavel.
- Produto sob consulta precisa ter motivo consultivo: configuracao, projeto,
  showroom, instalacao, marcenaria, medida ou compra assistida.
- A reason precisa ser concreta o bastante para sustentar uma conversa de
  venda. "Mesmo ambiente" e "faixa premium semelhante" ajudam pouco sozinhos.
- A recomendacao deve preservar confianca. Se o cliente percebe empurro de
  ticket, a vitrine perde valor.

## Quando Produto Sob Consulta Deve Aparecer

Produto `Sob consulta` deve aparecer quando a ausencia de preco faz parte da
venda premium e nao prejudica a decisao:

- item configuravel, de projeto ou com dependencia de instalacao;
- item de marca/suite profissional vendido com atendimento consultivo;
- relacao muito forte com o produto atual, com pouca alternativa precificada;
- contexto de projeto completo, como cozinha planejada, espaco gourmet ou
  estacao de bebidas;
- produto que o vendedor da Kouzina naturalmente apresentaria na conversa.

Exemplo observado: `Adega Dual Zone Professional Tecno -> Frigobar Professional
Tecno` ou `Cervejeira Professional Tecno`, todos sob consulta, pode ser
comercialmente defensavel se a linha Professional for uma venda assistida de
estacao de bebidas. Nao deve ser rejeitado apenas por falta de preco.

## Quando Produto Sob Consulta Deve Ser Penalizado

Produto `Sob consulta` deve perder prioridade quando:

- existe alternativa precificada equivalente e mais facil de comprar;
- o item aparece como top-1 sem relacao funcional forte;
- a reason nao explica por que a consulta e necessaria;
- o carousel fica dominado por itens sem preco;
- o produto e apenas "mesma marca", "mesmo ambiente" ou "faixa premium";
- a ausencia de preco pode gerar frustracao em uma jornada de ecommerce.

Politica comercial sugerida: `Sob consulta` pode entrar no top-3, mas nao deve
ser top-1 por padrao quando houver recomendado precificado equivalente,
disponivel e comercialmente claro.

## Relacoes Boas Para Cross-Sell

- `Cooktop/Rangetop -> Coifa`: cross-sell tecnico de coccao e exaustao.
- `Coifa -> Cooktop/Rangetop/Forno`: bom quando largura, instalacao e proposta
  do projeto fecham.
- `Cuba -> Misturador`: cross-sell universal de bancada.
- `Misturador -> Cuba`: forte quando acabamento, furo e instalacao combinam.
- `Forno -> Cooktop/Rangetop`: composicao de cozinha planejada.
- `Rangetop -> Forno/Coifa`: venda consultiva de suite de coccao.
- `Adega -> Cervejeira/Frigobar`: bom em estacao de bebidas.
- `Churrasqueira -> Cervejeira/Adega/Maquina de Gelo`: bom em espaco gourmet,
  desde que a narrativa seja projeto completo.
- `Acessorio de Coifa -> Coifa`: bom quando a compatibilidade de modelo e
  clara.

## Relacoes Que Parecem Apenas Empurrar Ticket

- Lavanderia recomendando cozinha gourmet, como `Lavadora SpeedQueen -> Adega`
  ou `Secadora SpeedQueen -> Forno/Rangetop`. O ticket e premium, mas a
  intencao de compra nao e a mesma.
- Acessorio decorativo ou de mesa recomendando produto tecnico de bancada,
  como `Set Azeite & Vinagre Le Creuset -> Cuba/Misturador/Painel de
  Lava-Loucas`.
- Mesmo ambiente sem complementaridade funcional, principalmente quando o
  ambiente e amplo demais.
- Produto de marca forte recomendando outra categoria sem suite, linha ou uso
  conjunto.
- Item `Sob consulta` no topo apenas por marca, ambiente e premium semelhante.

## Como Diferenciar Tipos De Relacao

`complemento`: o recomendado completa o uso do produto atual. Exemplo:
`Cuba -> Misturador`, `Rangetop -> Coifa`, `Acessorio de Coifa -> Coifa`.

`alternativa`: o recomendado resolve a mesma necessidade em outra faixa,
marca, medida ou configuracao. Deve aparecer em modulo separado de
substituicao, nao como "complete seu projeto".

`mesma suite`: o recomendado pertence a uma familia visual ou linha de
embutidos. Exemplo: `Cafeteira Mythos -> Micro-ondas Mythos`. Aqui marca e
linha pesam mais que preco.

`editorial`: o recomendado e uma escolha de curadoria da Kouzina, por campanha,
mix, margem, showroom ou estrategia comercial. Pode ser valido, mas deve ser
registrado como especifico da Kouzina, nao como relacao universal.

## Exemplos De Recomendacoes Fortes

- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Linea Touch | Franke`
  com score 95: aprovar como venda tecnica se o kit for compativel com modelo,
  largura e instalacao. Rating sugerido: `4` ou `5`.
- `Cuba Box De Embutir e Sobrepor | Franke -> Misturador Monocomando | Franke`:
  cross-sell direto de bancada. Rating sugerido: `5`.
- `Misturador Monocomando | Franke -> Cubas Franke`: bom complemento, com
  confirmacao de furo, altura, acabamento e uso. Rating sugerido: `4` ou `5`.
- `Rangetop Master Bertazzoni -> Forno Bertazzoni`: venda de suite de coccao,
  forte para cozinha planejada high-end. Rating sugerido: `5`.
- `Rangetop Master Bertazzoni -> Coifa 90cm`: forte por exaustao e coccao,
  desde que largura/vazao/instalacao sejam coerentes. Rating sugerido: `4`.
- `Adega Tecno -> Frigobar/Cervejeira Tecno`: bom para estacao de bebidas,
  especialmente em linha Professional sob consulta. Rating sugerido: `4`, ou
  `5` se a Kouzina confirmar venda conjunta recorrente.

## Exemplos De Recomendacoes Fracas

- `Set Azeite & Vinagre Le Creuset -> Cuba Franke`: parece vazamento por
  ambiente/premium. Rating sugerido: `1` ou `2`.
- `Set Azeite & Vinagre Le Creuset -> Misturador Franke`: fraco como
  recomendacao automatica; pode ser editorial, mas nao complemento. Rating
  sugerido: `2`.
- `Set Azeite & Vinagre Le Creuset -> Painel Decorativo Frente Lava-Loucas`:
  remover como complemento. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Adega Elettromec`: cruza lavanderia e bebidas por
  preco/premium, sem venda consultiva clara. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Cooktop e Coifa Mythos`: nao fecha intencao de
  compra. Rating sugerido: `1`.
- `Secadora SpeedQueen -> Fogao Bertazzoni` ou `Rangetop Bertazzoni`: parece
  empurro de ticket por faixa premium. Rating sugerido: `1`.
- `Cervejeira -> Coifa de churrasqueira`: pode ser contextual em area gourmet,
  mas nao deve ser universal nem top-1 sem projeto. Rating sugerido: `2` ou
  `3`.

## O Que Deve Ser Mantido

- Complementaridade funcional como eixo principal da revisao.
- Exclusao do proprio produto.
- Reason textual, mesmo que precise ficar mais concreta no futuro.
- `Sob consulta` como estado comercial valido em premium, mas com criterio.
- Relacoes de suite de marca/linha quando a Kouzina confirmar colecao,
  acabamento ou modulo visual.
- Cross-sell de projeto que o consultor venderia em loja ou showroom.

## O Que Deve Ser Restringido

- Preco proximo e faixa premium como argumentos fortes.
- Mesma marca sem mesma linha, colecao ou compatibilidade.
- Mesmo ambiente amplo como justificativa principal.
- Produtos `Sob consulta` no top-1.
- Cross-sell gourmet quando depender de projeto completo.
- Recomendacoes sem preco em excesso no mesmo bloco.
- Relacoes editoriais que ainda nao foram assumidas pela Kouzina.

## O Que Deve Ser Removido

- Lavanderia recomendando cozinha, gourmet, adega, coifa, forno, cooktop ou
  rangetop.
- Acessorio decorativo/de mesa recomendando produto tecnico de bancada,
  marcenaria ou instalacao.
- Recomendacao sustentada apenas por ticket, preco proximo ou premium
  semelhante.
- Produto `Sob consulta` sem motivo consultivo claro e sem relacao forte.
- Casos de catalogacao suspeita que tratem refrigerador como adega ou produto
  tecnico como categoria errada, ate revisao manual.

## Como Registrar Decisoes No `reviewer_comment`

Usar comentarios curtos, padronizados e acionaveis:

```text
universal; complemento; aprovar; venda consultiva clara.
universal; complemento tecnico; aprovar; depende de largura/instalacao.
contextual; espaco gourmet; aprovar no top-3 se projeto incluir bebidas.
mesma suite; aprovar; marca/linha pesa mais que preco.
curadoria Kouzina; editorial; manter se for prioridade comercial.
sob consulta; permitir; item consultivo/configuravel de projeto.
sob consulta; restringir; nao usar como top-1 com alternativa precificada.
restringir; mesmo ambiente sem complemento funcional suficiente.
remover; parece empurro de ticket por preco/premium.
remover; lavanderia cruzando com cozinha/gourmet.
remover; decorativo puxando produto tecnico sem intencao de compra.
```

## Politica Comercial Para Top-1, Top-3 E Itens Sem Preco

Top-1:

- deve ser complemento funcional, tecnico ou de suite muito claro;
- deve ser facil de defender por um vendedor da Kouzina em uma frase;
- preferir item com preco informado quando houver equivalente forte;
- item `Sob consulta` so deve ser top-1 se for claramente consultivo,
  configuravel, de projeto ou parte de uma suite premium confirmada.

Top-3:

- pode misturar um complemento tecnico, uma suite/linha e uma opcao editorial;
- pode incluir `Sob consulta`, desde que nao domine o bloco;
- deve evitar tres itens com a mesma justificativa generica;
- deve preservar variedade comercial sem parecer aleatorio.

Itens sem preco:

- permitir quando a relacao e forte e o processo de venda exige atendimento;
- limitar a presenca quando houver alternativas precificadas equivalentes;
- exigir comentario de validacao na Fase 4.8;
- nao usar preco ausente como proxy de premium;
- registrar o motivo: `configuracao`, `instalacao`, `showroom`,
  `marcenaria`, `linha profissional` ou `venda consultiva`.

## Perguntas Para A Reuniao Real Com A Kouzina

- Esse produto ajuda o cliente a fechar projeto ou apenas aumenta ticket?
- O vendedor da Kouzina recomendaria este par em atendimento consultivo?
- Se o cliente perguntasse "por que isso?", a explicacao seria convincente?
- Marca pesa neste caso por suite/linha ou apenas por grife?
- Preco parecido esta ajudando coerencia ou criando falsa afinidade?
- Produto `Sob consulta` deve aparecer neste contexto ou gerar atrito?
- Este item sem preco pode ser top-1 ou apenas top-3?
- A relacao e complemento, alternativa, mesma suite ou editorial?
- A relacao e universal, contextual ou especifica da Kouzina?
- Algum produto precificado deveria aparecer antes?
- Existe risco de parecer empurro de produto caro?
- A recomendacao depende de medida, voltagem, largura, instalacao, combustivel
  ou marcenaria?

## Decisoes Sugeridas Para Registrar Em `reviewer_comment`

- `Cuba -> Misturador`: `universal; complemento; aprovar; cross-sell direto de
  bancada; validar acabamento/furo.`
- `Misturador -> Cuba`: `universal; complemento; aprovar; depende de
  acabamento, altura e instalacao.`
- `Cooktop/Rangetop -> Coifa`: `universal; complemento tecnico; aprovar;
  depende de largura, vazao e tipo de instalacao.`
- `Rangetop -> Forno`: `mesma suite/complemento; aprovar; forte para cozinha
  planejada high-end.`
- `Acessorio de Coifa -> Coifa`: `universal quando compativel; aprovar com
  confirmacao de modelo.`
- `Adega -> Cervejeira/Frigobar`: `contextual; estacao de bebidas; aprovar no
  top-3; pode ser top-1 se mesma linha/projeto.`
- `Churrasqueira -> Adega/Cervejeira/Maquina de Gelo`: `contextual; espaco
  gourmet; aprovar se projeto completo.`
- `Cafeteira embutida -> Micro-ondas/Forno da mesma linha`: `mesma suite;
  aprovar; marca/linha pesa mais que preco.`
- `Decorativo de mesa -> Cuba/Misturador/Lava-loucas`: `remover; decorativo
  puxando produto tecnico sem intencao de compra.`
- `Lavanderia -> Cozinha/Gourmet`: `remover; cruzamento de dominio sem venda
  consultiva clara.`
- `Sob consulta no top-1`: `restringir; permitir so quando consultivo,
  configuravel ou tecnicamente indispensavel.`
- `Mesmo ambiente sem funcao`: `restringir; ambiente sozinho nao sustenta
  recomendacao premium.`

## Proximo Passo Recomendado

Na reuniao Fase 4.8, revisar uma amostra de 24 a 40 recomendacoes, nao as 120
em sequencia. A amostra comercial deve conter:

- 8 a 10 casos fortes de cross-sell tecnico ou suite;
- 6 a 8 casos `Sob consulta`;
- 6 a 8 casos contextuais de espaco gourmet/bebidas;
- 6 a 8 casos suspeitos de empurro de ticket, ambiente amplo ou lavanderia.

Preencher `reviewer_rating` e `reviewer_comment` com a taxonomia acima. Depois
consolidar os comentarios em decisoes editoriais antes de qualquer CTR, fuzzy,
ontologia, deploy ou mudanca de ranking.

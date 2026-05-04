# Fase 4.8 - Revisao Do Arquiteto De Interiores High-End

Este documento registra a avaliacao simulada do agente "Arquiteto de
Interiores High-End" para a reuniao qualitativa da Fase 4.8 do Kouzina Reco.

Escopo desta avaliacao:

- atuar como especialista de dominio, nao como programador;
- avaliar recomendacoes do ponto de vista de projeto, ambiente, estetica,
  suite de produtos, cozinha planejada, espaco gourmet e experiencia premium;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao usar dados pessoais.

## Diagnostico

Como Arquiteto de Interiores High-End, eu aprovaria o recomendador v0 como base
de reuniao, mas nao como curadoria final. Ele acerta quando recomenda produtos
que ajudam a montar uma zona completa de projeto: coccao + exaustao, cuba +
misturador, adega + cervejeira ou frigobar, churrasqueira + refrigeracao
gourmet, rangetop + forno ou coifa.

Ele falha quando deixa ambiente, preco ou faixa premium criarem ponte entre
produtos que nao pertencem ao mesmo gesto de projeto.

## Criterios Arquitetonicos Para Aprovar Uma Recomendacao

- Complementaridade de projeto: o item ajuda a completar o ambiente?
- Coerencia estetica: acabamento, cor, inox/preto, linguagem visual e
  marca/linha combinam?
- Suite de produtos: ha linha, colecao ou familia visual clara?
- Compatibilidade de instalacao: embutir, sobrepor, ilha, parede, largura,
  abertura, marcenaria e voltagem.
- Hierarquia de ambiente: cozinha gourmet, espaco gourmet, refrigeracao e
  lavanderia nao devem se misturar sem intencao clara.
- Papel do produto: produto tecnico/estrutural pesa mais que produto
  decorativo na recomendacao automatica.
- Experiencia premium: a recomendacao deve parecer consultiva, nao apenas
  "produto parecido caro".

## Relacoes Fortes Para Projeto High-End

- `Acessorio de Coifa -> Coifa`: forte quando o acessorio e compativel com o
  modelo, largura e instalacao.
- `Cooktop/Rangetop -> Coifa`: relacao tecnica de coccao e exaustao. Depende
  de largura, vazao, parede/ilha e instalacao.
- `Cuba -> Misturador`: relacao universal de bancada e area molhada.
- `Misturador -> Cuba`: forte quando furo, altura, acabamento e instalacao
  forem coerentes.
- `Rangetop -> Forno`: forte para cozinha planejada high-end e suite de
  coccao.
- `Forno -> Cooktop/Rangetop`: composicao comum de projeto.
- `Adega -> Cervejeira/Frigobar`: forte em estacao de bebidas ou espaco
  gourmet, mas ainda contextual.
- `Churrasqueira -> Cervejeira/Adega/Maquina de Gelo`: boa em area gourmet
  completa, desde que nao pareca cross-sell generico.
- Built-ins da mesma linha visual: forte quando ha mesma colecao, altura,
  modulo, acabamento e linguagem de painel.

## Exemplos De Recomendacoes Fortes Observadas

- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Linea Touch | Franke`:
  forte como relacao tecnica e de mesma familia. Rating sugerido: `4` ou `5`,
  dependendo da compatibilidade exata do kit com o modelo.
- `Cuba Box De Embutir e Sobrepor 54x41 | Franke -> Misturador Monocomando |
  Franke`: relacao universal de bancada/molhada. Rating sugerido: `5`.
- `Misturador Monocomando | Franke -> Cubas Franke`: forte por funcao,
  acabamento e marca. Rating sugerido: `4` ou `5`, exigindo confirmacao de
  furacao/instalacao.
- `Rangetop Master Bertazzoni -> Forno Bertazzoni`: forte para cozinha
  planejada high-end e suite de coccao. Rating sugerido: `5`.
- `Rangetop -> Coifa`: forte por exaustao e coccao; depende de largura, vazao,
  parede/ilha e instalacao. Rating sugerido: `4` ou `5`.
- `Adega -> Cervejeira/Frigobar`: forte em estacao de bebidas ou espaco
  gourmet. Rating sugerido: `4`, podendo virar `5` quando mesma linha, medida
  e acabamento forem confirmados.

## Relacoes Fracas Ou Artificiais

- Produto decorativo de mesa puxando produto tecnico de bancada ou marcenaria.
- Lavanderia puxando cozinha gourmet, coccao, coifa, adega ou rangetop.
- Mesmo ambiente puxando item sem complementaridade funcional.
- Mesma faixa premium ou preco proximo substituindo relacao de projeto.
- Mesma marca sem mesma linha, colecao ou compatibilidade tecnica.
- Produto `Sob consulta` aparecendo no topo sem justificativa de projeto,
  consultoria ou configuracao.
- Recomendacao com reason generica demais para justificar produto high-end.

## Exemplos De Recomendacoes Fracas Observadas

- `Set Azeite & Vinagre Le Creuset -> Cuba/Misturador/Painel de Lava-Loucas`:
  fraca. E produto decorativo/de mesa puxando produto tecnico de bancada ou
  marcenaria. Rating sugerido: `1` ou `2`.
- `Secadora SpeedQueen -> Fogao Bertazzoni`: remover. Lavanderia e coccao nao
  formam projeto conjunto. Rating sugerido: `1`.
- `Secadora SpeedQueen -> Rangetop`: remover. A ligacao parece sustentada por
  preco, voltagem ou faixa premium, nao por projeto. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Adega`: remover. Mesma faixa premium/preco nao
  justifica cruzar lavanderia com cozinha gourmet. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Coifa`: remover. Nao ha relacao arquitetonica clara.
  Rating sugerido: `1`.
- `Cervejeira -> Coifa de churrasqueira` com score alto: contextual, nao
  universal. Pode fazer sentido em area gourmet completa, mas nao deve aparecer
  como regra forte sem projeto. Rating sugerido: `2` ou `3`.
- `Churrasqueira -> Refrigerador classificado como Adega`: precisa revisao de
  tipo/catalogacao. Pode ser util em area gourmet, mas a tipagem errada
  prejudica confianca.

## Quando Ambiente Pesa Mais Que Categoria

Ambiente pesa mais quando o cliente esta montando uma zona completa de uso:
espaco gourmet, ilha com coccao, bar, area de bebidas ou varanda gourmet.
Nesses casos, `Churrasqueira -> Cervejeira/Adega/Maquina de Gelo` pode ser mais
util que uma relacao puramente categorial.

Mesmo assim, ambiente deve funcionar como contexto, nao como permissao ampla
para recomendar qualquer item caro do mesmo universo.

## Quando Categoria Ou Tipo Deve Pesar Mais Que Ambiente

Categoria e tipo devem pesar mais quando ha compatibilidade tecnica:

- coifa com cooktop/rangetop;
- cuba com misturador;
- lava-loucas com painel, cuba ou area molhada;
- forno com built-ins da mesma suite;
- acessorio de coifa com modelo de coifa compativel.

Se a instalacao nao fecha, o ambiente nao deve salvar a recomendacao.

## O Que Deve Ser Mantido

- Relacoes tecnicas: `Cooktop/Rangetop -> Coifa`, `Cuba -> Misturador`,
  `Forno -> Cooktop/Rangetop`, `Acessorio de Coifa -> Coifa`.
- Relacoes de suite visual: built-ins da mesma linha, mesma marca e mesma
  altura/modulacao.
- Relacoes de zona gourmet: `Churrasqueira -> Cervejeira/Adega/Maquina de
  Gelo`, mas como contextual.
- Exclusao do proprio produto.
- Reason textual, desde que futuramente fique mais arquitetonica e concreta.

## O Que Deve Ser Restringido

- Mesmo ambiente sozinho.
- Mesma marca sem linha/colecao.
- Faixa premium ou preco como criterio forte.
- Produtos `Sob consulta` no topo, salvo item claramente consultivo ou de
  projeto.
- Relacoes entre produtos decorativos e produtos tecnicos.
- Relacoes entre lavanderia e cozinha/gourmet.

## O Que Deve Ser Removido

- Lavadora ou secadora recomendando forno, coifa, rangetop, adega ou cooktop.
- Acessorio decorativo de mesa puxando cuba, misturador ou painel de
  lava-loucas.
- Qualquer relacao que so exista por preco parecido, sem ambiente e sem
  funcao.
- Produto tecnico de instalacao sendo recomendado por item solto/decorativo sem
  ligacao de projeto.

## Como Registrar Comentarios No `reviewer_comment`

Usar comentarios curtos e padronizados:

```text
universal; complemento tecnico; aprovar; depende de largura/instalacao.
contextual; espaco gourmet; aprovar se projeto incluir estacao de bebidas.
curadoria Kouzina; mesma suite visual; confirmar linha/acabamento.
restringir; produto sob consulta so com atendimento consultivo.
remover; decorativo puxando produto tecnico sem relacao de projeto.
remover; lavanderia cruzando com cozinha gourmet.
```

## Campos Que Faltam No Catalogo Para Avaliacao Arquitetonica

- acabamento;
- cor;
- linha, colecao ou design line;
- largura, altura e profundidade;
- tipo de instalacao: embutir, sobrepor, parede, ilha, built-in;
- panel-ready, painel ou dependencia de marcenaria;
- abertura da porta: direita ou esquerda;
- indoor/outdoor;
- combustivel: GLP, GN ou eletrico;
- compatibilidade de exaustao ou vazao;
- modulo/altura de built-ins;
- indicacao de suite visual;
- familia estetica ou colecao comercial;
- necessidade de nicho, ventilacao, recuo ou ponto hidraulico.

## Perguntas Para A Reuniao Real Com A Kouzina

- Esse par aparece em um projeto real de cozinha planejada?
- A recomendacao melhora o ambiente ou so parece produto caro parecido?
- O acabamento e a linha visual combinam?
- Depende de marcenaria, medida, instalacao ou abertura?
- Esse item deve aparecer automaticamente ou apenas em atendimento consultivo?
- Produto `Sob consulta` pode aparecer no topo nesse contexto?
- Essa relacao e universal, contextual ou especifica da curadoria Kouzina?
- A reason esta clara para um cliente premium?
- Esse item ajuda a montar projeto completo ou apenas amplia o ticket?

## Decisoes Sugeridas Para Registrar

- `Cuba -> Misturador`: universal; manter; depende de instalacao, furo e
  acabamento.
- `Cooktop/Rangetop -> Coifa`: universal; manter; depende de largura, vazao e
  tipo de instalacao.
- `Forno -> Cooktop/Rangetop`: universal/contextual; manter; melhora suite de
  coccao.
- `Acessorio de Coifa -> Coifa`: universal quando compativel; exigir
  confirmacao de modelo.
- `Adega -> Cervejeira/Frigobar`: contextual; aprovar para estacao de bebidas.
- `Churrasqueira -> Adega/Cervejeira/Maquina de Gelo`: contextual; aprovar para
  espaco gourmet, restringir fora desse contexto.
- `Cafeteira embutida -> Forno/Micro-ondas`: curadoria/suite; aprovar quando
  mesma linha ou modulo visual.
- Decorativo de mesa -> produto tecnico: remover.
- Lavanderia -> cozinha/gourmet: remover.
- Mesmo ambiente sem funcao: restringir.
- `Sob consulta`: restringir; permitir quando o item for consultivo, de
  projeto, configuravel ou muito forte para o contexto.

## Decisao Final

Podem virar conhecimento universal:

- `Cuba -> Misturador`;
- `Cooktop/Rangetop -> Coifa`;
- `Forno -> Cooktop/Rangetop`;
- `Acessorio de Coifa -> Coifa`, quando houver compatibilidade de modelo;
- built-ins da mesma suite, quando linha, medida e acabamento forem
  confirmados.

Dependem de curadoria:

- `Churrasqueira -> Adega/Cervejeira/Maquina de Gelo`;
- `Adega -> Frigobar/Cervejeira`;
- `Cafeteira embutida -> Forno/Micro-ondas`;
- produtos `Sob consulta`;
- relacoes por marca;
- relacoes por ambiente gourmet;
- relacoes de merchandising editorial da Kouzina.

Devem ser vetadas:

- cruzamentos lavanderia/cozinha;
- decorativo/tecnico sem projeto;
- recomendacoes sustentadas apenas por preco, ambiente generico ou faixa
  premium.

## Proximo Passo Recomendado

Na reuniao Fase 4.8, revisar 24 a 40 cards e preencher `reviewer_rating` e
`reviewer_comment` com esta taxonomia:

- `universal`;
- `contextual`;
- `curadoria Kouzina`;
- `restringir`;
- `remover`.

Depois, consolidar os comentarios antes de qualquer mudanca no ranking v0.

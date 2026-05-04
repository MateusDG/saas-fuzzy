# Fase 4.8 - Revisao Do Curador De Catalogo E Taxonomia

Este documento registra a avaliacao simulada do agente "Curador de Catalogo e
Taxonomia" para a reuniao qualitativa da Fase 4.8 do Kouzina Reco.

Escopo desta avaliacao:

- atuar como especialista de dominio, nao como programador;
- avaliar `product_type`, `category`, `environment`, `brand`, `price`,
  `availability_text` e relacoes do recomendador v0;
- separar relacoes universais, contextuais, especificas da Kouzina e
  proibidas/restritas;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao versionar `reports/*.csv` ou `reports/*.html`;
- nao usar dados pessoais.

## Diagnostico

Do ponto de vista de catalogo e taxonomia, o MVP esta pronto para a reuniao da
Fase 4.8. O catalogo oficial ja tem cobertura boa para uma revisao qualitativa:
281 produtos importados, todos com `product_type`, `environment`, categoria,
marca, URL e imagem. O Review Pack atual le 120 linhas, 30 produtos de origem
e 27 tipos de origem.

O principal problema nao e ausencia de dados basicos. O problema e que alguns
campos estao amplos demais ou misturam papeis diferentes:

- `environment` ajuda, mas esta muito largo para decidir ranking sozinho;
- `product_type` resolve bem tipos principais, mas ainda confunde alguns
  subtipo/uso, como coifas de churrasqueira, paineis de lava-loucas, dispenser
  de agua e refrigeradores classificados como adega em alguns exemplos;
- `category` ainda reflete a arvore comercial da loja, nao necessariamente a
  taxonomia semantica do produto;
- `availability_text = Sob consulta` e informativo, mas precisa virar uma
  decisao de politica na revisao;
- relacoes por preco, marca ou ambiente conseguem produzir recomendacoes sem
  complementaridade real.

A recomendacao geral e usar a Fase 4.8 para transformar julgamentos humanos em
uma politica de relacoes versionavel, antes de qualquer mudanca no ranking.

## Criterios Usados

- `product_type` deve representar o que o produto e, nao onde ele aparece no
  site.
- `category` pode continuar comercial, mas nao deve ser confundida com tipo.
- `environment` deve indicar contexto de uso, nao validar relacao sozinho.
- `brand` deve ajudar em suite/linha, mas nao substituir compatibilidade.
- `price` deve moderar coerencia, nao criar relacao funcional.
- `availability_text` deve separar preco informado, sob consulta,
  indisponivel e estados futuros.
- Relacao complementar precisa ter funcao, instalacao, uso conjunto ou suite
  clara.
- Relacao contextual precisa de ambiente/projeto explicito.
- Relacao especifica da Kouzina precisa ser marcada como curadoria local.
- Relacao proibida deve ser registrada para evitar que vire conhecimento
  universal futuro.

## Relacoes Atuais Que Parecem Universais

Sao relacoes que tendem a valer em catalogos high-end semelhantes, pois nascem
de uso, funcao ou instalacao.

- `Cuba -> Misturador`: complementaridade direta de area molhada.
- `Misturador -> Cuba`: complementaridade direta, com cuidado para acabamento,
  furo e instalacao.
- `Cooktop -> Coifa`: relacao tecnica de coccao e exaustao.
- `Coifa -> Cooktop`: relacao tecnica inversa, dependente de largura e
  instalacao.
- `Rangetop -> Coifa`: relacao tecnica de coccao potente e exaustao.
- `Rangetop -> Forno`: composicao comum de cozinha planejada.
- `Forno -> Cooktop/Rangetop`: composicao de coccao.
- `Acessorio de Coifa -> Coifa`: universal apenas quando houver
  compatibilidade de modelo.
- `Lava-loucas -> Cuba/Misturador`: relacao funcional de area molhada, mas com
  dependencia de instalacao e marcenaria.
- `Freezer -> Refrigerador`: relacao de refrigeracao complementar, quando o
  projeto comporta os dois volumes.

## Relacoes Que Parecem Contextuais

Sao plausiveis, mas dependem de ambiente, projeto, intencao de uso ou
curadoria da loja.

- `Adega -> Cervejeira/Frigobar`: forte em estacao de bebidas, nao universal
  para toda cozinha.
- `Cervejeira -> Adega/Frigobar`: coerente em bar, varanda gourmet ou area de
  entretenimento.
- `Churrasqueira -> Adega/Cervejeira/Maquina de Gelo`: boa em espaco gourmet
  completo, mas deve depender do contexto.
- `Forno de Pizza -> Churrasqueira/Adega/Cervejeira`: coerente em area gourmet,
  nao obrigatorio.
- `Maquina de Gelo -> Cervejeira/Frigobar/Adega`: bom para bar e bebidas, mas
  nao deve subir sem ambiente claro.
- `Cafeteira -> Forno/Micro-ondas/Gaveta Aquecida`: aceitavel quando houver
  built-ins, mesma linha ou torre quente.
- `Gaveta Aquecida -> Forno/Cooktop`: aceitavel em cozinha planejada premium.
- `Refrigerador -> Freezer/Frigobar/Cervejeira`: depende de projeto de
  refrigeracao, espaco e papel do produto.
- `Dispenser de Agua -> Adega/Frigobar/Cervejeira`: contextual fraco; pode
  fazer sentido em bar, mas nao como regra forte.

## Relacoes Especificas Da Kouzina

Sao relacoes que podem fazer sentido pelo mix, posicionamento, marcas e
curadoria comercial da Kouzina, mas nao devem virar verdade universal sem
validacao externa.

- Priorizar produtos de uma marca quando a Kouzina trabalha uma linha completa.
- Aproximar produtos com mesma linha comercial ou mesma familia visual, quando
  isso estiver confirmado pela equipe.
- Exibir `Sob consulta` quando o item exige atendimento consultivo e representa
  venda de projeto.
- Promover itens de alto valor quando ha estrategia editorial de showroom.
- Usar categorias comerciais da loja para montar vitrines, desde que o
  comentario registre `curadoria Kouzina`.
- Manter pares de marca diferente quando a Kouzina sabe que sao combinacoes
  frequentes em projetos reais.

## Relacoes Que Devem Ser Proibidas Ou Restringidas

Devem ser proibidas:

- `Lavadora/Secadora -> Forno/Cooktop/Coifa/Rangetop/Adega`: cruza lavanderia
  com cozinha/gourmet sem complementaridade.
- `Acessorio de Cozinha decorativo -> Cuba/Misturador/Painel de Lava-loucas`:
  produto de mesa ou decorativo nao deve puxar produto tecnico de instalacao.
- Relacoes sustentadas apenas por preco proximo e faixa premium.
- Relacoes sustentadas apenas por mesma marca quando os tipos nao se
  complementam.
- Relacoes entre categorias de dominios distintos sem projeto claro.

Devem ser restringidas:

- `Dispenser de Agua -> Adega/Frigobar/Cervejeira`: permitir apenas em bar ou
  espaco gourmet explicitamente validado.
- `Cervejeira -> Coifa de Churrasqueira`: pode ser area gourmet, mas nao deve
  ser universal.
- `Churrasqueira -> Refrigerador/Adega`: manter como contextual e validar
  `product_type` do recomendado.
- `Cuba -> Painel de Lava-loucas`: pode haver area molhada, mas painel de
  lava-loucas depende de modelo, marcenaria e contexto.
- `Produto sob consulta` no top-1: permitir apenas quando o par for muito forte
  ou consultivo.

## Exemplos De Recomendacoes Fortes

- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Linea Touch | Franke`:
  boa relacao `Acessorio de Coifa -> Coifa`; exige validacao de
  compatibilidade do modelo.
- `Cuba Box De Embutir e Sobrepor 54x41 | Franke -> Misturador Monocomando |
  Franke`: relacao universal `Cuba -> Misturador`.
- `Misturador Monocomando | Franke -> Cubas Franke`: relacao universal
  `Misturador -> Cuba`, com dependencia de acabamento e instalacao.
- `Rangetop Master Bertazzoni -> Forno Bertazzoni`: boa relacao de suite de
  coccao.
- `Rangetop -> Coifa`: relacao tecnica forte, mesmo quando a marca muda, desde
  que largura e instalacao sejam compativeis.
- `Adega -> Cervejeira/Frigobar`: boa como relacao contextual de bebidas.

## Exemplos De Recomendacoes Fracas

- `Set Azeite & Vinagre Le Creuset -> Cuba`: fraca; `Acessorio de Cozinha`
  esta amplo demais e mistura item de mesa/decorativo com item tecnico.
- `Set Azeite & Vinagre Le Creuset -> Misturador`: fraca pelo mesmo motivo.
- `Set Azeite & Vinagre Le Creuset -> Painel Decorativo Frente Lava-Loucas`:
  fraca; mistura decorativo de mesa com componente de marcenaria/lava-loucas.
- `Lavadora SpeedQueen -> Adega`: proibida; dominios diferentes.
- `Lavadora SpeedQueen -> Coifa`: proibida; dominios diferentes.
- `Secadora SpeedQueen -> Fogao/Rangetop`: proibida; parece efeito de preco,
  voltagem ou faixa premium.
- `Dispenser de Agua -> Coifa Profissional Churrasqueira`: restringir; mesmo
  ambiente nao basta.
- `Cervejeira -> Coifa de Parede Churrasqueira`: restringir; pode ser
  editorial de area gourmet, mas nao universal.

## Onde `environment` Esta Amplo Demais

O campo `environment` e util, mas hoje parece cobrir macrocontextos muito
largos:

- `Cozinha Gourmet` reune cuba, misturador, coifa, forno, cooktop, decorativo,
  refrigeracao embutida e paineis. Isso facilita vazamento entre produto de
  bancada, produto de instalacao e item de mesa.
- `Espaco Gourmet` junta churrasqueira, adega, cervejeira, dispenser de agua,
  maquina de gelo e coifas de churrasqueira. Isso permite relacoes plausiveis,
  mas nem sempre fortes.
- `Refrigeracao` diferencia pouco refrigerador, freezer, frigobar, adega,
  cervejeira e gaveta refrigerada.
- `Lavanderia` esta correto como macroambiente, mas deve ficar isolado de
  cozinha e gourmet.

Subambientes recomendados para revisao futura:

- `area_molhada`;
- `zona_coccao`;
- `torre_quente`;
- `exaustao`;
- `estacao_bebidas`;
- `bar_gourmet`;
- `area_churrasco`;
- `refrigeracao_principal`;
- `refrigeracao_bebidas`;
- `lavanderia`;
- `mesa_servir`;
- `marcenaria_painel`.

## Onde `product_type` Precisa Ser Refinado

- `Acessorio de Cozinha`: esta amplo demais. Separar `Acessorio Decorativo`,
  `Acessorio Funcional`, `Acessorio de Instalacao`, `Item de Mesa` e
  `Acessorio de Lava-loucas`.
- `Churrasqueira`: esta recebendo itens que parecem coifas de churrasqueira em
  alguns nomes. Separar `Churrasqueira`, `Coifa de Churrasqueira` e
  `Acessorio de Churrasqueira`.
- `Adega`: revisar casos em que o nome indica `Refrigerador Bottom` ou `Wine
  Dispenser`; podem precisar de `Refrigerador`, `Wine Dispenser` ou
  `Dispenser de Vinho`.
- `Frigobar`: revisar beer centers; possivelmente separar `Beer Center`,
  `Frigobar` e `Cervejeira`.
- `Lava-loucas`: separar maquina de lava-loucas de `Painel de Lava-loucas`.
- `Fogao`, `Forno` e `Rangetop`: manter separados; revisar itens combinados
  como fogao com forno.
- `Domino`: manter como tipo proprio, mas registrar modulo de coccao.
- `Gaveta Aquecida` e `Gaveta Refrigerada`: boas como tipo, mas precisam de
  subclasse `built_in`.
- `Dispenser de Agua`: manter separado, mas tratar relacoes como contextuais
  fracas.

## Campos Novos Recomendados Para CSV/HTML

Campos de classificacao:

- `source_environment`;
- `recommended_environment`;
- `source_subenvironment`;
- `recommended_subenvironment`;
- `source_taxonomy_note`;
- `recommended_taxonomy_note`;
- `source_product_role`;
- `recommended_product_role`;

Campos de relacao:

- `relation_class`: `universal`, `contextual`, `especifica_kouzina`,
  `restringir`, `proibida`;
- `relation_type`: `complemento`, `alternativa`, `mesma_suite`, `editorial`,
  `acessorio`, `instalacao`;
- `relation_strength`: `forte`, `media`, `fraca`;
- `requires_project_context`;
- `requires_installation_check`;
- `must_show_before`;

Campos de catalogo:

- `availability_status`: `in_stock`, `quote_only`, `backorder`,
  `discontinued`;
- `quote_reason`;
- `collection`;
- `design_line`;
- `finish`;
- `color`;
- `installation_type`;
- `width_cm`;
- `height_cm`;
- `depth_cm`;
- `opening_side`;
- `fuel_type`;
- `panel_ready`;
- `indoor_outdoor`;
- `voltage_normalized`;

Campos de revisao:

- `taxonomy_issue`;
- `relation_policy_decision`;
- `reviewer_role`;
- `expert_validated`;
- `confidence_note`.

## Como Transformar A Reuniao Em Uma Politica De Relacoes

1. Revisar 24 a 40 recomendacoes em quatro blocos: casos fortes, casos medios,
   produtos sob consulta e casos controversos.
2. Para cada linha, preencher `reviewer_rating` de 1 a 5.
3. Em `reviewer_comment`, registrar sempre a classe da relacao:
   `universal`, `contextual`, `especifica Kouzina`, `restringir` ou
   `proibida`.
4. Registrar tambem o tipo de relacao: `complemento`, `alternativa`,
   `mesma suite`, `editorial`, `acessorio` ou `instalacao`.
5. Marcar dependencias: medida, voltagem, acabamento, marcenaria, abertura,
   linha, instalacao ou atendimento consultivo.
6. Separar decisoes por par de tipos, nao apenas por produto individual.
7. Consolidar em uma tabela de politica:
   `source_type`, `recommended_type`, `relation_class`, `relation_type`,
   `default_action`, `required_conditions`, `example_good`,
   `example_bad`.
8. Usar a politica consolidada como insumo para ajustes editoriais futuros,
   sem alterar ranking automaticamente durante a reuniao.

## Perguntas Para A Reuniao Real Com A Kouzina

- O `product_type` deste produto esta correto ou esta amplo demais?
- A `category` da loja ajuda ou confunde a avaliacao semantica?
- O `environment` e suficiente ou falta subambiente?
- Esta relacao e universal, contextual, especifica Kouzina ou proibida?
- O produto recomendado e complemento, alternativa, mesma suite, acessorio ou
  editorial?
- A recomendacao depende de medida, instalacao, marcenaria, linha ou
  acabamento?
- Produto `Sob consulta` deve aparecer nesse contexto?
- O score alto veio de complementaridade real ou de marca/preco/ambiente?
- Algum item deveria ser reclassificado antes de avaliar a relacao?

## Decisoes Sugeridas Para Registrar Em `reviewer_comment`

Exemplos de comentarios padronizados:

```text
universal; complemento; manter; area molhada; validar instalacao/acabamento.
universal; instalacao; manter; coccao/exaustao; validar largura e voltagem.
contextual; estacao de bebidas; manter se ambiente = espaco gourmet/bar.
especifica Kouzina; editorial; manter apenas se curadoria comercial confirmar.
restringir; sob consulta; permitir apenas com atendimento consultivo.
restringir; mesmo ambiente insuficiente; baixar prioridade futura.
proibida; lavanderia cruzando com cozinha/gourmet.
proibida; acessorio decorativo puxando produto tecnico.
taxonomia; revisar product_type do recomendado antes de decidir.
```

## O Que Deve Ser Mantido

- Separacao entre `product_type`, `category` e `environment`.
- Cobertura atual de `product_type` e `environment` para todos os produtos.
- Regra de `Sob consulta` como `price = null`, sem pontuar preco proximo.
- Razao textual em todas as recomendacoes.
- Relacoes universais de area molhada, coccao, exaustao e built-ins.
- Review Pack como ferramenta visual e nao como painel.

## O Que Deve Ser Restringido

- `environment` como criterio de ranking quando nao houver complementaridade.
- `brand` sem `collection` ou `design_line`.
- `price` como aproximador de relacao.
- `Acessorio de Cozinha` sem subtipo.
- `Sob consulta` em excesso no mesmo bloco.
- Recomendacoes de categorias comerciais que nao representam tipo real.

## O Que Deve Ser Removido

- Relacoes entre lavanderia e cozinha/gourmet.
- Relacoes de acessorio decorativo para produto tecnico.
- Relacoes geradas apenas por preco/faixa premium.
- Relacoes com tipagem claramente errada sem anotacao de revisao.
- Uso de coifa de churrasqueira como `Churrasqueira` quando a intencao for
  exaustao, nao coccao.

## Proximo Passo Recomendado

Na reuniao Fase 4.8, usar o HTML apenas como visualizacao e preencher a planilha
com uma politica minima de relacoes. A saida operacional deve ser uma lista
curada com:

- pares universais aprovados;
- pares contextuais aprovados com condicoes;
- pares especificos da Kouzina;
- pares proibidos;
- itens que exigem revisao de `product_type`, `category` ou `environment`.

Somente depois dessa consolidacao faz sentido discutir ajuste editorial do v0.
Nao alterar ranking durante a reuniao.

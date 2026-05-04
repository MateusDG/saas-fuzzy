# Ata Simulada - Reuniao De Especialistas Kouzina - Fase 4.8

Data da consolidacao: 2026-05-04

Esta ata consolida a reuniao simulada de especialistas da Kouzina para a Fase
4.8 do Kouzina Reco MVP. O objetivo e registrar criterios e decisoes
qualitativas para orientar a revisao humana do Review Pack, sem alterar codigo,
ranking v0, API, banco, widget, contrato, CSV/HTML de relatorio, fuzzy,
ontologia, CTR, painel, login, Tray ou deploy.

Fontes lidas e consolidadas:

- `docs/agents/phase_4_8_architect_review.md`
- `docs/agents/phase_4_8_technical_review.md`
- `docs/agents/phase_4_8_commercial_review.md`
- `docs/agents/phase_4_8_catalog_review.md`
- `docs/agents/phase_4_8_recommender_review.md`
- `docs/agents/phase_4_8_qa_review.md`
- `docs/RELATION_POLICY.md`
- `docs/RECOMMENDATION_REVIEW.md`
- `docs/PHASE_4_8_VALIDACAO_KOUZINA.md`
- `reports/recommendation_review.csv`
- `reports/recommendation_review.html`

## 1. Participantes Simulados

- Moderador da reuniao simulada: consolidacao das decisoes, conflitos e
  proximos passos.
- Arquiteto de Interiores High-End: avaliacao de projeto, ambiente, suite,
  estetica e experiencia premium.
- Especialista Tecnico de Instalacao, Eletrodomesticos e Marcenaria:
  avaliacao de voltagem, largura, nicho, instalacao, exaustao, abertura,
  combustivel, panel-ready e risco tecnico.
- Consultor Comercial High-End: avaliacao de venda consultiva, ticket medio,
  percepcao de valor, cross-sell, upsell e produtos sob consulta.
- Curador de Catalogo e Taxonomia: avaliacao de `product_type`, `category`,
  `environment`, marca, disponibilidade e qualidade catalogal.
- Cientista de Recomendacao: avaliacao metodologica, rotulagem, baseline,
  labels e uso futuro em Fases 5, 6 e 7.
- Auditor Critico/QA: contraditorio, vieses, riscos, falsos positivos e
  limites da reuniao.

## 2. Objetivo Da Reuniao

Validar qualitativamente uma amostra do recomendador v0 antes de qualquer CTR,
fuzzy, ontologia, deploy ou mudanca de ranking.

Saidas esperadas:

- separar relacoes universais, contextuais, especificas da Kouzina e
  fracas/proibidas;
- definir politica inicial para produtos `Sob consulta`;
- padronizar comentarios em `reviewer_comment`;
- sugerir campos futuros para CSV/HTML de revisao;
- identificar o que pode alimentar Fase 5, Fase 6 e Fase 7;
- listar decisoes que ainda exigem validacao humana real da Kouzina.

O Review Pack atual tem 120 linhas. A leitura do CSV indica 40 recomendacoes
com item recomendado `Sob consulta`, 48 linhas com produto de origem `Sob
consulta` e 49 linhas com score igual ou acima de 90. A reuniao reforca que
score alto no v0 nao e prova de qualidade especialista.

## 3. Criterios De Avaliacao

- Complementaridade funcional: o recomendado completa o uso do produto atual?
- Compatibilidade tecnica: ha coerencia de voltagem, largura, instalacao,
  abertura, combustivel, exaustao, marcenaria, capacidade e ambiente?
- Coerencia de projeto: o par aparece em cozinha planejada, area molhada,
  torre quente, estacao de bebidas, lavanderia ou espaco gourmet real?
- Papel comercial: a recomendacao ajuda venda consultiva ou apenas empurra
  ticket?
- Tipo de relacao: complemento, alternativa, mesma suite ou editorial.
- Escopo da relacao: universal, contextual, especifica Kouzina, restringir ou
  proibida.
- Qualidade catalogal: `product_type`, `category`, `environment` e marca
  sustentam a relacao ou estao amplos demais?
- Politica de preco: preco deve moderar coerencia, nao criar relacao.
- Politica de marca: marca so pesa fortemente quando houver linha, colecao,
  suite ou linguagem visual.
- Politica de ambiente: ambiente e contexto auxiliar, nao fundamento isolado.
- Produto `Sob consulta`: deve ter motivo consultivo, tecnico ou de projeto.
- Reason textual: precisa ser concreta e auditavel; reasons genericas devem
  ser marcadas para reescrita futura.

Escala recomendada para `reviewer_rating`:

- `1`: ruim; remover ou bloquear a relacao.
- `2`: fraca; so faria sentido em contexto muito especifico.
- `3`: aceitavel; pode aparecer abaixo, com reason melhor ou restricao.
- `4`: boa; manter com eventual ressalva tecnica.
- `5`: excelente; complemento natural, quase obrigatorio ou suite evidente.

## 4. Relacoes Aprovadas Como Universais

Estas relacoes podem ser candidatas a conhecimento de dominio, desde que as
condicoes tecnicas sejam registradas. Universal nao significa sem excecao.

- `Cuba -> Misturador`: aprovada como complemento universal de area molhada.
  Exigir validacao de furo, acabamento, instalacao, altura e alcance da bica.
- `Misturador -> Cuba`: aprovada como complemento universal inverso, com as
  mesmas ressalvas de instalacao e acabamento.
- `Cooktop/Rangetop/Fogao -> Coifa`: aprovada como relacao tecnica de coccao e
  exaustao. Exigir largura, vazao, tipo parede/ilha, duto/depurador,
  combustivel e voltagem quando aplicavel.
- `Coifa -> Cooktop/Rangetop/Fogao`: aprovada como composicao tecnica inversa,
  desde que nao sugira compatibilidade automatica sem medidas.
- `Forno -> Cooktop/Rangetop`: aprovada como composicao de coccao e cozinha
  planejada, com validacao de linha, modulo, instalacao e voltagem.
- `Rangetop -> Forno/Coifa`: aprovada como suite de coccao high-end, com
  cautela para largura, exaustao e projeto.
- `Acessorio de Coifa -> Coifa`: aprovada somente quando o acessorio for
  compativel com modelo, largura e instalacao da coifa.
- `Lava-loucas -> Cuba/Misturador`: aprovada como relacao funcional de area
  molhada, mas com cautela para marcenaria, pontos hidraulicos e instalacao.
- `Lavadora -> Secadora`: aprovada dentro do dominio de lavanderia, com
  validacao de capacidade, voltagem, empilhamento, ventilacao e drenagem.

## 5. Relacoes Aprovadas Como Contextuais

Estas relacoes sao comercialmente plausiveis, mas dependem de ambiente,
projeto, subambiente, consultoria ou curadoria. Nao devem virar regra universal
sem condicoes.

- `Adega -> Cervejeira/Frigobar`: aprovar para estacao de bebidas, bar,
  varanda ou espaco gourmet.
- `Cervejeira -> Adega/Frigobar/Maquina de Gelo`: aprovar para projeto de
  bebidas, nao para qualquer refrigeracao.
- `Churrasqueira -> Adega/Cervejeira/Frigobar/Maquina de Gelo`: aprovar quando
  houver espaco gourmet completo ou area de churrasco planejada.
- `Churrasqueira -> Coifa/Cooktop/Queimador/Forno de Pizza`: aprovar apenas se
  o projeto justificar coccao complementar, exaustao ou preparo gourmet.
- `Forno de Pizza -> Churrasqueira/Adega/Cervejeira`: aprovar como area
  gourmet, mas nao como obrigatorio.
- `Maquina de Gelo -> Cervejeira/Frigobar/Adega/Churrasqueira`: aprovar para
  bar, bebidas ou apoio gourmet.
- `Cafeteira embutida -> Forno/Micro-ondas/Gaveta Aquecida`: aprovar quando
  houver built-ins, torre quente, mesma linha, modulo visual ou suite.
- `Gaveta Aquecida -> Forno/Cooktop`: aprovar em cozinha planejada premium,
  com validacao de nicho, linha e instalacao.
- `Refrigerador -> Freezer/Frigobar/Cervejeira`: aprovar em projeto de
  refrigeracao, com cuidado para abertura, modulo e papel do produto.
- `Dispenser de Agua -> Adega/Frigobar/Cervejeira`: classificar como
  contextual fraco; permitir apenas em bar ou gourmet explicitamente validado.

## 6. Relacoes Especificas Da Kouzina

Estas relacoes podem fazer sentido por mix, marcas, showroom, estoque,
campanha, margem, curadoria comercial ou experiencia da equipe Kouzina. Devem
ser registradas como `especifica Kouzina` ou `curadoria Kouzina`, nao como
conhecimento universal.

- Priorizar produtos da mesma marca quando a Kouzina trabalha uma linha ou
  suite comercial confirmada.
- Aproximar produtos de mesma colecao, design line, acabamento ou familia
  visual quando a equipe validar.
- Exibir item `Sob consulta` como venda consultiva quando o produto exige
  projeto, configuracao, marcenaria, instalacao ou atendimento de showroom.
- Promover produtos por estrategia editorial, campanha ou relevancia comercial
  local.
- Manter combinacoes frequentes de marca diferente quando a Kouzina confirma
  recorrencia em projetos reais.
- Usar categorias comerciais da loja para vitrines editoriais, desde que o
  comentario nao confunda isso com relacao semantica universal.

## 7. Relacoes Fracas Ou Proibidas

Decisao consolidada: estes padroes devem ser removidos, bloqueados ou
fortemente restringidos em fases futuras. Na Fase 4.8, apenas registrar nos
comentarios; nao alterar ranking agora.

Proibidas:

- `Lavadora/Secadora -> Adega/Coifa/Forno/Fogao/Cooktop/Rangetop`.
- `Acessorio de Cozinha` decorativo ou item de mesa -> `Cuba/Misturador/Painel
  de Lava-loucas`.
- Relacoes sustentadas apenas por preco proximo, faixa premium ou ticket.
- Relacoes sustentadas apenas por marca, sem suite, linha ou uso conjunto.
- Relacoes entre dominios diferentes sem projeto claro.
- Produto `Sob consulta` sem motivo consultivo claro e sem relacao forte.

Restringidas:

- `Dispenser de Agua -> Churrasqueira/Adega/Frigobar/Cervejeira`, salvo bar ou
  projeto gourmet especifico.
- `Cervejeira -> Coifa de Churrasqueira`, salvo espaco gourmet validado.
- `Cuba -> Painel de Lava-loucas`, salvo quando houver modelo, marcenaria e
  panel-ready compativeis.
- `Coifa -> Forno` quando nao houver relacao clara de coccao, suite ou projeto.
- Recomendacoes com tipagem suspeita, como refrigerador classificado como
  adega, ate revisao catalogal.
- Qualquer recomendacao em que "mesmo ambiente" seja a principal justificativa
  sem complementaridade funcional.

## 8. Politica Para Produtos Sob Consulta

Produto `Sob consulta` nao e erro de catalogo. Em high-end, pode ser parte da
venda assistida. Mas a ausencia de preco tambem pode reduzir confianca no
carousel se nao houver motivo claro.

Decisoes consolidadas:

- Permitir `Sob consulta` quando o produto for configuravel, consultivo, de
  projeto, dealer/showroom, marcenaria, instalacao especializada, prazo ou
  importacao.
- Permitir quando a relacao for tecnicamente forte e houver poucas
  alternativas precificadas equivalentes.
- Evitar `Sob consulta` como top-1 quando houver alternativa precificada e
  comercialmente equivalente.
- Exigir `reviewer_comment` para todo item `Sob consulta` avaliado.
- Registrar o motivo: `configuracao`, `instalacao`, `showroom`, `marcenaria`,
  `linha profissional`, `prazo`, `importacao` ou `venda consultiva`.
- Limitar excesso de itens sem preco no mesmo bloco; sugestao de politica
  futura: se mais de 25% do carousel for `quote_only`, substituir excedentes
  por itens precificados equivalentes.
- Diferenciar futuramente `quote_only`, `backorder`, `discontinued`,
  `in_stock` e `out_of_stock`.

Politica por posicao:

- Top-1: somente se for complemento muito forte, suite confirmada ou venda
  consultiva indispensavel.
- Top-3: permitido com explicacao e sem dominar o bloco.
- Itens sem preco: nunca usar ausencia de preco como proxy de premium.

## 9. Campos Novos Recomendados Para CSV/HTML

Campos de relacao:

- `relation_class`
- `relation_type`
- `relation_strength`
- `relation_policy_decision`
- `requires_project_context`
- `requires_installation_check`
- `must_show_before`
- `expert_validated`
- `confidence_note`

Campos de catalogo e taxonomia:

- `source_environment`
- `recommended_environment`
- `source_subenvironment`
- `recommended_subenvironment`
- `source_product_role`
- `recommended_product_role`
- `source_taxonomy_note`
- `recommended_taxonomy_note`
- `taxonomy_issue`

Campos tecnicos:

- `voltage_normalized`
- `width_cm`
- `height_cm`
- `depth_cm`
- `cutout_width_cm`
- `cutout_height_cm`
- `cutout_depth_cm`
- `installation_type`
- `fuel_type`
- `gas_type`
- `hood_type`
- `airflow_capacity`
- `ducted_or_filter`
- `sink_mount_type`
- `tap_hole_count`
- `faucet_mount_type`
- `panel_ready`
- `panel_model_compatibility`
- `opening_side`
- `reversible_door`
- `capacity_l`
- `capacity_bottles`
- `place_settings`
- `capacity_kg`
- `indoor_outdoor`
- `finish`
- `color`
- `collection`
- `design_line`

Campos comerciais:

- `availability_status`
- `quote_reason`
- `project_required`
- `customizable`
- `lead_time_days`
- `business_priority`
- `editorial_campaign`

Campos de revisao:

- `reviewer_id`
- `reviewer_role`
- `review_round`
- `reason_quality`
- `quote_policy`
- `labels`

## 10. Comentarios Padrao Para `reviewer_comment`

Formato recomendado:

```text
scope=<universal|contextual|kouzina|proibida>; kind=<complemento|alternativa|mesma_suite|editorial>; decision=<manter|restringir|remover|demote|pendente>; labels=<lista>; note=<motivo e dependencia>
```

Comentarios prontos:

```text
scope=universal; kind=complemento; decision=manter; labels=area_molhada; note=validar furo, acabamento e instalacao.
```

```text
scope=universal; kind=complemento_tecnico; decision=manter; labels=coccao,exaustao; note=validar largura, vazao e tipo de coifa.
```

```text
scope=contextual; kind=complemento; decision=restringir; labels=espaco_gourmet,bebidas; note=mostrar apenas em projeto gourmet ou estacao de bebidas.
```

```text
scope=kouzina; kind=editorial; decision=demote; labels=curadoria_comercial; note=nao tratar como relacao universal.
```

```text
scope=contextual; kind=mesma_suite; decision=restringir; labels=quote_only,mesma_linha; note=sob consulta aceitavel somente com atendimento consultivo.
```

```text
scope=proibida; kind=none; decision=remover; labels=cross_domain_leakage; note=lavanderia nao deve puxar cozinha ou gourmet.
```

```text
scope=proibida; kind=none; decision=remover; labels=decorative_to_structural; note=acessorio decorativo nao complementa produto tecnico de bancada.
```

```text
scope=contextual; kind=complemento; decision=pendente; labels=taxonomy_issue; note=revisar product_type antes de aprovar.
```

```text
scope=contextual; kind=complemento; decision=restringir; labels=quote_only_topk_risk; note=nao usar top-1 com alternativa precificada equivalente.
```

```text
scope=universal; kind=complemento; decision=manter; labels=lavanderia; note=lavadora e secadora apenas dentro do dominio de lavanderia.
```

## 11. Decisoes Que Precisam De Validacao Humana Real

- Confirmar com a Kouzina quais categorias `Sob consulta` sao consultivas por
  natureza e quais representam apenas falta de preco.
- Confirmar se `Sob consulta` pode aparecer como top-1 e em quais excecoes.
- Validar compatibilidade de `Acessorio de Coifa -> Coifa` por modelo real.
- Definir regra comercial para largura minima de coifa em relacao a cooktop,
  fogao, rangetop e churrasqueira.
- Separar coifa de parede, coifa de ilha e coifa de churrasqueira como subtipos
  comerciais/tecnicos.
- Validar se a Kouzina aceita recomendacoes com voltagem divergente quando os
  produtos sao complementares independentes.
- Confirmar quais marcas/linhas sao realmente suites ou colecoes vendidas em
  conjunto.
- Revisar tipagens suspeitas: coifa de churrasqueira como `Churrasqueira`,
  painel de lava-loucas como `Lava-loucas`, refrigerador como `Adega`, e
  `Acessorio de Cozinha` decorativo como acessorio funcional.
- Confirmar se `Dispenser de Agua` deve aparecer em bar/gourmet ou permanecer
  fora do top-k.
- Confirmar quais relacoes gourmet sao venda consultiva real e quais sao
  merchandising.
- Definir quem na Kouzina tem autoridade final para classificar relacoes como
  universais, contextuais ou especificas da loja.

## 12. O Que Pode Ir Para Fase 5

A Fase 5 pode usar a Fase 4.8 como insumo de protocolo academico e baseline,
sem depender de deploy ou CTR.

Pode ir para Fase 5:

- gold set pequeno com 24 a 40 recomendacoes rotuladas por especialistas;
- mapeamento de `reviewer_rating` para relevancia offline;
- preservacao do score original do v0 para comparacao;
- protocolo de avaliacao com `Precision@k`, `Recall@k`, `nDCG@k`, MRR,
  cobertura por tipo e taxa de falsos positivos;
- analise de correlacao entre score v0 e nota humana;
- separacao entre validacao comercial local e validacao academica
  generalizavel;
- selecao futura de dataset publico para comparacao reproduzivel;
- registro de discordancia entre especialistas como dado metodologico.

Nao pode ir para Fase 5 como conclusao:

- afirmar que o v0 aumenta CTR;
- afirmar que a nota da Kouzina generaliza para outros e-commerces;
- usar a reuniao como prova estatistica de desempenho.

## 13. O Que Pode Ir Para Fase 6

A Fase 6 pode usar as decisoes como base para ontologia minima, mas somente
depois da validacao humana real.

Pode ir para Fase 6:

- relacoes `scope=universal` como candidatas a propriedades semanticas;
- relacoes `scope=contextual` condicionadas por `Environment`,
  `Subenvironment` ou `ProjectContext`;
- `scope=kouzina` separado como camada editorial, fora da ontologia universal;
- `scope=proibida` como exemplos negativos ou restricoes;
- classes candidatas: `Product`, `ProductType`, `Brand`, `Collection`,
  `Environment`, `Subenvironment`, `Offer`, `AvailabilityState`,
  `TechnicalSpec`, `RelationType`, `ProjectContext`;
- propriedades candidatas: `complements`, `alternativeTo`, `sameSuiteAs`,
  `requiresAccessory`, `compatibleWith`, `hasAvailabilityState`,
  `belongsToCollection`, `suitedForEnvironment`.

Nao pode ir para Fase 6:

- relacao fraca formalizada como ontologia;
- decisao especifica da Kouzina tratada como universal;
- relacao sem atributos tecnicos minimos quando ela sugere compatibilidade.

## 14. O Que Pode Ir Para Fase 7

A Fase 7 pode usar os labels da Fase 4.8 para calibrar variaveis fuzzy futuras,
sem implementar fuzzy agora.

Pode ir para Fase 7:

- ratings `5` como exemplos de alta complementaridade funcional;
- ratings `4` como relacoes boas com ressalvas tecnicas;
- ratings `3` como zona intermediaria;
- ratings `1` e `2` como penalidades ou baixa relevancia;
- comentarios sobre `Sob consulta` como base de `quote_acceptability`;
- comentarios de risco tecnico como base de `technical_compatibility`;
- comentarios sobre linha/suite como base de `brand_line_affinity`;
- comentarios sobre reason como base de `reason_confidence`.

Variaveis fuzzy candidatas:

- `functional_complementarity`
- `technical_compatibility`
- `installation_compatibility`
- `environment_affinity`
- `brand_line_affinity`
- `price_proximity`
- `quote_acceptability`
- `recommendation_confidence`

Nao pode ir para Fase 7:

- usar o score v0 como score fuzzy;
- usar `Sob consulta` como sinal automatico de premium;
- transformar preco, marca ou ambiente em criterio principal isolado.

## 15. Riscos E Limitacoes

- A reuniao simulada nao substitui validacao humana real da Kouzina.
- O CSV de 120 linhas e amostra qualitativa, nao avaliacao estatistica.
- O HTML e pacote visual estatico; nao salva rating nem altera banco.
- Relatorios `reports/*.csv` e `reports/*.html` nao devem ser versionados.
- Score alto do v0 nao significa confianca especialista.
- Ha risco de vies da loja-piloto: transformar mix da Kouzina em verdade
  universal.
- Ha risco de vies de ticket: aceitar produto caro como recomendacao boa.
- Ha risco de vies de marca: confundir mesma marca com mesma suite.
- Ha risco de vies de ambiente: `Cozinha Gourmet` e `Espaco Gourmet` sao
  amplos e podem gerar pontes fracas.
- Ha risco de romantizar `Sob consulta` como premium, quando pode gerar
  friccao no ecommerce.
- Ha risco de tipagem: alguns nomes sugerem subtipos mais precisos que o
  `product_type` atual.
- Faltam atributos tecnicos para garantir compatibilidade: largura, nicho,
  vazao, abertura, combustivel, instalacao, acabamento, linha e panel-ready.
- A reuniao nao mede CTR, receita, clique assistido ou comportamento real de
  usuario.
- A reuniao nao prova que ontologia ou fuzzy melhoram o v0.
- A proxima acao deve ser preencher `reviewer_rating` e `reviewer_comment` em
  amostra real de 24 a 40 recomendacoes, nao alterar ranking imediatamente.

## Encaminhamento Final

A reuniao simulada recomenda realizar uma reuniao real com a Kouzina usando
amostra estratificada:

- 8 a 10 casos fortes;
- 6 a 8 casos `Sob consulta`;
- 6 a 8 casos contextuais de gourmet/bebidas;
- 6 a 8 casos fracos ou controversos;
- 4 casos de possivel erro de tipagem ou confusao entre complemento,
  alternativa, suite e editorial.

Ao final, consolidar uma tabela de relacoes com `manter`, `restringir`,
`remover`, `demote`, `pendente` e `curadoria Kouzina`. Somente depois dessa
validacao humana real deve-se discutir ajuste editorial do v0 ou preparar as
Fases 5, 6 e 7.

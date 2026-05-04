# Fase 4.8 - Revisao Do Cientista De Recomendacao

Este documento registra a avaliacao simulada do agente "Cientista de
Recomendacao" para a reuniao qualitativa da Fase 4.8 do Kouzina Reco.

Escopo desta avaliacao:

- atuar como especialista de dominio e metodologia de recomendacao, nao como
  programador;
- transformar julgamento humano em dataset rotulado para baseline, ontologia e
  fuzzy futuros;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao editar nem versionar `reports/*.csv` ou `reports/*.html`.

## Diagnostico

Do ponto de vista de ciencia de recomendacao, o v0 esta pronto para ser
avaliado qualitativamente, mas ainda nao deve ser usado como evidencia de
performance. Ele e um baseline explicavel de cold start, apoiado em atributos
catalogais e regras comerciais, mas mistura quatro fenomenos que precisam ser
separados antes de qualquer etapa academica:

- complemento funcional real;
- alternativa/substituto;
- mesma suite, linha ou linguagem visual;
- relacao editorial ou comercial da Kouzina.

O pacote `reports/recommendation_review.csv` tem 120 linhas para revisao, com
notas e comentarios ainda vazios. Isso deve ser tratado como uma fila de
rotulagem especializada, nao como log de comportamento de usuario.

O principal valor da Fase 4.8 nao e "aprovar" o recomendador. E transformar
comentarios humanos em decisoes estruturadas que possam ser usadas depois para:

- ajustar o baseline v0 sem perder explicabilidade;
- separar conhecimento universal de curadoria local;
- definir classes e propriedades de uma ontologia minima;
- calibrar variaveis fuzzy com base em julgamento especialista;
- montar um protocolo academico reproduzivel.

## Criterios Usados

Usei os seguintes criterios para avaliar cada recomendacao:

- Complementaridade funcional: o recomendado completa o uso do produto atual?
- Compatibilidade tecnica: ha risco de voltagem, largura, instalacao, abertura,
  marcenaria, combustivel ou ambiente invalidar a sugestao?
- Classe da relacao: universal, contextual, especifica da Kouzina ou proibida.
- Papel comercial: complemento, alternativa, mesma suite ou editorial.
- Forca da evidencia: a relacao vem do tipo de produto ou apenas de marca,
  preco, premium e ambiente?
- Qualidade da explicacao: o `reason` explica a decisao de forma auditavel?
- Status comercial: produto `Sob consulta` ajuda uma venda consultiva ou reduz
  confianca no carousel?
- Utilidade academica: o julgamento pode virar rotulo claro para baseline,
  ontologia e fuzzy?

## Exemplos De Recomendacoes Fortes

- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Linea Touch | Franke`.
  Relacao forte quando o kit for compativel com o modelo. Label sugerida:
  `universal`, `complemento`, `compatibilidade_instalacao`, `mesma_marca`.
  Rating provavel: `4` ou `5`.

- `Cuba Box De Embutir e Sobrepor 54x41 | Franke -> Misturador Monocomando |
  Franke`. Relacao estrutural de area molhada. Label sugerida: `universal`,
  `complemento`, `area_molhada`, `mesma_marca`. Rating provavel: `5`, com
  observacao sobre furacao, altura e acabamento.

- `Misturador Monocomando | Franke -> Cuba de Sobrepor/Embutir | Franke`.
  Relacao inversa igualmente defensavel. Rating provavel: `4` ou `5`, desde
  que nao dependa de medida ausente.

- `Cooktop -> Coifa/Forno`. Relacao classica de coccao, exaustao e composicao
  de cozinha planejada. Rating provavel: `4` ou `5`, dependendo de largura,
  tipo de instalacao e voltagem.

- `Forno -> Micro-ondas/Cooktop/Coifa`. Forte quando estiver em suite de
  embutidos ou composicao de coccao. Rating provavel: `4`, podendo chegar a
  `5` quando mesma linha e acabamento forem confirmados.

- `Adega -> Cervejeira/Frigobar` e `Churrasqueira -> Cervejeira/Adega`.
  Relacoes boas para estacao de bebidas e espaco gourmet, mas contextuais.
  Rating provavel: `4`, com comentario exigindo ambiente/projeto.

## Exemplos De Recomendacoes Fracas

- `Set Azeite & Vinagre Le Creuset -> Cuba/Misturador/Painel de Lava-Loucas`.
  O sistema leu `Acessorio de Cozinha` como tipo complementar, mas o item e
  decorativo/de mesa. Relacao deve ser tratada como editorial fraca ou
  proibida para ranking automatico. Rating provavel: `1` ou `2`.

- `Dispenser de Agua Sole Built-in -> Churrasqueira/Adega/Frigobar` apenas por
  marca, faixa de preco, ambiente e premium. Pode existir em projeto gourmet,
  mas nao como relacao universal. Rating provavel: `2` ou `3`, com label
  `contextual_fraca`.

- `Lavadora -> Adega/Coifa` e `Secadora -> Forno/Rangetop`. Esses casos mostram
  vazamento por voltagem, preco e premium entre lavanderia e cozinha gourmet.
  Devem ser proibidos ou fortemente restringidos. Rating provavel: `1`.

- `Fogao -> Gaveta Aquecida/Coifa` quando todos os itens estao `Sob consulta`
  e a razao e generica. Pode fazer sentido em suite, mas precisa de contexto de
  linha, instalacao e disponibilidade. Rating provavel: `2` a `4`, dependendo
  da confirmacao comercial.

## O Que Deve Ser Mantido

- O uso de `reviewer_rating` de 1 a 5 como julgamento humano principal.
- O `reviewer_comment` como campo obrigatorio para casos nota 1, 2, 3 e para
  qualquer produto `Sob consulta`.
- A separacao entre relacoes universais, contextuais, especificas da Kouzina e
  proibidas.
- A distincao entre complemento, alternativa, mesma suite e editorial.
- A exclusao do proprio produto como regra inegociavel.
- O v0 como baseline explicavel antes de fuzzy e ontologia.
- A revisao por amostra estratificada, nao 120 cards em sequencia.

## O Que Deve Ser Restringido

- `Mesmo ambiente` deve ser apenas sinal auxiliar; nao deve salvar uma relacao
  sem complementaridade real.
- `Faixa premium semelhante` e `preco proximo` devem ser tratados como
  moderadores, nao como fundamento da recomendacao.
- `Mesma marca` deve ser separada de `mesma linha`, `mesma colecao` e `mesma
  suite`; marca sozinha nao garante compatibilidade.
- Produtos `Sob consulta` devem aparecer quando forem tecnicamente fortes ou
  consultivos, mas nao devem dominar o top-k sem justificativa.
- Acessorios genericos precisam ser subdivididos: acessorio tecnico, acessorio
  decorativo, acessorio de instalacao, acessorio de uso.
- Relacoes entre dominios diferentes, como lavanderia e cozinha gourmet, devem
  exigir justificativa explicita.

## O Que Deve Ser Removido

- Relacoes automaticas de acessorio decorativo para produto estrutural.
- Recomendacoes entre lavanderia e coccao/refrigeracao gourmet sem projeto
  declarado.
- Pares puxados apenas por preco, premium, voltagem ou marca sem relacao
  funcional.
- Reasons genericas que dizem "produto complementar" quando a
  complementaridade nao e clara para o especialista.
- Uso de item `Sob consulta` como top-1 quando houver equivalente precificado e
  comercialmente mais claro.

## Como Transformar Comentarios Da Reuniao Em Dataset Rotulado

Cada linha revisada deve virar uma unidade de rotulagem:

```text
source_product_id
recommended_product_id
reviewer_id
reviewer_role
reviewer_rating
reviewer_comment
relation_scope
relation_kind
decision
labels
requires_context
quote_policy
reason_quality
review_round
```

Na planilha atual, isso pode ser registrado inicialmente dentro de
`reviewer_comment` em formato padronizado, sem alterar o codigo:

```text
scope=universal; kind=complemento; decision=manter; labels=area_molhada,mesma_marca; note=confirmar furacao e acabamento
```

Depois da reuniao, esse texto pode ser normalizado para um dataset de pesquisa.
O dataset rotulado deve preservar o score original do v0 para permitir comparar
o ranking antes e depois da curadoria humana.

## Labels Que Deveriam Ser Extraidos

Labels principais:

- `scope_universal`
- `scope_contextual`
- `scope_kouzina`
- `scope_proibida`
- `kind_complemento`
- `kind_alternativa`
- `kind_mesma_suite`
- `kind_editorial`

Labels tecnicas:

- `requires_voltage_match`
- `requires_width_match`
- `requires_installation_match`
- `requires_finish_match`
- `requires_opening_side`
- `requires_panel_ready`
- `requires_project_context`
- `requires_consultancy`

Labels de risco:

- `weak_same_environment`
- `weak_same_brand_only`
- `weak_price_only`
- `weak_premium_only`
- `cross_domain_leakage`
- `decorative_to_structural`
- `quote_only_topk_risk`
- `generic_reason`

Labels de decisao:

- `keep`
- `restrict`
- `remove`
- `demote`
- `needs_manual_relation`
- `needs_better_attributes`
- `needs_reason_rewrite`

## Como Usar Nota 1 A 5

Use a nota como julgamento ordinal, nao como probabilidade:

- `1`: ruim. Nao faz sentido; remover ou bloquear a relacao.
- `2`: fraca. Existe alguma associacao, mas nao deve aparecer no top-k sem
  contexto.
- `3`: aceitavel. Pode aparecer abaixo de relacoes fortes; exige reason melhor
  ou atributo faltante.
- `4`: boa. Comercialmente defensavel; manter, talvez com restricao tecnica.
- `5`: excelente. Complemento natural, quase obrigatorio ou suite evidente.

Para uso academico:

- binarizar `4` e `5` como relevante em metricas `Precision@k` e `Recall@k`;
- tratar `3` como parcialmente relevante em `nDCG@k`;
- tratar `1` e `2` como nao relevante;
- manter a escala completa para correlacao com score do v0 e calibragem fuzzy.

## Concordancia Entre Especialistas

Se houver mais de um especialista, usar no minimo:

- dois avaliadores por linha em uma amostra de 24 a 40 recomendacoes;
- media e desvio da nota por relacao;
- percentual de concordancia exata;
- percentual de concordancia relaxada, considerando diferenca maxima de 1 ponto;
- Cohen's Kappa para dois avaliadores, com categorias `baixa`, `media` e
  `alta` relevancia;
- Fleiss' Kappa se houver tres ou mais avaliadores.

Para decisao pratica da Fase 4.8:

- manter relacoes com media >= 4 e concordancia relaxada >= 70%;
- restringir relacoes com media entre 3 e 3,9 ou alta divergencia;
- remover ou bloquear relacoes com media < 3;
- levar para nova rodada qualquer relacao com comentarios contraditorios.

## Como Usar As Decisoes Para Ajustar O v0 Depois

Sem alterar o ranking nesta fase, as decisoes devem gerar uma fila de ajustes:

- `keep`: manter a relacao no baseline e documentar como candidata a ontologia.
- `restrict`: exigir contexto, ambiente, instalacao, voltagem, largura ou
  categoria especifica antes de pontuar.
- `remove`: retirar a relacao do conjunto editorial futuro.
- `demote`: manter como recomendacao secundaria, nao top-k principal.
- `manual_relation`: cadastrar relacao especifica da Kouzina em fase futura.
- `reason_rewrite`: melhorar a explicacao sem mudar a relacao.

O ajuste do v0 deve acontecer somente depois da consolidacao da reuniao, usando
os comentarios como evidencia. A prioridade deve ser corrigir falsos positivos
fortes antes de tentar aumentar cobertura.

## Uso Das Decisoes Na Fase 5

Na Fase 5, as notas da Kouzina devem servir para construir o protocolo de
baseline academico:

- definir o v0 como baseline explicavel;
- criar um gold set pequeno de pares rotulados por especialista;
- selecionar dataset publico comparavel para avaliacao reproduzivel;
- mapear `reviewer_rating` para relevancia offline;
- separar avaliacao comercial local de avaliacao academica generalizavel.

Entregavel sugerido: protocolo que explica como o gold set da Kouzina foi usado
para calibrar criterios, mas nao como unica prova academica.

## Uso Das Decisoes Na Fase 6

Na Fase 6, as relacoes aprovadas devem orientar a ontologia minima:

- `scope_universal` vira candidata a propriedade semantica estavel;
- `scope_contextual` vira relacao condicionada por `Environment` ou
  `ProjectContext`;
- `scope_kouzina` fica fora da ontologia universal e entra como camada
  editorial;
- `scope_proibida` vira restricao ou teste negativo;
- `kind_complemento`, `kind_alternativa`, `kind_mesma_suite` e
  `kind_editorial` viram tipos distintos de relacao.

Nao se deve formalizar na ontologia relacoes que a reuniao marcou como fracas
ou especificas da loja-piloto sem essa separacao explicita.

## Uso Das Decisoes Na Fase 7

Na Fase 7, os labels devem calibrar o motor fuzzy:

- ratings `5` ajudam a definir pertinencia alta de complementaridade funcional;
- ratings `4` ajudam a definir relacoes boas com restricoes tecnicas;
- ratings `3` ajudam a calibrar zona intermediaria;
- ratings `1` e `2` ajudam a criar penalidades e regras de baixa relevancia;
- comentarios sobre `Sob consulta` ajudam a criar `quote_acceptability`;
- comentarios sobre reason ajudam a definir `recommendation_confidence`.

Variaveis fuzzy candidatas:

- `functional_complementarity`
- `technical_compatibility`
- `environment_affinity`
- `brand_line_affinity`
- `price_proximity`
- `quote_acceptability`
- `reason_confidence`

## Metricas Futuras

Metricas offline:

- `Precision@k`
- `Recall@k`
- `nDCG@k`
- `MRR`
- cobertura por tipo de produto;
- taxa de falsos positivos por relacao;
- correlacao entre score v0 e `reviewer_rating`;
- erro medio absoluto entre score normalizado e nota humana;
- concordancia entre especialistas.

Metricas online futuras, somente depois de deploy controlado:

- impressao por widget;
- CTR por produto de origem;
- CTR por tipo de relacao;
- clique assistido;
- taxa de clique em itens `Sob consulta`;
- diversidade do carousel;
- taxa de abandono ou ausencia de clique quando top-k tem excesso de itens sem
  preco.

Metricas academicas complementares:

- comparacao v0 vs baseline simples;
- comparacao v0 vs ontologia minima;
- comparacao v0 vs fuzzy;
- analise de ablation por criterio: tipo, ambiente, marca, preco, voltagem e
  disponibilidade.

## O Que Nao Pode Ser Concluido So Com Essa Reuniao

A Fase 4.8 nao permite concluir:

- que o recomendador aumenta CTR;
- que o recomendador aumenta receita;
- que o ranking generaliza para outros e-commerces high-end;
- que ontologia fuzzy melhora o v0;
- que a nota de especialista equivale a comportamento real de usuario;
- que produtos `Sob consulta` performam melhor ou pior;
- que a ordem atual do top-k e otima;
- que as relacoes especificas da Kouzina sao universais.

A reuniao produz rotulos especializados. Ela nao substitui experimento offline,
dataset publico, teste online, metricas de clique ou avaliacao estatistica.

## Perguntas Para A Reuniao Real Com A Kouzina

- Esta relacao e complemento, alternativa, mesma suite ou editorial?
- Ela e universal do dominio ou especifica da Kouzina?
- O item recomendado deveria aparecer no top-1, no top-k baixo ou nunca?
- Qual atributo faltante mudaria sua avaliacao: largura, voltagem, instalacao,
  acabamento, abertura, linha, colecao ou estoque?
- O produto `Sob consulta` deve aparecer neste contexto? Por que?
- A ausencia de preco exige CTA consultivo ou reduz confianca?
- Existe um produto que deveria aparecer antes deste?
- O motivo textual atual seria aceitavel para cliente final?
- A relacao depende de arquiteto, projeto ou atendimento consultivo?
- Esse par deve virar exemplo positivo, exemplo negativo ou excecao editorial?

## Decisoes Sugeridas Para Registrar Em reviewer_comment

Exemplos de comentarios padronizados:

```text
scope=universal; kind=complemento; decision=manter; labels=coccao,exaustao; note=confirmar largura e instalacao
```

```text
scope=contextual; kind=complemento; decision=restringir; labels=espaco_gourmet,bebidas; note=mostrar apenas em projeto gourmet
```

```text
scope=kouzina; kind=editorial; decision=demote; labels=curadoria_comercial; note=nao tratar como relacao universal
```

```text
scope=proibida; kind=none; decision=remover; labels=cross_domain_leakage; note=lavanderia nao deve puxar coccao
```

```text
scope=contextual; kind=mesma_suite; decision=restringir; labels=quote_only,mesma_linha; note=sob consulta aceitavel somente com atendimento consultivo
```

## Proximo Passo Recomendado

Realizar a reuniao com uma amostra estratificada de 24 a 40 recomendacoes,
preenchendo `reviewer_rating` e `reviewer_comment` com o formato padronizado
acima. Depois, consolidar as decisoes em uma tabela de relacoes com quatro
estados: `manter`, `restringir`, `remover` e `editorial Kouzina`.

Somente depois dessa consolidacao faz sentido planejar ajuste do v0. Fase 5,
Fase 6 e Fase 7 devem usar os rotulos como insumo, nao como autorizacao para
pular direto para fuzzy, ontologia ou CTR.

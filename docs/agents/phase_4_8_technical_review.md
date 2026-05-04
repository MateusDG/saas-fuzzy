# Fase 4.8 - Revisao Tecnica De Instalacao, Eletrodomesticos E Marcenaria

Este documento registra a avaliacao simulada do agente "Especialista Tecnico
de Instalacao, Eletrodomesticos e Marcenaria" para a reuniao qualitativa da
Fase 4.8 do Kouzina Reco.

Escopo desta avaliacao:

- atuar como especialista de dominio, nao como programador;
- avaliar se as recomendacoes fazem sentido tecnicamente;
- revisar voltagem, largura, embutir, exaustao, area molhada, panel-ready,
  abertura de porta, capacidade, tipo de instalacao, uso interno/externo,
  marcenaria e dependencia de projeto tecnico;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao baixar imagens e nao versionar relatorios gerados.

## Diagnostico Tecnico

O recomendador v0 esta adequado como base de discussao, mas ainda nao esta
pronto para ser tratado como curadoria tecnica final. Ele acerta quando a
relacao depende de funcao evidente: coccao com exaustao, cuba com misturador,
adega com cervejeira/frigobar em uma estacao de bebidas, ou aparelhos
embutidos da mesma linha.

O risco principal e que o ranking ainda nao conhece atributos duros de projeto.
Ele ve tipo, marca, ambiente, preco, disponibilidade e voltagem, mas nao ve
largura real de nicho, largura de coifa versus cooktop, vazao de exaustao,
tipo de instalacao, abertura de porta, gas GLP/GN, panel-ready, furo de cuba,
pressao de agua, area interna/externa, clearance, profundidade ou necessidade
de marcenaria.

Do ponto de vista tecnico, isso significa que varias recomendacoes podem ser
comercialmente boas, mas devem receber comentario de cautela. A recomendacao
nao pode dar a entender que dois produtos sao compativeis apenas porque sao da
mesma marca, do mesmo ambiente ou da mesma faixa premium.

## Criterios Tecnicos Obrigatorios

- Compatibilidade eletrica: voltagem, bivolt, potencia, tomada/circuito
  dedicado e eventual incompatibilidade entre 127V e 220V.
- Compatibilidade dimensional: largura, altura, profundidade, nicho, recorte,
  folgas de ventilacao, largura de bancada e espaco de abertura.
- Tipo de instalacao: embutir, sobrepor, parede, ilha, built-in, undercounter,
  freestanding, mesa, parede, gas, eletrico, inducao, GLP/GN.
- Coifa versus equipamento de coccao: largura da coifa, tipo parede/ilha,
  vazao, duto/depurador, tipo de uso e largura do cooktop/rangetop/fogao.
- Area molhada: cuba, misturador, furo de bancada, mesa/parede, altura e
  alcance da bica, pressao minima e acabamento.
- Panel-ready e marcenaria: confirmacao de painel, largura, sistema de
  fixacao, peso do painel, puxador, abertura e modelo compativel.
- Abertura de porta: lado esquerdo/direito, reversibilidade e conflito com
  paredes, ilhas, outros modulos e portas vizinhas.
- Capacidade e modulo: litros, garrafas, servicos, bocas, largura modular de
  45/60/76/90/120 cm e coerencia com o projeto.
- Ambiente: uso interno, externo, gourmet coberto, area molhada, area de
  churrasqueira e resistencia adequada ao local.
- Produto sob consulta: precisa de razao tecnica ou consultiva clara para
  aparecer no topo.

## Criterios Usados Na Avaliacao

- `5 - excelente`: complemento natural e tecnicamente defensavel, com baixo
  risco mesmo antes de projeto detalhado.
- `4 - boa`: relacao tecnicamente forte, mas requer confirmacao de atributo
  especifico como medida, voltagem, abertura, acabamento ou modelo.
- `3 - aceitavel`: pode aparecer como inspiracao de projeto, mas nao como
  compatibilidade implicita.
- `2 - fraca`: relacao possivel apenas em contexto muito especifico; deve cair
  no ranking ou exigir filtro adicional.
- `1 - ruim`: relacao tecnicamente enganosa, sem complementaridade real ou
  cruzando dominios sem justificativa.

## Relacoes Tecnicamente Fortes

- `Cooktop/Rangetop/Fogao -> Coifa`: forte por funcao, mas exige largura,
  tipo de instalacao e vazao. A coifa deve ser compativel com a largura e com
  o modo de instalacao do equipamento de coccao.
- `Coifa -> Cooktop/Rangetop/Fogao`: forte como composicao de coccao e
  ventilacao, desde que nao ignore parede/ilha, largura, tensao e duto.
- `Cuba -> Misturador`: forte e quase universal para area molhada, com
  validacao de furo, tipo de bancada, altura/alcance da bica e acabamento.
- `Misturador -> Cuba`: forte, mas nao deve prometer compatibilidade sem saber
  se o misturador e de mesa ou parede e se a cuba comporta a instalacao.
- `Lava-loucas -> painel/acessorio compativel`: forte quando o produto for
  panel-ready e o painel for do mesmo modelo, largura e servicos.
- `Forno/Micro-ondas/Cafeteira/Gaveta Aquecida embutidos`: forte como suite
  vertical ou horizontal quando linha, altura, nicho, voltagem e acabamento
  forem coerentes.
- `Adega -> Cervejeira/Frigobar/Maquina de Gelo`: forte em estacao de bebidas,
  bar ou espaco gourmet, mas contextual e dependente de medidas, ventilacao e
  abertura de portas.
- `Churrasqueira/Forno de Pizza -> refrigeracao gourmet/preparo`: forte em
  area gourmet quando o produto e adequado ao ambiente e ao projeto tecnico.
- `Lavadora -> Secadora`: tecnicamente forte dentro de lavanderia, desde que
  capacidade, voltagem, empilhamento, ventilacao/exaustao e drenagem sejam
  compativeis.

## Exemplos De Recomendacoes Fortes Observadas

- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Linea Touch | Franke`:
  relacao tecnicamente forte se o kit for realmente compativel com o modelo da
  coifa. Rating sugerido: `4`; subir para `5` apenas com compatibilidade de
  modelo confirmada.
- `Cuba Box De Embutir e Sobrepor 54x41 | Franke -> Misturador Monocomando |
  Franke`: relacao forte de area molhada. Rating sugerido: `5`, com comentario
  para confirmar furo de bancada, altura da bica e acabamento.
- `Misturador Monocomando de Mesa Aco Inox Eos Neo Fosco | Franke -> Cubas
  Franke`: boa relacao por funcao e marca. Rating sugerido: `4` ou `5`,
  dependendo da furacao, alcance da bica e tipo de cuba.
- `Adega Dual Zone Professional 46 Garrafas 136L 60cm 220V | Tecno ->
  Frigobar Professional Ab. Esquerda 136L 60cm 220V | Tecno`: forte como suite
  de refrigeracao modular de 60 cm. Rating sugerido: `4`, exigindo validar
  abertura de porta e ventilacao.
- `Adega Dual Zone Professional 46 Garrafas 136L 60cm 220V | Tecno ->
  Cervejeira Professional Ab. Esquerda Inox 433L 60cm 220V | Tecno`: forte
  para estacao de bebidas premium, mas deve ser marcada como contextual e sob
  consulta. Rating sugerido: `4`.
- `Lavadora Residencial Eletrica Branca 10,5kg 220V | SpeedQueen -> Secadora
  Residencial Eletrica Branca 10,5kg 220V | SpeedQueen`: relacao tecnicamente
  coerente dentro de lavanderia. Rating sugerido: `4` ou `5`, se instalacao e
  ventilacao forem adequadas.

## Relacoes Tecnicamente Arriscadas

- `Cooktop a Gas Inox 6 Bocas 93cm 220V -> Coifa de Parede 90cm 220V`: a
  relacao cooktop/coifa e correta, mas uma coifa de 90 cm para cooktop de 93 cm
  precisa revisao. Pode ser inadequada por largura, vazao e tipo de instalacao.
- `Coifa Dupla Parede New Calabria 120cm 127V -> Cooktop/Fornos 220V`: a
  relacao de coccao/exaustao existe, mas a mistura de 127V e 220V deve ser
  sinalizada. Pode ser aceitavel em projeto com circuitos separados, mas nao
  deve parecer compatibilidade automatica.
- `Lava-loucas de Embutir Inox 14 Servicos 60cm 220V -> Gaveta Aquecida,
  Coifa, Micro-ondas ou Cooktop`: tecnicamente fraca. A relacao vem de marca,
  ambiente ou faixa premium, nao de dependencia funcional da lava-loucas.
- `Dispenser de Agua Built-in 60cm 220V -> Adega/Frigobar/Churrasqueira`:
  pode fazer sentido em bar ou area gourmet, mas exige contexto de projeto.
  Como regra geral, e fraca.
- `Adega/Cervejeira/Frigobar com mesma abertura de porta`: pode ser positivo
  para padronizacao visual, mas a abertura esquerda/direita pode causar
  conflito dependendo da posicao no layout.
- `Produto sob consulta -> outro produto sob consulta` como top-1: aceitavel
  em projeto consultivo, mas arriscado quando nao ha explicacao tecnica clara.

## Relacoes Que Devem Exigir Atributo Adicional Antes De Recomendar

- Coifa e cooktop/rangetop/fogao: exigir `width_cm`, `installation_type`,
  `hood_type`, `airflow_capacity`, `ducted_or_filter`, `fuel_type` e contexto
  de parede/ilha.
- Cuba e misturador: exigir `sink_mount_type`, `tap_hole_count`,
  `faucet_mount_type`, `spout_height_cm`, `spout_reach_cm`, `water_pressure`
  e acabamento.
- Lava-loucas e painel decorativo: exigir `panel_ready`, `dishwasher_width_cm`,
  `place_settings`, `panel_model_compatibility`, `door_system` e peso do
  painel.
- Refrigeracao built-in: exigir `width_cm`, `height_cm`, `depth_cm`,
  `ventilation_type`, `opening_side`, `reversible_door` e tipo de instalacao.
- Lavadora e secadora: exigir `capacity_kg`, `stackable`, `voltage`,
  `dryer_venting_type`, `drainage_required` e dimensoes.
- Churrasqueira, coifa de churrasqueira e forno de pizza: exigir `indoor_outdoor`,
  `covered_area`, `fuel_type`, `gas_type`, `exhaust_required`, largura,
  material e restricoes de seguranca.
- Gaveta aquecida com forno/cafeteira/micro-ondas: exigir altura modular,
  largura, nicho, colecao/linha, acabamento e voltagem.
- Itens sob consulta: exigir `quote_reason`, `project_required`,
  `customizable`, `lead_time_days` e motivo tecnico da consulta.

## Produtos Sob Consulta Por Instalacao Ou Projeto

Produtos `Sob consulta` nao devem ser tratados como erro no catalogo. Em
eletrodomesticos premium, muitos itens dependem de projeto, disponibilidade,
configuracao, prazo, marcenaria, instalacao especializada ou venda consultiva.

Minha recomendacao para a reuniao:

- permitir `Sob consulta` quando o produto for tecnicamente forte para o item
  atual e houver motivo de projeto claro;
- evitar `Sob consulta` como top-1 quando existir alternativa precificada e
  tecnicamente equivalente;
- exigir comentario em `reviewer_comment` explicando se a consulta e por
  instalacao, configuracao, prazo, importacao, marcenaria ou disponibilidade;
- nao misturar muitos itens `Sob consulta` no mesmo bloco sem justificar o
  valor consultivo;
- diferenciar `Sob consulta` de `indisponivel` e de `descontinuado` em fase
  futura.

## Quando Mesma Voltagem Deveria Ser Filtro Duro

Mesma voltagem deve ser filtro duro quando a recomendacao comunica substituicao
ou compatibilidade direta:

- alternativas do mesmo tipo de produto;
- acessorios ou kits eletricos dependentes de um modelo especifico;
- paineis, modulos ou componentes vendidos como parte do mesmo aparelho;
- suites built-in em que a loja quer prometer instalacao conjunta simples;
- recomendacoes de lavanderia, refrigeracao, forno, micro-ondas, cafeteira,
  gaveta aquecida, cooktop eletrico/inducao ou coifa quando o projeto nao
  informa circuitos separados;
- qualquer caso em que o usuario possa interpretar que basta comprar juntos.

Mesma voltagem pode ser criterio forte, mas nao necessariamente filtro duro,
quando os produtos sao complementares independentes e podem ter pontos
eletricos separados. Exemplo: um cooktop a gas 220V e uma coifa 127V podem
existir no mesmo projeto se a infraestrutura previr dois circuitos, mas isso
deve entrar como `requer confirmacao eletrica`, nao como recomendacao limpa.

Para produtos sem energia eletrica relevante, como cubas e alguns acessorios,
voltagem nao deve pesar.

## Campos Tecnicos Que Faltam No Catalogo

- `voltage_normalized` com valores controlados: `127v`, `220v`, `bivolt`,
  `not_applicable`, `unknown`.
- `power_watts`, `amperage`, `plug_type` e `dedicated_circuit_required`.
- `width_cm`, `height_cm`, `depth_cm`, `cutout_width_cm`,
  `cutout_height_cm`, `cutout_depth_cm`.
- `installation_type`: embutir, sobrepor, parede, ilha, built-in,
  undercounter, freestanding, mesa, parede.
- `fuel_type` e `gas_type`: eletrico, inducao, gas, GLP, GN, dual fuel.
- `hood_type`, `airflow_capacity`, `ducted_or_filter` e largura recomendada de
  equipamento de coccao.
- `sink_mount_type`, `tap_hole_count`, `faucet_mount_type`,
  `spout_height_cm`, `spout_reach_cm`, `water_pressure_min`.
- `panel_ready`, `panel_model_compatibility`, `door_system`,
  `panel_weight_limit`.
- `opening_side`, `reversible_door`, `hinge_type`.
- `capacity_l`, `capacity_bottles`, `place_settings`, `capacity_kg`,
  `burner_count`.
- `indoor_outdoor`, `covered_area_required`, `weather_resistant`.
- `finish_color`, `material`, `collection`, `design_line`.
- `project_required`, `quote_reason`, `lead_time_days`,
  `installation_notes`.

## O Que Deve Ser Mantido

- Manter coccao com exaustao como relacao forte, mas com checagem de largura e
  instalacao na revisao.
- Manter cuba com misturador como relacao tecnica universal.
- Manter suites de embutidos premium quando houver linha, modulo, acabamento e
  nicho coerentes.
- Manter refrigeracao gourmet combinada quando a proposta for estacao de
  bebidas ou area gourmet.
- Manter lavadora com secadora dentro do dominio de lavanderia.
- Manter `reason` textual, mas enriquecer futuramente com atributos tecnicos
  concretos.

## O Que Deve Ser Restringido

- Restringir coifa/cooktop quando a largura da coifa for menor que a largura do
  equipamento de coccao ou quando parede/ilha nao bater.
- Restringir relacoes com voltagem divergente, exigindo confirmacao de projeto
  eletrico.
- Restringir `Sob consulta` no topo sem motivo tecnico ou comercial claro.
- Restringir recomendacoes puxadas apenas por mesma marca, mesmo ambiente ou
  faixa premium.
- Restringir dispenser de agua com churrasqueira/adega/beer center a projetos
  de bar, gourmet ou apoio de bebidas.
- Restringir lava-loucas a cubas, area molhada, acessorios especificos e
  paineis compativeis; nao usar como ponte para coccao.
- Restringir refrigeracao com abertura de porta desconhecida em composicoes
  lado a lado.

## O Que Deve Ser Removido

- Produto decorativo de mesa, como set de azeite e vinagre, puxando cuba,
  misturador ou painel de lava-loucas como complemento tecnico.
- Lavadora ou secadora puxando adega, coifa, forno, fogao, cooktop ou rangetop.
- Lava-loucas puxando coifa, cooktop, micro-ondas ou gaveta aquecida apenas por
  marca, ambiente ou faixa premium.
- Dispenser de agua puxando churrasqueira como regra geral.
- Recomendacoes que parecem substituicao tecnica, mas trazem voltagem
  incompatvel sem aviso.
- Paineis decorativos de lava-loucas recomendados sem amarracao ao modelo
  compativel.

## Exemplos De Recomendacoes Fracas Observadas

- `Set Azeite & Vinagre Classico 17 cm Le Creuset -> Cuba Box De Embutir e
  Sobrepor 54x41 | Franke`: rating sugerido `1`. Produto decorativo de mesa
  nao deveria puxar produto tecnico de bancada.
- `Set Azeite & Vinagre Classico 17 cm Le Creuset -> Misturador Monocomando |
  Franke`: rating sugerido `1`. Nao ha dependencia tecnica nem projeto de
  instalacao comum.
- `Set Azeite & Vinagre Classico 17 cm Le Creuset -> Painel Decorativo Frente
  Lava-Loucas`: rating sugerido `1`. Parece vazamento por ambiente/premium.
- `Lava-loucas de Embutir Inox 14 Servicos 60cm 220V | Tecno -> Coifa de Ilha
  Original Inox Escovado 120cm 220V | Tecno`: rating sugerido `1` ou `2`.
  Mesma marca e voltagem nao bastam.
- `Lavadora Residencial Eletrica Branca 10,5kg 220V | SpeedQueen -> Adega 160
  Garrafas Dual Zone Built-in Connect 220v | Elettromec`: rating sugerido `1`.
  Cruza lavanderia com refrigeracao premium sem relacao de instalacao.
- `Secadora Residencial Eletrica Branca 10,5kg 220V | SpeedQueen -> Rangetop
  Master a Gas 91 cm 220v | Bertazzoni`: rating sugerido `1`. Mesmo nivel de
  preco/voltagem nao cria compatibilidade tecnica.
- `Dispenser de Agua Sole Built-in 60cm 220v | Elettromec -> Coifa
  Profissional Churrasqueira`: rating sugerido `2`; so faria sentido em
  projeto gourmet especifico, nao como regra universal.

## Perguntas Para A Reuniao Real Com A Kouzina

- A Kouzina quer que recomendacao comunique compatibilidade tecnica ou apenas
  inspiracao de projeto?
- Em coifas, qual regra comercial a loja usa para largura minima em relacao a
  cooktop, fogao, rangetop e churrasqueira?
- Coifa de parede, coifa de ilha e coifa para churrasqueira devem ser tratadas
  como subtipos separados?
- Para cooktops e fornos a gas, a loja precisa distinguir GLP e GN antes de
  recomendar complementos?
- A loja considera aceitavel recomendar 127V com 220V quando os produtos sao
  complementares, ou isso deve ser bloqueado visualmente?
- Em cubas e misturadores, quais atributos a equipe mais checa antes da venda:
  furo, pressao, bica, acabamento, instalacao ou medida?
- Produtos panel-ready devem aparecer apenas quando houver painel compativel do
  mesmo modelo?
- Em refrigeracao modular, a abertura de porta esquerda/direita deve ser
  otimizada para par lado a lado?
- Quais categorias `Sob consulta` sao consultivas por natureza e quais sao
  apenas falta de preco?
- A Kouzina prefere esconder itens `Sob consulta` quando ha produto precificado
  equivalente?
- Em area gourmet, quais produtos sao adequados para area externa, area
  coberta ou apenas uso interno?
- Quais recomendacoes deveriam obrigatoriamente receber aviso "consulte projeto
  tecnico"?

## Decisoes Sugeridas Para Registrar Em reviewer_comment

- `universal | complemento tecnico | aprovar | depende de largura/vazao/tipo de instalacao`
- `universal | area molhada | aprovar | confirmar furo de bancada, bica e acabamento`
- `contextual | estacao de bebidas | aprovar com cautela | validar abertura de porta, ventilacao e modulo 60cm`
- `contextual | suite built-in | aprovar | exige mesma linha, nicho, acabamento e voltagem`
- `contextual | sob consulta | aprovar somente com projeto | consulta por marcenaria/instalacao/prazo`
- `restringir | voltagem divergente | exige confirmacao eletrica antes de recomendar`
- `restringir | largura incerta | coifa deve ser validada contra largura do equipamento de coccao`
- `restringir | panel-ready | recomendar apenas se painel for compativel com modelo e servicos`
- `remover | acessorio decorativo nao complementa produto tecnico de bancada`
- `remover | lavanderia nao deve puxar cozinha gourmet ou refrigeracao`
- `remover | mesma marca/ambiente/preco nao justificam relacao tecnica`
- `proibida | recomendacao sugere compatibilidade tecnica sem atributos minimos`

## Proximo Passo Recomendado

Na reuniao da Fase 4.8, revisar uma amostra de 24 a 40 recomendacoes com uma
coluna mental de "risco tecnico". Para cada par, preencher `reviewer_comment`
com uma das decisoes acima e, quando necessario, anotar o atributo que falta.

O resultado desta rodada nao deve ser alteracao imediata de ranking. O proximo
passo correto e consolidar uma lista de relacoes aprovadas, restringidas e
removidas, mais uma lista de campos tecnicos prioritarios para enriquecer o
catalogo antes de qualquer fuzzy, ontologia, CTR ou deploy.

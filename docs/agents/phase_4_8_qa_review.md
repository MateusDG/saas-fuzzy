# Fase 4.8 - Auditoria Critica Da Revisao Qualitativa

Este documento registra a avaliacao simulada do agente "Auditor Critico" para
a reuniao qualitativa da Fase 4.8 do Kouzina Reco.

Escopo desta auditoria:

- atuar como especialista de dominio e qualidade de decisao, nao como
  programador;
- questionar conclusoes fracas dos demais especialistas;
- detectar vieses de catalogo, loja-piloto, marca, preco, ambiente e produto
  sob consulta;
- nao alterar codigo, ranking v0, API, banco, widget ou contrato;
- nao implementar fuzzy, ontologia, CTR, painel, login, Tray ou deploy;
- nao baixar imagens;
- nao versionar `reports/*.html` ou `reports/*.csv`.

## Diagnostico Do Auditor Critico

O recomendador v0 esta pronto para ser auditado em reuniao, mas ainda nao esta
pronto para virar regra semantica, politica universal ou base de ontologia. O
maior risco da Fase 4.8 nao e encontrar recomendacoes ruins; isso ja aparece no
CSV. O maior risco e aprovar recomendacoes plausiveis demais sem separar:

- complemento real;
- alternativa;
- mesma suite;
- merchandising editorial;
- curadoria especifica da Kouzina;
- coincidencia de preco, ambiente ou marca.

Os pareceres do Arquiteto e do Consultor Comercial convergem em bons pontos:
`Cuba -> Misturador`, `Cooktop/Rangetop -> Coifa`, `Rangetop -> Forno` e
`Adega -> Cervejeira/Frigobar` sao candidatos fortes. Mesmo assim, a auditoria
nao deve aceitar essas relacoes sem qualificadores. Em high-end, uma relacao
boa no nivel de categoria pode falhar no produto concreto por largura,
instalacao, abertura, acabamento, linha, combustivel, voltagem ou estado
comercial.

O pacote atual tem 120 linhas no CSV. Ha 40 recomendacoes com item recomendado
`Sob consulta` e 48 linhas com produto de origem `Sob consulta`. Isso e alto o
suficiente para virar tema central da reuniao, nao um detalhe. Tambem ha 49
linhas com score igual ou acima de 90, o que reforca outro alerta: score alto
no v0 nao significa confianca de especialista.

## Criterios Usados

- Complementaridade funcional: o recomendado completa o uso do produto atual?
- Compatibilidade tecnica: medida, largura, instalacao, combustivel, abertura,
  voltagem e marcenaria podem ser defendidos?
- Separacao entre complemento e alternativa: o item completa ou substitui?
- Evidencia de suite: marca so pesa quando houver linha, colecao, modulo,
  acabamento ou familia visual confirmada.
- Ambiente como contexto, nao como motor: mesmo ambiente nao deve aprovar item
  sem relacao funcional.
- Preco como guardrail, nao como prova: item caro ou premium nao e
  automaticamente coerente.
- Politica de `Sob consulta`: ausencia de preco exige motivo consultivo claro.
- Generalizacao: a relacao valeria em outro catalogo high-end ou e decisao da
  Kouzina?
- Risco de tipagem: produto mal classificado nao deve gerar regra.
- Clareza da reason: a explicacao precisa citar algo auditavel, nao apenas
  "mesmo ambiente" ou "faixa premium semelhante".

## Exemplos De Recomendacoes Fortes

- `Cuba Box De Embutir e Sobrepor 54x41 | Franke -> Misturador Monocomando |
  Franke`: forte como relacao de bancada, mas aprovar com dependencia de furo,
  altura, acabamento e instalacao. Rating sugerido: `4` ou `5`.
- `Misturador Monocomando | Franke -> Cubas Franke`: forte, desde que a reuniao
  nao confunda qualquer cuba com cuba compativel. Rating sugerido: `4` ou `5`.
- `Rangetop Master Bertazzoni -> Forno Bertazzoni`: forte como suite de coccao
  e projeto high-end, desde que linha, dimensao e proposta de cozinha planejada
  sejam confirmadas. Rating sugerido: `5`.
- `Rangetop -> Coifa 90cm`: forte como exaustao e coccao, mas a aprovacao deve
  exigir largura, vazao e tipo de instalacao. Rating sugerido: `4` ou `5`.
- `Kit Exaustor p/ Extractor Mythos | Franke -> Coifa Franke`: forte somente
  se o kit for efetivamente compativel com o modelo de coifa. Sem essa
  evidencia, deve ser `contextual/pendente`, nao universal.
- `Adega Tecno -> Cervejeira/Frigobar Tecno Professional`: comercialmente
  plausivel para estacao de bebidas, mas nao universal. Deve ser aprovado como
  contextual ou suite, especialmente quando os itens estao `Sob consulta`.

## Exemplos De Recomendacoes Fracas

- `Set Azeite & Vinagre Le Creuset -> Cuba Franke`: fraca. Um acessorio de
  mesa/decorativo nao deve puxar produto tecnico de bancada como complemento.
  Rating sugerido: `1` ou `2`.
- `Set Azeite & Vinagre Le Creuset -> Misturador Franke`: fraca como
  recomendacao automatica. Pode ate ser merchandising editorial, mas nao
  complemento. Rating sugerido: `2`.
- `Set Azeite & Vinagre Le Creuset -> Painel Decorativo Frente Lava-Loucas`:
  remover como complemento. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Adega Elettromec`: risco claro de preco/premium
  substituindo intencao de compra. Rating sugerido: `1`.
- `Lavadora SpeedQueen -> Cooktop e Coifa Mythos`: cruza lavanderia e cozinha
  gourmet sem relacao funcional. Rating sugerido: `1`.
- `Secadora SpeedQueen -> Fogao/Rangetop Bertazzoni`: parece afinidade por
  ticket e voltagem, nao venda consultiva. Rating sugerido: `1`.
- `Dispenser de Agua -> Churrasqueira/Coifa de Churrasqueira`: pode existir em
  projeto gourmet especifico, mas nao deve ser regra universal nem top de
  carousel sem contexto. Rating sugerido: `2`.
- `Cervejeira -> Coifa de churrasqueira`: contextual no maximo. Deve exigir
  projeto de espaco gourmet; fora disso, e vazamento de ambiente.

## O Que Deve Ser Mantido

- Complementaridade funcional como eixo principal da avaliacao.
- Exclusao do proprio produto.
- Reasons textuais, desde que a reuniao cobre explicacoes mais concretas.
- A taxonomia `universal`, `contextual`, `especifica Kouzina`, `restringir` e
  `remover`.
- A separacao entre complemento, alternativa, mesma suite e editorial.
- Produtos `Sob consulta` como possibilidade comercial em venda premium, mas
  nunca como selo automatico de valor.
- Revisao manual de 24 a 40 recomendacoes, com amostra estratificada e casos
  controversos obrigatorios.

## O Que Deve Ser Restringido

- `Sob consulta` no top-1 quando houver alternativa precificada equivalente.
- Marca como criterio forte sem linha, colecao, familia visual ou
  compatibilidade tecnica.
- Mesmo ambiente como justificativa principal.
- Faixa premium e preco proximo como argumentos de aprovacao.
- Relacoes gourmet amplas, como churrasqueira com bebidas e gelo, quando nao
  houver projeto completo.
- Relacoes de acessorios decorativos com produtos tecnicos.
- Relacoes aprovadas por apenas um especialista sem contraditorio.
- Conclusoes baseadas somente no catalogo atual da Kouzina.

## O Que Deve Ser Removido

- Decorativo de mesa puxando cuba, misturador, lava-loucas ou painel tecnico.
- Lavanderia puxando cozinha, gourmet, adega, forno, coifa, cooktop ou
  rangetop.
- Recomendacao sustentada apenas por preco, premium ou marca.
- Produto `Sob consulta` sem motivo consultivo claro.
- Relacao marcada como universal quando depende de politica comercial da
  Kouzina.
- Casos em que a tipagem parece errada, como refrigerador classificado como
  adega, ate revisao catalogal.

## 1. Principais Riscos Da Reuniao

- Consenso facil: todos concordarem com pares high-end plausiveis sem testar
  excecoes.
- Vies de loja-piloto: transformar o mix atual da Kouzina em verdade do
  dominio.
- Vies de ticket: aceitar recomendacao porque ambos os itens sao caros.
- Vies de marca: tratar mesma marca como suite, mesmo sem linha ou colecao.
- Vies de ambiente: deixar "Espaco Gourmet" puxar qualquer item gourmet.
- Vies de disponibilidade consultiva: romantizar `Sob consulta` como premium,
  quando pode frustrar o usuario.
- Confusao entre complemento e alternativa: recomendar substitutos dentro de um
  bloco chamado "complete seu projeto".
- Formalizacao precoce: transformar opiniao isolada de vendedor ou arquiteto em
  ontologia.
- Score como autoridade: aceitar score 95/100 como se fosse evidencia externa.
- Reason generica: aprovar relacao porque o texto parece correto, mesmo quando
  os atributos reais nao sustentam a recomendacao.

## 2. Perguntas Dificeis Que Precisam Ser Feitas

- Esta relacao continuaria correta em outro e-commerce high-end, com outras
  marcas e outro mix?
- Se removesse preco, marca e ambiente, ainda haveria complemento real?
- O cliente entenderia essa recomendacao em uma frase sem parecer empurro de
  ticket?
- O recomendado completa o produto atual ou substitui uma necessidade parecida?
- O produto `Sob consulta` deve aparecer antes de uma alternativa precificada?
  Por que?
- A recomendacao depende de largura, vazao, abertura, combustivel, marcenaria,
  instalacao ou voltagem?
- A marca e importante por suite/linha ou apenas por prestigio?
- Esse par e venda consultiva real ou apenas merchandising editorial da
  Kouzina?
- Que evidencia faria a reuniao mudar de ideia?
- Quem na Kouzina tem autoridade para classificar a relacao como universal,
  contextual ou especifica?

## 3. Decisoes Que Exigem Evidencia Adicional

- Aprovar `Acessorio de Coifa -> Coifa` como universal: exige compatibilidade
  de modelo, largura e instalacao.
- Aprovar `Coifa -> Forno/Cooktop/Rangetop` no produto concreto: exige tipo de
  coifa, vazao, largura e contexto de coccao.
- Aprovar `Adega -> Cervejeira/Frigobar` como forte: exige contexto de estacao
  de bebidas ou suite/linha.
- Aprovar `Churrasqueira -> Adega/Cervejeira/Maquina de Gelo`: exige projeto de
  espaco gourmet, nao apenas ambiente igual.
- Aprovar `Cafeteira -> Forno/Micro-ondas`: exige mesma linha visual ou modulo
  de built-in.
- Aprovar `Sob consulta` no top-1: exige motivo consultivo explicito e ausencia
  de alternativa precificada equivalente.
- Aprovar recomendacoes por marca: exige colecao, acabamento, linha ou venda
  conjunta recorrente.
- Marcar relacao como universal: exige pelo menos uma justificativa funcional
  ou tecnica que nao dependa da Kouzina.

## 4. Relacoes Que Devem Ser Testadas Com Mais Cuidado

- `Acessorio de Cozinha -> Cuba/Misturador/Lava-loucas`: separar acessorio
  funcional de acessorio decorativo.
- `Dispenser de Agua -> Adega/Frigobar/Churrasqueira`: provavelmente
  contextual fraco; testar com projeto real.
- `Cervejeira -> Churrasqueira/Coifa de Churrasqueira`: pode ser ambiente
  gourmet, mas nao complemento direto.
- `Churrasqueira -> Adega/Cervejeira`: validar se e estacao gourmet real ou
  cross-sell amplo.
- `Forno de Pizza -> Adega/Cervejeira`: validar se e composicao de area gourmet
  ou apenas proximidade editorial.
- `Lava-loucas -> Cuba/Misturador`: boa em area molhada, mas painel decorativo
  e marcenaria devem ser tratados separadamente.
- `Lavadora -> Secadora/Conjugada`: dentro de lavanderia e plausivel; qualquer
  salto para cozinha/gourmet deve ser removido.
- `Coifa -> Forno`: pode ser suite de coccao, mas coifa complementa mais
  diretamente cooktop/rangetop/churrasqueira.
- `Refrigerador -> Freezer/Frigobar/Cervejeira`: separar refrigeracao
  residencial, bebidas e gourmet.

## 5. O Que Nao Deve Virar Regra Universal

- "Produtos high-end combinam com produtos high-end."
- "Mesma marca sempre combina."
- "Mesmo ambiente basta."
- "Preco proximo indica afinidade."
- "Sob consulta e necessariamente premium."
- "Espaco gourmet autoriza qualquer relacao entre bebidas, churrasqueira,
  gelo, coifa e refrigeracao."
- "O que a Kouzina vende junto hoje vale para todo e-commerce high-end."
- "Produto recomendado com score alto e comercialmente correto."
- "Acessorio de cozinha sempre complementa qualquer produto de cozinha."
- "Opiniao de um especialista isolado e conhecimento ontologico."

## 6. Como Evitar Vies Da Loja-Piloto

- Registrar explicitamente `universal`, `contextual` ou `especifica Kouzina` em
  cada `reviewer_comment`.
- Exigir que relacoes universais sejam justificadas por funcao, tecnica,
  instalacao ou suite, nao por mix atual.
- Separar decisoes comerciais da Kouzina de conhecimento de dominio.
- Revisar uma amostra com casos fortes, medios, `Sob consulta` e controversos,
  nao apenas exemplos bonitos.
- Usar discordancia entre especialistas como dado, nao como problema a ocultar.
- Marcar casos dependentes de marca, campanha, estoque ou showroom como
  `especifica Kouzina`.
- Reavaliar relacoes aprovadas com um segundo catalogo ou dataset em fase
  academica posterior antes de formalizar ontologia.
- Manter `reviewer_comment` granular: motivo, dependencia, classificacao e
  restricao.

## 7. Criterios Minimos Para Aprovar Relacao Como Universal

Uma relacao so deve ser classificada como universal se cumprir todos estes
criterios:

- Existe complementaridade funcional, tecnica, de instalacao ou de suite
  verificavel.
- A relacao continua plausivel sem depender da marca especifica da Kouzina.
- A relacao continua plausivel sem depender de preco semelhante.
- A relacao continua plausivel fora do catalogo atual da loja-piloto.
- O recomendado nao e apenas alternativa disfarcada de complemento.
- A relacao tem excecoes conhecidas registradas: largura, voltagem, abertura,
  combustivel, instalacao, marcenaria, acabamento ou linha.
- Um especialista conseguiria explicar a recomendacao com atributo concreto.
- Produto `Sob consulta` nao e requisito para a relacao funcionar.
- A relacao recebe rating medio esperado de `4` ou `5` na amostra revisada e
  nao apresenta discordancia critica sem resolucao.
- O `reviewer_comment` contem a classificacao e a dependencia principal.

## Perguntas Para A Reuniao Real Com A Kouzina

- Quais relacoes a Kouzina considera consultivas e quais sao apenas
  merchandising?
- Em quais categorias `Sob consulta` e aceitavel no carousel?
- O top-1 pode ser `Sob consulta`? Em quais excecoes?
- O vendedor recomendaria este par espontaneamente ou apenas se houvesse
  campanha?
- Existe linha, colecao ou suite confirmada para este par?
- O recomendado exige medida, nicho, ventilacao, ponto hidraulico, abertura ou
  marcenaria especifica?
- O par funciona em outro catalogo high-end ou so no mix da Kouzina?
- Que recomendacao deveria aparecer antes desta?
- Algum item esta classificado com tipo errado?
- Qual relacao aprovada hoje nao deve virar ontologia futura?

## Decisoes Sugeridas Para Registrar Em `reviewer_comment`

- `universal; complemento; aprovar; cuba e misturador; validar furo,
  acabamento e instalacao.`
- `universal; complemento tecnico; aprovar; coccao e exaustao; validar largura,
  vazao e tipo de coifa.`
- `mesma suite; aprovar; depende de linha, modulo visual e acabamento
  confirmados.`
- `contextual; espaco gourmet; aprovar no top-3; depende de projeto com
  bebidas/refrigeracao.`
- `contextual; estacao de bebidas; aprovar; nao tratar como universal.`
- `sob consulta; permitir; item consultivo/configuravel; exige explicacao
  comercial.`
- `sob consulta; restringir; nao usar top-1 com alternativa precificada
  equivalente.`
- `restringir; mesma marca sem evidencia de linha ou suite.`
- `restringir; mesmo ambiente sem complemento funcional suficiente.`
- `remover; decorativo puxando produto tecnico sem intencao de compra.`
- `remover; lavanderia cruzando com cozinha/gourmet.`
- `remover; recomendacao sustentada por preco/premium, sem funcao.`
- `pendente; revisar tipagem do catalogo antes de aprovar.`

## Proximo Passo Recomendado

Na reuniao simulada ou real, usar este parecer como checklist de contraditorio.
Antes de consolidar qualquer decisao, escolher 24 a 40 recomendacoes com pelo
menos:

- 8 casos fortes;
- 6 casos `Sob consulta`;
- 6 casos contextuais de gourmet/bebidas;
- 6 casos fracos ou controversos;
- 4 casos de possivel erro de tipagem ou confusao complemento/alternativa.

Depois, preencher `reviewer_rating` e `reviewer_comment` com classificacao,
motivo e dependencia. A proxima acao deve ser consolidar evidencias da reuniao,
nao alterar ranking, implementar fuzzy, criar ontologia, medir CTR ou fazer
deploy.

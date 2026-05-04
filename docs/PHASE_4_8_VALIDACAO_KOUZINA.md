# Pesquisa aprofundada sobre o recomendador high-end e a transição para ontologia fuzzy

## Nota de uso no projeto

Este documento e uma pesquisa de apoio para preparar a Fase 4.8. Ele nao
autoriza implementacao imediata de fuzzy, ontologia, deploy, CTR, painel,
integracao Tray ou mudanca no ranking v0.

Os marcadores de referencia no formato `turnXsearchY`, `turnXviewY` e
`turnXfileY` vieram do processo de pesquisa e nao devem ser tratados como links
reais do repositorio. Antes de usar este conteudo em texto academico final, as
referencias devem ser revisadas, substituidas por citacoes verificaveis e
normalizadas conforme o padrao exigido pelo TCC.

Uso pratico nesta fase:

- preparar a reuniao qualitativa com a Kouzina;
- separar relacoes universais, contextuais e especificas da loja-piloto;
- definir politica inicial para produtos sob consulta;
- gerar rotulos de especialista a partir de `reviewer_rating` e
  `reviewer_comment`;
- adiar fuzzy e ontologia ate que as relacoes do v0 sejam revisadas.

## Resumo executivo

A proposta do TCC estabelece um destino metodológico claro: um sistema de recomendação híbrido, baseado em ontologias fuzzy, capaz de lidar com preferências graduais, conhecimento semântico do domínio e cenários de cold start, com validação em datasets públicos. O estado atual do projeto, porém, ainda é explicitamente um MVP comercial com ranking v0 por regras; o próprio repositório informa que fuzzy e ontologia continuam fora de escopo nesta fase e que a revisão qualitativa deve acontecer antes de métricas, CTR e qualquer camada semântica mais sofisticada. Em outras palavras: o projeto está **coerente como baseline operacional**, mas **ainda não está próximo do método final prometido pela proposta**. fileciteturn0file4 citeturn20view0turn22view0turn24view0

A reunião com a loja-piloto faz sentido, e mais do que isso: **ela é necessária**, mas com um papel bem delimitado. Ela serve para validar plausibilidade comercial, corrigir relações editoriais frágeis e gerar rótulos especializados para a próxima etapa. Ela **não substitui** validação acadêmica, não prova generalização e não basta sozinha para sustentar a parte “ontologia fuzzy” do TCC. O próprio projeto já documenta a revisão qualitativa como etapa anterior a métricas e às fases futuras de fuzzy e ontologia. citeturn24view0turn20view0turn22view0

A resposta curta para “por que ainda não foi implementado ontologias fuzzy?” é: porque o projeto está em uma fase em que ainda se está validando se as relações básicas do catálogo fazem sentido no mundo real. Isso é metodologicamente defensável. Formalizar cedo demais uma ontologia ou um motor fuzzy sobre relações ainda frágeis endureceria erros conceituais e comerciais no sistema. A literatura de recomendação semântica e de cold start reforça que ontologias e modelos híbridos ajudam exatamente quando há pouca interação histórica, mas a qualidade desse ganho depende da qualidade do conhecimento de domínio incorporado. citeturn10search0turn10search4turn10search5turn10search8

| Tipo de validação         | O que responde                                                         | A reunião resolve sozinha?              | O que ainda falta                                                                                                                                                                 |
| --------------------------- | ---------------------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validação acadêmica      | Se o método proposto melhora a recomendação de forma mensurável    | Não                                     | Dataset público, baseline comparável, métricas offline e, se possível, métricas online fileciteturn0file4 citeturn25search0turn25search5                       |
| Validação comercial       | Se a sugestão ajuda venda, projeto, curadoria e percepção de valor  | Parcialmente, sim                        | Depois da revisão, medir CTR, clique assistido e, idealmente, receita assistida citeturn24view0turn25search0                                                             |
| Validação de especialista | Se a relação “faz sentido” no contexto premium e no catálogo real | Sim, este é o papel central da reunião | Registrar rating, comentários e exceções por tipo de produto citeturn24view0                                                                                             |
| Validação generalizável  | Se as regras valem para outros e-commerces high-end                    | Não                                     | Separar relações universais, contextuais e específicas da loja-piloto; testar em catálogo público ou em segundo domínio citeturn22view0turn10search0turn10search8 |

## O que os anexos e o projeto atual mostram

**Evidência.** O repositório atual é apresentado como “MVP comercial mínimo de recomendação”, com API mínima, widget, catálogo importado, curadoria de tipo/ambiente/marca/voltagem, relações complementares comerciais iniciais e relatório CSV para revisão qualitativa. Fuzzy, ontologia, integração completa com plataforma, painel, login, deploy e ranking mais sofisticado estão explicitamente fora de escopo. O recomendador v0 soma pesos fixos: +30 para complementaridade de tipo, +20 para disponibilidade, +15 para mesma voltagem, +15 para faixa de preço próxima, +10 para mesma marca, +10 para mesmo ambiente e +10 para nível premium semelhante; indisponibilidade recebe penalidade. O catálogo oficial importado tem 281 produtos, com 52 itens “sob consulta”, e o relatório reconhece que essas relações complementares ainda precisam de validação qualitativa. citeturn20view0turn22view0turn23view0

**Evidência.** O pacote visual anexado para revisão qualitativa foi feito exatamente para essa etapa: discutir recomendações com especialista da loja, preencher `reviewer_rating` e `reviewer_comment`, e responder perguntas sobre complementaridade real, sentido comercial, reorder, presença de itens sob consulta e clareza da explicação. O HTML foi montado como artefato visual de revisão, não como mecanismo de feedback automatizado. fileciteturn0file5 citeturn24view0

**Inferência.** O projeto hoje está **mais próximo de um motor editorial explicável de merchandising** do que de um recomendador semântico-fuzzy completo. Isso não é incoerente; na verdade, é uma boa base. O problema é outro: se o TCC parar aqui, ele entrega um ranking por regras e uma revisão manual, não uma abordagem híbrida baseada em ontologia fuzzy. A coerência, portanto, é **de trajetória**, não **de chegada**. fileciteturn0file4 citeturn22view0turn24view0

**Inferência.** A leitura do anexo mostra sinais claros dessa transição incompleta. Há pares fortes, como recomendações entre superfícies de cocção e exaustão, entre cuba e misturador, e entre aparelhos embutidos de uma mesma família de cozinha. Mas também aparecem pares comercialmente fracos, como um acessório de mesa decorativo puxando cuba e misturador embutidos, ou itens de lavanderia puxando produtos de cozinha gourmet. Isso sugere que o v0 já captura alguma noção de complementaridade, mas ainda sofre de “vazamento” por ambiente, marca e faixa premium. fileciteturn0file5

**Recomendação.** A leitura correta do estágio atual é esta: ele está **suficientemente maduro para uma Fase 4.8 de validação especializada**, mas **ainda não é suficiente para dizer que a proposta de ontologia fuzzy foi implementada**. O próximo passo lógico não é pular direto para um motor fuzzy completo; é primeiro limpar relações fracas, enriquecer atributos e separar o que é universal do que é apenas editorial. citeturn22view0turn24view0turn10search0turn10search5

## Matriz de decisão para as perguntas centrais

| Pergunta                                                                   | Resposta provável para e-commerce high-end                                                                                                                            | Evidências encontradas                                                                                                                                                                                                                                                                                       | Impacto no recomendador                                                                               | Regra prática                                                                                                                                 |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Essa recomendação faz sentido comercial?                                 | Só quando ajuda o cliente a completar a compra, o projeto ou a “suite” do ambiente — e não quando parece um empilhamento arbitrário de marca, ambiente e preço. | Recomendações suplementares ajudam usuários a “finish the package”, mas precisam ser distintas de alternativas; no luxo, clientes estão mais críticos com preço, qualidade e valor percebido. citeturn0search1turn2search0turn0search48                                                     | O v0 precisa premiar complementaridade real e parar de elevar links apenas por vizinhança editorial. | Colocar “sentido comercial” depois de “compatibilidade funcional/técnica” e antes de preço.                                              |
| Esse produto realmente complementa o produto atual?                        | Complementaridade forte é funcional, técnica, de instalação ou de suite; “mesmo ambiente” sozinho não basta.                                                    | Fabricantes premium documentam relações claras como cocção→ventilação, cuba→misturador, café embutido→linha de fornos/micro-ondas e lava-louças panel-ready→integração com marcenaria. citeturn4search3turn5search2turn6search0turn16search0turn16search1                         | Complementaridade deve virar o eixo central do ranking.                                               | Criar relação primária `complements` e subtipos: funcional, técnica, estética, instalação.                                            |
| Algum produto deveria aparecer antes?                                      | Sim. Complementos obrigatórios e compatíveis devem subir; itens apenas “parecidos” ou “do mesmo ambiente” devem descer.                                          | Baymard mostra que complementares e alternativas têm finalidades diferentes e que rótulos/contextos claros importam; para itens indisponíveis ou descontinuados, alternativas devem ser promovidas agressivamente e em contexto próprio. citeturn0search1turn13search7turn8search0              | A ordenação atual precisa separar “complemento”, “alternativa” e “suite”.                     | Ordem sugerida: compatibilidade dura → complemento funcional → instalação → linha/coleção → ambiente → preço.                        |
| Produtos “sob consulta” devem aparecer?                                  | Sim, mas condicionalmente. Em premium/aparelhos consultivos, quote-only é aceitável; como default do carousel, não.                                                 | Preço é informação vital em PDP; preço ausente ou pouco visível gera incerteza e desconfiança. Ao mesmo tempo, marcas premium usam showrooms, especialistas e canais autorizados para decisões consultivas e projetos de cozinha. citeturn8search1turn14search0turn14search1turn14search5 | “Sob consulta” precisa deixar de ser tratado como meramente disponível.                            | Permitir itens quote-only apenas com badge claro, CTA consultivo e penalidade de ranking quando houver alternativas precificadas equivalentes. |
| A explicação do motivo está clara?                                      | Ainda não o suficiente para high-end. “Mesmo ambiente” e “faixa premium semelhante” são genéricos demais.                                                       | Rótulos claros ajudam usuários a interpretar sugestões; explicações em recomendadores elevam transparência e calibram confiança. citeturn13search7turn13search5turn13search10                                                                                                                | A reason precisa ser mais específica e verificável.                                                 | Trocar explicações genéricas por razões concretas: voltagem, largura, linha, panel-ready, uso outdoor, abertura, acabamento.               |
| Em produto high-end, marca pesa mais que preço?                           | Não de forma universal. Marca pesa muito em suite, coleção e simbolismo; preço pesa como guardrail de coerência e como sinal de valor percebido.                  | Estudos recentes indicam teto para aumentos de preço e questionamento da relação preço-qualidade no luxo; ao mesmo tempo, fabricantes premium vendem linhas combináveis e coleções estéticas consistentes. citeturn2search0turn0search48turn6search0turn7search4                          | Marca não pode empurrar produto incompatível; preço não pode derrubar produto ideal.              | Marca como bônus contextual; preço como moderador, nunca como critério principal isolado.                                                   |
| Ambiente pesa mais que categoria?                                          | Para descoberta e merchandising, muitas vezes sim; para compatibilidade e ranking final, não.                                                                         | Planejamento de cozinha e gourmet usa activity centers e zonas; porém relações como coifa↔cooktop dependem de largura, instalação e uso, não apenas do ambiente. citeturn7search0turn18search0turn4search3                                                                                   | “Ambiente” deve guiar navegação e segunda camada de ranking.                                      | Categoria/tipo domina como filtro base; ambiente entra como contexto adicional.                                                                |
| Quais relações são universais e quais são específicas da loja-piloto? | Universais são as que decorrem de função, instalação e suite; específicas são as editoriais, de catálogo e de curadoria comercial local.                       | As páginas oficiais de fabricantes sustentam pares universais; a documentação do projeto mostra que a lista atual ainda é curadoria inicial e não ontologia formal. citeturn4search3turn5search2turn16search0turn17search7turn22view0                                                      | O projeto precisa separar relações por classe.                                                      | Criar três camadas: universal, contextual por domínio e específica da loja-piloto.                                                          |

## Critérios comerciais para avaliar recomendações high-end

**Evidência da web.** Em e-commerce premium, a qualidade da recomendação não depende só de “quem comprou isto comprou aquilo”. Ela depende de um conjunto de fatores que aparecem repetidamente em UX de PDP, dados de catálogo, planejamento de cozinhas e suites premium, e literatura de recomendação contextual e semântica: atributos essenciais do produto, estado de oferta, imagens confiáveis, suíte/coleção, compatibilidade de instalação e explicação clara. Fontes de dados de produto e marcação estruturada também reforçam a centralidade de preço, disponibilidade, marca, identificadores, imagem e oferta como base mínima para experiência consistente. citeturn9search0turn9search2turn11search3turn11search7turn15search1turn9search6turn7search0turn18search0turn10search8

| Critério                       | Definição e por que importa                                                         | Como medir no catálogo                                                    | Como transformar em fuzzy                         | Universal ou específico                        |
| ------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| Complementaridade funcional     | Se o item ajuda a completar o uso do produto atual                                    | `product_type`, `relation_type`, uso principal                         | `low / medium / high complementarity`           | Universal                                       |
| Compatibilidade técnica        | Se tensão, largura, combustível, abertura, capacidade e interface são compatíveis | `voltage`, `width_cm`, `fuel_type`, `opening_side`, `capacity_l` | pertinência por distância/igualdade compatível | Universal                                       |
| Compatibilidade de instalação | Se o item pode ser instalado no mesmo projeto/mobiliário                             | `installation_type`, `panel_ready`, `cutout`, `mounting`           | `installation_fit`                              | Universal                                       |
| Consistência estética         | Se acabamento, cor e linguagem visual combinam                                        | `finish`, `color`, `design_line`, `collection`                     | `aesthetic_coherence`                           | Universal em high-end                           |
| Consistência de marca/linha    | Se a recomendação pertence à mesma família ou suite de marca                      | `brand`, `collection`, `series`                                      | `brand_line_affinity`                           | Universal em built-ins; opcional em acessórios |
| Ambiente de uso                 | Se o item pertence ao mesmo espaço de projeto                                        | `environment` como cozinha, gourmet, outdoor, lavanderia                 | `environment_affinity`                          | Universal, mas auxiliar                         |
| Faixa premium                   | Se o item ocupa patamar semelhante de posicionamento                                  | bucket de preço, marca, coleção, acabamento                             | `premium_similarity`                            | Universal                                       |
| Preço relativo                 | Se a sugestão é coerente com o ticket do item atual                                 | variação percentual, bucket de faixa                                     | `price_proximity` com peso baixo                | Universal, mas moderador                        |
| Disponibilidade                 | Se o item pode ser comprado agora, depois, por encomenda ou só por consulta          | `availability_status`, `lead_time_days`                                | `availability_strength`                         | Universal                                       |
| Produto sob consulta            | Se ausência de preço é aceitável naquele contexto                                 | `quote_only`, `quote_reason`, `dealer_only`                          | `quote_acceptability`                           | Universal, mas sensível ao domínio            |
| Margem comercial                | Se vale a pena promover em cross-sell                                                 | `margin_band` ou proxy interno                                           | `business_priority`                             | Específico da loja                             |
| Intenção da jornada           | Se o usuário está em descoberta, comparação, projeto ou finalização             | widget/contexto, página, tipo de PDP                                      | `journey_fit`                                   | Contextual                                      |
| Nível de confiança            | Se a recomendação é sustentada por dados suficientes                               | contagem de critérios válidos, validação especialista                  | `confidence_score`                              | Universal                                       |
| Explicabilidade                 | Se o motivo pode ser explicado de forma concreta                                      | cobertura dos atributos usados                                             | `explainability_strength`                       | Universal                                       |

**Inferência para o seu projeto.** O v0 já tem a intuição correta ao usar complementaridade, disponibilidade, voltagem, preço, marca, ambiente e nível premium. O problema é que essas variáveis ainda são discretas, somadas em bloco, e várias delas estão com semântica muito larga. Ambiente, por exemplo, está concentrado em etiquetas amplas do catálogo oficial; isso ajuda descoberta, mas pode aproximar produtos que dividem o mesmo espaço e não a mesma intenção de compra. O mesmo vale para “mesma marca” e “faixa premium semelhante”, que são bons critérios de desempate, mas ruins como motor principal de relevância. citeturn22view0turn23view0

**Recomendação prática.** Para a próxima versão do CSV/HTML de revisão, faltam pelo menos estes campos: `availability_status` (`in_stock`, `backorder`, `quote_only`, `discontinued`), `quote_reason`, `lead_time_days`, `installation_type`, `width_cm`, `opening_side`, `panel_ready`, `collection/design_line`, `finish/color`, `indoor_outdoor`, `relation_type` (`mandatory_accessory`, `functional_complement`, `same_suite`, `alternative`) e `confidence_score`. Sem isso, a revisão fica excessivamente subjetiva e a ontologia futura fica pobre demais. citeturn9search0turn11search3turn11search7turn15search1turn16search0turn17search3

## Marca, preço, ambiente e produtos sob consulta

### Quando marca pesa mais que preço

**Evidência da web.** O mercado de luxo passou a conviver com maior sensibilidade a preço, teto para elevação de ticket e questionamento do vínculo entre preço alto e qualidade percebida. Ao mesmo tempo, o premium de eletrodomésticos e cozinhas continua operando fortemente com linguagem de coleção, design line, craftsmanship, suite e experiência consultiva. Isso significa que “marca” continua relevante, mas já não funciona como passe livre para recomendar qualquer item do mesmo fabricante. citeturn2search0turn0search48turn14search1turn14search0turn6search0

**Inferência por segmento.**
Em **luxo aspiracional e decorativo**, marca, herança e storytelling pesam mais do que uma faixa exata de preço; o usuário compra também símbolo e linguagem visual. Em **eletrodomésticos premium embutidos**, o trio dominante passa a ser **compatibilidade técnica + coerência de linha + marca**; preço atua como guardrail para não sugerir algo muito abaixo ou muito acima do patamar esperado. Em **produtos técnicos de instalação**, como ventilação, cuba, misturador, panel-ready e appliances embutidos, marca só deve pesar depois de filtros técnicos. Em **acessórios de cozinha e mesa**, marca e coleção podem voltar a ganhar peso — mas aí o sistema deveria recomendar itens do mesmo universo de uso, não plumbing ou marcenaria por mera coincidência de ambiente. citeturn4search3turn5search2turn6search0turn16search0turn8search1

**Recomendação.** No motor futuro, “marca” não deve entrar como um peso fixo único. O melhor desenho é separar: `same_brand`, `same_collection`, `same_design_line` e `brand_prestige_tier`. Entre eles, `same_collection` e `same_design_line` são muito mais úteis que `same_brand` puro em produtos embutidos high-end. citeturn6search0turn7search4turn14search9

### Quando o ambiente pesa mais que a categoria

**Evidência da web.** O planejamento profissional de cozinhas e áreas gourmet usa activity centers, support spaces e zonas de uso, inclusive outdoor. Em áreas externas, por exemplo, a seleção costuma começar pelo contexto do espaço e então agregar cocção, preparo, água, refrigeração e acessórios. Já em relações como cooktop→coifa, o fabricante enfatiza largura, extração, modo de operação e tipo de instalação. citeturn7search0turn7search8turn18search0turn18search4turn4search3

**Inferência.** Portanto, em high-end o ambiente pesa mais em **descoberta**, **merchandising** e **curadoria de projeto**; a categoria pesa mais em **compatibilidade** e **ordem final do ranking**. Traduzindo para o seu sistema: ambiente deve ajudar a montar o “universo possível”; categoria/tipo e atributos técnicos devem decidir o “topo do ranking”. Isso é particularmente importante porque, no catálogo atual, o campo de ambiente está relativamente concentrado em poucos rótulos amplos, o que o torna útil como contexto, mas perigoso como critério central. citeturn23view0turn22view0

**Recomendação.** A regra de negócio ideal é hierárquica:
primeiro, filtros duros de tipo/instalação/voltagem/uso indoor-outdoor;
depois, complementaridade funcional;
depois, ambiente;
por fim, coleção/marca e preço relativo.
Essa ordem reduz justamente os falsos positivos observados na leitura do anexo. citeturn22view0turn18search0turn4search3

### Regra objetiva para produtos sob consulta

**Evidência da web.** Em PDP, preço é informação vital, e preço pouco visível ou ausente pode gerar frustração e desconfiança. Ao mesmo tempo, o mercado premium de cozinha trabalha com showrooms, especialistas, revendedores autorizados, alinhamento com marcenaria e decisões consultivas de projeto. Esse duplo regime explica por que “sob consulta” não é automaticamente errado — mas também por que não pode ser tratado como um item comum. citeturn8search1turn14search0turn14search1turn14search8turn14search5

**Regra recomendada para o ranking.**
Um item `quote_only` pode aparecer se, e somente se, ao menos uma destas condições for verdadeira:
o produto for claramente **configurável/de projeto**;
o fabricante trabalhar fortemente com **dealer/showroom/consultoria**;
ou a relação com o item atual for **tecnicamente forte** e pouco substituível.
Mesmo assim, ele não deve entrar como `top-1` por padrão quando houver uma alternativa precificada e comparável. Ele deve vir com badge explícito, CTA consultivo e explicação do tipo “Sob consulta por configuração/instalação, mas compatível com o projeto atual”. Isso reduz o choque entre UX de transparência e prática comercial premium. citeturn8search1turn14search1turn14search0turn9search0

**Regra objetiva sugerida.**
Se `availability_status = discontinued`, não mostrar como complementar; usar apenas módulo de alternativa/replacement.
Se `availability_status = quote_only`, aplicar penalidade moderada de ranking e exigir `compatibility_score` alto.
Se `price` estiver ausente, nunca usar regra de proximidade de preço.
Se mais de 25% do carousel ficar `quote_only`, substituir excedentes por itens precificados equivalentes.
Essa proposta é uma recomendação de projeto, derivada das evidências acima. citeturn22view0turn8search0turn8search1

## Relações universais, avaliação do v0 e tradução para ontologia fuzzy

### Relações universais, contextuais e específicas da loja-piloto

**Evidência da web.** Fabricantes premium documentam algumas relações com alta estabilidade semântica. Ventilação deve ser dimensionada em relação à superfície de cocção; cubas aparecem com misturadores e acessórios “perfectly matched”; lava-louças panel-ready se conectam diretamente à lógica de painéis e integração à marcenaria; linhas de embutidos de cozinha são vendidas como famílias combináveis; cozinhas externas agregam grill, pia/preparo, refrigeração e acessórios; e módulos de vinho/bebidas/refrigeração sob balcão são pensados como zonas complementares. citeturn4search3turn5search2turn5search3turn16search0turn16search1turn6search0turn18search0turn18search3turn17search3turn17search7

| Relação                                                               | Classificação                         | Justificativa                                                                     |
| ----------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------- |
| Cooktop → Coifa                                                        | Universal de cozinha/eletro             | É uma relação técnico-funcional e de dimensionamento                          |
| Cuba → Misturador                                                      | Universal de cozinha/eletro             | É complementaridade estrutural e de uso                                          |
| Lava-louças → Painel/integração/acessórios                         | Universal de cozinha/eletro             | Panel-ready e integração à marcenaria são parte do produto                    |
| Cafeteira embutida → Forno/micro-ondas da mesma linha                  | Universal em built-ins high-end         | A lógica é de suite e linguagem visual combinável                              |
| Churrasqueira → pia/preparo/refrigeração/acessórios/forno de pizza  | Universal contextual de gourmet/outdoor | Faz parte da zona de cocção e preparo                                           |
| Adega → cervejeira/frigobar                                            | Contextual                              | Faz sentido em “estação de bebidas”, mas não é obrigatório em todo projeto |
| Acessório de mesa decorativo → cuba/misturador/painel de lava-louças | Específico e fraco                     | Não há base universal forte; parece vazamento por ambiente/premium              |
| Lavadora/secadora → adega/coifa/forno/rangetop                         | Específico e inadequado                | Cruza domínios distintos sem complementaridade real                              |
| Dispenser de água → churrasqueira/adega                               | Contextual muito fraco                  | Pode ocorrer em áreas gourmet específicas, mas não deve virar regra universal  |

**Inferência.** A lista atual do v0 mistura relações universalmente defensáveis com curadoria editorial que ainda precisa de veto humano. Isso confirma que a reunião com a loja-piloto não é enfeite: ela é o mecanismo que vai separar conhecimento de domínio estável de mero palpite comercial inicial. citeturn22view0turn24view0

### Avaliação do recomendador v0

**Evidência.** O v0 é transparente, explicável e útil para cold start em catálogo pequeno porque depende de atributos do item, não de histórico de usuário. Isso é um ponto forte e é consistente com literatura que recomenda enriquecer recomendação com semântica/contexto em cenários de baixa interação. O repositório também acerta ao declarar que o score não é probabilidade e que as relações ainda são curadoria inicial. citeturn22view0turn10search0turn10search4turn10search8

| Critério atual do v0     | Julgamento                     | O que fazer                                                           |
| ------------------------- | ------------------------------ | --------------------------------------------------------------------- |
| Complementaridade de tipo | **Manter**               | Virar relação semântica central da ontologia                       |
| Disponibilidade           | **Manter e refinar**     | Separar `in_stock`, `backorder`, `quote_only`, `discontinued` |
| Mesma voltagem            | **Aumentar peso**        | Em vários casos, deve virar filtro duro de compatibilidade           |
| Faixa de preço próxima  | **Reduzir peso**         | Usar só dentro de cluster comparável; não como motor principal     |
| Mesma marca               | **Ajustar**              | Dividir em marca, coleção e design line                             |
| Mesmo ambiente            | **Manter como auxiliar** | Não deixar “ambiente” puxar item não complementar                 |
| Faixa premium semelhante  | **Transformar em fuzzy** | Útil como nuance, ruim como binário fixo                            |
| Reason textual            | **Manter e enriquecer**  | Tornar explicação concreta e auditável por atributo                |

**Conclusão sobre o baseline.** Sim, o v0 é um **bom baseline de TCC**, mas só se for tratado explicitamente como baseline. Ele é bom para mostrar:
um primeiro método explicável;
um ranking operacional em cold start;
um instrumento de revisão com especialista;
e um ponto de comparação para a camada futura.
Ele não é suficiente como entrega final do TCC porque ainda não cumpre a promessa central de ontologia fuzzy, nem produz validação comparativa por dataset público e métricas adequadas. fileciteturn0file4 citeturn22view0turn24view0turn25search5

### Tradução para ontologia fuzzy

**Evidência da web.** OWL foi feito para representar classes, propriedades, indivíduos e relações com semântica explícita; marcações de produto/oferta suportam preço e disponibilidade; bibliotecas fuzzy já oferecem funções triangulares, trapezoidais e gaussianas; e a literatura recente segue apontando valor em abordagens semânticas, context-aware e fuzzy para recomendação em e-commerce. citeturn11search1turn11search3turn11search7turn11search4turn10search0turn10search2turn10search5turn10search8

**Plano técnico mínimo.**

**Classes da ontologia**

- `Product`
- `ProductType`
- `Brand`
- `Collection`
- `Environment`
- `Offer`
- `AvailabilityState`
- `TechnicalSpec`
- `RelationType`
- `ProjectContext`

**Propriedades objetais**

- `hasType`
- `hasBrand`
- `belongsToCollection`
- `suitedForEnvironment`
- `hasOffer`
- `hasAvailabilityState`
- `complements`
- `alternativeTo`
- `requiresAccessory`
- `compatibleWith`
- `sameSuiteAs`

**Propriedades de dados**

- `price`
- `voltage`
- `widthCm`
- `openingSide`
- `installationType`
- `finish`
- `leadTimeDays`
- `quoteOnly`
- `panelReady`

**Exemplos de triplas**

- `Cooktop_90 hasType Cooktop`
- `Hood_90 hasType Hood`
- `Hood_90 complements Cooktop_90`
- `Hood_90 voltage 220`
- `Sink_X complements Faucet_Y`
- `CoffeeMachine_A sameSuiteAs Oven_A`
- `Dishwasher_PanelReady requiresAccessory CabinetPanel`

**Variáveis fuzzy recomendadas**

- `functionalComplementarity`
- `technicalCompatibility`
- `installationCompatibility`
- `aestheticCoherence`
- `brandLineAffinity`
- `environmentAffinity`
- `priceProximity`
- `quoteAcceptability`
- `recommendationConfidence`

**Funções de pertinência sugeridas**

- `trimf` ou `trapmf` para proximidade de preço e aderência de ambiente
- `gaussmf` para similaridade contínua de largura/capacidade
- `smf/zmf` para aceitabilidade de quote-only e confiança
  Esses tipos de função são suportados em bibliotecas fuzzy conhecidas e são adequados para começar sem complexidade excessiva. citeturn11search4

**Regras fuzzy iniciais**

- Se `functionalComplementarity` for alta **e** `technicalCompatibility` for alta, então `relevance` é muito alta.
- Se `installationCompatibility` for baixa, então `relevance` é baixa, mesmo que a marca seja a mesma.
- Se `sameSuiteAs` for verdadeiro **e** `aestheticCoherence` for alta, então `relevance` sobe.
- Se `quoteAcceptability` for baixa **e** `price` estiver ausente, então `relevance` cai.
- Se `environmentAffinity` for alta, mas `functionalComplementarity` for baixa, então a relevância no máximo fica média.
- Se `recommendationConfidence` for baixa por falta de atributos, então a explicação deve sinalizar incerteza.

**Score final recomendado**

1. Aplicar filtros duros: excluir mesmo produto, incompatibilidade técnica evidente, itens descontinuados.
2. Rodar inferência fuzzy sobre os candidatos restantes.
3. Produzir `fuzzy_score` de 0 a 100.
4. Compor `reason` com os atributos efetivamente usados.
5. Adicionar um `confidence_score` separado.

Essa arquitetura resolve exatamente o problema atual do v0: ela preserva explicabilidade, mas troca saltos discretos por graus de pertinência. citeturn10search5turn10search8turn13search5

## Roteiro de reunião com a loja-piloto

**Evidência.** A documentação do projeto define a revisão qualitativa como etapa para decidir se o recomendador v0 faz sentido comercialmente, usando `reviewer_rating` e `reviewer_comment`, antes de CTR, fuzzy ou ontologia. O próprio pacote visual foi desenhado para isso. citeturn24view0 fileciteturn0file5

**Recomendação.** A reunião deve acontecer, mas não precisa ser longa nem vaga. O formato ideal é um workshop objetivo de **45 a 60 minutos**, com amostra estratificada, não revisão cega de 120 cards seguidos. O melhor desenho é revisar entre **24 e 40 recomendações** divididas em quatro grupos:
pares fortes prováveis;
pares médios;
itens sob consulta;
pares controversos ou suspeitos.
Isso reduz fadiga, melhora consistência do julgamento e produz um dataset de validação mais útil. A recomendação de separar contexto e rótulos também está alinhada às boas práticas de UX para recomendações. citeturn13search7turn24view0

| Bloco              |       Tempo | O que mostrar                                                                   | Saída esperada                                         |
| ------------------ | ----------: | ------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Alinhamento        |       5 min | Objetivo da sessão, o que é v0 e o que ainda não é fuzzy/ontologia          | Todos avaliam com o mesmo critério                     |
| Casos fortes       |      10 min | Relações universalmente plausíveis                                           | Confirmar o que já pode virar base semântica          |
| Casos médios      |      10 min | Itens corretos, mas com ordem ou explicação discutível                       | Reordenar prioridades                                   |
| Casos sob consulta |      10 min | Itens quote-only e equivalentes precificados                                    | Definir política de exibição                         |
| Casos controversos | 10 a 15 min | Pares suspeitos, cruzamento entre domínios, exemplos de vazamento por ambiente | Identificar relações a remover ou restringir          |
| Fechamento         |  5 a 10 min | Consolidação das decisões                                                    | Lista de relações universais, contextuais e proibidas |

**Escala recomendada de 1 a 5**

- **1 — ruim:** não faz sentido; ocultar ou remover a relação.
- **2 — fraca:** relação até existe, mas está mal posicionada ou fora de contexto.
- **3 — aceitável:** pode aparecer, mas não no topo; explicação precisa melhorar.
- **4 — boa:** recomendação comercialmente sólida.
- **5 — excelente:** complemento natural ou quase obrigatório.
  Essa escala já está alinhada ao artefato atual do projeto. citeturn24view0 fileciteturn0file5

**Perguntas adicionais que valem mais do que a reunião atual pergunta hoje**

- Esta relação é **universal**, **contextual** ou **específica da loja-piloto**?
- A relação é de **complemento**, **alternativa**, **mesma suite** ou **merchandising editorial**?
- O item deveria aparecer **somente** quando houver projeto/consultoria?
- O item depende de **medida**, **abertura**, **marcenaria** ou **instalação**?
- O item é “high-end coerente” ou só “high-ticket próximo”?

**Campos que deveriam ser acrescentados ao review CSV/HTML**

- `relation_type`
- `availability_status`
- `quote_reason`
- `collection/design_line`
- `installation_type`
- `width_cm`
- `panel_ready`
- `indoor_outdoor`
- `must_show_before`
- `universal_context_specific`
- `confidence_score`
- `expert_validated`
  Esses campos aproximam a revisão manual da ontologia futura e reduzem retrabalho. citeturn9search0turn11search3turn11search7turn16search0turn17search3

## Plano de ação

**Evidência.** A proposta acadêmica prevê revisão de datasets, modelagem de ontologia, implementação do motor fuzzy e avaliação por métricas. O estado atual do projeto já entregou o baseline operacional e a etapa de revisão qualitativa. Falta, portanto, a ponte que transforma esse baseline em método acadêmico comparável. fileciteturn0file4 citeturn20view0turn22view0turn24view0

| Fase     | Objetivo                                           | Entregáveis                                                                                           | Arquivos prováveis                                                                                   | Critério de conclusão                                                  |
| -------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Fase 4.8 | Validar o baseline com especialista da loja-piloto | planilha revisada, taxonomia de relações, política de `quote_only`, lista de relações proibidas | `reports/recommendation_review.csv`, `docs/RECOMMENDATION_REVIEW.md`, `docs/RELATION_POLICY.md` | 24–40 recomendações avaliadas com notas e comentários consistentes   |
| Fase 5   | Criar baseline acadêmico com dataset público     | seleção de dataset, notebook de baseline, protocolo de avaliação                                   | `data/public/`, `notebooks/baseline_eval.ipynb`, `docs/EVALUATION_PROTOCOL.md`                  | baseline reproduzível com métricas offline                             |
| Fase 6   | Implementar ontologia mínima                      | classes, propriedades, triplas e mapeamento do catálogo                                               | `ontology/kitchen_high_end.owl`, `backend/app/ontology_mapper.py`, `docs/ONTOLOGY.md`           | ontologia cobre tipos, ambientes, suites, oferta e relações principais |
| Fase 7   | Implementar motor fuzzy                            | membership functions, regras, score e explanation composer                                             | `backend/app/fuzzy_engine.py`, `backend/tests/test_fuzzy_engine.py`, `docs/FUZZY_RULES.md`      | motor retorna score gradual e reason concreta                            |
| Fase 8   | Comparar v0 vs ontologia-fuzzy                     | experimento comparativo, precisão@k, recall@k, nDCG@k, análise qualitativa                           | `notebooks/compare_v0_vs_fuzzy.ipynb`, `docs/RESULTS.md`                                          | melhoria mensurável ou, no mínimo, trade-off explicitado com rigor     |

**Recomendação para dataset público.** Um caminho pragmático é usar um corpus recente de reviews e metadata de e-commerce como ponto de partida para o baseline acadêmico, já que ele oferece reviews, preço, descrições, imagens e grafos de “bought together”. Isso não substitui o catálogo premium local, mas dá o que a proposta precisa: comparabilidade e reprodutibilidade acadêmica. citeturn11search2turn11search6

**Recomendação para métricas.** Na comparação entre v0 e a camada ontologia-fuzzy, as métricas mínimas deveriam ser `Precision@k`, `Recall@k` e `nDCG@k`, complementadas por acordo com especialista (`reviewer_rating`) e, se o piloto permitir, CTR e clique assistido em produção. Isso fecha a lacuna entre validação comercial e validação acadêmica. citeturn25search0turn25search5turn24view0

**Conclusão final.**
Sim, **é preciso fazer a reunião com a loja-piloto**. Não porque o projeto dependa eternamente dela, mas porque o seu recomendador v0 ainda mistura relações universalmente corretas com curadoria editorial fraca, e isso precisa ser separado antes de formalizar uma ontologia fuzzy. A reunião ajuda a generalizar o sistema justamente quando produz essa separação: o que é universal do domínio high-end, o que é contextual de cozinha/gourmet/eletro, e o que é específico do catálogo da loja-piloto. Se essa separação for feita, a reunião deixa de ser “cobaia” e passa a ser o primeiro passo de uma metodologia reaproveitável para outros e-commerces high-end. citeturn22view0turn24view0turn10search0turn10search5turn10search8

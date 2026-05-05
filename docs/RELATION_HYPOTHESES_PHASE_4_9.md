# Hipoteses De Relacao - Fase 4.9

Este documento registra hipoteses provisoria de relacoes para o ranking v0.

Base do documento:

- derivado da revisao dos agentes da Fase 4.8;
- nao validado por cliente ainda;
- pendente de validacao por comportamento real;
- sem reuniao humana real nesta fase.

## Classificacao Das Hipoteses

### Relacoes universais provisoria

Hipoteses com maior estabilidade funcional/tecnica:

- `Cuba -> Misturador`
- `Misturador -> Cuba`
- `Cooktop -> Coifa`
- `Coifa -> Cooktop`
- `Rangetop -> Coifa`
- `Rangetop -> Forno`
- `Forno -> Cooktop`
- `Acessorio de Coifa -> Coifa` (com compatibilidade de modelo)
- `Lavadora -> Secadora` (somente no dominio lavanderia)

Status: `agent_hypothesis`, `pending_client_data`.

### Relacoes contextuais provisoria

Hipoteses plausiveis, mas dependentes de contexto:

- `Adega -> Cervejeira/Frigobar`
- `Cervejeira -> Adega/Frigobar`
- `Churrasqueira -> Adega/Cervejeira/Frigobar`
- `Churrasqueira -> Coifa/Cooktop`
- `Forno de Pizza -> Churrasqueira`
- `Maquina de Gelo -> Adega/Cervejeira/Frigobar`
- `Cafeteira -> Forno/Micro-ondas` (suite de embutidos)
- `Gaveta Aquecida -> Forno/Cooktop`

Status: `agent_hypothesis`, `pending_client_data`.

### Relacoes especificas da Kouzina

Hipoteses editoriais derivadas do mix da loja:

- relacao por mesma marca sem evidencia tecnica forte;
- relacao por mesma suite validada apenas pela curadoria da loja;
- recomendacao editorial para campanha, showroom ou estrategia comercial.

Status: `agent_hypothesis`, `pending_client_data`.

### Relacoes fracas

Hipoteses com risco alto de falso positivo:

- `Acessorio de Cozinha -> Cuba/Misturador/Lava-loucas` quando o item for
  decorativo e nao tecnico;
- `Dispenser de Agua -> Adega/Churrasqueira` sem projeto claro;
- pares sustentados apenas por ambiente amplo, preco proximo ou premium.

Status: `agent_hypothesis`, `pending_client_data`.

### Relacoes proibidas ou a rebaixar

Hipoteses de bloqueio/rebaixamento imediato no baseline:

- `Lavadora/Secadora/Conjugada -> Adega/Coifa/Cooktop/Forno/Rangetop`;
- cruzamento claro de dominio sem complementaridade funcional;
- relacao que pareca apenas empurro de ticket sem utilidade de projeto.

Status: `agent_hypothesis`, `pending_client_data`.

## Politica Provisoria Para `Sob consulta`

- `Sob consulta` nao e erro por si so.
- `Sob consulta` e hipotese aceitavel quando houver intencao consultiva
  (projeto, configuracao, instalacao, showroom, marcenaria).
- `Sob consulta` nao deve dominar top-1/top-3 sem relacao forte.
- recomendacao `Sob consulta` sem relacao forte deve ser rebaixada.

Status: `agent_hypothesis`, `pending_client_data`.

## Riscos De Falso Positivo

- ambiente amplo sendo usado como atalho;
- marca como substituto de complementaridade real;
- preco como sinal dominante;
- confusao entre complemento e alternativa;
- tipagem ampla de `Acessorio de Cozinha`;
- classificacao de produto possivelmente incorreta no catalogo.

## Hipoteses Que So Podem Ser Confirmadas Com Dados Reais

- relacao universal performa melhor que contextual?
- `Sob consulta` gera mais pedido de orcamento ou mais rejeicao?
- marca pesa mais que complementaridade funcional no publico real?
- ambiente pesa mais que categoria no clique real?
- score v0 prediz interesse comportamental real?
- relacao tecnica converte melhor que editorial?

Todas as perguntas acima estao:

- pendente de validacao por comportamento real;
- nao validado por cliente ainda;
- sem conclusao definitiva nesta fase.

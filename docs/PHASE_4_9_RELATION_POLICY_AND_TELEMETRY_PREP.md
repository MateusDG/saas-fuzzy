# Fase 4.9 - Politica Provisoria De Relacoes E Preparacao Para Telemetria

## Objetivo Da Fase

A Fase 4.9 implementa uma camada provisoria de politica de relacoes para o
ranking v0 e prepara a base tecnica/documental para coleta futura de eventos
reais.

Esta fase nao executa analise real de dados de clientes.

## Premissas Estrategicas

- A reuniao simulada de especialistas da Fase 4.8 gerou hipoteses
  especialistas provisoria.
- Essas hipoteses nao representam validacao final de negocio.
- Nao houve validacao humana real com equipe Kouzina nesta fase.
- Nao existem, nesta fase, dados comportamentais reais suficientes para
  conclusao de funil.

## O Que Esta Sendo Feito Agora

- versionamento de hipoteses de relacoes;
- aplicacao de guardrails editoriais simples no ranking v0;
- bloqueio/rebaixamento de relacoes problematica;
- melhoria de explicacoes de recomendacao para reduzir reason generica;
- tratamento mais cauteloso para itens `Sob consulta`;
- enriquecimento do review CSV/HTML para auditoria futura;
- preparacao de estrutura de eventos para fase futura de funil.

## O Que Nao Esta Sendo Feito Agora

- analise estatistica de comportamento real;
- dashboard de produto/BI;
- fuzzy;
- ontologia;
- deploy;
- painel administrativo;
- integracao final com site em producao;
- simulacao de conversao, CTR ou receita como se fosse dado real.

## Posicionamento Metodologico

As regras adicionadas nesta fase devem ser tratadas como:

- `hipotese provisoria`;
- `derivado da revisao dos agentes`;
- `pendente de validacao por comportamento real`;
- `nao validado por cliente ainda`.

## Validacao Futura Planejada

A validacao real devera ocorrer somente depois de:

- API integrada ao site/widget real;
- volume relevante de interacoes reais;
- coleta consistente de eventos anonimos;
- revisao de LGPD e campos de telemetria.

Somente nesse momento sera possivel avaliar com dados reais:

- impressao;
- clique;
- expansao/fechamento;
- pedido de orcamento;
- add-to-cart;
- abandono;
- performance por relacao e contexto.

## Escopo Tecnico Do Ranking Nesta Fase

O ranking v0 continua baseline explicavel.

A Fase 4.9 apenas adiciona guardrails editoriais:

- bloquear ou rebaixar relacoes fracas/proibidas;
- distinguir relacao universal, contextual e editorial;
- evitar que marca/preco/ambiente dominem sem complementaridade funcional;
- reduzir risco de `Sob consulta` dominar top sem relacao forte.

Sem fuzzy e sem ontologia.

## Entregaveis Principais Da Fase 4.9

- politica versionada em CSV (`data/relation_policy_seed.csv`);
- loader simples e testavel da politica (`backend/app/relation_policy.py`);
- recomendador com guardrails provisoria;
- review pack enriquecido com campos de politica;
- eventos preparados para funil futuro;
- plano documental de analise futura.

## Resultado Esperado

Ao final da Fase 4.9, o sistema fica:

- mais robusto contra falsos positivos evidentes;
- mais auditavel para curadoria futura;
- pronto para coletar dados uteis assim que houver integracao real;
- ainda simples, explicavel e alinhado ao baseline v0.

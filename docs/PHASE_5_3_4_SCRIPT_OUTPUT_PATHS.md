# Fase 5.3.4 - Padronizacao De Paths De Saida

## Regra adotada

Para scripts de baseline/review/evaluation, paths relativos agora seguem uma
regra unica:

- paths relativos sao resolvidos a partir da raiz do repositorio;
- um prefixo legado `../` (apenas um nivel) e normalizado para manter
  compatibilidade de comandos antigos executados dentro de `backend/`;
- tentativas de escapar da raiz com caminho relativo (ex.: `../../...`) sao
  bloqueadas com erro explicito.

Paths absolutos continuam aceitos como override intencional.

## Exemplos

Exemplo correto (recomendado):

```powershell
python -m app.freeze_v0_baseline --output reports/baselines/v0_baseline_path_test.json
```

Exemplo legado normalizado automaticamente:

```powershell
python -m app.freeze_v0_baseline --output ../reports/baselines/v0_baseline_path_test.json
```

Exemplo perigoso/bloqueado:

```powershell
python -m app.freeze_v0_baseline --output ../../reports/baselines/v0_baseline_path_test.json
```

## Como evitar gravacao fora do repositorio

1. Preferir sempre `reports/...` e `data/...` sem `../`.
2. Evitar caminhos relativos com mais de um `..` no inicio.
3. Em duvida, usar path absoluto somente quando a gravacao externa for
   intencional.

## Scripts cobertos

- `app.freeze_v0_baseline`
- `app.review.review_recommendations`
- `app.review.export_review_pack`
- `app.evaluation.run_offline_evaluation`
- `app.evaluation.preprocess_amazon_reviews_2023`

## Testes

Foram adicionados testes de path policy em:

- `backend/tests/test_script_output_paths.py`

Cobertura principal:

- `reports/...` permanece dentro da raiz do repositorio;
- `../reports/...` e normalizado para dentro da raiz;
- `../../...` e rejeitado para evitar escape acidental.

## Resultado Da Execucao

- Comando validado:
  `python -m app.freeze_v0_baseline --limit-products 30 --top-k 4 --output reports/baselines/v0_baseline_path_test.json`
- Arquivo gerado dentro do repositorio:
  `reports/baselines/v0_baseline_path_test.json`
- Comando legado validado:
  `--output ../reports/baselines/...` com normalizacao e aviso no console.
- Suite de testes:
  `python -m pytest` -> `60 passed`
- Fingerprint canônico do snapshot principal permaneceu:
  `e1e8d8cf2f28f3499834a831e84cb75dacfff76746538ad49b304296e160ed42`

• Handoff

1. Fases concluídas e validadas: Fases 1, 2, 3, 3.1, 4, 4.2, 4.2.1 e 4.3. A API FastAPI roda, PostgreSQL funciona,
   eventos são persistidos, recomendador v0 por regras funciona, catálogo oficial autorizado importa de data/
   products_kouzina_official.csv, testes passam, e fuzzy/ontologia/Tray/painel/login/deploy/crawler/scraping seguem
   fora do escopo.
2. Estado atual do repositório: há mudanças locais não commitadas de fases anteriores. git status visto por último
   indicava alterações em README.md, backend/app/seed.py, backend/tests/test_api.py, docs/CATALOG_QUALITY.md, docs/
   DATA_MODEL.md e avisos de permissão no git global ignore. O arquivo oficial canônico é data/
   products_kouzina_official.csv e é ignorado pelo Git.
3. Arquivos alterados nas Fases 4.2 e 4.3: .gitignore, README.md, backend/app/seed.py, backend/app/recommender.py,
   backend/tests/test_api.py, docs/API.md, docs/DATA_MODEL.md, docs/MVP.md, docs/RECOMMENDER.md, docs/
   CATALOG_QUALITY.md, widget/demo.html. Na 4.2.1 houve padronização documental/operacional para usar apenas data/
   products_kouzina_official.csv.
4. Comandos executados e resultado: docker compose up -d confirmou o PostgreSQL rodando; python -m pytest passou, por
   último com 18 passed; python -m app.seed --file ../data/products_kouzina_official.csv --replace-products importou
   318 produtos na versão anterior do CSV; validações via TestClient para 119, 3618, GW951X-BR, 2477, 2139 retornaram
   recomendações ordenadas, sem o próprio produto e com reason.
5. Decisões importantes: products_seed.csv permanece seed fictício de desenvolvimento; products_kouzina_official.csv é
   o catálogo oficial autorizado local e não deve ser commitado; Preço venda = 0.00 significa Sob consulta, com
   price=null, available=true; produtos sob consulta não entram na regra de preço próximo; não há download de imagens
   nem dados pessoais; importação oficial usa --file e pode substituir produtos com --replace-products preservando
   eventos.
6. Pendências conhecidas: antes da atualização mais recente do CSV, o catálogo oficial não tinha URL Tray nem imagens;
   image_url ficava vazio e url usava fallback seguro. Também havia 37 produtos sem categoria, 37 sem marca, 37 sem
   preço informado e 90 sem voltagem. Após a Fase 4.3, product_type vazio caiu de 25 para 0 e environment vazio ficou
   em 0. Tipos novos como Cuba, Misturador, Queimador e Acessório de Coifa ainda não têm relações complementares
   específicas no recomendador v0.
7. Próximo passo exato: implementar somente a Fase 4.4 de suporte completo a URL e imagens no catálogo oficial
   atualizado, lendo Endereço do Produto (URL Tray) e Imagem principal/Imagem 2/Imagem 3/Imagem 4, sem fuzzy,
   ontologia, deploy, Tray automático, crawler, scraping, painel, login, mudança estrutural no banco ou coleta de
   dados pessoais.

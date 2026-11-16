# Rota Livre — MVP CitizenTech

## Ficha técnica
- Produto: registro e acompanhamento de barreiras nas calçadas.
- Público: pessoas com mobilidade reduzida e gestores de espaços.
- Território inicial: entorno da FIAP, Avenida Lins de Vasconcelos, 1222 e 1264, São Paulo.
- Problema: barreiras físicas sem registro e acompanhamento organizado.
- Proposta: localizar, descrever e acompanhar ocorrências até sua resolução.
- Arquitetura: React/Vinext, API em Cloudflare Worker, D1 para registros e R2 para fotos.
- Dados: registros do usuário e quatro exemplos fictícios no entorno da FIAP carregados por ação explícita. Cartografia OpenStreetMap com atribuição.
- IA: não integrada nesta versão. Não há detecção automática nem cálculo de rotas seguras.
- Indicadores: registros por status e tempo médio entre criação e última atualização dos registros resolvidos. Incluem exemplos quando carregados; não representam impacto externo validado.
- ODS propostos para discussão no pitch: 10 e 11.
- Equipe: Gabriel Gomes Catanzaro (93445), Lucas Gomes Alcântara (98766), Henrique Canali Cuzato (551326).

## Executar
Node 22.13 ou superior. `npm ci`, `npm run db:generate` somente após mudanças de esquema, `npm run build`.
Aplicar cada migração local uma única vez:
`node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_fast_thanos.sql`
`npm run dev` inicia o ambiente de desenvolvimento.
Hospedagem utiliza os bindings DB (D1) e BUCKET (R2), declarados no manifesto.

## Fluxo para o pitch
1. Carregar exemplos fictícios ou registrar uma barreira.
2. Informar título, categoria, endereço e localização no mapa (ou coordenadas).
3. Opcionalmente anexar JPG, PNG ou WebP de até 4 MB.
4. Consultar o registro e filtrar por categoria/status.
5. Abrir painel de gestão, selecionar ocorrência e alterar status.
6. Recarregar para demonstrar persistência. Exportar JSON se necessário.

## Contrato inicial para integração
- GET /api/occurrences: lista de registros.
- POST /api/occurrences: JSON com title, category, address, description, lat, lng e photo opcional; retorna 201 e registro.
- PATCH /api/occurrences: JSON com id e status (Registrada, Em análise ou Resolvida).
- POST /api/photo: multipart com campo photo; retorna URL.
- GET /api/photo?id=UUID: imagem armazenada.
- POST /api/occurrences com action=seed: adiciona exemplos idempotentemente.

## Limites da versão
Site público de demonstração acadêmica. Não existem papéis separados de cidadão e gestor; o painel compartilhado não possui autorização de gestão separada; use apenas dados de demonstração. Sem conexão com prefeitura, protocolos oficiais, IA, sensores ou lakehouse. RPA integrado por importação e exportação JSON na aba Meu trajeto. Não certifica acessibilidade de caminhos. Não enviar dados pessoais, rostos ou placas nas fotos. Tiles de mapa e fontes dependem de acesso externo. Validação de foto usa tipo informado pelo upload e limite de tamanho; adicionar decodificação e remoção de metadados antes de uso público.

## Validação
Build e TypeScript. No navegador local: carga de exemplos, mudança de status e persistência após recarregar, cadastro com ponto selecionado. Banco local é independente do publicado.

## Referência de localização
Endereço confirmado em https://www.fiap.com.br/graduacao/contato/ . Coordenada do marcador extraída do destino do link de mapa oficial: -23.5740619, -46.6231674. Campus Aclimação. Exemplos antigos são preservados; os novos possuem IDs fiap-demo-* e só são criados ao clicar no botão correspondente.

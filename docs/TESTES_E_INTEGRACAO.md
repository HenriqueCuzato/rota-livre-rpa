# Testes e integração — Rota Livre

## Validação executada nesta preparação

- Nove testes Python: aprovados (ver `tests/resultado.txt`).
- Seis verificações do consumidor TypeScript com JSON realmente gerado pelo Python: aprovadas (lote ativo, lote vazio, envelope inválido, IDs repetidos, latitude textual e status resolvido indevidamente presente na saída).
- Compilação do MVP: concluída.
- Navegador de desenvolvimento: importação de um alerta, seleção de FIAP e alerta no trajeto, exibição de um alerta a zero metro do traçado; importação do lote resolvido, exibição de zero alerta. O banco de cadastros do ambiente de desenvolvimento não carregou; o teste visual utilizou os lotes fictícios e não comprova uma exportação real.

## Como repetir os testes de contrato (opcional, Node 22.13+)

Na raiz `rota-livre-rpa`:

```powershell
py .\src\triagem.py .\dados\ocorrencias_teste.json --saida .\tests\ativo.json
py .\src\triagem.py .\dados\apos_resolucao.json --saida .\tests\vazio.json
node --experimental-strip-types .\mvp\lib\rpa.test.mjs .\tests\ativo.json .\tests\vazio.json
```

## Evidência de ponta a ponta a gravar pela equipe

1. Cadastre no MVP uma ocorrência claramente identificada como DEMO; não informe dados pessoais.
2. Exporte pelo botão específico da aba Meu trajeto e processe esse arquivo no Python.
3. Importe a saída no mesmo MVP, mostre ID da execução, horário e alertas no mapa.
4. Atualize o status da ocorrência para Resolvida no painel de gestão, exporte novamente, reprocesse e importe a nova saída. O alerta daquela ocorrência deve sair do conjunto (o total pode não ser zero se houver outras ocorrências).
5. Demonstre arquivo ausente e a última linha do log.
6. Execute os nove testes e mostre `OK`.

Salve prints em `assets/`, com legendas e sem dados sensíveis. A interface importada é salva no navegador de cada visitante; não afirmar sincronização automática entre usuários.

## Matriz dos testes Python

| Cenário | Resultado esperado |
|---|---|
| IDs conflitantes | Nenhum alerta desse ID; decisão conflito_de_id |
| Coordenadas inválidas | Registro excluído; coordenada_invalida |
| Duplicatas idênticas | Um alerta por ID |
| Registro com campos extras do MVP | Saída somente com campos permitidos |
| ID/categoria/status inválidos | Rejeição individual e motivo |
| JSON inválido/raiz incorreta | Falha; saída anterior preservada |
| Lista vazia | Saída ativa vazia |
| Resolvida | Não gera alerta |
| Ciclo e recuperação | 1 alerta, repetição sem duplicar, falha preservada, 0 após resolução |

## Roteiro do vídeo — até 3 minutos

- 0:00–0:20: problema operacional, triagem de registros colaborativos.
- 0:20–1:20: exportação do MVP, comando Python, importação e mapa.
- 1:20–1:55: resolução e atualização do conjunto.
- 1:55–2:30: arquivo ausente, auditoria e recuperação.
- 2:30–2:55: testes OK, limites do protótipo e links de entrega.

## Contrato

Entrada: lista de objetos com `id`, `category`, `status`, `lat`, `lng`.
Saída: objeto com `execucao` (identificador da execução), `atualizado` (data/hora ISO), `alertas` (lista validada). O consumidor valida todo o arquivo antes de substituir o estado. Não há execução de Python no navegador ou no site: ela ocorre no computador do operador.

## Atualização do mapa
Todos os alertas em aberto ficam visíveis antes e durante o traçado. O filtro inicial combina cadastros e RPA; IDs repetidos são unificados com prioridade ao cadastro atual. Registros resolvidos são excluídos. O lote importado é salvo em localStorage, com opção de remoção. Testes de união, deduplicação, resolução e lote vazio passaram, e a compilação foi concluída.

# Rota Livre — RPA integrado ao MVP

FIAP · Robotic Process Automation · CitizenTech · 2026.2

- Gabriel Gomes Catanzaro — RM 93445
- Lucas Gomes Alcântara — RM 98766
- Henrique Canali Cuzato — RM 551326

MVP: https://rota-livre-henrique.sproutingchaff.chatgpt.site

## Comece aqui no VS Code

1. Extraia o ZIP. Abra **a pasta `rota-livre-rpa`** em Arquivo → Abrir Pasta.
2. Abra Terminal → Novo Terminal. O terminal deve estar nessa pasta (que contém `src`, `tests` e `dados`).
3. É necessário Python 3.9 ou superior. No Windows, confirme: `py --version`.
4. Não há bibliotecas externas para instalar para executar a automação.

```powershell
py -m unittest discover -s tests -v
py .\src\triagem.py
```

Os nove testes devem terminar em `OK`. A triagem inicial mostra `4 registros processados. 1 alerta(s) ativo(s).` Mensagens de falha durante os testes são esperadas nos cenários de erro; o resultado final deve ser OK.

## Integração com o MVP publicado (não exige Node)

1. Abra o MVP e a aba **Meu trajeto**.
2. Clique **1. Exportar ocorrências para RPA**. O navegador baixa `ocorrencias_mvp.json`. Se a base estiver vazia, cadastre uma barreira de demonstração ou utilize os exemplos fictícios antes de exportar.
3. Copie esse arquivo para `dados` deste projeto.
4. No terminal do VS Code:

```powershell
py .\src\triagem.py .\dados\ocorrencias_mvp.json
```

5. No MVP, em **Meu trajeto**, clique **2. Importar resultado do robô** e escolha `painel/alertas_ativos.json`.
6. A fonte muda para **Todos: cadastros + RPA**. Você pode filtrar para **Resultado importado do RPA**. Confira total, horário e identificador de execução. Antes e durante o traçado, o mapa apresenta todos os alertas em aberto das fontes escolhidas; use o zoom se estiverem fora da região da FIAP.
7. Escolha FIAP e um alerta pela lista **Adicionar ponto de referência**, ou marque dois ou mais pontos no mapa. O MVP mostra relatos em aberto a até 25 metros do traçado.
8. Para voltar aos dados originais, selecione **Cadastros do aplicativo**.

A transferência de arquivos é manual; validação, classificação, seleção e auditoria são automáticas. O resultado importado é usado pelo componente de trajeto do próprio MVP, salvo localmente no navegador. Não grava sobre os cadastros compartilhados nem sincroniza todos os visitantes. Ao recarregar, o lote é restaurado neste navegador. Outros dispositivos precisam importar seu próprio lote. Um arquivo inválido não substitui um resultado já importado. A importação não garante que a barreira existe fisicamente.

## Demonstração controlada: um alerta, resolução e falha

Os arquivos em `dados` são fictícios, no entorno da FIAP. Importe o resultado no MVP após cada execução bem-sucedida.

### 1. Alerta ativo
```powershell
py .\src\triagem.py .\dados\ocorrencias_teste.json
```
Esperado: 4 registros, 1 alerta. Importe `painel/alertas_ativos.json` no MVP.

### 2. Após resolução
```powershell
py .\src\triagem.py .\dados\apos_resolucao.json
```
Esperado: 4 registros, 0 alertas. Importe o mesmo arquivo de saída novamente. A lista anterior deve ser substituída por uma lista vazia.

### 3. Arquivo ausente
```powershell
py .\src\triagem.py .\dados\arquivo_inexistente.json
Get-Content .\logs\auditoria.jsonl -Tail 1
```
Esperado: erro FileNotFoundError e auditoria `falha_lote`. A saída da última execução válida é preservada. O arquivo ausente NÃO está incluído de propósito.

### 4. Recuperação
```powershell
py .\src\triagem.py .\dados\ocorrencias_teste.json
```
Esperado: 1 alerta novamente.

## Painel local opcional

```powershell
py -m http.server 8000 --bind 127.0.0.1 --directory painel
```
Abra http://127.0.0.1:8000. Mantenha esse terminal aberto; execute o robô em outro terminal. O botão Atualizar alertas lê o JSON; não executa o Python. Esse painel é auxiliar, a integração principal está em Meu trajeto no MVP.

## Pastas

- `src/`: robô Python e regras de negócio.
- `dados/`: dois lotes fictícios para repetição dos cenários.
- `painel/`: consumidor local auxiliar e JSON de saída.
- `logs/`: auditoria gerada, com uma linha JSON por evento.
- `tests/`: nove testes Python e resultado da execução desta preparação.
- `docs/`: PDD, fluxo, integração, evidências e roteiro de vídeo.
- `assets/`: espaço para os prints feitos pela equipe.
- `mvp/`: código-fonte do MVP com integração RPA (não é necessário executá-lo localmente para testar pelo link).

## Regras e exceções

IDs ausentes, coordenadas não numéricas ou fora dos limites, categoria vazia e status desconhecido são rejeitados. Duplicatas idênticas produzem um alerta; registros divergentes com o mesmo ID são excluídos e registrados como conflito. Ocorrências resolvidas não geram alerta. Cada lote válido substitui a saída inteira, inclusive quando vazio; sempre exporte o conjunto completo.

Arquivos ausentes, JSON inválido e raiz diferente de lista geram falha registrada. A escrita usa arquivo temporário e substituição. A retomada é uma nova execução com entrada corrigida. A auditoria precisa estar gravável; sem ela a execução falha. Não há controle de execuções concorrentes nem transação única entre arquivo final e log.

## Segurança e publicação

Não publique exportações com dados reais ou credenciais. O exportador específico de RPA inclui somente ID, categoria, status, latitude e longitude; não inclui foto ou descrição. Os exemplos são fictícios. O `.gitignore` evita publicar exportação real e arquivos de execução; a pasta `docs` explica como produzi-los.

## Links da entrega

- Repositório: https://github.com/HenriqueCuzato/rota-livre-rpa
- Vídeo demonstrativo: https://youtu.be/WdjrOumpX98
- MVP: https://rota-livre-henrique.sproutingchaff.chatgpt.site/

O relatório PDF acompanha o pacote de entrega e inclui as evidências de testes e integração, além dos links acima.

## Evidências a registrar

Consulte `docs/TESTES_E_INTEGRACAO.md`. Para salvar o resultado dos testes no Windows:

```powershell
py -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath .\tests\resultado_windows.txt
```

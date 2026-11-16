# Descrição do processo
Objetivo: atualizar os alertas em aberto a cada lote completo, preservando a base de relatos original.
Entrada: exportação JSON do Rota Livre ou lote fictício no mesmo formato.
Disparo: execução do comando pelo operador.
1. Abrir auditoria e ler o lote. Arquivo ausente, JSON inválido ou raiz diferente de lista encerra a execução com erro e preserva a saída anterior.
2. Agrupar por ID. Repetições idênticas contam uma vez. Registros divergentes com o mesmo ID ficam em quarentena lógica até correção na origem.
3. Para cada grupo, ignorar resolvidas, validar status, coordenadas e categoria. Registrar a decisão para cada posição do lote.
4. Publicar o conjunto JSON por substituição atômica. Um lote válido sem alertas gera uma lista vazia.
5. O operador importa o arquivo no MVP, aba Meu trajeto. O consumidor valida o envelope e todos os alertas antes de substituir o estado da sessão.
6. O mapa e a lista de proximidade usam os alertas importados; lista vazia remove os alertas do lote anterior. Arquivo inválido mantém o estado anterior. O painel local via HTTP permanece como consumidor auxiliar.
Responsável pela correção: operador revisa os erros na origem e reexecuta o lote completo.

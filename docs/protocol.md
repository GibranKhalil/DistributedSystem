# Algoritmos e Protocolos de Coordenação Distribuída

## Relógios Lógicos de Lamport

O sistema utiliza o mecanismo de relógios lógicos proposto por Lamport para ordenação causal de eventos:

- Cada nó mantém um contador interno que é incrementado:
  - Antes de executar qualquer ação local
  - Ao enviar mensagens para outros nós
- Nas mensagens enviadas, o nó inclui:
  - Seu timestamp lógico atual
- No recebimento de mensagens, o nó:
  - Compara seu relógio local com o timestamp recebido
  - Ajusta seu contador para o maior valor entre os dois + 1

## Protocolo de Exclusão Mútua Distribuída

Implementação de um algoritmo descentralizado para controle de acesso a recursos compartilhados:

### Fluxo de Operação:

1. **Solicitação de Acesso**:
   - Quando um cliente precisa do recurso, envia:
     - Mensagem de requisição para todos os participantes
     - Seu timestamp lógico atual

2. **Processamento de Requisições**:
   - Ao receber uma solicitação, cada cliente:
     - Responde imediatamente se:
       * Não está usando o recurso
       * Não deseja acessá-lo
     - Caso contrário:
       * Compara timestamps (e IDs em caso de empate)
       * Adia a resposta se:
         - Possuir requisição com prioridade maior (timestamp menor)
         - Em caso de timestamps iguais, ID menor tem prioridade

3. **Obtenção do Recurso**:
   - O cliente obtém acesso quando:
     - Recebe respostas positivas de todos os demais nós

4. **Liberação do Recurso**:
   - Após utilizar o recurso, o cliente:
     - Envia mensagens de liberação
     - Especificamente para nós que tiveram respostas adiadas
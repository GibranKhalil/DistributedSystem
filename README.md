# Coordenador de Sistema Distribuído

Um coordenador de sistema distribuído que implementa passagem de mensagens, exclusão mútua e sincronização de relógios.

## Funcionalidades

- **Passagem de Mensagens**:
  - Unicast (comunicação direta entre nós)
  - Multicast (comunicação em grupo baseada em canais)
  - Broadcast (comunicação para todo o sistema)

- **Exclusão Mútua**:
  - Implementação de algoritmo de exclusão mútua distribuída
  - Gerenciamento de requisições/liberação de recursos
  - Tratamento de requisições baseado em prioridades usando relógios lógicos

- **Sincronização de Relógios**:
  - Relógios lógicos para ordenação de eventos
  - Tratamento de mensagens baseado em timestamp

## Componentes

1. **DistributedCoordinator**: Coordenador central que gerencia nós, canais e recursos
2. **Node**: Representa um cliente/nó no sistema com capacidades de comunicação
3. **MessageQueue**: Buffer para armazenamento e ordenação de mensagens
4. **BroadcastGroup**: Gerencia canais de multicast e seus assinantes
5. **MutualExclusionManager**: Gerencia o acesso a recursos usando exclusão mútua
6. **Clock**: Implementação de relógio lógico para ordenação de eventos
7. **Message**: Estrutura de dados para todas as comunicações do sistema

## Como Começar

1. Clone o repositório
2. Execute o sistema:
   ```bash
   python __main__.py
   ```

## Testes

O sistema inclui dois cenários de teste automatizados:

1. **Teste de Mensagens**:
   - Demonstra o envio de mensagens unicast, multicast e broadcast
   - Mostra a ordenação das mensagens utilizando relógios lógicos

2. **Teste de Exclusão Mútua**:
   - Simula três clientes competindo por um recurso compartilhado
   - Mostra a correta aquisição e liberação dos recursos

## Registro de Logs

Todas as atividades do sistema são registradas no arquivo `distributed_coordinator.log` com timestamps para fins de depuração e análise.

## Requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa necessária

## Notas de Design

- Implementação segura para múltiplas threads usando locks
- Relógios lógicos garantem a ordenação causal dos eventos
- Priorização de requisições baseada em timestamps e IDs dos nós
- Registro abrangente de todas as atividades do sistema
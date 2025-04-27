# Arquitetura do Sistema

## Visão Geral
O sistema é uma plataforma distribuída que gerencia recursos compartilhados, comunicação entre nós e sincronização de eventos através de relógios lógicos. A arquitetura foi projetada para garantir consistência, escalabilidade e tolerância a falhas em ambientes distribuídos.

## Componentes Principais

### DistributedCoordinator
**Responsabilidade**: Componente central que orquestra todas as operações do sistema distribuído.  
**Funcionalidades**:
- Gerencia o registro e autenticação de clientes
- Administra canais de comunicação e alocação de recursos
- Mantém e sincroniza um relógio lógico global entre todos os nós
- Monitora o estado geral do sistema e balanceamento de carga
- Implementa mecanismos de recuperação em caso de falhas

**Interfaces**:
- `registerNode(node: Node)`: Adiciona um novo nó ao sistema
- `syncGlobalClock(timestamp: int)`: Sincroniza o relógio lógico global

---

### Node
**Responsabilidade**: Representa uma unidade computacional no sistema distribuído.  
**Funcionalidades**:
- Comunicação bidirecional com outros nós (envio/recebimento de mensagens)
- Gerenciamento de requisições de recursos compartilhados
- Manutenção de um buffer de mensagens ordenadas
- Implementação de um relógio lógico local sincronizado
- Processamento de mensagens de acordo com a ordem causal

**Atributos**:
- `nodeId: String`: Identificador único do nó
- `localClock: Clock`: Instância do relógio lógico local
- `messageBuffer: MessageQueue`: Buffer de mensagens recebidas

---

### Message
**Responsabilidade**: Estrutura de dados que encapsula informações trocadas entre nós.  
**Estrutura**:
```typescript
{
  messageId: string;       // UUID único
  senderId: string;       // Identificador do nó remetente
  timestamp: number;      // Timestamp lógico (Lamport)
  type: MessageType;      // Tipo da mensagem (REQUEST|REPLY|RELEASE|etc)
  payload: any;           // Conteúdo da mensagem
  deliveryStatus: Status; // Status de entrega (PENDING|DELIVERED|FAILED)
}
```

**Tipos de Mensagem**:
- `RESOURCE_REQUEST`: Solicitação de recurso compartilhado
- `RESOURCE_RELEASE`: Liberação de recurso
- `SYNC`: Sincronização de relógio
- `HEARTBEAT`: Mensagem de keep-alive

---

### MessageQueue
**Responsabilidade**: Gerenciamento ordenado de mensagens baseado em causalidade.  
**Funcionalidades**:
- Ordenação FIFO baseada em timestamps lógicos
- Rastreamento completo do ciclo de vida das mensagens
- Mecanismos de retransmissão para mensagens perdidas
- Priorização de mensagens críticas
- Limpeza automática de mensagens processadas

**Algoritmos**:
- Ordenação Lamport para garantia de ordem causal
- Algoritmo de descarte seletivo para otimização de memória

---

### BroadcastGroup
**Responsabilidade**: Canal de comunicação multicast para grupos de nós.  
**Funcionalidades**:
- Gerenciamento dinâmico de assinantes (join/leave)
- Buffer circular de mensagens com política de descarte configurável
- Garantia de entrega ordenada para todos os membros do grupo
- Suporte a tópicos hierárquicos (ex: /sensors/temperature)

**Métodos Principais**:
- `subscribe(node: Node)`: Adiciona nó ao grupo
- `unsubscribe(node: Node)`: Remove nó do grupo
- `broadcast(message: Message)`: Distribui mensagem para todos os assinantes

---

### MutualExclusionManager
**Responsabilidade**: Controle de acesso a recursos compartilhados usando exclusão mútua distribuída.  
**Protocolo Implementado**:
- Algoritmo de Ricart-Agrawala modificado
- Priorização baseada em timestamps lógicos
- Tratamento de deadlocks e starvation

**Fluxo de Operação**:
1. Nó envia REQUEST com timestamp
2. Coordenador coloca na fila de espera
3. Quando recurso liberado, concede acesso ao nó com menor timestamp
4. Nó envia RELEASE quando termina

**Métricas**:
- Tempo médio de espera
- Taxa de utilização de recursos
- Número de conflitos resolvidos

---

### Clock
**Responsabilidade**: Implementação do relógio lógico de Lamport para ordenação de eventos.  
**Funcionalidades**:
- Incremento local para eventos internos
- Sincronização em eventos de recebimento de mensagem
- `max(local, receivedTimestamp) + 1` para atualização
- Geração de timestamps monotonicamente crescentes

**Métodos**:
- `increment()`: Incrementa contador interno
- `sync(receivedTimestamp: number)`: Sincroniza com timestamp externo
- `getTimestamp()`: Retorna valor atual

---
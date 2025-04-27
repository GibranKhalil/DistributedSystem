# Requisitos do Sistema

## 1. Introdução
Este documento descreve os requisitos funcionais e não funcionais do sistema de comunicação distribuída, incluindo gerenciamento de clientes, canais de comunicação, recursos compartilhados e temporização lógica.

## 2. Requisitos Funcionais

### 2.1 Gerenciamento de Clientes (Nodees)
- **RF01**: O sistema deve permitir o registro de clientes com identificação única (UUID ou similar).
- **RF02**: Cada cliente deve ser capaz de autenticar-se no sistema.
- **RF03**: Clientes devem poder enviar e receber mensagens de outros clientes e canais.
- **RF04**: O sistema deve manter um registro ativo de clientes conectados.

### 2.2 Comunicação
- **RF05**: Comunicação unicast (um-para-um) entre clientes identificados.
- **RF06**: Comunicação multicast (um-para-muitos) através de canais nomeados.
- **RF07**: Comunicação broadcast (um-para-todos) para todos os clientes conectados.
- **RF08**: Confirmação de recebimento para mensagens críticas.

### 2.3 Canais de Comunicação
- **RF09**: Criação e destruição de canais nomeados por clientes autorizados.
- **RF10**: Inscrição e cancelamento de inscrição de clientes em canais.
- **RF11**: Bufferização configurável de mensagens por canal (tamanho máximo e política de descarte).
- **RF12**: Listagem de canais disponíveis e seus participantes.

### 2.4 Gerenciamento de Recursos
- **RF13**: Criação e identificação de recursos compartilhados com metadados descritivos.
- **RF14**: Implementação de bloqueio mútuo (mutex) para acesso a recursos.
- **RF15**: Protocolo de requisição, uso e liberação de recursos com timeout configurável.
- **RF16**: Detecção e tratamento de deadlocks.

### 2.5 Temporização Lógica
- **RF17**: Implementação de relógios lógicos (Lamport ou Vector Clock) para ordenação de eventos.
- **RF18**: Sincronização de eventos entre clientes distribuídos.
- **RF19**: Carimbo de tempo lógico em todas as mensagens.

## 3. Requisitos Não Funcionais

### 3.1 Confiabilidade
- **RNF01**: Garantia de entrega de mensagens com mecanismo de retransmissão.
- **RNF02**: Persistência de mensagens críticas em caso de falha.
- **RNF03**: Recuperação automática de falhas parciais sem perda de estado crítico.

### 3.2 Escalabilidade
- **RNF04**: Suporte para pelo menos 10.000 clientes simultâneos.
- **RNF05**: Gerenciamento eficiente de até 1.000 canais ativos.
- **RNF06**: Balanceamento de carga para distribuição de mensagens.

### 3.3 Consistência
- **RNF07**: Ordenação causal de mensagens garantida pelos relógios lógicos.
- **RNF08**: Garantia de exclusão mútua estrita para recursos compartilhados.
- **RNF09**: Consistência eventual para estados não críticos.

### 3.4 Desempenho
- **RNF10**: Latência média de mensagens <100ms em rede local.
- **RNF11**: Throughput mínimo de 1.000 mensagens/segundo.
- **RNF12**: Utilização de CPU não superior a 70% em carga máxima.

### 3.5 Observabilidade
- **RNF13**: Logs estruturados para todos os eventos críticos.
- **RNF14**: Métricas em tempo real de mensagens enviadas/recebidas.
- **RNF15**: Interface de monitoramento para status do sistema e recursos.
- **RNF16**: Rastreamento distribuído de mensagens (trace ID).

## 4. Glossário
- **Node/Cliente**: Entidade participante do sistema capaz de enviar/receber mensagens.
- **Canal**: Grupo de comunicação multicast com nome único.
- **Recurso Compartilhado**: Objeto com acesso controlado por exclusão mútua.
- **Relógio Lógico**: Mecanismo para ordenação de eventos em sistemas distribuídos.

## 5. Priorização
- Must Have: RF01-RF08, RF13-RF15, RNF01-RNF03, RNF07, RNF10, RNF13
- Should Have: RF09-RF12, RF16-RF19, RNF04-RNF06, RNF11
- Could Have: RNF08-RNF09, RNF12, RNF14-RNF16

---
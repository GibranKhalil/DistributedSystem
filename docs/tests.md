# Protocolo de Testes do Sistema Distribuído

## 1. Introdução
Este documento descreve os procedimentos de teste para validar os requisitos funcionais e não funcionais do sistema de comunicação distribuída, incluindo testes de comunicação, gerenciamento de recursos e temporização lógica.

## 2. Testes Funcionais

### 2.1 Comunicação Básica

#### Teste F01: Comunicação Unicast
**Objetivo:** Validar o envio e recebimento de mensagens ponto-a-ponto  
**Pré-condições:**  
- Dois clientes registrados (cliente1, cliente2)  
**Procedimento:**  
1. cliente1 envia mensagem "TESTE_UNICAST" para cliente2  
2. Aguardar 2 segundos  
**Critérios de Sucesso:**  
- [ ] cliente2 recebe mensagem idêntica à enviada  
- [ ] Timestamp lógico incrementado (consumed_ts > produced_ts)  
- [ ] Log do sistema registra produção e consumo  

#### Teste F02: Comunicação Multicast
**Objetivo:** Verificar entrega seletiva em canais  
**Pré-condições:**  
- Canal "noticias" criado  
- cliente1, cliente2 inscritos no canal  
- cliente3 não inscrito  
**Procedimento:**  
1. cliente4 envia "ATUALIZACAO" para canal "noticias"  
**Critérios de Sucesso:**  
- [ ] cliente1 e cliente2 recebem mensagem  
- [ ] cliente3 não recebe mensagem  
- [ ] cliente4 não recebe própria mensagem  
- [ ] Log mostra 2 consumos válidos  

#### Teste F03: Comunicação Broadcast
**Objetivo:** Validar entrega para todos os clientes  
**Pré-condições:**  
- 4 clientes conectados  
**Procedimento:**  
1. cliente1 envia "ALERTA_GERAL" via broadcast  
**Critérios de Sucesso:**  
- [ ] cliente2, cliente3, cliente4 recebem mensagem  
- [ ] cliente1 não recebe própria mensagem  
- [ ] Timestamps consistentes em todos os receptores  

### 2.2 Gerenciamento de Recursos

#### Teste F04: Exclusão Mútua
**Objetivo:** Validar acesso serializado a recursos  
**Pré-condições:**  
- Recurso "impressora" criado  
- 3 clientes ativos  
**Procedimento:**  
1. cliente1, cliente2, cliente3 solicitam recurso simultaneamente  
2. Aguardar 10 segundos  
**Critérios de Sucesso:**  
- [ ] Apenas um cliente obtém acesso por vez  
- [ ] Todos os clientes eventualmente acessam o recurso  
- [ ] Logs mostram sequência correta de aquisição/liberação  

### 2.3 Temporização Lógica

#### Teste F05: Ordenação Causal
**Objetivo:** Validar relógios lógicos  
**Pré-condições:**  
- 3 clientes conectados  
**Procedimento:**  
1. cliente1 envia M1 para cliente2  
2. cliente2 envia M2 para cliente3 após receber M1  
3. cliente3 envia M3 para cliente1  
**Critérios de Sucesso:**  
- [ ] Timestamps obedecem relação causal (M1.ts < M2.ts < M3.ts)  
- [ ] Relógios locais atualizados conforme regras de Lamport  

## 3. Testes Não-Funcionais

### 3.1 Testes de Desempenho

#### Teste NF01: Carga Básica
**Objetivo:** Medir desempenho em condições normais  
**Configuração:**  
- 10 clientes conectados  
- Cada cliente envia 100 mensagens unicast  
**Métricas:**  
- [ ] Taxa de entrega: 100%  
- [ ] Latência média: <100ms  
- [ ] Throughput: >500 msg/seg  

#### Teste NF02: Estresse
**Objetivo:** Validar limites do sistema  
**Configuração:**  
- 50 clientes simultâneos  
- 1000 mensagens multicast  
**Métricas:**  
- [ ] Sem perda de mensagens  
- [ ] Latência máxima: <500ms  
- [ ] Uso de CPU: <80%  

## 4. Resultados Esperados

### Matriz de Verificação

| Teste ID | Descrição | Critérios | Status Esperado |
|----------|-----------|-----------|-----------------|
| F01 | Unicast | Entrega pontual | ✔️ |
| F02 | Multicast | Entrega seletiva | ✔️ |
| F03 | Broadcast | Entrega completa | ✔️ |
| F04 | Mutex | Acesso serializado | ✔️ |
| F05 | Relógios | Ordenação causal | ✔️ |
| NF01 | Carga | Desempenho base | ✔️ |
| NF02 | Estresse | Limites sistema | ✔️ |

## 5. Template de Relatório de Teste

```markdown
### Teste [ID] - [Descrição]
**Data Execução:** [DD/MM/AAAA HH:MM]  
**Ambiente:** [Especificações técnicas]  

**Resultados:**  
- Critério 1: [✔️/❌] [Observações]  
- Critério 2: [✔️/❌] [Observações]  

## 6. Anexos

### Exemplo de Log de Sucesso
```
[15:42:17] INFO - cliente2 recebeu: TESTE_UNICAST (sender=cliente1, ts=1, consumed_ts=2)
[15:42:18] METRIC - Latência média: 87ms
```

### Glossário
- **consumed_ts:** Timestamp lógico de consumo
- **Mutex:** Mecanismo de exclusão mútua
- **Throughput:** Mensagens processadas por segundo
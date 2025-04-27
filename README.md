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

## Exemplo de Saída

```
===== TESTE DE MENSAGENS =====

Teste Unicast:
[cliente2] Recebeu: Olá cliente2, como vai? (remetente=cliente1, ts=1, ts_consumido=2, tipo=normal)

Teste Multicast:
[cliente1] Recebeu: Nova atualização disponível! (remetente=cliente4, ts=3, ts_consumido=4, tipo=normal)
[cliente2] Recebeu: Nova atualização disponível! (remetente=cliente4, ts=3, ts_consumido=4, tipo=normal)
[cliente3] Recebeu: Nova atualização disponível! (remetente=cliente4, ts=3, ts_consumido=4, tipo=normal)

Teste Broadcast:
[cliente2] Recebeu: Mensagem importante para todos! (remetente=cliente1, ts=4, ts_consumido=5, tipo=normal)
[cliente3] Recebeu: Mensagem importante para todos! (remetente=cliente1, ts=4, ts_consumido=5, tipo=normal)
[cliente4] Recebeu: Mensagem importante para todos! (remetente=cliente1, ts=4, ts_consumido=5, tipo=normal)

===== TESTE DE EXCLUSÃO MÚTUA =====
[cliente1] tentando acessar impressora
[cliente1] adquiriu impressora
[cliente2] tentando acessar impressora
[cliente3] tentando acessar impressora
[cliente1] liberou impressora
[cliente2] adquiriu impressora
[cliente2] liberou impressora
[cliente3] adquiriu impressora
[cliente3] liberou impressora
```

---

Desenvolvido por [Gibran](https://github.com/GibranKhalil) e [Tales](https://github.com/talesviana) no dia 27/04/2025 via Discord

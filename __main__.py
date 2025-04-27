import logging
import threading
import time
import random
from models.distributed_coordinator import DistributedCoordinator
from models.node import Node
from models.message import Message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='distributed_coordinator.log',
    filemode='w'
)

def monitor_messages(client: Node, duration: int):
    """Monitora mensagens recebidas por um cliente"""
    start_time = time.time()
    while time.time() - start_time < duration:
        message = client.consume_message()
        if message:
            print(f"[{client.id}] Recebeu: {message}")
        time.sleep(0.5)

def stress_test(system: DistributedCoordinator, num_messages: int = 50):
    """Teste de estresse com muitas mensagens simultâneas"""
    print("\n===== TESTE DE ESTRESSE =====")
    
    for i in range(3):
        system.create_channel(f"canal_{i}")
        for client_id in system.clients:
            system.subscribe_to_channel(client_id, f"canal_{i}")
    
    def sender(client: Node):
        for i in range(num_messages):
            msg_type = random.choice(['unicast', 'multicast', 'broadcast'])
            if msg_type == 'unicast':
                target = random.choice(list(system.clients.keys()))
                if target != client.id:
                    client.send_unicast(target, f"Msg {i} de {client.id}")
            elif msg_type == 'multicast':
                channel = f"canal_{random.randint(0, 2)}"
                client.send_multicast(channel, f"Msg {i} no {channel}")
            else:
                client.send_broadcast(f"Broadcast {i} de {client.id}")
            time.sleep(random.uniform(0.1, 0.5))
    
    threads = []
    for client in system.clients.values():
        t = threading.Thread(target=sender, args=(client,))
        threads.append(t)
        t.start()
    
    monitor_threads = []
    for client in system.clients.values():
        t = threading.Thread(target=monitor_messages, args=(client, 30))
        monitor_threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    for t in monitor_threads:
        t.join()

def messaging_test(system: DistributedCoordinator):
    print("\n===== TESTE DE MENSAGENS =====")
    
    cliente1 = system.clients["cliente1"]
    cliente2 = system.clients["cliente2"]
    cliente3 = system.clients["cliente3"]
    cliente4 = system.clients["cliente4"]
    
    monitors = []
    for client in [cliente1, cliente2, cliente3, cliente4]:
        monitor = threading.Thread(target=monitor_messages, args=(client, 10))
        monitors.append(monitor)
        monitor.start()
    
    print("\nTeste Unicast:")
    timestamp = system.global_clock.increment()
    message = Message(cliente1.id, "Olá cliente2, como vai?", timestamp)
    cliente1.send_unicast("cliente2", message.content)
    time.sleep(1)
    
    print("\nTeste Multicast:")
    system.create_channel("noticias")
    system.subscribe_to_channel("cliente1", "noticias")
    system.subscribe_to_channel("cliente2", "noticias")
    system.subscribe_to_channel("cliente3", "noticias")
    
    cliente4.send_multicast("noticias", "Nova atualização disponível!")
    time.sleep(1)
    
    print("\nTeste Broadcast:")
    cliente1.send_broadcast("Mensagem importante para todos!")
    time.sleep(1)
    
    for monitor in monitors:
        monitor.join()


def resource_contention_test(system: DistributedCoordinator):
    """Teste de contenção de recursos com múltiplos recursos e clientes"""
    print("\n===== TESTE DE CONTENÇÃO DE RECURSOS =====")
    
    resources = ["impressora", "scanner", "servidor", "disco"]
    for res in resources:
        system.create_resource(res)
    
    def use_resources(client: Node):
        for _ in range(5):
            res = random.choice(resources)
            print(f"[{client.id}] Tentando acessar {res}")
            
            if client.request_resource(res):
                print(f"[{client.id}] Adquiriu {res}")
                time.sleep(random.uniform(0.5, 2))
                client.release_resource(res)
                print(f"[{client.id}] Liberou {res}")
            else:
                print(f"[{client.id}] Não conseguiu acessar {res}")
            time.sleep(random.uniform(0.5, 1))
    
    threads = []
    for client in system.clients.values():
        t = threading.Thread(target=use_resources, args=(client,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

def failure_recovery_test(system: DistributedCoordinator):
    """Teste de recuperação de falhas"""
    print("\n===== TESTE DE RECUPERAÇÃO DE FALHAS =====")
    
    system.create_resource("banco_de_dados")
    system.create_channel("backup")
    for client_id in system.clients:
        system.subscribe_to_channel(client_id, "backup")
    
    def failing_client_behavior(client: Node):
        if client.request_resource("banco_de_dados"):
            print(f"[{client.id}] Adquiriu o recurso e vai falhar")
            time.sleep(1)
            print(f"[{client.id}] Simulando falha...")
            return
        
    bad_client = system.clients["cliente1"]
    t = threading.Thread(target=failing_client_behavior, args=(bad_client,))
    t.start()
    t.join()
    
    def normal_client_behavior(client: Node):
        time.sleep(random.uniform(0.5, 2))
        if client.request_resource("banco_de_dados"):
            print(f"[{client.id}] Conseguiu acessar após falha")
            time.sleep(1)
            client.release_resource("banco_de_dados")
        else:
            print(f"[{client.id}] Não conseguiu acessar")
    
    threads = []
    for client_id, client in system.clients.items():
        if client_id != "cliente1":
            t = threading.Thread(target=normal_client_behavior, args=(client,))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()
    
    print("\nVerificando estado do sistema após falha...")
    time.sleep(3)

def clock_sync_test(system: DistributedCoordinator):
    """Teste de sincronização de relógios"""
    print("\n===== TESTE DE SINCRONIZAÇÃO DE RELÓGIOS =====")
    
    def send_messages(client: Node):
        for i in range(3):
            time.sleep(random.uniform(0.1, 0.5))
            target = random.choice(list(system.clients.keys()))
            if target != client.id:
                client.send_unicast(target, f"Msg {i} para verificar relógio")
    
    threads = []
    for client in system.clients.values():
        t = threading.Thread(target=send_messages, args=(client,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    time.sleep(1)
    print("\nRelógio global:", system.global_clock.get_time())

if __name__ == "__main__":
    system = DistributedCoordinator()
    for i in range(1, 6):
        system.register_client(f"cliente{i}")
    
    print("======== INICIANDO TESTES COMPLETOS ========")
    
    messaging_test(system)
    
    stress_test(system, num_messages=30)
    resource_contention_test(system)
    failure_recovery_test(system)
    clock_sync_test(system)
    
    print("\n===== LOGS DO SISTEMA =====")
    try:
        with open('distributed_coordinator.log', 'r') as f:
            log_content = f.read()
            print(log_content if log_content else "Nenhum log disponível")
    except FileNotFoundError:
        print("Arquivo de log não encontrado")
import logging
import threading
import time
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
    start_time = time.time()
    while time.time() - start_time < duration:
        message = client.consume_message()
        if message:
            print(f"[{client.id}] Recebeu: {message}")
        time.sleep(0.5)

def resource_usage_test(system: DistributedCoordinator):
    print("\n===== TESTE DE EXCLUSÃO MÚTUA =====")
    
    system.create_resource("impressora")
    
    def use_resource(client: Node, resource_id: str, delay: float = 0):
        time.sleep(delay)
        print(f"[{client.id}] tentando acessar {resource_id}")
        
        if client.request_resource(resource_id):
            print(f"[{client.id}] adquiriu {resource_id}")
            time.sleep(2)
            client.release_resource(resource_id)
            print(f"[{client.id}] liberou {resource_id}")
        else:
            print(f"[{client.id}] não conseguiu acessar {resource_id}")
    
    threads = []
    for idx, client_id in enumerate(["cliente1", "cliente2", "cliente3"]):
        thread = threading.Thread(
            target=use_resource, 
            args=(system.clients[client_id], "impressora", idx * 1.0)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

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

if __name__ == "__main__":
    
    system = DistributedCoordinator()
    
    for i in range(1, 5):
        system.register_client(f"cliente{i}")
    
    messaging_test(system)
    
    resource_usage_test(system)
    
    print("\n===== LOGS DO SISTEMA =====")
    with open('log.log', 'r') as f:
        log_content = f.read()
        print(log_content if log_content else "Nenhum log disponível")
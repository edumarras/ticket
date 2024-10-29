import docker
import time

# Configurações do Docker e da imagem
DOCKER_IMAGE_NAME = "pois0n/ticket-front:latest"  # Nome completo da imagem no Docker Hub
CONTAINER_NAME = "front"  # Nome para identificar o container frontend

# Inicializa o cliente Docker
client = docker.from_env()

def get_local_image_id():
    """Obtém o ID da imagem local do frontend."""
    try:
        image = client.images.get(DOCKER_IMAGE_NAME)
        return image.id
    except docker.errors.ImageNotFound:
        return None

def update_container():
    """Atualiza o container frontend com a última versão da imagem."""
    print("Atualizando o container para a nova imagem...")
    
    # Parar e remover o container atual se ele existir
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass
    
    # Puxar a última imagem do Docker Hub
    client.images.pull(DOCKER_IMAGE_NAME)
    
    # Iniciar um novo container com a nova imagem
    client.containers.run(
        DOCKER_IMAGE_NAME,
        name=CONTAINER_NAME,
        detach=True,
        network_mode="host"  # Usa a network=host
    )
    print("Container atualizado e em execução.")

def main():
    print("Iniciando o monitoramento de atualizações da imagem Docker frontend...")
    last_image_id = get_local_image_id()
    
    while True:
        time.sleep(30)  # Intervalo de verificação de 30 segundos
        
        # Obtém o ID da imagem local
        current_image_id = get_local_image_id()
        
        # Se o ID mudou, significa que há uma nova versão da imagem
        if current_image_id != last_image_id:
            print("Nova imagem detectada! Atualizando o container...")
            update_container()
            last_image_id = get_local_image_id()
        else:
            print("Nenhuma atualização detectada.")

if __name__ == "__main__":
    main()

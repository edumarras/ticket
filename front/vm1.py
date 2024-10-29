import docker
import time

# Configurações do Docker e da imagem
DOCKER_IMAGE_NAME = "pois0n/ticket-front:latest"  # Nome completo da imagem no Docker Hub
CONTAINER_NAME = "front"  # Nome para identificar o container frontend

# Inicializa o cliente Docker
client = docker.from_env()

def get_remote_image_digest():
    """Obtém o digest da imagem remota para verificar se há atualizações."""
    try:
        # Força o pull para garantir que temos a última versão e capturar o digest atualizado
        image = client.images.pull(DOCKER_IMAGE_NAME)
        return image.attrs['RepoDigests'][0]  # O digest da imagem remoto
    except docker.errors.APIError as e:
        print(f"Erro ao obter o digest da imagem remota: {e}")
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
    last_image_digest = get_remote_image_digest()  # Obtém o digest da imagem remota inicialmente
    
    while True:
        time.sleep(30)  # Intervalo de verificação de 30 segundos
        
        # Obtém o digest da imagem remota atual
        current_image_digest = get_remote_image_digest()
        
        # Se o digest mudou, significa que há uma nova versão da imagem
        if current_image_digest and current_image_digest != last_image_digest:
            print("Nova imagem detectada! Atualizando o container...")
            update_container()
            last_image_digest = current_image_digest  # Atualiza o digest da última versão
        else:
            print("Nenhuma atualização detectada.")

if __name__ == "__main__":
    main()

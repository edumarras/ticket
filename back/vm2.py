import docker
import time
import subprocess

# Configurações das imagens e containers
IMAGES = {
    "back": "pois0n/ticket-db:latest",
    "middle": "pois0n/ticket-api:latest"
}

# Inicializa o cliente Docker
client = docker.from_env()

def get_remote_image_digest(image_name):
    """Obtém o digest da imagem remota para verificar se há atualizações."""
    try:
        # Força o pull para garantir que temos a última versão e capturar o digest atualizado
        image = client.images.pull(image_name)
        return image.attrs['RepoDigests'][0]  # O digest da imagem remoto
    except docker.errors.APIError as e:
        print(f"Erro ao obter o digest da imagem remota para {image_name}: {e}")
        return None

def update_code():
    """Atualiza o código da aplicação com git pull no diretório atual."""
    print("Atualizando o código da aplicação...")
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("Código atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o código: {e}")

def recreate_containers():
    """Recria os containers usando docker-compose para garantir o mapeamento correto de portas."""
    print("Recriando todos os containers usando docker-compose...")
    try:
        # Parar e remover todos os containers do docker-compose
        subprocess.run(["sudo", "docker-compose", "down"], check=True)
        # Reconstruir e subir os containers com as configurações do docker-compose.yml
        subprocess.run(["sudo", "docker-compose", "up", "-d"], check=True)
        print("Containers recriados com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao recriar os containers: {e}")

def main():
    print("Iniciando o monitoramento de atualizações das imagens Docker backend e middleware...")

    # Inicializa os últimos digests para cada imagem
    last_image_digests = {name: get_remote_image_digest(image) for name, image in IMAGES.items()}

    while True:
        time.sleep(10)  # Intervalo de verificação de 10 segundos

        for name, image_name in IMAGES.items():
            # Obtém o digest da imagem remota atual
            current_image_digest = get_remote_image_digest(image_name)

            # Se o digest mudou, significa que há uma nova versão da imagem
            if current_image_digest and current_image_digest != last_image_digests[name]:
                print(f"Nova imagem detectada para {name}! Atualizando o container e o código da aplicação...")
                update_code()  # Atualiza o código no diretório atual
                recreate_containers()  # Recria todos os containers usando docker-compose
                last_image_digests[name] = current_image_digest  # Atualiza o digest da última versão
            else:
                print(f"Nenhuma atualização detectada para {name}.")

if __name__ == "__main__":
    main()

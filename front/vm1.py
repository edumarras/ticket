import docker
import time
import logging
from datetime import datetime
#caguei em vc
# Configuração do logging
logging.basicConfig(
    filename='docker_update.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def check_and_update():
    try:
        # Conecta ao Docker
        client = docker.from_env()
        
        # Nome da imagem que queremos monitorar
        image_name = "pois0n/ticket-front:latest"
        
        # Puxa a imagem mais recente
        logging.info("Verificando por atualizações...")
        new_image = client.images.pull(image_name)
        
        # Encontra o container atual
        containers = client.containers.list(
            filters={'ancestor': image_name}
        )
        
        if containers:
            container = containers[0]
            # Captura o nome da imagem do container encontrado
            current_image_name = container.image.tags[0] if container.image.tags else "Imagem sem nome"
            
            # Loga e printa o nome da imagem do container
            logging.info(f"Container encontrado rodando a imagem: {current_image_name}")
            print(f"Container encontrado rodando a imagem: {current_image_name}")
            
            # Verifica se há uma atualização na imagem
            current_image_id = container.image.id
            new_image_id = new_image.id
            
            if current_image_id != new_image_id:
                logging.info("Nova imagem detectada. Atualizando o container...")
                print("Nova imagem detectada! Reiniciando o container...")

                # Remove o container antigo e cria um novo
                container.remove(force=True)
                client.containers.run(image_name, detach=True, name="ticket-front-container")
                
                logging.info("Container atualizado com a nova imagem com sucesso!")
                print("Container atualizado com a nova imagem com sucesso!")
            else:
                logging.info("Imagem já está atualizada. Nenhuma ação necessária.")
                print("Imagem já está atualizada. Nenhuma ação necessária.")
        else:
            logging.warning("Nenhum container encontrado rodando a imagem.")
            print("Nenhum container encontrado rodando a imagem.")
            
    except docker.errors.APIError as e:
        logging.error(f"Erro na API Docker: {e}")
        print(f"Erro na API Docker: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        print(f"Erro inesperado: {e}")

def main():
    while True:
        check_and_update()
        # Espera 30 segundos antes de verificar novamente
        time.sleep(30)

if __name__ == "__main__":
    logging.info("Iniciando serviço de atualização...")
    print("Iniciando serviço de atualização...")
    main()

import docker
import time
import logging
from datetime import datetime

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
       client.images.pull(image_name)
       
       # Encontra o container atual
       containers = client.containers.list(
           filters={'ancestor': image_name}
       )
       
       if containers:
           container = containers[0]
           logging.info("Reiniciando container...")
           container.restart()
           logging.info("Container reiniciado com sucesso!")
       else:
           logging.warning("Nenhum container encontrado rodando a imagem.")
           
   except docker.errors.APIError as e:
       logging.error(f"Erro na API Docker: {e}")
   except Exception as e:
       logging.error(f"Erro inesperado: {e}")

def main():
   while True:
       check_and_update()
       # Espera 30 segundos antes de verificar novamente
       time.sleep(30)

if __name__ == "__main__":
   logging.info("Iniciando serviço de atualização...")
   main()
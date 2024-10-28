import docker
import time
import logging
import subprocess
import os
from datetime import datetime

# Configuração do logging
logging.basicConfig(
   filename='docker_update.log',
   level=logging.INFO,
   format='%(asctime)s - %(message)s'
)

def toggle_network(enable=True):
   try:
       command = f"sudo ip link set ens33 {'up' if enable else 'down'}"
       subprocess.run(command.split(), check=True)
       logging.info(f"Rede {'ativada' if enable else 'desativada'} com sucesso")
       # Pequena pausa para garantir que a rede estabilize
       time.sleep(5)
       return True
   except subprocess.CalledProcessError as e:
       logging.error(f"Erro ao {'ativar' if enable else 'desativar'} a rede: {e}")
       return False

def check_and_update():
   try:
       # Ativa a rede
       if not toggle_network(True):
           return

       # Conecta ao Docker
       client = docker.from_env()
       
       # Lista de imagens para verificar
       images = [
           "pois0n/ticket-api:latest",
           "pois0n/ticket-db:latest"
       ]
       
       updated = False
       
       for image_name in images:
           try:
               # Puxa a imagem mais recente
               logging.info(f"Verificando atualizações para {image_name}...")
               client.images.pull(image_name)
               
               # Encontra o container correspondente
               containers = client.containers.list(
                   filters={'ancestor': image_name}
               )
               
               if containers:
                   container = containers[0]
                   logging.info(f"Reiniciando container {image_name}...")
                   container.restart()
                   logging.info(f"Container {image_name} reiniciado com sucesso!")
                   updated = True
               else:
                   logging.warning(f"Nenhum container encontrado rodando a imagem {image_name}")
                   
           except docker.errors.APIError as e:
               logging.error(f"Erro na API Docker para {image_name}: {e}")
               
   except Exception as e:
       logging.error(f"Erro inesperado: {e}")
   finally:
       # Desativa a rede independente do resultado
       toggle_network(False)

def main():
   while True:
       check_and_update()
       # Espera 1 minuto e 20 segundos antes de verificar novamente
       time.sleep(80)

if __name__ == "__main__":
   # Verifica se está rodando como root
   if os.geteuid() != 0:
       logging.error("Este script precisa ser executado como root")
       exit(1)
       
   logging.info("Iniciando serviço de atualização...")
   main()
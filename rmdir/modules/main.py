import os
import shutil
import logging
from pathlib import Path
from configparser import ConfigParser

def carrega_conf():
    config = ConfigParser()
    config.read('conf.ini')
    return config['SERVIDOR']

def limpar_diretorios(pasta, excecoes, logger):
    for entrada in os.scandir(pasta):
        if entrada.name in excecoes:
            continue
        try:
            if entrada.is_file():
                os.remove(entrada.path)
                logger.info(f"Arquivo excluído: {entrada.path}")
            elif entrada.is_dir():
                shutil.rmtree(entrada.path)
                logger.info(f"Diretório excluído: {entrada.path}")
        except Exception as e:
            logger.error(f"Erro ao excluir '{entrada.path}': {e}")

    logger.info(f"Todo conteúdo da pasta {pasta} foi excluído.")

def lista_usuarios(logger):
    usuarios = Path.cwd() / 'usuarios.txt'
    comando_dsquery = f'dsquery user "ou=Usuários SOLARIUM,dc=solarium,dc=corp" | dsget user -samid -disabled > {usuarios}'
    os.system(comando_dsquery)

    with open(usuarios, 'r') as arquivo:
        conteudo = arquivo.read()
        usuarios_ativos_ad = [valor.title().replace('.', ' ') for indice, valor in enumerate(conteudo.split()[:-3:2]) if valor not in ['samid', 'disabled'] and conteudo.split()[indice * 2 + 1] == 'no']
        logger.info(f"{len(usuarios_ativos_ad)} usuários encontrados no Active Directory.")

        return usuarios_ativos_ad

def criar_diretorios(usuarios_dominio, diretorio, logger):
    """Cria novos diretórios com base na lista de usuários do domínio."""
    # implementação
    for usuarios in usuarios_dominio:
        caminho = os.path.join(diretorio, usuarios)
        os.mkdir(caminho)
        logger.info(f"Criado diretório: {caminho}")

def main():
    """Função principal que inicia o fluxo de execução do programa."""
    # configurando o logger
    logging.basicConfig(filename='programa.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    # lê as informações do arquivo de configuração
    config = carrega_conf()
    ip = config.get('ip')
    compartilhamento = config.get('pasta_compartilhada')
    caminho_compartilhamento = os.path.join(ip, compartilhamento)
    excecoes = config.get('manter_diretorios')
    criar_dir = config.get('criar_diretorios')

    # exclui os diretórios antigos
    limpar_diretorios(caminho_compartilhamento, excecoes, logger)

    # lista de diretórios que serão criados
    diretorios = lista_usuarios(logger)

    # criando novos diretórios
    criar_diretorios(diretorios, caminho_compartilhamento, logger)

if __name__ == '__main__':
    main()

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
    pastas_nao_removidas = []
    for entrada in os.scandir(pasta):
        if entrada.name in excecoes:
            continue

        try:
            if entrada.is_file():
                os.remove(entrada.path)
            else:
                shutil.rmtree(entrada.path)

            logger.info(f"{entrada.path} foi excluido.")

        except Exception as erro:
            pastas_nao_removidas.append(entrada.name)
            logger.error(f"Erro ao excluir '{entrada.path}': {erro}")

    logger.info(f"Todo conteudo da pasta {pasta} foi excluido.\n")

    return pastas_nao_removidas

# Está função remove o conteúdo dos diretórios que retornaram erro na exclusão geral.
def removendo_outros_dir(caminho, lista_diretorios, logger):
    for diretorio in lista_diretorios:
        caminho_diretorio = os.path.join(caminho, diretorio)

        logger.info(f"Iniciando a exclusao da pasta: {caminho_diretorio}.")

        for caminho_raiz, nome_dir, arquivos in os.walk(caminho_diretorio):
            for arquivo in arquivos:
                elemento = os.path.join(caminho_raiz, arquivo)
                
                try:
                    os.remove(elemento)
                    logger.info(f"\t{elemento} foi excluido.")
                except Exception as erro:
                    logger.error(f"\tErro ao excluir '{elemento}': {erro}")
                    
        for caminho_raiz, nome_dir, arquivos in os.walk(caminho_diretorio):
            for diretorio in nome_dir:    
                if not os.listdir(caminho_raiz): # verifica se a lista de arquivos está vazia
                    try:
                        os.rmdir(caminho_raiz) # remove o diretório vazio
                        logger.info(f"\tDiretorio vazio excluido: {caminho_raiz}")
                    except Exception as erro:
                        logger.error(f"\tErro ao excluir diretório vazio '{caminho_raiz}': {erro}")


def lista_usuarios(logger):
    usuarios = Path.cwd() / 'usuarios.txt'
    comando_dsquery = f'dsquery user "ou=Usuários,dc=gbrcomponentes,dc=corp" | dsget user -samid -disabled > {usuarios}'
    os.system(comando_dsquery)

    with open(usuarios, 'r') as arquivo:
        conteudo = arquivo.read()

        usuarios_ativos_ad = [valor.title().replace('.', ' ') for indice, valor in enumerate(conteudo.split()[:-3:2]) if valor not in ['samid', 'disabled'] and conteudo.split()[indice * 2 + 1] == 'no']
        
        logger.info(f"{len(usuarios_ativos_ad)} usuarios encontrados no Active Directory.\n")

        return usuarios_ativos_ad


def criar_diretorios(caminho_compartilhamento, diretorios, logger):
    for diretorio in diretorios:
        caminho = os.path.join(caminho_compartilhamento, diretorio)

        try:
            os.mkdir(caminho)
            logger.info(f"Criado o diretorio: {caminho}")
        except:
            logger.error(f'O diretorio {caminho} ja existe.')


def main():
    # configurando o logger
    logging.basicConfig(filename='programa-log2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
    logger = logging.getLogger()

    # Carrega as informações do arquivo de configuração
    config = carrega_conf()
    caminho_compartilhamento = os.path.join(config.get('ip'), config.get('pasta_compartilhada'))
    excecoes = config.get('manter_diretorios')
    criar_dir = config.get('criar_diretorios')

    # Exclui os diretórios antigos
    diretorios_nao_removidos = limpar_diretorios(caminho_compartilhamento, excecoes.split(','), logger)

    # Apagando os elementos de uma pasta individualmente
    removendo_outros_dir(caminho_compartilhamento, diretorios_nao_removidos, logger)

    # Lista de diretórios que serão criados
    diretorios = lista_usuarios(logger)

    # Criando os diretórios com os nomes dos usuários ativos do AD
    criar_diretorios(caminho_compartilhamento, diretorios, logger)

    # criando novos diretórios
    # if criar_dir.lower() == 'true':
    #    criar_diretorios(diretorios, caminho_compartilhamento, logger)

if __name__ == '__main__':
    main()

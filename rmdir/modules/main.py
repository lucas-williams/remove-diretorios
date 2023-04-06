import os
import logging
from pathlib import Path
from configparser import ConfigParser

def carrega_conf():
    config = ConfigParser()
    config.read('conf.ini')
    return config['SERVIDOR']

def limpar_diretorios(pasta, excecoes):
    for entrada in os.scandir(pasta):
        if entrada.name in excecoes:
            print(f'O arquivo {entrada.name} não foi deletado! ')
            continue
        try:
            if entrada.is_file():
                os.remove(entrada.path)
            elif entrada.is_dir():
                os.rmdir(entrada.path)
        except Exception as e:
            print(f"Erro ao excluir '{entrada.path}': {e}")

    print(f"Todo conteúdo da pasta {pasta} foi excluído.")

def lista_usuarios():
    usuarios = Path.cwd() / 'usuarios.txt'
    comando_dsquery = f'dsquery user "ou=Usuários SOLARIUM,dc=solarium,dc=corp" | dsget user -samid -disabled > {usuarios}'
    os.system(comando_dsquery)

    with open(usuarios, 'r') as arquivo:
        conteudo = arquivo.read()
        usuarios_ativos_ad = [valor.title().replace('.', ' ') for indice, valor in enumerate(conteudo.split()[:-3:2]) if valor not in ['samid', 'disabled'] and conteudo.split()[indice * 2 + 1] == 'no']

        return usuarios_ativos_ad

def criar_diretorios(usuarios_dominio, diretorio):
    """Cria novos diretórios com base na lista de usuários do domínio."""
    # implementação
    for usuarios in usuarios_dominio:
        caminho = os.path.join(diretorio, usuarios)
        os.mkdir(caminho)

def main():
    """Função principal que inicia o fluxo de execução do programa."""
    # lê as informações do arquivo de configuração
    config = carrega_conf()
    ip = config.get('ip')
    compartilhamento = config.get('pasta_compartilhada')
    caminho_compartilhamento = os.path.join(ip, compartilhamento)
    excecoes = config.get('manter_diretorios')
    criar_dir = config.get('criar_diretorios')

    logging.basicConfig(filename='program.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')

    # registra a configuração carregada
    logging.info('Configuração carregada: {}'.format(config))

    # exclui os diretórios antigos
    limpar_diretorios(caminho_compartilhamento, excecoes)

    # registra a exclusão dos diretórios antigos
    logging.info('Diretórios antigos excluídos: {}'.format(caminho_compartilhamento))

    # lista de diretórios que serão criados
    diretorios = lista_usuarios()

    # criando novos diretórios
    criar_diretorios(diretorios, caminho_compartilhamento)

    # registra a criação dos novos diretórios
    logging.info('Novos diretórios criados: {}'.format(diretorios))

    # registra o final da execução
    logging.info('Programa finalizado com sucesso.')


if __name__ == '__main__':
    main()

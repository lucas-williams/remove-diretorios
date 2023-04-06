import os
import logging
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
    criar_diretorios = config.get('criar_diretorios')

    # exclui os diretórios antigos
    limpar_diretorios(caminho_compartilhamento, excecoes)

    # lista de diretórios que serão criados
    diretorios = lista_usuarios()

    # criando novos diretórios
    criar_diretorios(diretorios, caminho_compartilhamento)

    """
    # cria novos diretórios com base nos usuários do domínio
    domain_users = win32com.client.GetObject("LDAP://" + config['domain_name']).members()
    create_directories(domain_users, config['directory_path'])

    # registra as ações do programa em um arquivo de log
    logging.basicConfig(filename='program.log', level=logging.INFO)
    logging.info('Diretórios antigos excluídos: {}'.format(config['directory_path']))
    logging.info('Novos diretórios criados com base em: {}'.format(config['domain_name']))
    """

if __name__ == '__main__':
    main()

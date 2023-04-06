from configparser import ConfigParser
import os


def carrega_conf():
    config = ConfigParser()
    config.read('conf.ini')
    return config['SERVIDOR']


def principal():
    config = carrega_conf()
    ip = config.get('ip')
    compartilhamento = config.get('pasta_compartilhada')
    caminho_compartilhamento = os.path.join(ip, compartilhamento)
    manter_diretorios = config.get('manter_diretorios')
    criar_diretorios = config.get('criar_diretorios')
    print(f'{caminho_compartilhamento}, {manter_diretorios}, {criar_diretorios}')

principal()
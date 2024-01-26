
from logging import error, info
from os.path import isdir, isfile, join
from os import listdir
from random import randint
from time import sleep

class Archives:
    """Classe que define os métodos para manipulação de arquivos"""
    def __init__(self, logger) -> None:
        """Classe que define os métodos para manipulação de arquivos"""
        self.logger = logger

    def open_archive(self, directory:str, archive:str) -> str:
        """Tenta abrir o arquivo"""
        try:
            with open(f'{directory}/{archive}', 'r', encoding='utf-8') as file:
                data = file.read()
            return data
        except Exception as e:
            error(f"Erro ao ler o arquivo: {e}")
            return  f'Erro ao ler o arquivo: {archive}'

    def write_archive(self, directory:str, archive:str, data:str) -> str:
        """Tenta escrever o arquivo"""
        try:
            info("Escrevendo arquivo")
            for _ in range(randint(1, 5)):
                print(".", end="", flush=True)
                sleep(1)
            print("")
            with open(f'{directory}/{archive}', 'w', encoding='utf-8') as file:
                file.write(data)
            sleep(.5)
            info("Arquivo escrito com sucesso!")
            return data
        except Exception as e:
            error(f"Erro ao escrever o arquivo: {archive}")
            return  data

    def get_files_from_directory(self, directory:str, extension:str = '.nfo') -> list:
        """Método que recebe um diretório e retorna uma lista de arquivos"""

        try:
            info("Pegando arquivos do diretório")
            for _ in range(randint(1, 5)):
                print(".", end="", flush=True)
                sleep(1)
            print("")
            files = [file for file in listdir(directory) if file.endswith(extension)]
            info("Arquivos obtidos com sucesso!")
            return files
        except Exception as e:
            error(f"Erro ao listar arquivos no diretório: {e}")
            return []
    
    def is_valid_directory(self, path: str) -> bool:
        """Método que valida se o diretório do poster é válido."""
        if isdir(path):
            return True
        else:
            error(f"""O diretório "{path}" não é válido.""")
            return False
    
    def validate_directory(self, prompt:str):
        """"Método que valida se o diretório é válido."""
        while True:
            path = self.logger.formatted_input(prompt)
            if self.is_valid_directory(path):
                break
        return path
    
    def get_single_file(self, directory):
        while True:
            file = self.logger.formatted_input("Por favor, insira o nome do arquivo: ")
            if not file.endswith('.nfo'):
                if '.' not in file:
                    if isfile(join(directory, file + '.nfo')):
                        file += '.nfo'
                    else:
                        error(f"""O arquivo "{file}" não existe no diretório especificado. Por favor, insira um nome de arquivo válido.""")
                        continue
                elif not isfile(join(directory, file)):
                    error(f"""O arquivo "{file}" não existe no diretório especificado. Por favor, insira um nome de arquivo válido.""")
                    continue
            return file
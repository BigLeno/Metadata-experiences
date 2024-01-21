
from logging import error
from os.path import isdir
from os import listdir


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
            with open(f'{directory}/{archive}', 'w', encoding='utf-8') as file:
                file.write(data)
            return data
        except Exception as e:
            error(f"Erro ao escrever o arquivo: {archive}")
            return  data

    def get_files_from_directory(self, directory:str, extension:str = '.nfo') -> list:
        """Método que recebe um diretório e retorna uma lista de arquivos"""

        try:
            files = [file for file in listdir(directory) if file.endswith(extension)]
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
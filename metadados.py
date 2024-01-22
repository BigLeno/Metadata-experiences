
from time import sleep
from random import randint
from logging import info, error

from Modules.Logger import Logger
from Modules.Archives import Archives
from Modules.Subtitles import Subtitles

from Components.Plot import Plot
from Components.Poster import Poster
from Components.Season import Season
from Components.Episode import Episode
from Components.Language import Language

class Metadados(Poster, Plot, Language, Episode, Season): 
    """Classe que define os métodos para manipulação de metadados"""
    def __init__(self) -> None:
        """Classe que define os métodos para manipulação de metadados"""
        pass

    def handle_poster_change(self, data, poster_path):
        """Manipula a mudança na tag <art>."""
        data = self.handle_empty_art_tag(data, poster_path)
        data = self.handle_existing_poster_tag(data, poster_path)
        data = self.handle_no_art_tag(data, poster_path)
        return data

    def handle_plot_change(self, data) -> str:
        """Manipula a mudança na tag <plot>."""
        data = self.handle_existing_plot(data)
        data = self.handle_bad_plot(data)
        data = self.handle_no_plot(data)
        return data

    def handle_language_change(self, data:str) -> str:
        """Manipula a mudança na tag <language>."""
        data = self.handle_existing_language(data)
        data = self.handle_no_language(data)
        return data

    def handle_episode_change(self, data):
        """Manipula a mudança na tag <episode>."""
        data = self.handle_existing_episode(data)
        data = self.handle_no_episode(data)
        return data

    def handle_season_change(self, data, season):
        """Manipula a mudança na tag <season>."""
        data = self.handle_existing_season(data, season)
        data = self.handle_no_season(data, season)
        return data

    def get_files(self):
        """Método que vai receber o arquivo e modificar o texto"""
        while True:
            file_or_directory = self.logger.formatted_input("Você deseja processar um diretório ou um arquivo único? (D/A): ")
            if file_or_directory.upper() == 'D':
                directory = self.archives.validate_directory("Por favor, insira o caminho do diretório: ")
                files = self.archives.get_files_from_directory(directory)
                return directory, files
            elif file_or_directory.upper() == 'A':
                directory = self.archives.validate_directory("Por favor, insira o caminho do diretório: ")
                file = self.archives.get_single_file(directory)
                return directory, [file]
            else:
                error(f"""Erro ao indicar a escolha desejada: "{file_or_directory}". Tente novamente entre "D" ou "A".""")

    def process_file(self, directory, file, poster_path, season, subtitle_option):
        """Método que vai receber o arquivo e modificar o texto"""
        while True:
            change_file = self.logger.formatted_input(f"Deseja alterar o arquivo {file}? (S/N): ")
            if change_file.upper() == 'S':
                data = self.archives.open_archive(directory, file)
                data = self.handle_poster_change(data, poster_path)
                data = self.handle_plot_change(data)
                data = self.handle_language_change(data)
                data = self.handle_episode_change(data)
                data = self.handle_season_change(data, season)
                if subtitle_option.upper() == 'L':
                    data = self.legendas.enable_portuguese_subtitles(data)
                elif subtitle_option.upper() == 'D':
                    data = self.legendas.disable_subtitles(data)
                self.archives.write_archive(directory, file, data)
                break
            elif change_file.upper() == 'N':
                info(f"Nenhuma alteração feita no arquivo {file}.")
                break
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change_file}", Tente novamente entre "S" ou "N".""")

    def modify_files(self, directory, files):
        """Método que vai receber o arquivo e modificar o texto"""
        poster_path = self.archives.validate_directory("Por favor, insira o caminho do poster: ")
        season = self.logger.formatted_input("Por favor, insira a temporada: ")
        subtitle_option = self.legendas.get_subtitle_option()

        for file in files:
            self.process_file(directory, file, poster_path, season, subtitle_option)

    def get_and_modify(self):
        """Método que vai receber o arquivo e modificar o texto"""
        while True:
            directory, files = self.get_files()
            if directory and files:
                self.modify_files(directory, files)

            continue_processing = self.logger.formatted_input("Deseja processar outro diretório ou arquivo? (S/N): ")
            if continue_processing.upper() != 'S':
                info("Encerrando o programa...")
                break
        
    def run(self):
        """Método que vai receber o arquivo e modificar o texto"""
        try:
            self.logger = Logger()
            info("Iniciando o script")
            sleep(.5)
            for _ in range(randint(1, 15)):
                print(".", end="", flush=True)
                sleep(.5)
            print("")
            info("""Sistema de modificação de metadados foi iniciado!""")
            sleep(.5)
            self.archives = Archives(self.logger)
            self.legendas = Subtitles(self.logger)
            self.get_and_modify()
            sleep(.5)
            info("Programa encerrado com sucesso!")
        except KeyboardInterrupt:
            print("")
            info("Programa encerrado pelo usuário.")
            exit(-1)
        
        
if __name__ == '__main__':
    metadados = Metadados()
    metadados.run()


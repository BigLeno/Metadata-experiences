
from re import search, DOTALL
from logging import info, error
from random import randint
from time import sleep

from Modules.Logger import Logger
from Modules.Archives import Archives
from Modules.Subtitles import Subtitles


class Metadados: 
    """Classe que define os métodos para manipulação de metadados"""
    def __init__(self, logger, archives, subtitles) -> None:
        """Classe que define os métodos para manipulação de metadados"""
        self.logger = logger
        self.archives = archives
        self.legendas = subtitles
        self.get_and_modify()

    def handle_poster_change(self, data, poster_path):
        if '<art />' in data:
            error("""A tag <art /> não está formatada corretamente.""")
            poster_new = f"<art><poster>{poster_path}</poster></art>"
            data = data.replace('<art />', poster_new)
        elif '<poster>' in data and '</poster>' in data:
            poster_old = search('<poster>(.*?)</poster>', data).group()
            poster_new = f"<poster>{poster_path}</poster>"
            data = data.replace(poster_old, poster_new)
        else:
            info("""A tag <art /> não existe.""")
            poster_new = f"  <art><poster>{poster_path}</poster></art>"
            lines = data.split('\n')
            lines.insert(9, poster_new)
            data = '\n'.join(lines)
        return data

    def handle_plot_change(self, data) -> str:
        """Manipula a mudança na tag <plot>."""
        lines = data.split('\n')
        match_plot = search(r'<plot>(.*?)</plot>', data)
        match_bad_plot = search(r'<plot />', data)

        if match_plot:
            plot_old = match_plot.group(1)
            change = self.logger.formatted_input(f"""A sinopse atual é: \n\t-->  "{plot_old}". \n\tDeseja alterar? (S/N): """)
            if change.upper() == 'S':
                plot_new = self.logger.formatted_input("Por favor, insira a nova sinopse: ")
                data = data.replace(plot_old, plot_new)
                info("Sinopse Alterada.")
            elif change.upper() == 'N':
                info("Nenhuma alteração feita na sinopse.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change}", na sinopse. \n Tente novamente entre "S" ou "N".""")
        elif match_bad_plot:
            change_plot = self.logger.formatted_input("A tag <plot> está mal formatada. Deseja alterar a sinopse? (S/N): ")
            if change_plot.upper() == 'S':
                plot_new = self.logger.formatted_input("Por favor, insira a sinopse: ")
                data = data.replace('<plot />', f'<plot>{plot_new}</plot>')
                info("Sinopse Alterada.")
            elif change_plot.upper() == 'N':
                info("Nenhuma alteração feita na sinopse.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")

        else:
            add_plot = self.logger.formatted_input("A tag <plot> não existe. Deseja adicionar uma sinopse? (S/N): ")
            if add_plot.upper() == 'S':
                plot_new = self.logger.formatted_input("Por favor, insira a sinopse: ")
                lines.insert(2, f'  <plot>{plot_new}</plot>')
                data = '\n'.join(lines)
            elif add_plot.upper() == 'N':
                info("Nenhuma alteração feita na sinopse.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{add_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")

        return data

    def handle_language_change(self, data:str) -> str:
        """Manipula a mudança na tag <language>."""
        lines = data.split('\n')
        match_language = search(r'<episodedetails>.*?<streamdetails>.*?<audio>.*?<language>(.*?)</language>.*?</audio>.*?</streamdetails>.*?</episodedetails>', data, DOTALL)

        if match_language:
            language_old = match_language.group(1)
            change = self.logger.formatted_input(f"A linguagem atual té: \n\t-->    {language_old}. \n\tDeseja alterar? (S/N): ")
            if change.upper() == 'S':
                language_new = self.logger.formatted_input("""Por favor, insira a nova linguagem \n\t\t\tExemplo: \n\t\t\t    por, eng, jpn     : """)
                data = data.replace(language_old, language_new)
                info("Linguagem Alterada.")
            elif change.upper() == 'N':
                info("Nenhuma alteração feita na linguagem.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change}", na linguagem. \n Tente novamente entre "S" ou "N".""")
        else:
            add_language = self.logger.formatted_input("A tag <language> não existe. Deseja adicionar uma linguagem? (S/N): ")
            if add_language.upper() == 'S':
                language_new = self.logger.formatted_input("Por favor, insira a linguagem: ")
                lines.insert(2, f'<episodedetails><streamdetails><audio><language>{language_new}</language></audio></streamdetails></episodedetails>')
                data = '\n'.join(lines)
            elif add_language.upper() == 'N':
                info("Nenhuma alteração feita na linguagem.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{add_language}", na linguagem. \n Tente novamente entre "S" ou "N".""")

        return data

    def handle_episode_change(self, data):
        """Manipula a mudança na tag <episode>."""
        lines = data.split('\n')
        match_episode = search(r'<episodedetails>.*?<episode>(.*?)</episode>.*?</episodedetails>', data, DOTALL)

        if match_episode:
            episode_old = match_episode.group(1)
            change = self.logger.formatted_input(f"O episódio atual é: {episode_old}. Deseja alterar? (S/N): ")
            if change.upper() == 'S':
                episode_new = self.logger.formatted_input("Por favor, insira o novo episódio: ")
                data = data.replace(episode_old, episode_new)
            elif change.upper() == 'N':
                info("Nenhuma alteração feita no episódio.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change}", no episódio. \n Tente novamente entre "S" ou "N".""")

        else:
            add_episode = self.logger.formatted_input("A tag <episode> não existe. Deseja adicionar um episódio? (S/N): ")
            if add_episode.upper() == 'S':
                episode_new = self.logger.formatted_input("Por favor, insira o episódio: ")
                for i, line in enumerate(lines):
                    if '<showtitle>' in line:
                        lines.insert(i+1, f'  <episode>{episode_new}</episode>')
                        data = '\n'.join(lines)
                        break
            elif add_episode.upper() == 'N':
                info("Nenhuma alteração feita no episódio.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{add_episode}", no episódio. \n Tente novamente entre "S" ou "N".""")

        return data

    def handle_season_change(self, data, season):
        """Manipula a mudança na tag <season>."""
        lines = data.split('\n')
        match_season = search(r'<episodedetails>.*?<season>(.*?)</season>.*?</episodedetails>', data, DOTALL)

        if match_season:
            season_old = match_season.group(1)
            data = data.replace(season_old, season)
        else:
            for i, line in enumerate(lines):
                if '<showtitle>' in line:
                    lines.insert(i+1, f'  <season>{season}</season>')
                    data = '\n'.join(lines)
                    break

        return data
        

    def get_and_modify(self):
        """Método que vai receber o arquivo e modificar o texto"""
        while True:
            file_or_directory = self.logger.formatted_input("Você deseja processar um diretório ou um arquivo único? (D/A): ")
            if file_or_directory.upper() == 'D':
                directory = self.archives.validate_directory("Por favor, insira o caminho do diretório: ")
                files = self.archives.get_files_from_directory(directory)
            elif file_or_directory.upper() == 'A':
                directory = self.archives.validate_directory("Por favor, insira o caminho do diretório: ")
                file = self.logger.formatted_input("Por favor, insira o nome do arquivo: ")
                files = [file]
            else:
                error(f"""Erro ao indicar a escolha desejada: "{file_or_directory}". \n Tente novamente entre "D" ou "A".""")
                continue

            poster_path = self.archives.validate_directory("Por favor, insira o caminho do poster: ")
            season = self.logger.formatted_input("Por favor, insira a temporada: ")
            subtitle_option = self.logger.formatted_input("O arquivo é para legendado ou dublado? (L/D): ")

            for file in files:
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
                elif change_file.upper() == 'N':
                    info(f"Nenhuma alteração feita no arquivo {file}.")
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{change_file}", no arquivo {file}. \n Tente novamente entre "S" ou "N".""")

            continue_processing = self.logger.formatted_input("Deseja processar outro diretório ou arquivo? (S/N): ")
            if continue_processing.upper() != 'S':
                info("Encerrando o programa...")
                break
        
        
if __name__ == '__main__':
    try:
        logger = Logger()
        info("Iniciando o script")
        sleep(.5)
        for _ in range(randint(1, 15)):
            print(".", end="", flush=True)
            sleep(.5)
        print("")
        info("""Sistema de modificação de metadados foi iniciado!""")
        sleep(.5)
        archives = Archives(logger)
        subtitles = Subtitles()
        metadados = Metadados(logger, archives, subtitles)
        sleep(.5)
        info("Programa encerrado com sucesso!")
    except KeyboardInterrupt:
        print("")
        info("Programa encerrado pelo usuário.")
        exit(-1)


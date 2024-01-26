
from re import search, DOTALL
from logging import info, error

class Language:
    """Classe responsável por adicionar a linguagem ao arquivo XML."""

    def __init__(self):
        """Classe responsável por adicionar a linguagem ao arquivo XML."""
        pass

    def handle_existing_language(self, data):
        match_language = search(r'<episodedetails>.*?<streamdetails>.*?<audio>.*?<language>(.*?)</language>.*?</audio>.*?</streamdetails>.*?</episodedetails>', data, DOTALL)
        if match_language:
            language_old = match_language.group(1)
            while True:
                change = self.logger.formatted_input(f"A linguagem atual té: \n\t-->    {language_old}. \n\tDeseja alterar? (S/N): ")
                if change.upper() == 'S':
                    language_new = self.logger.formatted_input("""Por favor, insira a nova linguagem \n\t\t\tExemplo: \n\t\t\t    por, eng, jpn     : """)
                    data = data.replace(language_old, language_new)
                    info("Linguagem Alterada.")
                    break
                elif change.upper() == 'N':
                    info("Nenhuma alteração feita na linguagem.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{change}", na linguagem. \n Tente novamente entre "S" ou "N".""")
        return data

    def handle_no_language(self, data):
        lines = data.split('\n')
        if '<episodedetails>' not in data and '<streamdetails>' not in data and '<audio>' not in data and '<language>' not in data and '</language>' not in data:
            while True:
                add_language = self.logger.formatted_input("A tag <language> não existe. Deseja adicionar uma linguagem? (S/N): ")
                if add_language.upper() == 'S':
                    language_new = self.logger.formatted_input("Por favor, insira a linguagem: ")
                    lines.insert(2, f'<episodedetails><streamdetails><audio><language>{language_new}</language></audio></streamdetails></episodedetails>')
                    data = '\n'.join(lines)
                    break
                elif add_language.upper() == 'N':
                    info("Nenhuma alteração feita na linguagem.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{add_language}", na linguagem. \n Tente novamente entre "S" ou "N".""")
        return data
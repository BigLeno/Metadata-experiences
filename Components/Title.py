
from re import search, DOTALL
from logging import info, error

class Title:
    """Classe responsável por adicionar o título ao arquivo XML."""
    def __init__(self):
        """Classe responsável por adicionar o título ao arquivo XML."""
        pass

    def handle_existing_title(self, data):
        match_title = search(r'<episodedetails>.*?<title>(.*?)</title>.*?</episodedetails>', data, DOTALL)
        if match_title:
            title_old = match_title.group(1)
            while True:
                change = self.logger.formatted_input(f"O título atual é: {title_old}. Deseja alterar? (S/N): ")
                if change.upper() == 'S':
                    title_new = self.logger.formatted_input("Por favor, insira o novo título: ")
                    data = data.replace(f'<title>{title_old}</title>', f'<title>{title_new}</title>')
                    break
                elif change.upper() == 'N':
                    info("Nenhuma alteração feita no título.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{change}", no título. \n Tente novamente entre "S" ou "N".""")
        return data

    def handle_no_title(self, data):
        lines = data.split('\n')
        if '<episodedetails>' in data and '<title>' not in data and '</title>' not in data:
            while True:
                add_title = self.logger.formatted_input("A tag <title> não existe. Deseja adicionar um título? (S/N): ")
                if add_title.upper() == 'S':
                    title_new = self.logger.formatted_input("Por favor, insira o título: ")
                    for i, line in enumerate(lines):
                        if '<dateadded>' in line:
                            lines.insert(i+1, f'  <title>{title_new}</title>')
                            data = '\n'.join(lines)
                            break
                    break
                elif add_title.upper() == 'N':
                    info("Nenhuma alteração feita no título.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{add_title}", no título. \n Tente novamente entre "S" ou "N".""")
        return data
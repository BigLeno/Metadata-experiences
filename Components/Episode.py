
from re import search, DOTALL
from logging import info, error

class Episode:
    """Classe responsável por adicionar o episódio ao arquivo XML."""

    def __init__(self):
        """Classe responsável por adicionar o episódio ao arquivo XML."""
        pass

    def handle_existing_episode(self, data):
        match_episode = search(r'<episodedetails>.*?<episode>(.*?)</episode>.*?</episodedetails>', data, DOTALL)
        if match_episode:
            episode_old = match_episode.group(1)
            change = self.logger.formatted_input(f"O episódio atual é: {episode_old}. Deseja alterar? (S/N): ")
            if change.upper() == 'S':
                episode_new = self.logger.formatted_input("Por favor, insira o novo episódio: ")
                data = data.replace(f'<episode>{episode_old}</episode>', f'<episode>{episode_new}</episode>')
            elif change.upper() == 'N':
                info("Nenhuma alteração feita no episódio.")
            else:
                error(f"""Erro ao indicar a mudança desejada: "{change}", no episódio. \n Tente novamente entre "S" ou "N".""")
        return data

    def handle_no_episode(self, data):
        lines = data.split('\n')
        if '<episodedetails>' not in data and '<episode>' not in data and '</episode>' not in data:
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
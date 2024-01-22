
from re import search
from logging import info, error

class Poster:
    """Classe responsável por adicionar o poster ao arquivo XML."""

    def __init__(self):
        """Classe responsável por adicionar o poster ao arquivo XML."""
        pass

    def handle_empty_art_tag(self, data, poster_path):
        """Adiciona o poster ao arquivo XML."""
        if '<art />' in data:
            error("""A tag <art /> não está formatada corretamente.""")
            poster_new = f"<art><poster>{poster_path}</poster></art>"
            data = data.replace('<art />', poster_new)
        return data

    def handle_existing_poster_tag(self, data, poster_path):
        """Adiciona o poster ao arquivo XML."""
        if '<poster>' in data and '</poster>' in data:
            poster_old = search('<poster>(.*?)</poster>', data).group()
            poster_new = f"<poster>{poster_path}</poster>"
            data = data.replace(poster_old, poster_new)
        return data

    def handle_no_art_tag(self, data, poster_path):
        """Adiciona o poster ao arquivo XML."""
        if '<art />' not in data and '<poster>' not in data and '</poster>' not in data:
            info("""A tag <art /> não existe.""")
            poster_new = f"  <art><poster>{poster_path}</poster></art>"
            lines = data.split('\n')
            lines.insert(9, poster_new)
            data = '\n'.join(lines)
        return data
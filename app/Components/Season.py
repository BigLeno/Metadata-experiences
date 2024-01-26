
from re import search, DOTALL

class Season:
    """Classe responsável por adicionar a temporada ao arquivo XML."""
    def __init__(self) -> None:
        """Classe responsável por adicionar a temporada ao arquivo XML."""
        pass

    def handle_existing_season(self, data, season):
        match_season = search(r'<episodedetails>.*?<season>(.*?)</season>.*?</episodedetails>', data, DOTALL)
        if match_season:
            season_old = match_season.group(1)
            data = data.replace(f'<season>{season_old}</season>', f'<season>{season}</season>')
        return data

    def handle_no_season(self, data, season):
        lines = data.split('\n')
        if '<episodedetails>' in data and '<season>' not in data and '</season>' not in data:
            for i, line in enumerate(lines):
                if '<showtitle>' in line:
                    lines.insert(i+1, f'  <season>{season}</season>')
                    data = '\n'.join(lines)
                    break
        return data
import logging, datetime, pytz, re, os


def create_log() -> None:
    """Função que define e orienta o timezone e o formato do logger"""
    tz = pytz.timezone('America/Sao_Paulo')
    format='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')
    logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=tz).timetuple()

def formatted_input(prompt:str) -> str:
    """Solicita ao usuário que indique a mudança que deseja fazer, formatando a mensagem de maneira semelhante à biblioteca logging"""
    tz = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M:%S')
    return input(f"{current_time} - INPUT - {prompt}")

def open_archive(directory:str, archive:str) -> str:
    """Tenta abrir o arquivo"""
    try:
        with open(f'{directory}/{archive}', 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        return  f'Erro ao ler o arquivo: {archive}'

def write_archive(directory:str, archive:str, data:str) -> str:
    """Tenta escrever o arquivo"""
    try:
        with open(f'{directory}/{archive}', 'w', encoding='utf-8') as file:
            file.write(data)
        return data
    except Exception as e:
        logging.error(f"Erro ao escrever o arquivo: {archive}")
        return  data

def get_files_from_directory(directory:str, extension:str = '.nfo') -> list:
    """Método que recebe um diretório e retorna uma lista de arquivos"""

    try:
        files = [file for file in os.listdir(directory) if file.endswith(extension)]
        return files
    except Exception as e:
        logging.error(f"Erro ao listar arquivos no diretório: {e}")
        return []
    
def disable_subtitles(data:str) -> str:
    """Método que desabilita todas as legendas."""
    subtitles = re.findall(r'<subtitle>.*?</subtitle>', data, flags=re.DOTALL)
    for subtitle in subtitles:
        new_subtitle = re.sub(r'<default>True</default>', '<default>False</default>', subtitle)
        data = data.replace(subtitle, new_subtitle)
    
    logging.info(f"""Todas as legendas foram desabilitadas.""")

    return data

def enable_portuguese_subtitles(data:str) -> str:
    """Método que habilita todas as legendas em português."""
    subtitles = re.findall(r'<subtitle>.*?</subtitle>', data, flags=re.DOTALL)
    portuguese_enabled, english_enabled = False, False
    for subtitle in subtitles:
        if '<language>por</language>' in subtitle:
            new_subtitle = re.sub(r'<default>False</default>', '<default>True</default>', subtitle)
            data = data.replace(subtitle, new_subtitle)
            logging.info("""Legenda em português habilitada""")
            portuguese_enabled = True
        if not portuguese_enabled:
            if '<language>eng</language>' in subtitle:
                new_subtitle = re.sub(r'<default>False</default>', '<default>True</default>', subtitle)
                data = data.replace(subtitle, new_subtitle)
                logging.info("""Nenhuma legenda em português encontrada. Legenda em inglês habilitada.""") 
                english_enabled = True
    
    if not portuguese_enabled and not english_enabled:
        logging.info("""Nenhuma legenda encontrada. Nenhuma legenda habilitada.""")
        return ''

    return data

def handle_poster_change(data, poster_path):
    if '<art />' in data:
        logging.error("""A tag <art /> não está formatada corretamente.""")
        poster_new = f"<art><poster>{poster_path}</poster></art>"
        data = data.replace('<art />', poster_new)
    elif '<poster>' in data and '</poster>' in data:
        poster_old = re.search('<poster>(.*?)</poster>', data).group()
        poster_new = f"<poster>{poster_path}</poster>"
        data = data.replace(poster_old, poster_new)
    else:
        logging.info("""A tag <art /> não existe.""")
        poster_new = f"  <art><poster>{poster_path}</poster></art>"
        lines = data.split('\n')
        lines.insert(9, poster_new)
        data = '\n'.join(lines)
    return data

def handle_plot_change(data) -> str:
    """Manipula a mudança na tag <plot>."""
    lines = data.split('\n')
    match_plot = re.search(r'<plot>(.*?)</plot>', data)
    match_bad_plot = re.search(r'<plot />', data)

    if match_plot:
        plot_old = match_plot.group(1)
        change = formatted_input(f"""A sinopse atual é: \n\t-->  "{plot_old}". \n\tDeseja alterar? (S/N): """)
        if change.upper() == 'S':
            plot_new = formatted_input("Por favor, insira a nova sinopse: ")
            data = data.replace(plot_old, plot_new)
            logging.info("Sinopse Alterada.")
        elif change.upper() == 'N':
            logging.info("Nenhuma alteração feita na sinopse.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{change}", na sinopse. \n Tente novamente entre "S" ou "N".""")
    elif match_bad_plot:
        change_plot = formatted_input("A tag <plot> está mal formatada. Deseja alterar a sinopse? (S/N): ")
        if change_plot.upper() == 'S':
            plot_new = formatted_input("Por favor, insira a sinopse: ")
            data = data.replace('<plot />', f'<plot>{plot_new}</plot>')
            logging.info("Sinopse Alterada.")
        elif change_plot.upper() == 'N':
            logging.info("Nenhuma alteração feita na sinopse.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{change_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")

    else:
        add_plot = formatted_input("A tag <plot> não existe. Deseja adicionar uma sinopse? (S/N): ")
        if add_plot.upper() == 'S':
            plot_new = formatted_input("Por favor, insira a sinopse: ")
            lines.insert(2, f'  <plot>{plot_new}</plot>')
            data = '\n'.join(lines)
        elif add_plot.upper() == 'N':
            logging.info("Nenhuma alteração feita na sinopse.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{add_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")

    return data

def handle_language_change(archive:str, data:str) -> str:
    """Manipula a mudança na tag <language>."""
    lines = data.split('\n')
    match_language = re.search(r'<episodedetails>.*?<streamdetails>.*?<audio>.*?<language>(.*?)</language>.*?</audio>.*?</streamdetails>.*?</episodedetails>', data, re.DOTALL)

    if match_language:
        language_old = match_language.group(1)
        change = formatted_input(f"A linguagem atual té: \n\t-->    {language_old}. \n\tDeseja alterar? (S/N): ")
        if change.upper() == 'S':
            language_new = formatted_input("""Por favor, insira a nova linguagem \n\t\t\tExemplo: \n\t\t\t    por, eng, jpn     : """)
            data = data.replace(language_old, language_new)
            logging.info("Linguagem Alterada.")
        elif change.upper() == 'N':
            logging.info("Nenhuma alteração feita na linguagem.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{change}", na linguagem. \n Tente novamente entre "S" ou "N".""")
    else:
        add_language = formatted_input("A tag <language> não existe. Deseja adicionar uma linguagem? (S/N): ")
        if add_language.upper() == 'S':
            language_new = formatted_input("Por favor, insira a linguagem: ")
            lines.insert(2, f'<episodedetails><streamdetails><audio><language>{language_new}</language></audio></streamdetails></episodedetails>')
            data = '\n'.join(lines)
        elif add_language.upper() == 'N':
            logging.info("Nenhuma alteração feita na linguagem.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{add_language}", na linguagem. \n Tente novamente entre "S" ou "N".""")

    return data

def handle_episode_change(data):
    """Manipula a mudança na tag <episode>."""
    lines = data.split('\n')
    match_episode = re.search(r'<episodedetails>.*?<episode>(.*?)</episode>.*?</episodedetails>', data, re.DOTALL)

    if match_episode:
        episode_old = match_episode.group(1)
        change = formatted_input(f"O episódio atual é: {episode_old}. Deseja alterar? (S/N): ")
        if change.upper() == 'S':
            episode_new = formatted_input("Por favor, insira o novo episódio: ")
            data = data.replace(episode_old, episode_new)
        elif change.upper() == 'N':
            logging.info("Nenhuma alteração feita no episódio.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{change}", no episódio. \n Tente novamente entre "S" ou "N".""")

    else:
        add_episode = formatted_input("A tag <episode> não existe. Deseja adicionar um episódio? (S/N): ")
        if add_episode.upper() == 'S':
            episode_new = formatted_input("Por favor, insira o episódio: ")
            for i, line in enumerate(lines):
                if '<showtitle>' in line:
                    lines.insert(i+1, f'  <episode>{episode_new}</episode>')
                    data = '\n'.join(lines)
                    break
        elif add_episode.upper() == 'N':
            logging.info("Nenhuma alteração feita no episódio.")
        else:
            logging.error(f"""Erro ao indicar a mudança desejada: "{add_episode}", no episódio. \n Tente novamente entre "S" ou "N".""")

    return data

def handle_season_change(data, season):
    """Manipula a mudança na tag <season>."""
    lines = data.split('\n')
    match_season = re.search(r'<episodedetails>.*?<season>(.*?)</season>.*?</episodedetails>', data, re.DOTALL)

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
    

def get_and_modify():
    """Método que vai receber o arquivo e modificar o texto"""
    create_log()
    logging.info("""Iniciando o sistema de modificação de metadados....""")
    file_or_directory = formatted_input("Você deseja processar um diretório ou um arquivo único? (D/A): ")
    if file_or_directory.upper() == 'D':
        directory = formatted_input("Por favor, insira o nome do diretório: ")
        files = get_files_from_directory(directory)
    elif file_or_directory.upper() == 'A':
        directory = formatted_input("Por favor, insira o nome do diretório: ")
        file = formatted_input("Por favor, insira o nome do arquivo: ")
        files = [file]
    else:
        logging.error(f"""Erro ao indicar a escolha desejada: "{file_or_directory}". \n Tente novamente entre "D" ou "A".""")
        return

    poster_path = formatted_input("Por favor, insira o caminho do poster: ")
    season = formatted_input("Por favor, insira a temporada: ")
    subtitle_option = formatted_input("O arquivo é para legendado ou dublado? (L/D): ")

    for file in files:
        change_file = formatted_input(f"Deseja alterar o arquivo {file}? (S/N): ")
        if change_file.upper() == 'S':
            data = open_archive(directory, file)
            data = handle_poster_change(data, poster_path)
            data = handle_plot_change(data)
            data = handle_language_change(file, data)
            data = handle_episode_change(data)
            data = handle_season_change(data, season)
            if subtitle_option.upper() == 'L':
                data = enable_portuguese_subtitles(data)
            elif subtitle_option.upper() == 'D':
                data = disable_subtitles(data)
            write_archive(directory, file, data)

        
if __name__ == '__main__':
    try:
        get_and_modify()
    except KeyboardInterrupt:
        print("")
        logging.info("Programa encerrado pelo usuário.")
        exit(-1)


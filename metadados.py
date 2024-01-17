import logging, datetime, pytz, re, os

pattern_language = r"<audio>.*?<language>(.*?)</language>.*?</audio>"
pattern_poster = r"<art>.*?<poster>(.*?)</poster>.*?</art>"

def create_log() -> None:
    """Função que define e orienta o timezone e o formato do logger"""
    tz = pytz.timezone('America/Sao_Paulo')
    format='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')
    logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=tz).timetuple()

def formatted_input(prompt):
    """Solicita ao usuário que indique a mudança que deseja fazer, formatando a mensagem de maneira semelhante à biblioteca logging"""
    tz = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M:%S')
    return input(f"{current_time} - INPUT - {prompt}")

def open_archive(directory:str, archive:str):
    """Tenta abrir o arquivo"""
    try:
        with open(f'{directory}/{archive}', 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        return  f'Erro ao ler o arquivo: {archive}'

def write_archive(directory:str, archive:str, data):
    """Tenta escrever o arquivo"""
    try:
        with open(f'{directory}/{archive}', 'w', encoding='utf-8') as file:
            file.write(data)
        return data
    except Exception as e:
        logging.error(f"Erro ao escrever o arquivo: {e}")
        return  f'Erro ao escrever o arquivo: {archive}'

def get_files_from_directory(directory:str, extension:str = '.nfo'):
    """Método que recebe um diretório e retorna uma lista de arquivos"""

    try:
        files = [file for file in os.listdir(directory) if file.endswith(extension)]
        return files
    except Exception as e:
        logging.error(f"Erro ao listar arquivos no diretório: {e}")
        return f'Erro ao listar arquivos no diretório {directory}'
    
def get_change(directory:str, archive:str):
    """Solicita ao usuário que indique a mudança que deseja fazer"""
    change = formatted_input(f"""Indique a mudança que deseja fazer em: \n\t--> "{archive}"\n(Digite "D" para mudar de Legendado para Dublado ou "L" para mudar de Dublado para Legendado): """)
    data = open_archive(directory, archive)
    match_poster = get_match(pattern_poster, data)
    match_language = get_match(pattern_language, data)

    if change.upper() == 'L':
        poster_old = match_poster
        language_old = match_language
        logging.info(f"""O conteúdo da tag "poster" era: \n\t--> "{poster_old}".""")
        poster_new = poster_old.replace("Dublado", "Legendado")
        logging.info(f"""O conteúdo da tag "poster" agora é \n\t--> "{poster_new}".""")
        data = data.replace(poster_old, poster_new)
        logging.info(f"""O conteúdo da tag "language" era: \n\t--> "{language_old}".""")
        language_new = language_old.replace(language_old, "jpn")
        logging.info(f"""O conteúdo da tag "language" agora é \n\t--> "{language_new}".""")
        data = data.replace(language_old, language_new)
        write_archive(directory, archive, data)

    elif change.upper() == 'D':
        poster_old = match_poster
        language_old = match_language
        logging.info(f"""O conteúdo da tag "poster" era: \n\t--> "{poster_old}".""")
        poster_new = poster_old.replace("Legendado","Dublado")
        logging.info(f"""O conteúdo da tag "poster" agora é \n\t--> "{poster_new}".""")
        data = data.replace(poster_old, poster_new)
        logging.info(f"""O conteúdo da tag "language" era: \n\t--> "{language_old}".""")
        language_new = language_old.replace(language_old, "por")
        logging.info(f"""O conteúdo da tag "language" agora é \n\t--> "{language_new}".""")
        data = data.replace(language_old, language_new)
        write_archive(directory, archive, data)
    else:
        logging.error(f"Erro ao indicar a mudança desejada: {change}, no arquivo {archive}")
        return f'Erro ao indicar a mudança desejada: {change}, no arquivo {archive}'
    
def get_match(pattern:str, data):
    """Método que faz a comparação e encontra o match"""
    try:
        match = re.search(pattern, data, re.DOTALL)
        return match.group(1)
    except Exception as e:
        logging.error(f"Erro ao encontrar o match: {e}")
        return f'Erro ao encontrar o match: {pattern} em {data}'

def get_and_modify(archive:str):
    """Método que vai receber o arquivo e modificar o texto"""


archive = 'Data\sla.nfo'
# archive = 'Data\Black Clover Season 1 Episode 161 Português (Brasil).nfo'

create_log()
teste = get_files_from_directory("Data")
print(teste)
for i in teste:
    get_change('Data', i)

# try:
#     with open(archive, 'r', encoding='utf-8') as file:
#         data = file.read()

#     # Define a regular expression pattern for language
#     pattern_language = r"<audio>.*?<language>(.*?)</language>.*?</audio>"

#     # Search for the language pattern
#     match_language = re.search(pattern_language, data, re.DOTALL)

#     if match_language:
#         language = match_language.group(1)
#         if language != 'por':
#             # Define a regular expression pattern for poster
#             pattern_poster = r"<art>.*?<poster>(.*?)</poster>.*?</art>"
            
#             # Search for the poster pattern
#             match_poster = re.search(pattern_poster, data, re.DOTALL)

#             if match_poster:
#                 poster_old = match_poster.group(1)
#                 print(f"O conteúdo da tag 'poster' era '{poster_old}'.")
#                 # Substitui a tag 'poster' pela nova imagem
#                 # poster_new = poster_old.replace("Legendado", "Dublado")
#                 poster_new = poster_old.replace("Dublado", "Legendado")
#                 print(f"O conteúdo da tag 'poster' agora é '{poster_new}'.")
                
#                 # Replace the old poster content with the new one in the data
#                 data = data.replace(poster_old, poster_new)
#             else:
#                 print("Tag 'poster' não encontrada.")
#         else:
#             print(f"A linguagem é '{language}'.")
#     else:
#         print("Tag 'audio' não encontrada.")
    
#     # Write the changes back to the file
#     with open(archive, 'w', encoding='utf-8') as file:
#         file.write(data)

# except Exception as e:
#     print(f"Erro ao ler o arquivo: {e}")
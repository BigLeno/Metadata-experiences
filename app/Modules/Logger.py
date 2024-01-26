
from logging import basicConfig, Formatter, INFO
from datetime import datetime
from pytz import timezone

class Logger:
    """Classe que define e orienta o timezone e o formato do logger"""
    def __init__(self) -> None:
        """Classe que define e orienta o timezone e o formato do logger"""
        self.tz = timezone('America/Sao_Paulo')
        self.datefmt = '%d/%m/%Y %H:%M:%S'
        self.current_time = datetime.now(tz=self.tz)
        self.create_log()

    def create_log(self) -> None:
        """Função que define e orienta o timezone e o formato do logger"""
        format='%(asctime)s - %(levelname)s - %(message)s'
        basicConfig(format=format, level=INFO, datefmt=self.datefmt)
        Formatter.converter = lambda *args: self.current_time.timetuple()

    def formatted_input(self, prompt:str) -> str:
        """Solicita ao usuário que indique a mudança que deseja fazer, formatando a mensagem de maneira semelhante à biblioteca logging"""
        current_time = self.current_time.strftime(self.datefmt)
        return input(f"{current_time} - INPUT - {prompt}")
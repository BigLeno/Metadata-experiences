
from re import findall, sub, DOTALL
from logging import info


    

class Subtitles:
    
    """Módulo responsável pelas legendas"""

    def __init__(self) -> None:
        """Módulo responsável pelas legendas"""
        pass

    def disable_subtitles(self,data:str) -> str:
        """Método que desabilita todas as legendas."""
        subtitles = findall(r'<subtitle>.*?</subtitle>', data, flags=DOTALL)
        for subtitle in subtitles:
            new_subtitle = sub(r'<default>True</default>', '<default>False</default>', subtitle)
            data = data.replace(subtitle, new_subtitle)
        
        info(f"""Todas as legendas foram desabilitadas.""")

        return data

    def enable_portuguese_subtitles(self, data:str) -> str:
        """Método que habilita todas as legendas em português."""
        subtitles = findall(r'<subtitle>.*?</subtitle>', data, flags=DOTALL)
        portuguese_enabled, english_enabled = False, False
        for subtitle in subtitles:
            if '<language>por</language>' in subtitle:
                new_subtitle = sub(r'<default>False</default>', '<default>True</default>', subtitle)
                data = data.replace(subtitle, new_subtitle)
                info("""Legenda em português habilitada""")
                portuguese_enabled = True

        if not portuguese_enabled:
            for subtitle in subtitles:
                if '<language>eng</language>' in subtitle:
                    new_subtitle = sub(r'<default>False</default>', '<default>True</default>', subtitle)
                    data = data.replace(subtitle, new_subtitle)
                    info("""Nenhuma legenda em português encontrada. Legenda em inglês habilitada.""") 
                    english_enabled = True
                    break
        
        if not portuguese_enabled and not english_enabled:
            info("""Nenhuma legenda encontrada. Nenhuma legenda habilitada.""")

        return data
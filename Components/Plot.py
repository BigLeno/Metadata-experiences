
from re import search
from logging import info, error

class Plot:
    """Classe responsável por adicionar a sinopse ao arquivo XML."""

    def __init__(self):
        """Classe responsável por adicionar a sinopse ao arquivo XML."""
        pass

    def handle_existing_plot(self, data):
        match_plot = search(r'<plot>(.*?)</plot>', data)
        if match_plot:
            plot_old = match_plot.group(1)
            while True:
                change = self.logger.formatted_input(f"""A sinopse atual é: \n\t-->  "{plot_old}". \n\tDeseja alterar? (S/N): """)
                if change.upper() == 'S':
                    plot_new = self.logger.formatted_input("Por favor, insira a nova sinopse: ")
                    data = data.replace(plot_old, plot_new)
                    info("Sinopse Alterada.")
                    break
                elif change.upper() == 'N':
                    info("Nenhuma alteração feita na sinopse.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{change}", na sinopse. \n Tente novamente entre "S" ou "N".""")
        return data

    def handle_bad_plot(self, data):
        match_bad_plot = search(r'<plot />', data)
        if match_bad_plot:
            while True:
                change_plot = self.logger.formatted_input("A tag <plot> está mal formatada. Deseja alterar a sinopse? (S/N): ")
                if change_plot.upper() == 'S':
                    plot_new = self.logger.formatted_input("Por favor, insira a sinopse: ")
                    data = data.replace('<plot />', f'<plot>{plot_new}</plot>')
                    info("Sinopse Alterada.")
                    break
                elif change_plot.upper() == 'N':
                    info("Nenhuma alteração feita na sinopse.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{change_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")
        return data

    def handle_no_plot(self, data):
        lines = data.split('\n')
        if '<plot>' not in data and '</plot>' not in data and '<plot />' not in data:
            while True:
                add_plot = self.logger.formatted_input("A tag <plot> não existe. Deseja adicionar uma sinopse? (S/N): ")
                if add_plot.upper() == 'S':
                    plot_new = self.logger.formatted_input("Por favor, insira a sinopse: ")
                    lines.insert(2, f'  <plot>{plot_new}</plot>')
                    data = '\n'.join(lines)
                    break
                elif add_plot.upper() == 'N':
                    info("Nenhuma alteração feita na sinopse.")
                    break
                else:
                    error(f"""Erro ao indicar a mudança desejada: "{add_plot}", na sinopse. \n Tente novamente entre "S" ou "N".""")
        return data
from module import UseerBOT
from utils import PriceComparator

if __name__ == '__main__':
    telegram_bot = UseerBOT()
    telegram_bot.inicio()
    telegram_bot.definindo_regras()
    telegram_bot.filtragens()
    telegram_bot.start()

    # Verifica se a opção de consulta deve ser executada
    should_run_consulta = True
    if should_run_consulta:
        comparator = PriceComparator()
        comparator.compare_prices()
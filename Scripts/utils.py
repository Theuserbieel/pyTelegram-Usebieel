import requests
import bs4
import regex as re
import json
import asyncio

class PriceComparator:
    def __init__(self):
        self.load_config()

    def load_config(self):
        config_path = '/home/bieel/Área de Trabalho/ParallelBot/Scripts/json/config.json'
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.product_url = config['product_url']
            self.last_price = config['last_price']
            self.interval_hours = config['interval_hours']

    def update_last_price(self, new_price):
        config_path = '/home/bieel/Área de Trabalho/ParallelBot/Scripts/json/config.json'
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            config['last_price'] = new_price

        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

    async def compare_prices(self):
        while True:
            req = requests.get(self.product_url)

            html = bs4.BeautifulSoup(req.content, 'html.parser')
            price_element = html.find(class_='finalPrice')
            price_content = price_element.string

            real, cents = map(lambda value: re.sub(r'[^0-9]', "", value), price_content.split(','))
            price = float('.'.join([real, cents]))

            if self.last_price and price < self.last_price:
                print('O preço diminuiu!!')
            
            elif self.last_price and price == self.last_price:
                print("O preço está o mesmo!!")
            
            self.update_last_price(price)
            await asyncio.sleep(60 * 60 * self.interval_hours)  # Use await para pausar assincronamente

async def main():
    comparator = PriceComparator()
    task = asyncio.create_task(comparator.compare_prices())  # Execute a função compare_prices em segundo plano
    await task  # Aguarde a tarefa

if __name__ == '__main__':
    asyncio.run(main())

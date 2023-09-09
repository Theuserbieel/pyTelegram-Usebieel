from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from utils import PriceComparator

class UseerBOT:
    def __init__(self):
        self.load_sensitive_info()

        # Instânciando o Bot em uma variável com as informações fornecidas e a pasta de sessões
        self.userBot = Client(
            "Userbieel_Bot",
            api_id=self.TELEGRAM_API_ID,
            api_hash=self.TELEGRAM_API_HASH,
            bot_token=self.TELEGRAM_BOT_TOKEN,
            workdir='/home/bieel/Área de Trabalho/ParallelBot/Scripts/telegram_Sessions'
        )
        self.comparator = PriceComparator()

    def load_sensitive_info(self):
        if not hasattr(self, 'TELEGRAM_API_ID'):
            load_dotenv(dotenv_path='/home/bieel/Área de Trabalho/ParallelBot/Scripts/env/Telegram_Info.env')
            self.TELEGRAM_API_ID = getenv('TELEGRAM_API_ID')
            self.TELEGRAM_API_HASH = getenv('TELEGRAM_API_HASH')
            self.TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
  
    def start(self):
    #Iniciando o Bot.    
        self.userBot.run()

       
    def inicio(self):
    #Definindo as mensagens iniciais do Bot.
        @self.userBot.on_message(filters.command('help') |filters.command('start'))
        async def initial_commands(client,message):
            await message.reply('**Bem-Vindo ao UseerBOT!!**\n'
                                'Use /start para iniciar o bot!\n'
                                'Use /menu para ver as opções!\n'
                                'Use /consulta para ver se houveram alterações de valores!\n'
                                'Use /criar para criar uma nova consulta de valores!\n'
                                'Para saber mais use /regras \n'
    
                               )
    #Criando a opção de consulta no bot interligando com o comparador de preços.
        @self.userBot.on_message(filters.command('consulta'))
        async def option_consulta(client, message):
            await self.consulta_precos(message)

        
    #Criando um menu de opções com as mensagens iniciais do Bot.
        @self.userBot.on_message(filters.command('menu'))
        async def initial_menu(client,message):
            opcoes = ReplyKeyboardMarkup(
                                [['/start'], ['/consulta'], ['/criar'], ['/regras']],
                                resize_keyboard=True)
            await message.reply(
                'Escolha uma opção!', 
                reply_markup=opcoes)

        
    def definindo_regras(self):
    #Iniciando um novo comando com as regras do bot.
        @self.userBot.on_message(filters.command('regras'))
        async def options(client,message):
            await message.reply('**Bem-vindo as Regras do UseerBOT!!**\n'
                                '-> `Não me mande áudios`, **eu odeio**\n'
                                '-> Não me mande fotos ou vídeos (**Não gosto de Nudes!**)\n'
                                '-> Meu processamento é lento então tenha paciência cmg :)\n'
                                '-> --Me faça sorrir me mande um sticker XD!!--\n'   
                                )

    def filtragens(self):
    #Iniciando um novo filtro com as regras do bot.
        @self.userBot.on_message(filters.sticker | filters.photo)
        async def my_handler(client, message):
            await message.reply('Ah não, espero que não sejam **nudes**...')

    #Iniciando um novo filtro com as regras do bot.
        @self.userBot.on_message(filters.audio | filters.voice)
        async def my_handler(client, message):
            await message.reply('Ah não, la vem o podcast...')

    #Iniciando um novo filtro com as regras do bot.
        @self.userBot.on_message(filters.document | filters.animation)
        async def my_handler(client, message):
            await message.reply('Espero que não sejam, virus...')

    async def consulta_precos(self,message):
        # Instânciando e executando o PriceComparator.
        comparator = PriceComparator()
        last_price = comparator.last_price
        comparator.compare_prices()

        new_price = comparator.last_price

        if new_price < last_price:
            reply_message = f'O PREÇO DIMINUIU!!\n Valor anterior: R${last_price:.2f} \n Valor atual: R${new_price:.2f}'
        else:
            reply_message = f'O PREÇO ESTÁ O MESMO!!\n Valor atual: R${new_price:.2f}'

    # Enviando a mensagem para o chat especificado.
        await message.reply_text('**Produto: Fonte ATX Fortrek Black Hawk 500W** \n' + reply_message)


if __name__ == '__main__':
    
    telegram_bot = UseerBOT()
    telegram_bot.inicio()
    telegram_bot.definindo_regras()
    telegram_bot.filtragens()
    telegram_bot.start()
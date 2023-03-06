import requests
from bs4 import BeautifulSoup
import re

from aiogram import Dispatcher,Bot,executor,types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from aiogram.dispatcher import FSMContext



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
token = '5997866840:AAEqO-Uke_D6JlyVtCdTaKHsnSpM3iwo56k'
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)






global tbase, tc
tbase = sqlite3.connect('user.db')
tc = tbase.cursor()
tbase.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY)')

tbase.commit()




class search_(StatesGroup):
    answer_ = State()
@dp.message_handler(commands=['start'])
async def strxdx(msg: types.Message):
    await msg.answer_animation(caption='Добро пожаловать', animation='https://simple-animation.ru/uploads/posts/2023-01/1674155919_gif-20.gif', reply_markup=wel())



    
    
    
    
    
    
    
    with tbase:
        tc.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)',(msg.from_user.id,))



def wel():
    x = ReplyKeyboardMarkup(resize_keyboard=True)

    x3 = KeyboardButton(text='Поиск')
    x5 = KeyboardButton(text='Инструкции')
    x33 = KeyboardButton(text='Подробнее')
    x555 = KeyboardButton(text='Топ')
    x.add(x3).row(x5,x33).row(x555)
    return x

@dp.message_handler(text='Инструкции')
async def instructi(msg: types.Message):
    await msg.answer(f'Для промотра потоков вам нужно установить [ТЫК](https://www.videolan.org/vlc/) ----- [ТЫК](https://www.mxplayer.in/)', parse_mode='markdown')


@dp.message_handler(text='Подробнее')
async def tices(msg: types.Message):

    await msg.answer('Тут информация (возможно ссылки на ваши каналы) - @log131')

@dp.message_handler(text='Топ')
async def top_(msg: types.Message):
    await msg.answer('Тут по желанию будут топ 99 фильмов')


@dp.message_handler(text='Поиск', state=None)
async def start_search(msg: types.Message, state: FSMContext):
    await search_.answer_.set()
    await msg.answer('Напишите Название Фильма : если не тот фильм добавьте в конец (год)')





@dp.message_handler(state=search_.answer_)
async def start_answer(msg: types.Message, state: FSMContext):
    params = {
    'do': 'search',
        }

    data_ = {
    'do': 'search',
    'subaction': 'search',
    'search_start': '1',
    'full_search': '0',
    'result_from': '1',
    'story': f'{msg.text}',
    }

    try:
        
        r = requests.post('https://kinokrad.cc/index.php?do=search', params=params, data=data_)
        s = BeautifulSoup(r.text, 'lxml')
        answers = s.find('div', class_='searchitem')
        hrefs = answers.find('a').get('href')
        x = requests.get(f'{hrefs}')
        s_finder = BeautifulSoup(x.text, 'lxml')
        titles = s_finder.find('div', class_='fulltext').text
        
        sendit = s_finder.find('div', class_='bigposter').find('img').get('src')
    
        series = s_finder.find('div', class_='boxfilm').find('script').text
        finds = re.findall(r'\[720p\](\S+)', series)
        if finds:
            keysx = InlineKeyboardMarkup()
            keysx.add(InlineKeyboardButton(text='Смотреть', url=finds[0].replace('"', ''), callback_data=''))
        await msg.answer(titles)
        await msg.answer_photo(sendit, reply_markup=keysx)
        await state.finish()
        
    except:
        await state.finish()
        await msg.answer('Такого нет')

    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = 'top secret'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(text='Calories')
async def set_sex(message):
    await message.answer('Введите свой пол (м/ж):')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def set_age(message, state):
    await state.update_data(sex=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['sex'] == 'ж':
        calorie_norm = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        await message.answer(f'Ваша норма - {calorie_norm} калорий в сутки')
    elif data['sex'] == 'м':
        calorie_norm = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        await message.answer(f'Ваша норма - {calorie_norm} калорий в сутки')
    else:
        await message.answer('Данные введены неверно. Попробуйте снова.')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Этот бот умеет рассчитывать калории для оптимального похудения или сохранения'
                         'нормального веса по формуле Миффлина-Сан Жеора.\n'
                         'Для расчета нормы калорий введите "Calories".')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

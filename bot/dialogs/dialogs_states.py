from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    main = State()


class ProductsListSG(StatesGroup):
    all = State()
    down = State()
    up = State()


class ProductSG(StatesGroup):
    add = State()


class ProductViewSG(StatesGroup):
    view = State()
    error = State()

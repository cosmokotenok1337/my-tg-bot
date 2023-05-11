"""Aiogram dialog StatesGroup's """

from aiogram.fsm.state import StatesGroup, State


class ClientSG(StatesGroup):
    """Client"""

    start = State()


class BotServiceOfferSG(StatesGroup):
    """Bot service offer"""

    set_title = State()
    set_description = State()
    offer_created = State()


class AdminServicesSG(StatesGroup):
    """Admin-side bot services list"""

    services_list = State()


class AdminServiceSG(StatesGroup):
    service_details = State()


class AdminSG(StatesGroup):
    """Admin-panel"""

    admin = State()

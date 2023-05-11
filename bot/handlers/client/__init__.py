from aiogram import Dispatcher
from aiogram.filters import Command

from .client import start, start_dialog
from .botservice_offer import botservice_offer_dialog

from aiogram_dialog import DialogRegistry


def register_handlers(dp: Dispatcher):
    """Register all client-side handlers"""

    dp.message.register(start, Command(commands="start"))


def register_dialogs(registry: DialogRegistry):
    registry.register(start_dialog)
    registry.register(botservice_offer_dialog)

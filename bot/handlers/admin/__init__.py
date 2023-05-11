from aiogram import Dispatcher
from aiogram.filters import Command

from .admin import admin_dialog, admin
from .bot_services import services_dialog
from .service_details import service_details_dialog

from aiogram_dialog import DialogRegistry

from .admin_filter import IsAdminFilter


def register_handlers(dp: Dispatcher):
    """Register all admin-side handlers"""

    dp.message.register(admin, Command(commands="admin"), IsAdminFilter())


def register_dialogs(registry: DialogRegistry):
    registry.register(admin_dialog)
    registry.register(services_dialog)
    registry.register(service_details_dialog)

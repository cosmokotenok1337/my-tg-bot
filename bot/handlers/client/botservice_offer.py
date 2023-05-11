"""Service order create client-side handlers"""
import logging
from typing import Any

from pydantic import ValidationError

from aiogram import types, Bot

from aiogram_dialog import DialogManager, Window, Dialog

from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from dialog.dialog_state import BotServiceOfferSG

from db.services.botservice import create_service

from schemas.client import BotServiceModel

from sqlalchemy.exc import DBAPIError

from config_loader import Config

offer_created_window = Window(
    Const("Заказ создан, ожидайте, c вами свяжутся в течении 30 минут."),
    Cancel(Const("Назад")),
    state=BotServiceOfferSG.offer_created,
)


async def pm_admins(config: Config) -> None:
    for admin in config.bot.admins:
        bot: Bot = Bot.get_current()

        await bot.send_message(admin, "Новый заказ!")


async def set_description(
    message: types.Message,
    widget: Any,
    manager: DialogManager,
    input: str,
):
    """Set description and create offer"""

    manager.dialog_data["description"] = input
    manager.dialog_data["user_id"] = message.from_user.id

    config: Config = manager.middleware_data.get("config")

    db_session = manager.middleware_data.get("db_session")

    try:
        service = BotServiceModel(**manager.dialog_data)
        await create_service(
            db_session,
            service,
        )

        await pm_admins(config)

        await manager.switch_to(BotServiceOfferSG.offer_created)
    except (DBAPIError, ValidationError) as exc:
        logging.ERROR(exc)
        await message.answer("Что то пошло не так..")
        await manager.done()


set_description_window = Window(
    Const("Полностью опишите техническое задание."),
    Cancel(Const("Отмена")),
    TextInput("botservicedescinp", str, on_success=set_description),
    state=BotServiceOfferSG.set_description,
)


async def set_title(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set title"""

    manager.dialog_data["title"] = input

    await manager.switch_to(BotServiceOfferSG.set_description)


set_title_window = Window(
    Const("Кратко опишите какой бот вам нужен, не более 50 символов."),
    Cancel(Const("Отмена")),
    TextInput("botservicetitleinp", str, on_success=set_title),
    state=BotServiceOfferSG.set_title,
)

botservice_offer_dialog = Dialog(
    set_title_window,
    set_description_window,
    offer_created_window,
)

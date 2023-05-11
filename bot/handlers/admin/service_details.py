"""Admin-side service details handlers"""
import logging

from aiogram import Bot, types

from typing import Any

from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import AdminServiceSG

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from db.services.botservice import get_bot_service, delete_bot_service

from ..utils import get_user_username


async def delete_service(
    call: types.CallbackQuery, widget: Any, manager: DialogManager
):
    """Delete service"""

    try:
        db_session: Session = manager.middleware_data.get("db_session")
        service_id: int = manager.start_data.get("service_id")

        await delete_bot_service(db_session, service_id)

        await call.answer("Успешно удалено!")
    except DBAPIError as exc:
        logging.ERROR(exc)
        await call.answer("Произошла ошибка!")
    finally:
        await manager.done()


async def get_service_data(
    db_session: Session,
    dialog_manager: DialogManager,
    bot: Bot,
    **kwargs,
):
    """Order details window data getter"""

    service_id: int = dialog_manager.start_data.get("service_id")

    service = await get_bot_service(db_session, service_id)
    service_customer = await get_user_username(service.user_id, bot)

    return {
        "service_id": service.id,
        "service_customer": service_customer,
        "service_title": service.title,
        "service_description": service.description,
    }


service_details_window = Window(
    Format("Информация о заказе\n"),
    Format("Идентификатор: {service_id}"),
    Format("Заказчик: {service_customer}"),
    Format('Название: "{service_title}"'),
    Format(
        "Описание бота:\n{service_description}",
        when="service_description",
    ),
    Button(Const("Удалить"), id="deleteservice", on_click=delete_service),
    Cancel(Const("Назад")),
    state=AdminServiceSG.service_details,
    getter=get_service_data,
)

service_details_dialog = Dialog(service_details_window)

"""Admin-side services handlers"""

import operator

from typing import Any

from aiogram import Bot, types
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import AdminServicesSG, AdminServiceSG

from sqlalchemy.orm import Session

from db.services.botservice import get_bot_services

from ..utils import get_user_username


async def get_service_details(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, service_id: str
):
    """Get order details"""

    await manager.start(AdminServiceSG.service_details, {"service_id": int(service_id)})


async def get_services_data(db_session: Session, bot: Bot, **kwargs):
    """Bot services data getter"""

    services = [
        (item.id, item.title, await get_user_username(item.user_id, bot))
        for item in await get_bot_services(db_session)
    ]

    return {
        "services": services,
        "count": len(services),
    }


services_window = Window(
    Const("Заказы:"),
    Cancel(Const("Назад")),
    ScrollingGroup(
        Select(
            Format("{item[1]} от {item[2]}"),
            id="botserviceselsel",
            item_id_getter=operator.itemgetter(0),
            items="services",
            on_click=get_service_details,
        ),
        width=2,
        height=4,
        id="admservicessel",
    ),
    state=AdminServicesSG.services_list,
    getter=get_services_data,
)

services_dialog = Dialog(services_window)

"""Admin-side main handlers"""

from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from dialog.dialog_state import AdminSG, AdminServicesSG

from sqlalchemy.orm import Session

admin_window = Window(
    Const("🔥 Хозяин, я к вашим услугам. 🔥"),
    Start(
        Const("🤖 Заказы ботов"),
        id="adminpanelbotservices",
        state=AdminServicesSG.services_list,
    ),
    state=AdminSG.admin,
)


async def admin(
    message: types.Message, dialog_manager: DialogManager, db_session: Session
):
    """
    This handler will be called when user sends `/admin` command

    Admin main menu.
    """

    await dialog_manager.start(AdminSG.admin, mode=StartMode.RESET_STACK)


admin_dialog = Dialog(admin_window)

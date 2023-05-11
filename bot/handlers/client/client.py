"""Welcome"""

from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager, StartMode

from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import ClientSG, BotServiceOfferSG

from db.services.users import is_user_exists, create_user

from sqlalchemy.orm import Session

start_window = Window(
    Format(
        "⚡ Привет, это личный бот кота шредингера, тут ты можешь заказать его услуги! ⚡"
    ),
    Row(
        Start(
            Const("🤖 Заказать бота 🤖"),
            id="botservice_order",
            state=BotServiceOfferSG.set_title,
        ),
    ),
    state=ClientSG.start,
)


async def start(
    message: types.Message, dialog_manager: DialogManager, db_session: Session
):
    """
    This handler will be called when user sends `/start` command
    Main menu.
    """

    user_id = message.from_user.id

    is_user_register = await is_user_exists(db_session, user_id)

    if not is_user_register:
        await create_user(db_session, user_id=user_id)

    await dialog_manager.start(ClientSG.start, mode=StartMode.RESET_STACK)


start_dialog = Dialog(start_window)

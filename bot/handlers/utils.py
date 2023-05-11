from aiogram import Bot


async def get_user_username(user_id: int, bot: Bot) -> str:
    """Get user username by user id"""

    return f"@{(await bot.get_chat(user_id)).username}"

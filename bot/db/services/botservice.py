"""Services (queries) for the BotService model"""

from sqlalchemy.orm import Session

from db.models import BotService

from schemas.client import BotServiceModel

from sqlalchemy import select, delete


async def create_service(session: Session, service_obj: BotServiceModel) -> BotService:
    """Create the ServiceCategory instance"""

    service = BotService(
        title=service_obj.title,
        description=service_obj.description,
        user_id=service_obj.user_id,
    )

    session.add(service)

    await session.commit()

    return service


async def get_bot_services(session: Session) -> list[BotService]:
    """Get bot services"""

    q = select(BotService)
    res = await session.execute(q)

    return res.scalars().all()


async def get_bot_service(session: Session, service_id: int) -> BotService:
    """Get bot service"""

    q = select(BotService).where(BotService.id == service_id)
    res = await session.execute(q)

    return res.scalar()


async def delete_bot_service(session: Session, service_id: int) -> None:
    """Delete bot service"""

    q = delete(BotService).where(BotService.id == service_id)

    await session.execute(q)
    await session.commit()

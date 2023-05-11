"""Services (queries) for the User model"""

from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from db.models import User


async def is_user_exists(session: Session, user_id: int) -> bool:
    """Checks for the presence of a user with the passed id"""

    q = select(exists().where(User.id == user_id))
    res = await session.execute(q)
    return res.scalar()


async def create_user(session: Session, user_id: int) -> None:
    """Create the User instance"""

    user = User(id=user_id)
    session.add(user)
    await session.commit()


async def get_user(session: Session, user_id: int) -> User:
    """Get User instance"""

    q = select(User).where(User.id == user_id)
    res = await session.execute(q)

    return res.scalar()

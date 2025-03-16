from uuid import UUID
from sqlalchemy import UUID as UUID_sqlalchemy, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ================================================
# SQLAlchemy Model
# ================================================
class BaseModelDeclarative(DeclarativeBase):
    pass

class MemberModel(BaseModelDeclarative):
    __tablename__ = "members"

    id: Mapped[UUID] = mapped_column(UUID_sqlalchemy, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

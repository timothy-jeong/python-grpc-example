from uuid import UUID
from sqlalchemy import UUID as UUID_sqlalchemy, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ================================================
# SQLAlchemy Model
# ================================================
class BaseModelDeclarative(DeclarativeBase):
    pass

class BoardModel(BaseModelDeclarative):
    __tablename__ = "boards"

    id: Mapped[UUID] = mapped_column(UUID_sqlalchemy, primary_key=True)
    member_id: Mapped[UUID] = mapped_column(UUID_sqlalchemy)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

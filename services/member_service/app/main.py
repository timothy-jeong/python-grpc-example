from typing import Annotated
from uuid import UUID, uuid4
import json
from contextlib import asynccontextmanager

from sqlalchemy import select

from pydantic import BaseModel, Field
from fastapi import FastAPI, status, Path, Response, Depends, Body, HTTPException
from app.database.connection import get_db, engine, AsyncSession
from app.database.model import MemberModel, BaseModelDeclarative



# ================================================
# Pydantic Schema
# ================================================
class MemberSchema(BaseModel):
    member_id: UUID | None = Field(description="member id")
    member_name: str = Field(description="member name", max_length=20)


# ================================================
# lifespan for create table
# ================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModelDeclarative.metadata.create_all)

    yield

    # dispose resource
    await engine.dispose()

# ================================================
# API Route
# ================================================
app = FastAPI(lifespan=lifespan)

@app.post("/members", summary="create member", status_code=status.HTTP_201_CREATED)
async def create_user(
    request_body: Annotated[MemberSchema, Body(..., description="member info")],
    db: AsyncSession = Depends(get_db),
):
    member_id = uuid4()
    new_member = MemberModel(id=member_id, name=request_body.member_name)
    db.add(new_member)
    await db.commit()

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"member_id": str(new_member.id)}),
        media_type="application/json",
    )

@app.get("/members", summary="read all members", status_code=status.HTTP_200_OK, response_model=list[MemberSchema])
async def get_all_members(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MemberModel))
    members = result.scalars().all()
    return [MemberSchema(member_id=m.id, member_name=m.name) for m in members]


@app.delete("/members/{member_id}", summary="delete member", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(
    member_id: Annotated[UUID, Path(description="member id")],
    db: AsyncSession = Depends(get_db),
):
    member = await db.get(MemberModel, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    await db.delete(member)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

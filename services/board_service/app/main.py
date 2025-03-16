from typing import Annotated
from uuid import UUID, uuid4
import json
from contextlib import asynccontextmanager

from sqlalchemy import select

from pydantic import BaseModel, Field
from fastapi import FastAPI, status, Path, Response, Depends, Body, HTTPException
from app.database.connection import get_db, engine, AsyncSession
from app.database.model import BoardModel, BaseModelDeclarative
from app.grpc_client import MemberServiceClient

# ================================================
# Pydantic Schema
# ================================================
class BoardSchema(BaseModel):
    board_id: UUID | None = Field(description="member id")
    member_id: UUID = Field(description="writer id")
    member_name: str = Field(description="writer name")
    title: str = Field(...)
    content: str = Field(...)


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

@app.post("/boards", summary="create board", status_code=status.HTTP_201_CREATED)
async def create_board(
    request_body: Annotated[BoardSchema, Body(..., description="member info")],
    db: AsyncSession = Depends(get_db),
):
    board_id = uuid4()
    new_board = BoardModel(id=board_id, member_id=request_body.member_id, title=request_body.title, content=request_body.content)
    db.add(new_board)
    await db.commit()

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"board_id": str(new_board.id)}),
        media_type="application/json",
    )

@app.get("/boards", summary="read all boards", status_code=status.HTTP_200_OK, response_model=list[BoardSchema])
async def get_all_boards(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BoardModel))
    boards = result.scalars().all()
    response_items: list[BoardSchema] = []
    for board in boards:
        member_response: dict = await MemberServiceClient.get_member_by(str(board.member_id))
        response_items.append(BoardSchema(
            board_id=board.id,
            title=board.title,
            content=board.content,
            member_id=board.member_id,
            member_name=member_response.get("member_name", None),
        ))
    return response_items


@app.delete("/boards/{board_id}", summary="delete board", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: Annotated[UUID, Path(description="board id")],
    db: AsyncSession = Depends(get_db),
):
    board = await db.get(BoardModel, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    await db.delete(board)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

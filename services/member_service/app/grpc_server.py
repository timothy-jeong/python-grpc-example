import asyncio
import grpc
import uuid

from sqlalchemy import select

from app.pb import member_service_pb2_grpc
from app.pb.message import member_request_pb2, member_response_pb2
from app.pb.member_service_pb2_grpc import MemberServiceServicer
from app.database.connection import async_session, engine
from app.database.model import MemberModel, BaseModelDeclarative

class MemberServiceServicerImpl(MemberServiceServicer):
    async def GetMember(self, request: member_request_pb2.MemberRequest, context):
        async with async_session() as db:
            result = await db.execute(
                select(MemberModel).where(MemberModel.id == uuid.UUID(request.member_id))
            )
            member = result.scalars().first()

            if not member:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Member not found")
                return member_response_pb2.MemberResponse()

        return member_response_pb2.MemberResponse(
            member_id=str(member.id),
            member_name=member.name
        )

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModelDeclarative.metadata.create_all)

async def serve():
    await init_db()

    server = grpc.aio.server()
    member_service_pb2_grpc.add_MemberServiceServicer_to_server(MemberServiceServicerImpl(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())

from uuid import UUID

import grpc
from google.protobuf.json_format import MessageToDict

from app.pb import member_service_pb2_grpc
from app.pb.message import member_request_pb2

channel = grpc.aio.insecure_channel("member-service:50051")
stub = member_service_pb2_grpc.MemberServiceStub(channel)


class MemberServiceClient:
    @staticmethod
    async def get_member_by(member_id: UUID):
        member_response = await stub.GetMember(member_request_pb2.MemberRequest(member_id=str(member_id)))
        return MessageToDict(member_response, preserving_proto_field_name=True)
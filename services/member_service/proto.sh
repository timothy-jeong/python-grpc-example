#!/bin/bash

set -e

python -m grpc_tools.protoc \
  -I=../../proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  ../../proto/member_service.proto

python -m grpc_tools.protoc \
  -I=../../proto \
  --python_out=./app/pb \
  --grpc_python_out=./app/pb \
  --pyi_out=./app/pb \
  ../../proto/message/*.proto
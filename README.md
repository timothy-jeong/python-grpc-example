# gRPC 통신 예제 프로젝트

이 프로젝트는 FastAPI와 gRPC를 이용하여 두 개의 서비스를 연결하는 예제를 보여줍니다.  
**member-service**는 FastAPI REST API와 gRPC 서버를 동시에 호스팅하며,  
**board-service**는 member-service의 gRPC 서버에 클라이언트로 요청하여 데이터를 가져옵니다.

## 프로젝트 구조
```bash.
├── README.md
├── docker-compose.yml
├── proto
│   ├── member_service.proto
│   └── message
│       ├── member_request.proto
│       └── member_response.proto
└── services
    ├── board_service
    │   ├── Dockerfile
    │   ├── app
    │   │   ├── database
    │   │   ├── grpc_client.py
    │   │   ├── main.py
    │   │   └── pb
    │   ├── proto.sh
    │   └── requirements.txt
    └── member_service
        ├── Dockerfile
        ├── app
        │   ├── database
        │   ├── grpc_server.py
        │   ├── main.py
        │   └── pb
        ├── proto.sh
        ├── requirements.txt
        └── supervisord.conf
```

## 주요 기능

- **FastAPI REST API**  
  member-service와 board-service 각각에서 FastAPI를 통해 HTTP API를 제공합니다.
  
- **gRPC 서버 & 클라이언트**  
  - member-service는 gRPC 서버(`grpc_server.py`)를 실행하여 클라이언트 요청을 처리합니다.
  - board-service는 gRPC 클라이언트(`grpc_client.py`)를 통해 member-service의 gRPC API에 접근합니다.

- **데이터베이스 초기화**  
  - FastAPI 앱의 lifespan 이벤트와 gRPC 서버 실행 전 별도의 초기화 로직을 통해 데이터베이스 테이블이 생성됩니다.
  - 초기 버전에서는 SQLite를 사용하며, 파일 기반(`test.db`) 데이터베이스로 설정하여 두 프로세스에서 공유할 수 있도록 구성했습니다.

## 사전 요구사항

- Docker 및 Docker Compose 설치  
- Python 3.12 이상 (Dockerfile 내 사용)

## 실행 방법

1. **프로젝트 클론 및 디렉터리 이동**  
```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

2. **Docker Compose 실행**
```bash
docker-compose up --build
```

3. **서비스 확인**
- member-service
    - REST API: http://localhost:8000/docs
    - gRPC 서버: member-service:50051
- board-service
    - REST API: http://localhost:8001/docs
    - member-service 에서 만든 유저의 id로 board 를 만들고 조회해보세요.


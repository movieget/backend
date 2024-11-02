from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, tracemalloc
from pathlib import Path
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from dotenv import load_dotenv
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import socket
import logging

logging.basicConfig(level=logging.DEBUG)

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.app.api.root import api_router as root_router
from src.common.handlers.db_handler import lifespan

load_dotenv()


# def setup_opentelemetry():
#     """OpenTelemetry 설정"""

#     # 리소스 속성 설정
#     resource = Resource.create(
#         {
#             "service.name": os.getenv("OTEL_SERVICE_NAME", "fastapi-service"),
#             "service.version": os.getenv("OTEL_SERVICE_VERSION", "1.0.0"),
#             "host.name": socket.gethostname(),
#         }
#     )

#     # TracerProvider 설정
#     tracer_provider = TracerProvider(resource=resource)

#     # Elastic APM OTLP 엔드포인트로 내보내기 설정
#     otlp_exporter = OTLPSpanExporter(
#         endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:8200/v1/traces"),
#         headers=os.getenv("OTEL_EXPORTER_OTLP_HEADERS"),
#     )
#     print(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))

#     # BatchSpanProcessor를 TracerProvider에 추가
#     span_processor = BatchSpanProcessor(otlp_exporter)
#     tracer_provider.add_span_processor(span_processor)

#     # 글로벌 TracerProvider 설정
#     trace.set_tracer_provider(tracer_provider)


# # OpenTelemetry 설정 적용
# setup_opentelemetry()


tracemalloc.start()

app = FastAPI(lifespan=lifespan, debug=True)

# # 트레이서 프로바이더 설정
# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)

# # OTLP 익스포터 설정 (APM 서버의 엔드포인트를 지정)
# otlp_exporter = OTLPSpanExporter(endpoint="https://apm.kprolabs.space")

# # 배치 스팬 프로세서를 사용하여 스팬을 배치로 내보내기 설정
# span_processor = BatchSpanProcessor(otlp_exporter)
# trace.get_tracer_provider().add_span_processor(span_processor)

# # FastAPI 앱 계측
# FastAPIInstrumentor.instrument_app(app)

# NOTE: Turn off in Production
# app = FastAPI(openapi_url=None)

origins = ["http://localhost:5173", "https://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_origin_regex="http://111\.111\.111\.111(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")

# root_router를 api_router에 포함
api_router.include_router(root_router)

# api_router를 app에 포함
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8000)

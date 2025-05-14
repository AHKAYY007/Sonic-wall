import os
import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Summary
import sentry_sdk
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.api.routes import router as api_router

# ---------------------------
# Setup Logging
# ---------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, "app.log")
handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[handler]
)
logger = logging.getLogger(__name__)

# ---------------------------
# Sentry Setup
# ---------------------------
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    environment=os.getenv("ENVIRONMENT", "development")
)

# ---------------------------
# OpenTelemetry Setup
# ---------------------------
resource = Resource(attributes={
    SERVICE_NAME: "sonic-wallet-firewall"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")))
provider.add_span_processor(processor)

# Set global provider
from opentelemetry import trace
trace.set_tracer_provider(provider)

# ---------------------------
# FastAPI App Setup
# ---------------------------
app = FastAPI(title="Sonic Wallet Firewall")

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: Prometheus
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["method", "endpoint"])
REQUEST_LATENCY = Summary("api_request_duration_seconds", "API request latency")

@app.middleware("http")
async def prometheus_metrics(request: Request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    return response

@app.get("/metrics", include_in_schema=False)
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# Include API routes
app.include_router(api_router, prefix="/api")

# Instrument OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

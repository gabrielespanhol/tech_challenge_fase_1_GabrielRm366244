import time
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.metrics_model import Metrics


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Pre-request info
        client_ip = request.client.host
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        user_agent = request.headers.get("user-agent", "")
        referrer = request.headers.get("referer", "")
        auth_user_id = None  # (ex: parse do token JWT se quiser implementar depois)

        # Body size (apenas para POST/PUT)
        try:
            body = await request.body()
            body_size = len(body)
        except Exception:
            body_size = None

        # Chamada real da rota
        try:
            response = await call_next(request)
            status_code = response.status_code

            # Response size (caso seja StreamingResponse, isso pode ser None)
            try:
                response_size = len(response.body)
            except Exception:
                response_size = None

            error_message = None

        except Exception as e:
            status_code = 500
            response_size = None
            error_message = str(e)
            response = Response(content="Internal Server Error", status_code=500)

        duration = time.time() - start_time

        # Salva no banco
        db: Session = SessionLocal()
        log_entry = Metrics(
            method=method,
            path=path,
            status_code=status_code,
            duration=duration,
            client_ip=client_ip,
            user_agent=user_agent,
            query_params=json.dumps(query_params),
            body_size=body_size,
            response_size=response_size,
            auth_user_id=auth_user_id,
            error_message=error_message,
        )
        db.add(log_entry)
        db.commit()
        db.close()

        return response

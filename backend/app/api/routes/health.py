"""Routes de santé et d'information système.

Endpoints :
    GET /health   : vérifie que l'API est opérationnelle
    GET /version  : retourne la version de l'application
    GET /info     : retourne des informations système

Ces endpoints sont utilisés par :
    - Les outils de monitoring (Docker healthcheck, Prometheus)
    - Le frontend (au démarrage, pour vérifier la connexion)
    - Les tests d'intégration
"""
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Schéma de réponse du endpoint /health."""

    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str


class VersionResponse(BaseModel):
    """Schéma de réponse du endpoint /version."""

    version: str
    app_name: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Vérifie que l'API est opérationnelle.",
)
async def health_check() -> HealthResponse:
    """Endpoint de santé pour les outils de monitoring."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Version de l'application",
)
async def get_version() -> VersionResponse:
    """Retourne la version de l'application AIS."""
    return VersionResponse(
        version=settings.app_version,
        app_name=settings.app_name,
    )
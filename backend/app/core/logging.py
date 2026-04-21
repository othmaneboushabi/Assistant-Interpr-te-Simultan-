"""Configuration du logging structuré avec Loguru.

Usage :
    from loguru import logger
    logger.info("Message")
    logger.error("Erreur: {}", exc)

Le logger est initialisé automatiquement au démarrage de l'application
(via setup_logging() appelé dans main.py).
"""
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    """Configure Loguru pour l'application AIS.

    - Remplace le handler Python par défaut par Loguru
    - Ajoute un handler console avec couleurs (dev-friendly)
    - Ajoute un handler fichier avec rotation automatique
    """
    # 1. Supprimer le handler par défaut de Loguru
    logger.remove()

    # 2. Handler console (développement)
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,
        diagnose=settings.debug,
    )

    # 3. Handler fichier avec rotation automatique
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        str(log_path),
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
        backtrace=True,
        diagnose=False,
        enqueue=True,
    )

    logger.info(
        f"Logging initialisé | niveau={settings.log_level} | "
        f"env={settings.app_env} | fichier={log_path}"
    )
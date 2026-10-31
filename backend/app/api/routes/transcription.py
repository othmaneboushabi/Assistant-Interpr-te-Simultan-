"""Routes de transcription audio.

Endpoints :
    POST /transcribe : transcription d'un fichier audio uploadé

Cet endpoint est pratique pour tester le service ASR
sans passer par le streaming WebSocket (qui sera ajouté en J6).
"""
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from loguru import logger

from app.schemas.transcription import TranscriptionResponse
from app.services.asr_service import get_asr_service

router = APIRouter()

# Formats audio supportés
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}
MAX_FILE_SIZE_MB = 25


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    summary="Transcription d'un fichier audio",
    description=(
        "Transcrit un fichier audio via faster-whisper. "
        "Formats supportés : WAV, MP3, M4A, FLAC, OGG, WEBM. "
        "Taille max : 25 MB. "
        "Langues : fr, en, es, ar (ou 'auto' pour détection automatique)."
    ),
    status_code=status.HTTP_200_OK,
)
async def transcribe_file(
    file: UploadFile = File(..., description="Fichier audio à transcrire"),
    language: Optional[str] = Query(
        "auto",
        description="Code langue (fr, en, es, ar) ou 'auto'",
        examples=["auto", "fr", "en", "es", "ar"],
    ),
) -> TranscriptionResponse:
    """Transcrit un fichier audio uploadé."""

    # ===== Validation du fichier =====
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucun nom de fichier fourni.",
        )

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format '{ext}' non supporté. Formats acceptés : {ALLOWED_EXTENSIONS}",
        )

    # Lecture du contenu
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Fichier trop volumineux : {size_mb:.1f} MB (max {MAX_FILE_SIZE_MB} MB).",
        )

    logger.info(f"📥 Fichier reçu : {file.filename} ({size_mb:.2f} MB)")

    # ===== Sauvegarde temporaire =====
    tmp_dir = Path("data/tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_filename = f"{uuid.uuid4()}{ext}"
    tmp_path = tmp_dir / tmp_filename

    try:
        tmp_path.write_bytes(content)

        # ===== Transcription =====
        asr = get_asr_service()
        result = asr.transcribe(str(tmp_path), language=language)
        return TranscriptionResponse(**result)

    except Exception as e:
        logger.exception(f"❌ Erreur lors de la transcription : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la transcription : {str(e)}",
        ) from e

    finally:
        # Nettoyage du fichier temporaire
        if tmp_path.exists():
            tmp_path.unlink()
            logger.debug(f"🗑️  Fichier temporaire supprimé : {tmp_path}")
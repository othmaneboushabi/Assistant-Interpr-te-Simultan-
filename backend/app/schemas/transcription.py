"""Schémas Pydantic pour les endpoints de transcription.

Ces schémas définissent le format des réponses API,
utilisés pour la validation et la génération de la doc Swagger.
"""
from pydantic import BaseModel, Field


class TranscriptionSegment(BaseModel):
    """Segment individuel d'une transcription."""

    start: float = Field(..., description="Temps de début en secondes")
    end: float = Field(..., description="Temps de fin en secondes")
    text: str = Field(..., description="Texte transcrit du segment")


class TranscriptionResponse(BaseModel):
    """Réponse complète d'une transcription audio."""

    text: str = Field(..., description="Transcription complète du fichier")
    language: str = Field(..., description="Code langue détecté (ISO 639-1)")
    language_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Confiance de détection (0 à 1)"
    )
    duration: float = Field(..., description="Durée du fichier audio (secondes)")
    segments: list[TranscriptionSegment] = Field(
        default_factory=list, description="Segments horodatés"
    )
    latency_ms: float = Field(..., description="Latence de transcription (ms)")
    realtime_factor: float = Field(
        ...,
        description="Facteur temps réel : > 1 signifie plus rapide que l'audio",
    )
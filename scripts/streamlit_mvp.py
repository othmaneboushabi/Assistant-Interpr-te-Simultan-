"""MVP Streamlit — Interface de démonstration AIS.

Cette interface web permet de :
    - Uploader un fichier audio (WAV, MP3, M4A, FLAC, OGG, WEBM)
    - Choisir la langue de transcription (ou détection automatique)
    - Visualiser la transcription avec segments horodatés
    - Afficher les métriques de performance (latence, RTF)

Lancement :
    1. Démarrer le backend : cd backend && uvicorn app.main:app --reload
    2. Démarrer Streamlit : streamlit run scripts/streamlit_mvp.py
    3. Ouvrir : http://localhost:8501

Auteurs : Othmane Boushabi & Mustapha Alaoui Hamdaoui
Projet : AIS - PFA EMSI 2025/2026
"""
import time

import httpx
import streamlit as st

# ===== Configuration =====
API_BASE_URL = "http://localhost:8000/api/v1"
PAGE_TITLE = "AIS — MVP Démonstration"
PAGE_ICON = "🎤"

# ===== Configuration de la page =====
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===== Fonctions utilitaires =====
def check_api_health() -> dict | None:
    """Vérifie si le backend FastAPI est opérationnel."""
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=2.0)
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError:
        return None
    return None


def transcribe_audio(file_bytes: bytes, filename: str, language: str) -> dict:
    """Envoie le fichier audio au backend pour transcription."""
    files = {"file": (filename, file_bytes)}
    params = {"language": language}
    response = httpx.post(
        f"{API_BASE_URL}/transcribe",
        files=files,
        params=params,
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()


# ===== Header =====
st.title(f"{PAGE_ICON} AIS — Assistant Interprète Simultané")
st.caption("MVP Semaine 1 — Démonstration de transcription automatique via faster-whisper")

# Alerte sur l'état de l'API
health = check_api_health()
if health is None:
    st.error(
        "⚠️ **Backend FastAPI inaccessible.** "
        "Vérifie que le serveur tourne : `cd backend && uvicorn app.main:app --reload`"
    )
    st.stop()
else:
    st.success(
        f"✅ Backend connecté : **{health['app_name']} v{health['version']}** "
        f"(environnement : {health['environment']})"
    )

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ Configuration")

    language = st.selectbox(
        "Langue de transcription",
        options=["auto", "fr", "en", "es", "ar"],
        index=0,
        help="'auto' détecte automatiquement la langue parlée",
    )

    st.divider()
    st.subheader("📊 Stack technique")
    st.caption("- **ASR** : faster-whisper (modèle `small`)")
    st.caption("- **Backend** : FastAPI + Uvicorn")
    st.caption("- **Frontend** : Streamlit")
    st.caption("- **BDD** : PostgreSQL via Docker")

    st.divider()
    st.subheader("👥 Équipe")
    st.caption("- Othmane")
    st.caption("- Mustapha Alaoui Hamdaoui")
    st.caption("- Encadrante : Dr. Hasnaa Chaabi")

# ===== Corps principal =====
col1, col2 = st.columns([1, 1])

# ----- Colonne gauche : Upload -----
with col1:
    st.subheader("📤 Fichier audio")

    uploaded_file = st.file_uploader(
        "Choisis un fichier audio à transcrire",
        type=["wav", "mp3", "m4a", "flac", "ogg", "webm"],
        help="Formats supportés : WAV, MP3, M4A, FLAC, OGG, WEBM (max 25 MB)",
    )

    if uploaded_file is not None:
        # Prévisualisation audio
        st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

        # Infos fichier
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.caption(f"📁 **{uploaded_file.name}** — {file_size_mb:.2f} MB")

        # Bouton de lancement
        if st.button("🚀 Transcrire", type="primary", use_container_width=True):
            with st.spinner("Transcription en cours... (le 1er appel charge le modèle)"):
                try:
                    start_time = time.time()
                    result = transcribe_audio(
                        file_bytes=uploaded_file.getvalue(),
                        filename=uploaded_file.name,
                        language=language,
                    )
                    total_time = time.time() - start_time

                    st.session_state["result"] = result
                    st.session_state["total_time"] = total_time
                    st.session_state["filename"] = uploaded_file.name
                    st.success("✅ Transcription réussie !")

                except httpx.HTTPStatusError as e:
                    st.error(f"❌ Erreur API ({e.response.status_code}) : {e.response.text}")
                except httpx.RequestError as e:
                    st.error(f"❌ Erreur réseau : {e}")
                except Exception as e:
                    st.exception(e)

# ----- Colonne droite : Résultats -----
with col2:
    st.subheader("📝 Résultats")

    if "result" in st.session_state:
        result = st.session_state["result"]

        # ----- Métriques clés -----
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            st.metric("🌍 Langue", result["language"].upper())
        with mcol2:
            st.metric("⏱️ Durée audio", f"{result['duration']:.1f}s")
        with mcol3:
            st.metric("⚡ Latence", f"{result['latency_ms']:.0f} ms")
        with mcol4:
            st.metric(
                "🚀 RTF",
                f"{result['realtime_factor']:.2f}x",
                help="Realtime Factor : > 1 = plus rapide que l'audio",
            )

        # Confiance langue
        conf_pct = result["language_probability"] * 100
        st.progress(
            result["language_probability"],
            text=f"Confiance détection langue : {conf_pct:.1f}%",
        )

        st.divider()

        # ----- Transcription complète -----
        st.markdown("### 📜 Transcription")
        st.info(result["text"])

        # ----- Segments détaillés -----
        with st.expander(f"🔍 {len(result['segments'])} segments horodatés"):
            for i, seg in enumerate(result["segments"], 1):
                st.markdown(
                    f"**Segment {i}** — [{seg['start']:.1f}s → {seg['end']:.1f}s]\n\n"
                    f"> {seg['text']}"
                )

        # ----- Télécharger résultat JSON -----
        import json

        st.download_button(
            "💾 Télécharger le résultat (JSON)",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name=f"transcription_{st.session_state.get('filename', 'audio')}.json",
            mime="application/json",
        )
    else:
        st.info("👈 Upload un fichier audio et clique sur **Transcrire** pour commencer.")
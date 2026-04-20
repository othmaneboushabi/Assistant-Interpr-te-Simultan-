# AIS — Assistant Interprète Simultané

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In_Development-orange.svg)](#)

> Un copilote IA temps réel pour interprètes professionnels en conférences scientifiques internationales.

## 🎯 Projet

AIS est un système d'assistance intelligent qui écoute le flux audio de l'orateur en temps réel et affiche sur l'écran de l'interprète les informations critiques (noms propres, chiffres, terminologie technique traduite, acronymes, résumé contextuel) pour l'aider à éviter les trous de mémoire sans le distraire.

**Projet de Fin d'Année (PFA)** — 4ème année Génie Informatique, spécialisation IIR-IA
**EMSI** en collaboration avec **ACM Chapter** & **SmartILab EMSI**
**Année universitaire** : 2025 — 2026

## 👥 Équipe

| Rôle | Nom |
|------|-----|
| Développeur 1 | **Othmane** |
| Développeur 2 | **Mustapha Alaoui Hamdaoui** |
| Encadrante | **Dr. Hasnaa Chaabi** |

## 🛠️ Stack technique (100% open-source)

| Couche | Technologie |
|--------|------------|
| ASR | faster-whisper + whisper-streaming |
| NER | spaCy (FR/EN/ES) + CAMeL-BERT (AR) |
| Traduction | NLLB-200 distilled 600M |
| LLM | Gemma 4 E4B via Ollama |
| Backend | FastAPI + WebSockets + LangGraph |
| Persistance | PostgreSQL + ChromaDB + Redis |
| Frontend | React 18 + Vite + TailwindCSS |
| Déploiement | Docker + Docker Compose |

## 📊 Progression du projet

- [ ] Semaine 1 — Fondations + ASR streaming
- [ ] Semaine 2 — NLP multilingue + Glossaires
- [ ] Semaine 3 — Gemma 4 + Résumé contextuel
- [ ] Semaine 4 — Documents + OCR + Frontend React
- [ ] Semaine 5 — Tests + Évaluation + Optimisation
- [ ] Semaine 6 — Déploiement + Documentation + Soutenance

## 📁 Structure du projet
ais-pfa/
├── backend/           # API FastAPI (Python)
├── frontend/          # Interface React (S4)
├── models/            # Modèles IA téléchargés (gitignorés)
├── docs/              # Documentation technique
│   └── reports/       # Rapports hebdomadaires
├── scripts/           # Scripts utilitaires
├── docker/            # Dockerfiles
└── data/              # Données de test (gitignorées)

## 🔒 Confidentialité & Sécurité

AIS fonctionne **100% en local**. Aucune donnée audio ou transcription ne transite par des serveurs externes. Conforme RGPD.

## 📄 Licence

Apache License 2.0 — voir [LICENSE](LICENSE).
# Benchmarks AIS — Mesures de performance

## Semaine 1 — J5-J6 : Validation faster-whisper

### Configuration matérielle
- **CPU** : [à remplir par Othmane, ex : Intel i7-12700H]
- **RAM** : [à remplir, ex : 16 GB]
- **OS** : Windows 11
- **Python** : 3.11
- **faster-whisper** : 1.0.3

### Configuration ASR
- **Modèle** : Whisper `small` (461 MB)
- **Device** : CPU
- **Compute type** : int8 (quantization)
- **VAD filter** : activé
- **Beam size** : 5

### Premier benchmark — JFK speech (11s, anglais)

| Tentative | Latence (ms) | RTF | Notes |
|-----------|--------------|-----|-------|
| 1ère (froid) | 7882 | 1.4x | Inclut le chargement modèle (~3-4s) |
| 2ème (chaud) | _à mesurer_ | _à mesurer_ | Modèle déjà en RAM |
| 3ème (chaud) | _à mesurer_ | _à mesurer_ | Baseline stable |

### Observations

- **Qualité transcription** : 100% exacte sur l'audio JFK standard.
- **Détection langue** : 95.56% de confiance (excellent).
- **RTF > 1** : confirme la faisabilité du streaming temps réel.
- **Objectif cahier (<2s latence)** : atteignable avec approche streaming (chunks 1-2s).

### Prochaines étapes

- [ ] Mesurer sur audio français (Common Voice dataset)
- [ ] Mesurer sur audio arabe (MSA)
- [ ] Implémenter whisper-streaming pour valider latence streaming
- [ ] Tester l'impact de modèles plus gros (medium, large-v3)
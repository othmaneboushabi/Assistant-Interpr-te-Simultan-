# ADR-001 : Choix de l'infrastructure PostgreSQL

**Date** : 20 avril 2026
**Statut** : ✅ Accepté
**Auteurs** : Othmane, Mustapha Alaoui Hamdaoui
**Encadrante** : Dr. Hasnaa Chaabi

---

## 📋 Contexte

Le projet **AIS (Assistant Interprète Simultané)** nécessite une base de données relationnelle robuste pour stocker :

- Les **sessions d'interprétation** (session_id, utilisateur, dates, métadonnées)
- Les **transcriptions** générées en temps réel par le module ASR
- Les **glossaires terminologiques** importés par les interprètes (formats CSV, JSON, XLSX, TBX)
- Les **termes** et leurs **traductions contextuelles** détectés dans le discours
- Les **acronymes** détectés et leurs expansions
- Les **résumés contextuels glissants** produits par l'agent Gemma 4
- Les **logs d'audit** (traçabilité RGPD)

Le cahier des charges (§5.1) spécifie explicitement **PostgreSQL 16** comme système de gestion de base de données relationnelle. Cette décision concerne maintenant le **mode de déploiement** de PostgreSQL dans l'environnement de développement.

---

## 🎯 Décision

**PostgreSQL 16 sera déployé via Docker** (image officielle `postgres:16-alpine`) orchestré par Docker Compose, dès la **Semaine 1** du projet.

L'infrastructure est définie dans le fichier `docker-compose.yml` à la racine du projet, et se lance avec une unique commande : `docker-compose up -d`.

---

## 🔄 Alternatives considérées

### Alternative 1 : SQLite (rejetée)

**Avantages** :
- Zéro setup, fichier unique
- Idéal pour prototypage rapide

**Inconvénients** :
- ❌ **Non conforme au cahier des charges §5.1** qui spécifie PostgreSQL
- ❌ Pas de support natif des requêtes vectorielles avancées
- ❌ Pas de véritable concurrence multi-sessions (critique pour NFR-SCA-02 : sessions simultanées)
- ❌ Migration vers PostgreSQL en S5 introduirait un risque technique tardif

**Verdict** : rejetée pour non-respect du cahier des charges.

### Alternative 2 : PostgreSQL installé localement (rejetée)

**Avantages** :
- Consommation mémoire plus faible (~150 MB vs ~250 MB pour Docker)
- Démarrage instantané (pas d'overhead Docker)
- Pas besoin d'installer Docker Desktop

**Inconvénients** :
- ❌ **Reproductibilité faible entre membres de l'équipe** : Mustapha et Othmane auraient des installations potentiellement divergentes (versions, encodage, permissions Windows)
- ❌ **Risque de conflit** avec d'autres projets installés localement utilisant PostgreSQL
- ❌ **Migration obligatoire vers Docker en S6** (cf. Roadmap §J36 : "Dockerisation complète") → dette technique à payer plus tard
- ❌ **Portabilité réduite** : difficulté pour la démonstration finale sur une machine tierce du jury
- ❌ **Nettoyage manuel** en fin de projet (désinstallation, purge données)

**Verdict** : rejetée pour raisons de reproductibilité équipe et cohérence avec la roadmap S6.

### Alternative 3 : PostgreSQL via Docker (✅ retenue)

Détails ci-dessous.

---

## ✅ Justification du choix (Docker)

### 1. Reproductibilité binôme (facteur décisif)

Othmane et Mustapha travaillent sur deux machines distinctes avec des configurations Windows potentiellement différentes. Avec Docker :

```bash
# Commande unique pour tous les membres de l'équipe
docker-compose up -d
```

Cette commande garantit une **base de données strictement identique** (version 16-alpine, utilisateur `ais_user`, base `ais_db`, port `5432`, même encodage UTF-8) sur les deux machines.

Sans Docker, la phase de setup de l'environnement peut prendre plusieurs heures pour Mustapha et générer des bugs latents difficiles à diagnostiquer.

### 2. Conformité avec la Roadmap

La **Semaine 6 (J36)** de la roadmap prévoit explicitement :
> Dockerisation complète — `docker-compose.yml` qui orchestre : backend, frontend, postgres, redis, chromadb

Commencer avec PostgreSQL dans Docker dès la S1 évite une migration risquée en fin de projet (à 2 semaines de la soutenance).

### 3. Conformité avec le Cahier des charges

Le **Cahier des charges §5.1** mentionne explicitement :
> PostgreSQL 16 via Docker

La décision est donc un alignement strict avec les spécifications initiales validées par l'encadrante.

### 4. Portabilité et démonstration

Le jour de la soutenance (S6), le jury peut demander :
- De tester le système sur une autre machine
- De vérifier la reproductibilité du projet
- D'inspecter la configuration

Avec Docker, ces scénarios sont gérés par une seule commande. Sans Docker, ils nécessitent des heures d'installation et de configuration.

### 5. Isolation

La base de données AIS est **isolée** des autres projets présents sur les machines de développement. Une erreur ou une corruption de données dans AIS n'impacte pas les autres environnements PostgreSQL éventuels.

### 6. Compétence valorisable

La maîtrise de Docker est une **compétence professionnelle recherchée** dans le domaine du DevOps et de l'IA/MLOps. L'utilisation de Docker dès le début du projet :
- Enrichit le CV des développeurs
- Justifie une section dédiée dans le rapport PFA (§Architecture)
- Démontre la maturité technique du projet au jury

---

## 📊 Conséquences

### Conséquences positives

- ✅ Setup identique entre Othmane et Mustapha (zéro divergence d'environnement)
- ✅ Prérequis Roadmap S6 satisfait dès la S1 (pas de migration tardive)
- ✅ Démonstration portable sur toute machine disposant de Docker
- ✅ Nettoyage en fin de projet trivial (`docker-compose down -v`)
- ✅ Isolation totale de la base de données AIS
- ✅ Apprentissage de Docker intégré au projet (valorisable)

### Conséquences négatives et mitigations

| Conséquence négative | Mitigation |
|---|---|
| Docker Desktop consomme ~2 GB de RAM | Arrêter Docker Desktop en dehors des sessions de développement |
| Overhead mémoire ~100 MB (vs local) | Acceptable sur machines 16 GB+ (cf. spec matérielle CDC §5.3) |
| Conflit potentiel avec PostgreSQL local sur le port 5432 | Arrêter le service PostgreSQL local pendant les sessions AIS : `Get-Service postgresql* \| Stop-Service` |
| Apprentissage initial de Docker | Compensé par la durée du projet (6 semaines = largement suffisant) |

---

## 🛠️ Configuration retenue

**Fichier** : `docker-compose.yml` (racine du projet)

**Image** : `postgres:16-alpine`
- PostgreSQL 16 (dernière version stable majeure)
- Alpine Linux (distribution minimaliste, image ~80 MB au lieu de ~400 MB)

**Credentials** (développement uniquement) :
- Utilisateur : `ais_user`
- Mot de passe : `ais_password`
- Base : `ais_db`
- Port hôte : `5432`

**Persistance** : volume Docker nommé `ais_postgres_data` pour garantir la pérennité des données entre redémarrages du conteneur.

**Healthcheck** : vérification automatique toutes les 10 secondes via `pg_isready`.

---

## 🔒 Considérations de sécurité

### En développement (statut actuel)

- Les credentials sont en clair dans `docker-compose.yml`
- La base est accessible uniquement sur `localhost:5432` (pas d'exposition réseau externe)
- Acceptable pour un environnement de développement local

### Pour la production (à traiter en S5)

Lors de la phase **Semaine 5 — Sécurité + Confidentialité (J33)**, cette configuration devra évoluer :

- [ ] Déplacer les credentials dans un fichier `.env` (exclus du versioning)
- [ ] Utiliser Docker Secrets ou un vault
- [ ] Activer TLS pour les connexions si la base devient accessible au-delà de `localhost`
- [ ] Définir une politique de mots de passe forts
- [ ] Mettre en place des sauvegardes automatiques

Référence : **REQ-SEC-06** et **REQ-SEC-07** du cahier des charges.

---

## 📚 Références

- Cahier des charges AIS v2 — §5.1 (Stack technologique)
- Cahier des charges AIS v2 — §5.3 (Configuration matérielle)
- Roadmap 6 semaines — J36 (Dockerisation complète)
- Documentation officielle PostgreSQL 16 : https://www.postgresql.org/docs/16/
- Documentation Docker Compose : https://docs.docker.com/compose/

---

## 🔄 Révision

Ce document sera révisé :
- En **Semaine 5 (J33)** lors de la phase de sécurisation
- En **Semaine 6 (J36)** lors de la dockerisation complète
- À tout moment si une limitation majeure du choix Docker est identifiée

---

*Document versionné dans `docs/adr/ADR-001-database-choice.md`.*


# Architecture Decision Records (ADR)

Ce dossier contient les décisions d'architecture majeures du projet AIS.

## Qu'est-ce qu'un ADR ?

Un ADR documente une décision technique importante : le contexte, les alternatives
considérées, la décision prise et ses conséquences. Il permet de tracer le
raisonnement et de s'y référer plus tard.

## Liste des ADRs

| N° | Titre | Statut | Date |
|----|-------|--------|------|
| 001 | Choix de l'infrastructure PostgreSQL | ✅ Accepté | 2026-04-20 |

## Prochains ADRs prévus

- ADR-002 : Choix du modèle ASR (faster-whisper vs alternatives) — S1
- ADR-003 : Choix du LLM (Gemma 4 vs Mistral vs Phi-3) — S3
- ADR-004 : Architecture multi-agents (LangGraph vs asyncio) — S3
- ADR-005 : Choix du frontend (React vs Streamlit pro) — S4
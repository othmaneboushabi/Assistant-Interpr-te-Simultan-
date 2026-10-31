# Troubleshooting — Journal de bord technique

## Semaine 1

### 🐛 [2026-04-20] Conflit potentiel PostgreSQL local vs Docker

**Contexte** : au lancement de `docker-compose up -d`, PostgreSQL local
(service Windows `postgresql-x64-16`) tournait également sur le port 5432.

**Symptômes** : aucun message d'erreur apparent, Docker `healthy` sur 5432.

**Diagnostic** : Docker a probablement réservé le port en premier au démarrage
du PC, le service Windows tournait "à vide" sans binder le port.

**Résolution** :
- Arrêt du service Windows : `Stop-Service postgresql-x64-16`
- Passage en démarrage manuel : `Set-Service -Name postgresql-x64-16 -StartupType Manual`

**Référence** : ADR-001-database-choice.md




### 🔐 [2026-04-20] Impossible d'arrêter le service PostgreSQL local

**Symptôme** :**Cause** : la commande `Stop-Service` nécessite les droits administrateurs
Windows pour agir sur les services système.

**Résolution** : ouvrir PowerShell en mode administrateur
(Windows → clic droit sur PowerShell → Exécuter en tant qu'administrateur),
puis exécuter `Stop-Service postgresql-x64-16`.

**Note sécurité** : on utilise PowerShell admin uniquement pour cette
opération système ponctuelle. Le développement courant se fait
toujours en PowerShell utilisateur standard.
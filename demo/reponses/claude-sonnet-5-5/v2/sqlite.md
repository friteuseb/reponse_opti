# Recommandation

Choisis SQLite si l'application tourne sur un seul serveur. Quelques centaines d'utilisateurs ne posent pas de problème à SQLite. Choisis PostgreSQL si l'un des cas ci-dessous s'applique.

## Choisir PostgreSQL si

- L'application tourne sur 2 serveurs ou plus. SQLite est un fichier local et n'accepte pas l'accès par le réseau.
- Le système de fichiers de l'hébergeur est éphémère (Heroku, conteneurs sans volume). Le fichier SQLite disparaît à chaque déploiement.
- L'application écrit en continu depuis de nombreuses requêtes simultanées. SQLite accepte un seul écrivain à la fois.
- Tu as besoin d'une fonction propre à PostgreSQL : PostGIS, `pg_trgm`, `LISTEN/NOTIFY`, sécurité par ligne, types riches (`jsonb`, tableaux, plages).
- Plusieurs personnes ou outils doivent interroger la base de données en direct (BI, scripts, réplicas en lecture).

## Choisir SQLite si

- Un seul serveur héberge l'application.
- La charge est surtout en lecture, avec des écritures courtes (moins de 50 ms par transaction).
- Tu veux zéro processus à administrer, un déploiement simple et des sauvegardes d'un seul fichier.
- Les tests et le développement doivent démarrer sans installation.

## Configurer SQLite pour une application web

Exécute ces commandes à chaque ouverture de connexion :

```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;
PRAGMA synchronous = NORMAL;
```

- `WAL` permet aux lecteurs de travailler pendant une écriture.
- `busy_timeout` fait attendre une requête 5 s au lieu d'échouer avec `database is locked`.
- `foreign_keys` est désactivé par défaut. Active-le toi-même.
- Garde les transactions d'écriture courtes. N'appelle pas d'API externe pendant une transaction.

## Sauvegarder

- Utilise `sqlite3 app.db ".backup 'copie.db'"` ou `VACUUM INTO 'copie.db'`.
- Utilise Litestream pour une réplication continue vers un stockage objet (S3 ou compatible).

Ne copie pas `app.db` avec `cp` pendant que l'application écrit. La copie peut être corrompue. En mode WAL, les fichiers `-wal` et `-shm` font aussi partie de l'état de la base de données.

Ne place pas le fichier sur NFS ou sur un autre partage réseau. Les verrous n'y sont pas fiables.

## Limites de SQLite à connaître

- Le typage est souple. Une colonne `INTEGER` accepte du texte, sauf si tu déclares la table en `STRICT` (SQLite 3.37 ou plus).
- `ALTER TABLE` reste limité. Certaines migrations obligent à recréer la table.
- Il n'y a pas de gestion des rôles ni des droits par utilisateur.

## Coût de PostgreSQL

- Un processus de plus à installer, mettre à jour et surveiller.
- Des sauvegardes à planifier : `pg_dump`, ou `pgBackRest` avec archivage WAL pour restaurer à un instant précis.
- Une alternative : un service managé. Il supprime l'administration, mais ajoute un coût mensuel et une latence réseau.

## Préparer une migration

Tu peux commencer avec SQLite et migrer plus tard. Pour limiter le risque :

1. Utilise un ORM ou un générateur de requêtes qui gère les deux moteurs.
2. Écris du SQL standard. Évite les particularités de SQLite (typage souple, `rowid`).
3. Teste la migration avec `pgloader` avant d'en avoir besoin.

## Résumé

| Critère | SQLite | PostgreSQL |
|---|---|---|
| Nombre de serveurs d'application | 1 | 1 ou plus |
| Écritures simultanées | Une à la fois | Nombreuses |
| Administration | Aucune | Moyenne |
| Sauvegarde | Fichier unique | Outils dédiés |
| Fonctions avancées | Limitées | Très riches |

Si tu hésites encore, prends SQLite pour démarrer, à condition que ton hébergeur conserve le disque entre les déploiements.
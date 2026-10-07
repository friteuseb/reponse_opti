**Recommandation : commence avec SQLite, sauf si un des cas ci-dessous s'applique.**

Pour quelques centaines d'utilisateurs, SQLite suffit. En mode WAL, il traite des milliers de lectures par seconde. Il accepte un seul écrivain à la fois, mais ce verrou dure quelques millisecondes par écriture.

## Choisis SQLite si

- l'application tourne sur un seul serveur ;
- la charge est surtout en lecture ;
- tu veux sauvegarder une seule base, sans service à administrer ;
- tu veux réduire les coûts et la maintenance.

## Choisis PostgreSQL si

- l'application tourne sur plusieurs serveurs qui partagent la même base ;
- plusieurs utilisateurs écrivent en même temps, avec des transactions longues ;
- tu as besoin de JSONB indexé, de PostGIS ou de la recherche plein texte avancée ;
- tu as besoin de réplication ou de haute disponibilité ;
- ton hébergeur efface le disque à chaque déploiement.

## Configuration minimale de SQLite

Exécute ces commandes à chaque ouverture de connexion :

```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;
```

Ne copie pas le fichier de la base pendant que l'application écrit. La copie peut être corrompue. Utilise `sqlite3 app.db ".backup sauvegarde.db"` ou Litestream.

## Migration future

Passer de SQLite à PostgreSQL coûte peu si tu utilises un ORM. Évite les fonctions propres à SQLite dans tes requêtes. Teste tes migrations sur les deux moteurs si tu prévois de changer.
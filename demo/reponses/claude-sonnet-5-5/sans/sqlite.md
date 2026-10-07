**Pour quelques centaines d'utilisateurs, SQLite est souvent suffisant**, et c'est même un très bon choix si votre situation s'y prête. PostgreSQL reste préférable dans certains cas précis.

## Choisir SQLite si :
- L'application tourne sur **un seul serveur** (pas de multi-instances).
- La charge en **écriture est modérée** : SQLite n'autorise qu'un seul écrivain à la fois, mais en mode WAL, c'est largement suffisant pour des centaines d'utilisateurs.
- Vous voulez une **infrastructure minimale** : pas de serveur à installer, configurer, sécuriser ou mettre à jour. La sauvegarde se résume à copier un fichier (ou utiliser `.backup` / Litestream).
- Vous voulez de **bonnes performances en lecture** : pas de latence réseau, tout est local.

Activez au minimum :
```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;
```

## Choisir PostgreSQL si :
- Vous prévoyez de **scaler horizontalement** (plusieurs serveurs d'application accédant à la même base).
- Vous avez beaucoup d'**écritures concurrentes** ou des transactions longues.
- Vous avez besoin de fonctionnalités avancées : types riches (JSONB, tableaux), recherche plein texte poussée, PostGIS, vues matérialisées, réplication, permissions fines par rôle.
- Vous déployez sur une plateforme **sans disque persistant** (certains PaaS, conteneurs éphémères, serverless), où un fichier SQLite poserait problème.
- Plusieurs services ou outils (BI, scripts, etc.) doivent accéder à la base en même temps.

## Points de vigilance
- **Typage souple** de SQLite : utilisez des tables `STRICT` si possible.
- **Migrations** : `ALTER TABLE` est plus limité qu'en PostgreSQL.
- **Migration future** : passer de SQLite à PostgreSQL est faisable, surtout si vous utilisez un ORM et évitez les spécificités de chaque moteur.

## Ma recommandation
Si vous démarrez, que l'app tient sur un serveur et que vous n'avez pas de besoin spécifique, **commencez avec SQLite** : moins de complexité, moins de coûts, et largement assez performant. Si vous savez déjà que vous aurez besoin de scaler, de haute disponibilité ou de fonctionnalités avancées, ou si votre hébergement impose une base externe, **partez directement sur PostgreSQL**.

Si vous me dites quel framework, quel hébergement et quel type de données vous utilisez, je peux affiner le conseil.
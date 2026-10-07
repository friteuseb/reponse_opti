**Recommandation :** pour quelques centaines d'utilisateurs sur un seul serveur, SQLite suffit dans la plupart des cas. Choisis PostgreSQL si un des critères de la section « Quand choisir PostgreSQL » s'applique.

## Comparaison

| Critère | SQLite | PostgreSQL |
|---|---|---|
| Installation | Aucune. La base est un fichier. | Un processus à installer, configurer et mettre à jour. |
| Lectures simultanées | Nombreuses. | Nombreuses. |
| Écritures simultanées | Une à la fois (verrou sur le fichier). | Plusieurs en parallèle. |
| Accès depuis plusieurs serveurs | Non adapté. | Oui, par le réseau. |
| Droits par utilisateur | Aucun. Le fichier appartient à l'application. | Rôles et permissions fins. |
| Types et extensions | Types limités. | JSONB, recherche plein texte, PostGIS, etc. |
| Sauvegarde | Copie du fichier avec `.backup`. | `pg_dump`, archivage WAL, outils managés. |
| Coût d'exploitation | Quasi nul. | Moyen : sauvegardes, mises à jour, supervision. |

## Quand choisir SQLite

- L'application tourne sur un seul serveur.
- Les écritures restent sous quelques centaines par seconde. Un SSD en absorbe plusieurs milliers.
- Tu veux déployer et sauvegarder simplement.
- Le disque du serveur est persistant.

## Quand choisir PostgreSQL

- Tu prévois plusieurs serveurs d'application, ou un déploiement avec disque éphémère (certains PaaS, conteneurs sans volume).
- Beaucoup de requêtes écrivent en même temps, ou une écriture dure plusieurs secondes.
- Tu as besoin de rôles, de réplication ou de types avancés.
- Un autre outil (BI, ETL) doit se connecter à la base par le réseau.
- Ton hébergeur propose PostgreSQL managé et tu veux éviter de gérer les sauvegardes.

## Réglages SQLite recommandés

1. Active le mode WAL : `PRAGMA journal_mode=WAL;`. Les lectures ne bloquent plus les écritures.
2. Définis un délai d'attente : `PRAGMA busy_timeout=5000;`. Une écriture attend 5 s au lieu d'échouer.
3. Active les clés étrangères : `PRAGMA foreign_keys=ON;`. SQLite les ignore par défaut.
4. Garde les transactions d'écriture courtes.

## Mises en garde

**Danger :** ne copie pas le fichier `.db` avec `cp` pendant que l'application tourne. La copie peut être corrompue. Utilise `sqlite3 base.db ".backup copie.db"` ou Litestream.

**Danger :** ne place pas le fichier SQLite sur un partage réseau (NFS, SMB). Le verrouillage y est peu fiable et la base peut se corrompre.

**Attention :** si tu lances plusieurs serveurs d'application, ils ne peuvent pas partager un même fichier SQLite. Passe alors à PostgreSQL.

## Migration ultérieure

La migration de SQLite vers PostgreSQL reste faisable. Utilise un ORM ou un générateur de requêtes, et évite les fonctions propres à SQLite. Tu limites ainsi le travail de migration, et tu peux commencer simple sans te bloquer.
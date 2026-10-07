# Restaurer une sauvegarde pg_dump sur un nouveau serveur

Dans ce document, « serveur source » désigne l'ancien serveur. « Serveur cible » désigne le nouveau.

## 1. Préparer le serveur cible

1. Installe PostgreSQL sur le serveur cible. Utilise la même version majeure que la source, ou une version plus récente.
2. Installe les mêmes extensions que sur la source (par exemple `postgresql-contrib` ou PostGIS). Sans elles, la restauration échoue sur `CREATE EXTENSION`.
3. Utilise un `pg_restore` de version égale ou supérieure à celle du `pg_dump` qui a créé le fichier.
4. Copie le fichier de sauvegarde sur le serveur cible (avec `scp` ou `rsync`).

## 2. Identifier le format du fichier

```bash
file sauvegarde.dump
```

| Format | Option `pg_dump` | Outil de restauration |
|---|---|---|
| SQL texte | `-Fp` (défaut) | `psql` |
| Custom | `-Fc` | `pg_restore` |
| Directory | `-Fd` | `pg_restore` |
| Tar | `-Ft` | `pg_restore` |

Pour tester un fichier non texte, liste son contenu :

```bash
pg_restore --list sauvegarde.dump
```

## 3. Recréer les rôles

`pg_dump` ne sauvegarde pas les rôles ni les tablespaces. Sans les rôles, la restauration affiche `role "xxx" does not exist`.

1. Sur le serveur source, exporte les rôles :

   ```bash
   pg_dumpall --globals-only -U postgres > globals.sql
   ```

2. Copie `globals.sql` sur le serveur cible.
3. Sur le serveur cible, importe les rôles :

   ```bash
   psql -U postgres -f globals.sql postgres
   ```

Si tu n'as pas accès à la source, crée les rôles à la main avec `CREATE ROLE`. Autre option : ajoute `--no-owner` à la restauration. Les objets appartiennent alors à l'utilisateur qui restaure.

Les tablespaces de `globals.sql` pointent vers des répertoires. Crée ces répertoires avant l'import, avec le propriétaire `postgres`.

## 4. Créer la base vide

```bash
createdb -U postgres -O proprietaire nom_base
```

Si tu utilises `pg_restore --create` (étape 5), saute cette étape.

## 5. Restaurer

### Format SQL texte

```bash
psql -U postgres -d nom_base -v ON_ERROR_STOP=1 --single-transaction -f sauvegarde.sql
```

- `ON_ERROR_STOP=1` arrête `psql` à la première erreur.
- `--single-transaction` annule tout en cas d'erreur. La base reste vide.

Pour un fichier compressé :

```bash
gunzip -c sauvegarde.sql.gz | psql -U postgres -d nom_base -v ON_ERROR_STOP=1
```

### Format custom, directory ou tar

```bash
pg_restore -U postgres -d nom_base --no-owner --jobs 4 sauvegarde.dump
```

- `--jobs 4` restaure avec 4 processus en parallèle. Fixe la valeur au nombre de cœurs du serveur cible. Cette option fonctionne avec les formats custom et directory.
- `--no-owner` ignore les propriétaires d'origine. Retire cette option si tu as recréé les rôles.
- `--exit-on-error` arrête la restauration à la première erreur.

N'utilise pas `--jobs` avec `--single-transaction`. Ces deux options sont incompatibles.

Pour créer la base pendant la restauration, connecte-toi à la base `postgres` :

```bash
pg_restore -U postgres -d postgres --create sauvegarde.dump
```

### Cas particuliers

- **Base existante :** ajoute `--clean --if-exists`. N'utilise pas ces options sur une base de production. Elles suppriment les objets existants.
- **Un seul schéma ou une seule table :** utilise `-n schema` ou `-t table`.
- **Serveur distant :** ajoute `-h hôte -p 5432`.
- **Mot de passe :** définis `PGPASSWORD` ou crée `~/.pgpass` (permissions `0600`).
- **Extraire le SQL sans l'exécuter :** `pg_restore -f sortie.sql sauvegarde.dump`.

## 6. Vérifier la restauration

1. Lis les erreurs affichées. Une erreur sur `CREATE EXTENSION` indique une extension manquante.
2. Liste les tables :

   ```bash
   psql -U postgres -d nom_base -c '\dt *.*'
   ```

3. Compare le nombre de lignes des tables principales entre la source et la cible.
4. Recalcule les statistiques du planificateur :

   ```bash
   vacuumdb -U postgres -d nom_base --analyze-only --jobs 4
   ```

   Avant PostgreSQL 18, `pg_dump` n'inclut pas ces statistiques. Sans `ANALYZE`, les requêtes peuvent être lentes.

## 7. Configurer le serveur cible

`pg_dump` ne sauvegarde pas les fichiers de configuration. Reporte à la main les réglages nécessaires depuis le serveur source :

- `postgresql.conf` (mémoire, connexions, journalisation) ;
- `pg_hba.conf` (règles d'authentification).

Recharge ensuite la configuration :

```bash
sudo systemctl reload postgresql
```

Teste enfin la connexion de l'application vers le serveur cible avant de basculer le trafic.
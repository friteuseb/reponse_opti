# Restaurer une sauvegarde pg_dump sur un nouveau serveur

## Avant de commencer

- Installe sur le nouveau serveur une version de PostgreSQL égale ou supérieure à celle de l'ancien serveur. `pg_restore` ne lit pas toujours une sauvegarde faite par une version plus récente.
- Installe aussi les mêmes extensions (par exemple `postgis` ou le paquet `contrib`).

## Procédure

1. **Copie le fichier de sauvegarde** sur le nouveau serveur :
   ```bash
   scp sauvegarde.dump utilisateur@nouveau-serveur:/tmp/
   ```

2. **Identifie le format du fichier.**
   ```bash
   file /tmp/sauvegarde.dump
   ```
   - Un fichier texte contenant du SQL est au format *plain*. Tu le restaures avec `psql`.
   - Un fichier « PostgreSQL custom database dump » ou un répertoire se restaure avec `pg_restore`.

3. **Recrée les rôles.** `pg_dump` ne sauvegarde pas les rôles. Sans eux, la restauration produit des erreurs `role does not exist`.
   - Sur l'ancien serveur :
     ```bash
     pg_dumpall --globals-only > globals.sql
     ```
   - Sur le nouveau serveur :
     ```bash
     psql -U postgres -f globals.sql postgres
     ```

4. **Crée la base vide** sur le nouveau serveur :
   ```bash
   createdb -U postgres -O proprietaire nom_base
   ```

5. **Restaure la sauvegarde** selon son format.
   - Format *plain* :
     ```bash
     psql -U postgres -d nom_base -v ON_ERROR_STOP=1 -f sauvegarde.sql
     ```
     Pour un fichier `.gz` : `gunzip -c sauvegarde.sql.gz | psql -U postgres -d nom_base`
   - Format custom ou répertoire :
     ```bash
     pg_restore -U postgres -d nom_base -j 4 --no-owner sauvegarde.dump
     ```

   Options utiles :
   - `-j 4` lance 4 tâches en parallèle. Elle ne fonctionne pas avec le format *plain*.
   - `--no-owner` ignore les propriétaires d'origine. Utilise-la si les rôles n'existent pas sur le nouveau serveur.
   - `-C` fait créer la base par `pg_restore`. Dans ce cas, connecte-toi à la base `postgres` avec `-d postgres` et saute l'étape 4.

   **Danger :** n'utilise pas `--clean` sur une base qui contient des données utiles. Cette option supprime les objets existants avant de les recréer.

6. **Mets à jour les statistiques.** Le planificateur de requêtes en a besoin pour choisir de bons plans :
   ```bash
   vacuumdb -U postgres --analyze-only nom_base
   ```

7. **Vérifie le résultat.**
   ```bash
   psql -U postgres -d nom_base -c "\dt"
   psql -U postgres -d nom_base -c "SELECT count(*) FROM ma_table;"
   ```
   Compare ce nombre avec celui de l'ancien serveur.

## Erreurs fréquentes

| Message | Cause | Action |
|---|---|---|
| `role "x" does not exist` | Le rôle manque. | Recrée-le (étape 3) ou ajoute `--no-owner`. |
| `extension "x" is not available` | Le paquet de l'extension manque. | Installe le paquet, puis relance. |
| `unsupported version in file header` | `pg_restore` est plus ancien que la source. | Installe une version égale ou supérieure. |
| `permission denied to create extension` | Le rôle n'est pas superutilisateur. | Restaure avec `postgres`. |

**Attention :** sans `-v ON_ERROR_STOP=1`, `psql` continue après une erreur. Tu obtiens alors une base incomplète sans alerte claire.
## Avant de commencer

Identifie le format du fichier de sauvegarde :

```bash
file sauvegarde.dump
```

- Si le résultat contient « PostgreSQL custom database dump », utilise `pg_restore`.
- Si le résultat indique « ASCII text » ou « SQL », utilise `psql`.

## Procédure

1. Installe PostgreSQL sur le nouveau serveur. Utilise la même version majeure que l'ancien serveur, ou une version plus récente.
2. Installe les paquets des extensions utilisées par la base (PostGIS, pg_trgm, etc.).
3. Copie le fichier de sauvegarde sur le nouveau serveur.
4. Exporte les rôles depuis l'ancien serveur :
   ```bash
   pg_dumpall --globals-only > globals.sql
   ```
5. Importe les rôles sur le nouveau serveur :
   ```bash
   psql -f globals.sql postgres
   ```
6. Crée la base vide :
   ```bash
   createdb -O proprietaire nom_base
   ```
7. Restaure la sauvegarde.

   Format SQL :
   ```bash
   psql -v ON_ERROR_STOP=1 -d nom_base -f sauvegarde.sql
   ```

   Format custom ou directory :
   ```bash
   pg_restore -d nom_base -j 4 sauvegarde.dump
   ```
8. Recalcule les statistiques :
   ```bash
   psql -d nom_base -c "ANALYZE;"
   ```
9. Vérifie la restauration. Compare le nombre de lignes des tables principales avec celui de l'ancien serveur.

## Avertissements

- Ne restaure pas vers une version majeure plus ancienne. Le format de sauvegarde peut être incompatible.
- Ne saute pas l'étape 4. `pg_dump` ne sauvegarde pas les rôles, et la restauration échoue si les propriétaires n'existent pas.
- Ne restaure pas dans une base non vide sans l'option `--clean`. Les objets existants provoquent des erreurs.
- L'option `-j 4` fonctionne seulement avec les formats custom et directory. Ajuste la valeur au nombre de cœurs du serveur.
# Restaurer une sauvegarde `pg_dump` sur un nouveau serveur

La méthode dépend du format de la sauvegarde.

## 1. Identifier le format du dump

- **Fichier `.sql`** (format texte, par défaut) → restauration avec `psql`
- **Fichier `.dump`, `.backup`, `.tar` ou dossier** (formats custom, tar, directory) → restauration avec `pg_restore`

Pour vérifier : `file sauvegarde.dump`

## 2. Préparer le nouveau serveur

Installez PostgreSQL (idéalement la même version majeure, ou plus récente que la source) :

```bash
# Debian/Ubuntu
sudo apt install postgresql

# Vérifier que le service tourne
sudo systemctl status postgresql
```

## 3. Recréer les rôles (important)

`pg_dump` ne sauvegarde **pas** les rôles/utilisateurs, car ce sont des objets globaux. Si votre base en utilise (propriétaires, droits), il faut les créer avant.

Sur l'**ancien** serveur, vous pouvez les exporter :

```bash
pg_dumpall --roles-only -f roles.sql
```

Puis sur le **nouveau** :

```bash
psql -U postgres -f roles.sql
```

Sinon, créez-les manuellement :

```sql
CREATE ROLE mon_user WITH LOGIN PASSWORD 'motdepasse';
```

## 4. Créer la base de données cible

```bash
createdb -U postgres -O mon_user ma_base
```

(ou en SQL : `CREATE DATABASE ma_base OWNER mon_user;`)

## 5. Restaurer

### Cas A : dump au format SQL

```bash
psql -U postgres -d ma_base -f sauvegarde.sql
```

Pour arrêter à la première erreur :

```bash
psql -U postgres -d ma_base -v ON_ERROR_STOP=1 -f sauvegarde.sql
```

### Cas B : dump au format custom/tar/directory

```bash
pg_restore -U postgres -d ma_base -v sauvegarde.dump
```

Options utiles :

| Option | Rôle |
|---|---|
| `-j 4` | Restauration en parallèle (4 jobs), plus rapide |
| `--no-owner` | Ignore les propriétaires d'origine |
| `--no-privileges` | Ignore les GRANT/REVOKE |
| `-C` | Crée la base (à utiliser avec `-d postgres`) |
| `--clean --if-exists` | Supprime les objets avant de les recréer |
| `-1` | Exécute tout dans une seule transaction |

Exemple pour créer la base automatiquement :

```bash
pg_restore -U postgres -C -d postgres sauvegarde.dump
```

## 6. Vérifier la restauration

```bash
psql -U postgres -d ma_base -c '\dt'
psql -U postgres -d ma_base -c 'SELECT count(*) FROM ma_table;'
```

Lancez ensuite une analyse pour mettre à jour les statistiques du planificateur :

```bash
psql -U postgres -d ma_base -c 'ANALYZE;'
```

## Problèmes fréquents

- **`role "xxx" does not exist`** : les rôles n'ont pas été créés (étape 3), ou utilisez `--no-owner`.
- **Extensions manquantes** (PostGIS, etc.) : installez les paquets correspondants sur le nouveau serveur avant la restauration.
- **Erreur de version** : `pg_restore` doit être de version égale ou supérieure à celle de `pg_dump` utilisé.
- **Authentification refusée** : vérifiez `pg_hba.conf`, ou ajoutez `-h localhost` pour passer par TCP.
- **Restauration depuis une machine distante** : ajoutez `-h adresse_ip -p 5432`.

Si vous me dites le format de votre dump, votre système d'exploitation et la version de PostgreSQL, je peux vous donner les commandes exactes.
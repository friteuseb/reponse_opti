## Rôle d'un index

Un index est une structure de données séparée de la table. Il stocke les valeurs d'une ou plusieurs colonnes, triées, avec un pointeur vers la ligne correspondante. Le type le plus courant est l'arbre B (B-tree).

Sans index, le moteur lit toute la table pour trouver une ligne. C'est un *scan complet*. Avec un index B-tree, il descend dans l'arbre. Pour 10 millions de lignes, cela représente environ 24 comparaisons au lieu de 10 millions.

Un index accélère ces opérations :

- `WHERE` sur une colonne indexée ;
- `JOIN` sur les colonnes de jointure ;
- `ORDER BY` et `GROUP BY`, car l'index est déjà trié ;
- les contraintes `UNIQUE` et `PRIMARY KEY`, que le moteur implémente avec un index.

Un *index couvrant* contient toutes les colonnes dont la requête a besoin. Le moteur ne lit alors pas la table.

## Coût d'un index

Un index accélère la lecture, mais il ralentit l'écriture et consomme des ressources.

- Chaque `INSERT`, `UPDATE` et `DELETE` met à jour tous les index de la table.
- L'index occupe de l'espace disque.
- L'index occupe de la mémoire dans le cache.
- L'index demande de la maintenance (`REINDEX`, `VACUUM`, défragmentation selon le moteur).

## Quand éviter de créer un index

| Situation | Raison |
|---|---|
| Table de quelques centaines de lignes | Le scan complet est aussi rapide que l'index. |
| Table à écriture intensive et peu lue (journaux, ingestion de mesures) | Chaque écriture paie le coût de chaque index. |
| Colonne à faible cardinalité (booléen, statut à 3 valeurs) | La requête retourne souvent plus de 10 à 20 % de la table. L'optimiseur préfère alors le scan complet. |
| Colonne absente des `WHERE`, `JOIN` et `ORDER BY` | L'index ne sert à rien. |
| Index redondant | Un index sur `(a, b)` couvre déjà les recherches sur `a`. Un index séparé sur `a` est inutile. |
| Colonne très large (texte long, `BLOB`) | L'index devient gros et lent. |
| Chargement en masse | Les index ralentissent l'import. |

## Cas particuliers

- **Fonction sur la colonne.** `WHERE LOWER(nom) = 'dupont'` n'utilise pas un index sur `nom`. Crée un index fonctionnel sur `LOWER(nom)`.
- **Joker en tête.** `LIKE '%dupont'` n'utilise pas un index B-tree. Utilise un index de texte intégral ou trigramme.
- **Faible cardinalité, valeur rare.** Si tu cherches souvent une valeur rare (par exemple `statut = 'erreur'`), crée un index partiel. PostgreSQL le permet avec `WHERE statut = 'erreur'`.
- **Index composite.** L'ordre des colonnes compte. Le moteur utilise l'index seulement à partir de la première colonne.
- **Chargement en masse.** Supprime les index, charge les données, puis recrée les index. C'est souvent plus rapide que de les maintenir pendant l'import.

## Décider avec des mesures

1. Exécute `EXPLAIN ANALYZE` sur la requête lente. Cherche un scan complet sur une grande table.
2. Crée l'index sur un environnement de test.
3. Compare le temps de la requête avant et après.
4. Mesure l'effet sur les écritures.
5. Vérifie régulièrement l'usage réel. Dans PostgreSQL, consulte `pg_stat_user_indexes`. Dans SQL Server, consulte `sys.dm_db_index_usage_stats`.
6. Supprime les index que personne n'utilise.
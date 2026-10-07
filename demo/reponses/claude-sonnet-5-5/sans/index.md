# À quoi sert un index ?

Un index est une structure de données auxiliaire (le plus souvent un **arbre B** ou B+, parfois une table de hachage, un index bitmap, etc.) qui permet au moteur de base de données de **retrouver rapidement des lignes** sans parcourir toute la table.

**Analogie** : c'est l'index à la fin d'un livre. Plutôt que de lire toutes les pages pour trouver un mot, on consulte l'index qui indique directement les pages concernées.

## Ce qu'un index accélère

- **Les recherches** : `WHERE email = 'a@b.fr'`
- **Les jointures** : `JOIN commandes ON commandes.client_id = clients.id`
- **Les tris** : `ORDER BY date_creation`
- **Les regroupements** : `GROUP BY`
- **Les contraintes d'unicité** : `UNIQUE`, clé primaire

Sans index, le moteur effectue un *full table scan* (complexité O(n)). Avec un index B-tree, la recherche passe en O(log n).

## Exemple

```sql
CREATE INDEX idx_clients_email ON clients(email);
```

## Quand éviter d'en créer ?

Un index n'est pas gratuit. Il a un coût qu'il faut mettre en balance avec le gain.

### 1. Tables à forte écriture
Chaque `INSERT`, `UPDATE` ou `DELETE` doit aussi mettre à jour tous les index concernés. Sur une table de logs ou d'événements écrite en continu, trop d'index dégradent les performances.

### 2. Petites tables
Si la table tient en quelques centaines de lignes, un scan complet est souvent aussi rapide, voire plus rapide, que le passage par l'index.

### 3. Colonnes à faible cardinalité
Un index sur une colonne avec peu de valeurs distinctes (ex. : booléen, sexe, statut avec 3 valeurs) est rarement utile, car il ne filtre pas assez. L'optimiseur l'ignorera souvent. *(Exception : index bitmap ou index partiel dans certains cas.)*

### 4. Colonnes rarement utilisées dans les requêtes
Un index que personne n'emploie consomme de l'espace disque et ralentit les écritures pour rien.

### 5. Requêtes qui lisent une grande partie de la table
Si une requête retourne par exemple 30 % des lignes, le scan séquentiel est généralement plus efficace que des accès aléatoires via l'index.

### 6. Colonnes très volumineuses
Indexer de gros champs (textes longs, JSON, blobs) est coûteux en espace. Mieux vaut utiliser un index spécialisé (full-text, GIN) ou indexer une version réduite (hash, préfixe).

### 7. Index redondants
Si un index composite `(a, b)` existe, un index séparé sur `(a)` est généralement inutile.

## Bonnes pratiques

- **Indexer selon les requêtes réelles**, pas par réflexe. Utiliser `EXPLAIN` / `EXPLAIN ANALYZE` pour vérifier l'usage.
- **Penser à l'ordre des colonnes** dans les index composites.
- **Surveiller et supprimer** les index inutilisés (vues statistiques du SGBD).
- **Utiliser des index partiels** quand seule une portion des données est ciblée (ex. : `WHERE actif = true`).

## En résumé

| Avantage | Inconvénient |
|---|---|
| Lectures beaucoup plus rapides | Écritures plus lentes |
| Tris et jointures optimisés | Espace disque supplémentaire |
| Garantit l'unicité | Maintenance et complexité accrues |

**Règle d'or** : indexer pour les lectures fréquentes et sélectives, éviter pour les tables très sollicitées en écriture ou les colonnes peu discriminantes.
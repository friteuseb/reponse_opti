## À quoi sert un index

Un index est une structure de données séparée de la table. Il associe les valeurs d'une ou plusieurs colonnes à l'emplacement des lignes. Le type le plus courant est l'arbre B (B-tree), qui reste trié.

Sans index, la base lit toute la table pour trouver une ligne. Avec un index, elle descend dans l'arbre et lit seulement les lignes utiles.

**Exemple.** La table `commandes` contient 10 millions de lignes. La requête suivante lit les 10 millions de lignes sans index :

```sql
SELECT * FROM commandes WHERE client_id = 42;
```

Après la création de l'index, la base traverse environ 3 à 4 niveaux d'arbre, puis lit seulement les commandes du client 42 :

```sql
CREATE INDEX idx_commandes_client ON commandes (client_id);
```

## Quand éviter d'en créer

Un index a un coût. Chaque `INSERT`, `UPDATE` et `DELETE` doit le mettre à jour, et il occupe de l'espace disque. Évite d'en créer dans ces cas :

- **Table petite** (quelques milliers de lignes) : le parcours complet est aussi rapide.
- **Colonne à faible cardinalité** (un booléen, par exemple) : l'index filtre mal, et la base l'ignore souvent.
- **Table écrite très souvent et lue rarement** (journaux, logs) : le coût d'écriture dépasse le gain de lecture.
- **Colonne absente des `WHERE`, `JOIN` et `ORDER BY`** : personne n'utilise l'index.
- **Index redondant** : un index sur `(a, b)` sert déjà les requêtes qui filtrent sur `a` seul.

**Limite principale.** Un index n'accélère que les requêtes que la base peut y faire correspondre. Une fonction sur la colonne, comme `WHERE LOWER(nom) = 'dupont'`, empêche souvent son usage. Vérifie toujours le plan d'exécution avec `EXPLAIN` avant et après la création.
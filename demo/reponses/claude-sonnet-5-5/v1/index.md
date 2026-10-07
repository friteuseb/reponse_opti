## Rôle d'un index

Un index est une structure de données séparée de la table. Il trie les valeurs d'une ou plusieurs colonnes et pointe vers les lignes correspondantes. Le moteur l'utilise pour trouver des lignes sans lire toute la table.

Exemple : une table contient 10 millions de lignes. Sans index, la requête `WHERE email = 'a@b.fr'` lit les 10 millions de lignes. Avec un index B-tree sur `email`, le moteur lit 3 ou 4 pages d'index, puis la ligne.

Un index accélère :

- les filtres (`WHERE`) ;
- les jointures (`JOIN`) ;
- les tris (`ORDER BY`) ;
- le contrôle d'unicité (`UNIQUE`).

## Coût d'un index

Chaque index a un prix :

- **Écriture** : le moteur met à jour l'index à chaque `INSERT`, `UPDATE` et `DELETE`.
- **Espace** : l'index occupe du disque et de la mémoire.
- **Maintenance** : l'index peut se fragmenter et demander une reconstruction.

## Quand éviter un index

| Cas | Raison |
|---|---|
| Table de quelques milliers de lignes | Le scan complet est aussi rapide. |
| Table surtout écrite, rarement lue (logs, journaux) | Le coût d'écriture dépasse le gain de lecture. |
| Colonne à faible cardinalité (booléen, statut à 3 valeurs) | L'index sépare mal les lignes. |
| Colonne absente des `WHERE`, `JOIN` et `ORDER BY` | Le moteur n'utilise jamais l'index. |
| Requête qui lit plus de 10 à 20 % de la table | L'optimiseur choisit le scan complet. |
| Index en doublon, par exemple `(a)` quand `(a, b)` existe | L'index `(a, b)` couvre déjà les recherches sur `a`. |

Deux pièges méritent une vérification :

- Une fonction sur la colonne désactive l'index. `WHERE LOWER(email) = ...` n'utilise pas un index sur `email`. Crée un index sur l'expression `LOWER(email)`.
- Un index partiel convient à une colonne à faible cardinalité si tu cherches la valeur rare. Exemple : `WHERE statut = 'en_erreur'`.

## Méthode

1. Repère les requêtes lentes.
2. Exécute `EXPLAIN` (ou `EXPLAIN ANALYZE`) sur chacune.
3. Crée l'index seulement si le plan montre un scan complet coûteux.
4. Relance `EXPLAIN` et compare les temps.
5. Supprime les index que le moteur n'utilise pas.
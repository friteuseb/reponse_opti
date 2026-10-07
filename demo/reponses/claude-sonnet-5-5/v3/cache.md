Un cache est une copie temporaire de données, rangée à un endroit plus rapide d'accès que la source d'origine.

## Mécanisme

Quand l'application a besoin d'une donnée, elle regarde d'abord dans le cache.

- **Hit** : la donnée est dans le cache. L'application la lit directement.
- **Miss** : la donnée est absente. L'application la demande à la source, puis en garde une copie dans le cache.

Le gain vient de l'écart de vitesse entre les deux emplacements. Une lecture dans la mémoire du processus prend environ 100 ns. Une requête SQL à travers le réseau prend de 1 à 10 ms. Le cache évite donc le trajet le plus lent pour les données déjà demandées.

## Exemple

Une page produit demande une requête SQL de 20 ms. Avec un cache, la première visite coûte 21 ms (requête, plus écriture dans le cache). Les visites suivantes coûtent 1 ms.

Avec 95 % de hits, le temps moyen tombe à environ 2 ms au lieu de 20 ms. La base de données reçoit aussi 20 fois moins de requêtes.

## Limite principale

Le cache contient une copie. Si la source change, la copie devient fausse, et l'application sert alors une donnée périmée.

Deux mécanismes limitent ce risque :

- **TTL** (durée de vie) : le cache supprime la copie après un délai fixé, par exemple 60 s.
- **Invalidation** : l'application supprime la copie dès qu'elle modifie la source.

Un TTL court réduit le risque de donnée périmée, mais il réduit aussi le taux de hits. Il faut choisir selon la tolérance de l'application à une donnée un peu ancienne.
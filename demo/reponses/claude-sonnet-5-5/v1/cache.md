## Définition

Un cache est une copie temporaire de données. Il se trouve à un endroit plus rapide d'accès que la source d'origine. L'application lit d'abord le cache. Si la donnée y est, elle ne contacte pas la source.

## Pourquoi le cache accélère l'application

- **Support plus rapide.** Le cache réside souvent en RAM, alors que la source est un disque, une base de données ou une API distante.
- **Résultat déjà calculé.** Le cache garde la réponse d'une requête ou d'un calcul. L'application ne le refait pas.

Ordres de grandeur de latence :

| Support | Latence approximative |
|---|---|
| Cache du processeur (L1) | 1 ns |
| RAM | 100 ns |
| SSD | 100 µs |
| Requête de base de données via le réseau | 1 à 10 ms |
| Appel d'une API distante | 50 à 500 ms |

Une lecture en RAM est donc 10 000 à 100 000 fois plus rapide qu'une requête de base de données via le réseau.

## Fonctionnement

1. L'application demande une donnée.
2. Elle cherche la donnée dans le cache.
3. Si le cache contient la donnée (*cache hit*), l'application la renvoie.
4. Sinon (*cache miss*), l'application lit la source, copie la donnée dans le cache, puis la renvoie.

Le cache fonctionne parce que les applications relisent souvent les mêmes données. Si 95 % des lectures aboutissent à un *cache hit*, seules 5 % des lectures atteignent la source lente.

## Limites

- **Taille limitée.** Quand le cache est plein, il supprime des données. La politique LRU supprime la donnée la moins récemment utilisée.
- **Données périmées.** La source change, mais le cache garde l'ancienne valeur. Définis une durée de vie (TTL) ou invalide l'entrée à chaque modification de la source.
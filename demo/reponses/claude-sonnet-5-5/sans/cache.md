# Qu'est-ce qu'un cache ?

Un **cache** est une zone de stockage temporaire, rapide d'accès, où l'on garde une copie de données déjà obtenues ou calculées, afin de ne pas avoir à les récupérer ou les recalculer à chaque fois.

## Une analogie simple

Imagine que tu cuisines. Au lieu d'aller chercher le sel à la cave à chaque fois, tu le gardes sur le plan de travail. La cave, c'est la source d'origine (lente) ; le plan de travail, c'est le cache (rapide).

## Pourquoi ça accélère une application ?

1. **Les sources de données sont lentes**
   Une base de données, une API distante ou un disque dur demandent du temps (latence réseau, lecture sur disque, requêtes complexes). Le cache, souvent en mémoire vive (RAM), répond beaucoup plus vite.

2. **On évite de refaire le même travail**
   Si un calcul coûteux ou une requête donne toujours le même résultat, on le fait une seule fois et on réutilise la réponse.

3. **On réduit la charge sur le système**
   Moins de requêtes vers la base de données ou le serveur, donc moins de saturation et une meilleure capacité à encaisser beaucoup d'utilisateurs.

4. **Le principe de localité**
   Les programmes ont tendance à réutiliser les mêmes données (localité temporelle) ou des données voisines (localité spatiale). Le cache exploite ce comportement.

## Comment ça fonctionne ?

- **Cache hit** : la donnée est dans le cache → réponse immédiate.
- **Cache miss** : la donnée n'y est pas → on va la chercher à la source, puis on la stocke dans le cache pour la prochaine fois.

## Exemples courants

| Niveau | Exemple |
|---|---|
| Processeur | Caches L1, L2, L3 |
| Navigateur | Images, CSS, JavaScript stockés localement |
| Web | CDN (copies de contenu proches de l'utilisateur) |
| Application | Redis, Memcached pour stocker des résultats de requêtes |
| Système | Cache disque du système d'exploitation |

## Les limites et défis

- **Fraîcheur des données** : si la source change, le cache peut contenir une version périmée. On utilise donc des durées d'expiration (TTL) ou des mécanismes d'invalidation.
- **Taille limitée** : on doit décider quoi supprimer quand il est plein (par ex. politique LRU : on retire ce qui a été utilisé le moins récemment).
- **Complexité** : comme le dit la célèbre blague, *« il n'y a que deux choses difficiles en informatique : l'invalidation de cache et nommer les choses »*.

## En résumé

Un cache accélère une application en gardant à portée de main les données fréquemment utilisées, ce qui évite des opérations lentes et coûteuses. Le compromis : un peu de mémoire en plus et la gestion de la fraîcheur des données.
## Définition

Un cache est une copie temporaire de données, stockée à un endroit plus rapide d'accès que la source. La source est l'endroit d'origine : base de données, disque, API distante, calcul coûteux.

L'application lit d'abord le cache. Si la donnée y est, c'est un **succès** (*cache hit*). Sinon, c'est un **échec** (*cache miss*) : l'application lit la source, puis copie le résultat dans le cache.

## Pourquoi le cache accélère l'application

Deux faits expliquent le gain.

1. **Le cache est plus rapide que la source.** Il utilise un support plus rapide, ou il évite un calcul ou un trajet réseau.
2. **Les accès se répètent.** Une application relit souvent les mêmes données (localité temporelle) ou des données voisines (localité spatiale).

Ordres de grandeur d'un accès :

| Support | Durée approximative |
|---|---|
| Cache L1 du processeur | 1 ns |
| Mémoire vive (RAM) | 100 ns |
| SSD | 100 µs |
| Réseau dans un centre de données | 0,5 ms |
| Disque dur (HDD) | 10 ms |
| Aller-retour réseau intercontinental | 100 à 150 ms |

Un cache en RAM, placé devant un disque dur, réduit donc l'accès d'un facteur 100 000 environ.

## Calculer le gain

Le temps moyen d'accès dépend du taux de succès :

`temps moyen = taux × temps du cache + (1 − taux) × temps de la source`

Exemple avec un cache à 1 ms et une source à 100 ms :

- Taux de succès de 90 % : 0,9 × 1 + 0,1 × 100 = **10,9 ms**.
- Taux de succès de 99 % : 0,99 × 1 + 0,01 × 100 = **environ 2 ms**.

Le taux de succès compte donc plus que la vitesse du cache. Passer de 90 % à 99 % divise le temps moyen par 5.

## Où l'on trouve des caches

- **Processeur** : caches L1, L2 et L3 devant la RAM.
- **Système d'exploitation** : le *page cache* garde en RAM les fichiers lus récemment.
- **Navigateur** : il garde les images, scripts et feuilles de style.
- **CDN** : il garde les contenus statiques près de l'utilisateur.
- **Application** : Redis ou Memcached gardent des résultats de requêtes SQL ou d'appels d'API.
- **Base de données** : elle garde en mémoire les pages de données et les plans de requêtes.

## Limites et précautions

Le cache a un coût. Il consomme de la mémoire, et sa taille est limitée. Quand il est plein, une **politique d'éviction** choisit les données à supprimer :

- **LRU** (*Least Recently Used*) : supprime la donnée lue le moins récemment.
- **LFU** (*Least Frequently Used*) : supprime la donnée lue le moins souvent.
- **FIFO** : supprime la donnée la plus ancienne dans le cache.
- **TTL** (*Time To Live*) : supprime la donnée après une durée fixée.

Le risque principal est la **donnée périmée**. La source change, mais le cache garde l'ancienne valeur. Deux solutions existent :

- Définir un TTL, par exemple 60 s.
- Invalider l'entrée du cache à chaque modification de la source.

Autres cas à connaître :

- **Démarrage à froid** : un cache vide produit 100 % d'échecs. L'application est lente jusqu'au remplissage.
- **Cache stampede** : une entrée populaire expire, et des centaines de requêtes lisent la source en même temps. Un verrou ou un TTL aléatoire limite ce risque.
- **Cohérence** : plusieurs caches peuvent contenir des valeurs différentes pour la même donnée.

Ne mets pas en cache des données qui changent à chaque requête. Le taux de succès reste proche de 0 %, et le cache ajoute un coût sans gain.
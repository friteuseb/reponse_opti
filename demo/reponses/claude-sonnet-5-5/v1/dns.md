## Principe

Le DNS traduit un nom de domaine (`www.exemple.com`) en adresse IP. Le navigateur a besoin de cette adresse IP pour ouvrir une connexion.

## Les étapes

Exemple : tu tapes `www.exemple.com`.

1. Le navigateur vérifie son cache DNS. Si l'entrée existe et n'a pas expiré, la résolution s'arrête ici.
2. Le navigateur demande au système d'exploitation. Le système vérifie son cache, puis le fichier `hosts`.
3. Le système envoie la requête au résolveur récursif. C'est celui de ton fournisseur d'accès, ou un résolveur public comme `1.1.1.1` ou `8.8.8.8`.
4. Le résolveur vérifie son cache. S'il n'a rien, il interroge un serveur racine. Le serveur racine renvoie les serveurs du TLD `.com`.
5. Le résolveur interroge un serveur du TLD. Ce serveur renvoie les serveurs faisant autorité pour `exemple.com`.
6. Le résolveur interroge un serveur faisant autorité. Ce serveur renvoie l'enregistrement demandé, par exemple l'adresse IP.
7. Le résolveur garde la réponse en cache pendant la durée du TTL. Il la renvoie ensuite au système, qui la renvoie au navigateur.
8. Le navigateur ouvre la connexion vers l'adresse IP, puis négocie TLS et envoie la requête HTTP.

## Les enregistrements courants

| Type | Contenu |
|---|---|
| A | Adresse IPv4 |
| AAAA | Adresse IPv6 |
| CNAME | Alias vers un autre nom |
| MX | Serveur de messagerie du domaine |
| TXT | Texte libre (SPF, vérification de domaine) |
| NS | Serveurs faisant autorité pour la zone |

## Cache et TTL

Chaque enregistrement porte un TTL, exprimé en secondes. Un TTL de 300 signifie que les caches gardent la réponse 5 minutes. Un TTL court propage un changement plus vite. Un TTL long réduit le nombre de requêtes.

## Transport

- Les requêtes classiques utilisent UDP sur le port 53.
- Le résolveur bascule sur TCP si la réponse est trop grande.
- DoT (DNS over TLS) et DoH (DNS over HTTPS) chiffrent la requête entre ton appareil et le résolveur.

## Durée

Une réponse en cache prend moins de 1 ms. Une résolution complète prend souvent entre 20 et 100 ms.

## Tester

Lance `dig +trace www.exemple.com`. La commande affiche chaque étape : racine, TLD, puis serveur faisant autorité.
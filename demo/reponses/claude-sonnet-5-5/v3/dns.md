Le DNS traduit un nom de domaine en adresse IP. Le navigateur a besoin de cette adresse pour ouvrir une connexion, car les routeurs ne comprennent pas les noms.

## Mécanisme

Prenons l'exemple de `www.exemple.fr` :

1. Le navigateur cherche d'abord dans son cache, puis dans celui du système. Si l'adresse y figure, la recherche s'arrête.
2. Sinon, le système envoie la question au résolveur. C'est le serveur DNS de votre fournisseur d'accès, ou un résolveur public comme 1.1.1.1.
3. Si le résolveur n'a pas la réponse en cache, il interroge un serveur racine. Celui-ci ne connaît pas l'adresse, mais il indique les serveurs de la zone `.fr`.
4. Le résolveur interroge un serveur de la zone `.fr`. Celui-ci indique les serveurs faisant autorité pour `exemple.fr`.
5. Le résolveur interroge un serveur faisant autorité. Celui-ci répond avec l'adresse IP, par exemple `203.0.113.10`.
6. Le résolveur renvoie l'adresse au navigateur et la garde en cache.

Le navigateur ouvre ensuite la connexion vers `203.0.113.10`.

## Limites principales

- **Le cache retarde les changements.** Chaque réponse porte une durée de vie (TTL), souvent entre 300 s et 86 400 s. Si vous modifiez un enregistrement, certains utilisateurs voient l'ancienne adresse jusqu'à l'expiration du TTL.
- **Le DNS classique n'est pas chiffré.** Les requêtes passent en clair sur le port 53. Le résolveur et le réseau local voient donc les noms que vous consultez. DNS over HTTPS (DoH) et DNS over TLS (DoT) corrigent ce point.
# Fonctionnement du DNS lors d'une requête dans le navigateur

Le DNS (Domain Name System) traduit un nom de domaine en adresse IP. Le navigateur a besoin de cette adresse pour ouvrir une connexion. Les exemples ci-dessous utilisent `www.exemple.fr`.

## Les acteurs

| Terme | Rôle |
|---|---|
| Résolveur local | Le logiciel du système d'exploitation qui envoie les requêtes DNS. |
| Résolveur récursif | Le serveur qui cherche la réponse pour toi. Exemples : ta box, `1.1.1.1`, `8.8.8.8`. |
| Serveur racine | Il connaît les serveurs de chaque extension (`.fr`, `.com`, etc.). |
| Serveur TLD | Il connaît les serveurs de chaque domaine d'une extension. |
| Serveur faisant autorité | Il détient les enregistrements du domaine. Il donne la réponse définitive. |

## Les étapes

1. Tu tapes `www.exemple.fr`. Le navigateur extrait le nom d'hôte.
2. Le navigateur consulte son cache DNS. S'il trouve une IP valide, il saute à l'étape 10.
3. Le navigateur demande au système d'exploitation. Le système lit d'abord le fichier `hosts`, puis son propre cache.
4. Le système envoie la requête au résolveur récursif. Le DHCP fournit son adresse, ou tu la configures à la main.
5. Le résolveur récursif consulte son cache. Il répond tout de suite s'il connaît la réponse.
6. Sinon, il interroge un serveur racine. Celui-ci ne donne pas l'IP. Il renvoie vers les serveurs de `.fr`.
7. Le résolveur récursif interroge un serveur de `.fr`. Celui-ci renvoie vers les serveurs de noms de `exemple.fr` (enregistrements NS).
8. Le résolveur récursif interroge le serveur faisant autorité de `exemple.fr`. Celui-ci renvoie l'enregistrement A (IPv4) ou AAAA (IPv6) de `www.exemple.fr`.
9. Le résolveur récursif garde la réponse en cache pendant la durée du TTL. Il la transmet au système, qui la transmet au navigateur.
10. Le navigateur ouvre une connexion vers l'IP. Il négocie TLS, puis envoie la requête HTTP.

Les étapes 6 à 8 forment la résolution récursive. Elles ne se produisent que si aucun cache ne contient la réponse. Dans la pratique, les caches répondent à la grande majorité des requêtes.

## Les enregistrements courants

| Type | Contenu |
|---|---|
| A | Adresse IPv4 |
| AAAA | Adresse IPv6 |
| CNAME | Alias vers un autre nom |
| NS | Serveurs de noms du domaine |
| MX | Serveurs de messagerie |
| TXT | Texte libre (SPF, vérifications de propriété) |

## Le cache et le TTL

Chaque enregistrement porte un TTL (Time To Live), en secondes. Il indique combien de temps un cache peut garder la réponse. Les valeurs courantes vont de 300 s (5 min) à 86 400 s (24 h).

Une modification d'enregistrement n'apparaît donc pas partout en même temps. Chaque cache attend la fin de son TTL. Pour préparer une migration, baisse le TTL au moins un TTL entier avant le changement.

## Les cas particuliers

- **CNAME** : si `www.exemple.fr` est un alias, le résolveur récursif suit la chaîne jusqu'à un enregistrement A ou AAAA.
- **Domaine inexistant** : le serveur faisant autorité répond `NXDOMAIN`. Les résolveurs mettent aussi cette réponse en cache.
- **Transport** : le DNS utilise UDP sur le port 53. Il passe en TCP si la réponse est trop grande pour un paquet UDP.
- **Chiffrement** : DoT (DNS over TLS) utilise le port 853. DoH (DNS over HTTPS) utilise le port 443. Les deux cachent tes requêtes au réseau local.
- **DNSSEC** : les serveurs signent leurs réponses. Le résolveur vérifie la signature et détecte une réponse falsifiée.
- **Plusieurs IP** : un serveur faisant autorité peut renvoyer plusieurs adresses. Le client en choisit une.

## Observer une résolution

Interroge le résolveur récursif par défaut :

```
dig www.exemple.fr
```

Interroge un résolveur précis :

```
dig @1.1.1.1 www.exemple.fr A
```

Suis toute la chaîne, de la racine au serveur faisant vautorité :

```
dig +trace www.exemple.fr
```

Dans la réponse, la colonne qui suit le nom donne le TTL restant en secondes.

## Vider les caches

Vide le cache du système quand une ancienne IP persiste.

- Windows : `ipconfig /flushdns`
- macOS : `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- Linux (systemd-resolved) : `resolvectl flush-caches`

Le cache du navigateur est séparé. Redémarre le navigateur pour le vider. Tu ne peux pas vider le cache du résolveur récursif d'un fournisseur tiers. Certains, comme `1.1.1.1` et `8.8.8.8`, proposent une page web pour purger un nom.

## Mise en garde

Ne modifie pas le fichier `hosts` sans sauvegarde. Une erreur de syntaxe ou une ligne oubliée peut rediriger un site vers une mauvaise IP pendant des jours sans que tu t'en souviennes.
# Fonctionnement du DNS lors de la saisie d'une adresse

Le DNS (*Domain Name System*) est l'« annuaire » d'Internet : il traduit un nom lisible (ex. `www.exemple.fr`) en adresse IP (ex. `93.184.216.34`), seule information que les machines utilisent réellement pour communiquer.

## Les étapes, de la saisie à la réponse

### 1. Vérification des caches locaux
Avant tout, le navigateur cherche si l'adresse est déjà connue :
- **Cache du navigateur** : il garde en mémoire les résolutions récentes.
- **Cache du système d'exploitation** : si le navigateur ne sait pas, il interroge l'OS.
- **Fichier `hosts`** : un fichier local qui peut associer manuellement des noms à des IP.

Si une réponse est trouvée, tout s'arrête ici : c'est le cas le plus rapide.

### 2. Requête au résolveur DNS
Sinon, l'ordinateur envoie la question à un **résolveur récursif** (aussi appelé « serveur DNS récursif »). Il s'agit généralement de celui de votre fournisseur d'accès (box Internet), ou d'un service public comme Cloudflare (`1.1.1.1`), Google (`8.8.8.8`) ou Quad9.

Le résolveur a aussi un cache. Si quelqu'un a récemment demandé le même site, il répond immédiatement.

### 3. Résolution hiérarchique (si rien en cache)
Le résolveur interroge alors successivement plusieurs serveurs, en descendant la hiérarchie du nom, qui se lit **de droite à gauche** :

1. **Serveurs racine** (`.`) : il y en a 13 groupes dans le monde. Ils ne connaissent pas l'IP, mais indiquent qui gère l'extension `.fr`.
2. **Serveurs TLD** (*Top-Level Domain*, ex. `.fr`, `.com`, `.org`) : ils indiquent quels serveurs gèrent `exemple.fr`.
3. **Serveurs faisant autorité** (*authoritative*) : ce sont eux qui détiennent les enregistrements du domaine et fournissent l'adresse IP finale de `www.exemple.fr`.

### 4. Retour de la réponse
Le résolveur renvoie l'IP à votre ordinateur et la **met en cache** pour une durée définie par le **TTL** (*Time To Live*) de l'enregistrement.

### 5. Connexion au site
Une fois l'IP connue, le navigateur ouvre une connexion (TCP, puis TLS pour HTTPS) vers ce serveur et envoie sa requête HTTP. Le DNS a fini son travail.

## Schéma simplifié

```
Navigateur → Cache OS → Résolveur récursif
                              │
                              ├─→ Serveur racine   : « Demande aux serveurs .fr »
                              ├─→ Serveur TLD .fr  : « Demande aux serveurs de exemple.fr »
                              └─→ Serveur autoritaire : « www.exemple.fr = 93.184.216.34 »
                              │
Navigateur ← IP ←─────────────┘
```

## Types d'enregistrements courants

| Type | Rôle |
|------|------|
| **A** | Associe un nom à une adresse IPv4 |
| **AAAA** | Associe un nom à une adresse IPv6 |
| **CNAME** | Alias vers un autre nom |
| **MX** | Serveurs de messagerie du domaine |
| **NS** | Serveurs DNS faisant autorité |
| **TXT** | Texte libre (vérifications, SPF, etc.) |

## À retenir

- Le DNS repose sur un **système hiérarchique et distribué** : aucun serveur ne connaît tout.
- Les **caches** à chaque niveau rendent la résolution généralement quasi instantanée.
- Le DNS classique utilise surtout **UDP sur le port 53**, mais des variantes chiffrées existent (**DoH**, **DoT**) pour protéger la confidentialité des requêtes.

Si vous voulez, je peux détailler un point précis : la sécurité (DNSSEC), les caches et le TTL, ou comment tester tout cela avec des commandes comme `nslookup` ou `dig`.
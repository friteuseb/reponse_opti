# Fonctionnement de « Se connecter avec Google »

Le bouton utilise **OpenID Connect (OIDC)**, une couche d'identité au-dessus d'**OAuth 2.0**. Le site ne reçoit jamais le mot de passe de l'utilisateur. Google authentifie l'utilisateur, puis il envoie au site une preuve d'identité signée.

## Les acteurs

| Acteur | Rôle |
|---|---|
| Utilisateur | Possède le compte Google. |
| Site | Demande l'identité de l'utilisateur. On l'appelle aussi « client ». |
| Google | Authentifie l'utilisateur et émet les jetons. |

## Préparation par le développeur

1. Crée un projet dans la Google Cloud Console.
2. Configure l'écran de consentement OAuth.
3. Crée un identifiant OAuth de type « Application Web ». Google fournit un `client_id` et un `client_secret`.
4. Déclare les URI de redirection autorisées, par exemple `https://monsite.fr/auth/callback`.

Garde le `client_secret` côté serveur. Ne l'envoie jamais au navigateur.

## Déroulement (flux « code d'autorisation »)

1. L'utilisateur clique sur le bouton Google.
2. Le site génère trois valeurs aléatoires : `state`, `nonce` et, avec PKCE, un `code_verifier`.
3. Le site redirige le navigateur vers `https://accounts.google.com/o/oauth2/v2/auth` avec ces paramètres :
   - `client_id`
   - `redirect_uri`
   - `response_type=code`
   - `scope=openid email profile`
   - `state`, `nonce`
   - `code_challenge` et `code_challenge_method=S256` (PKCE)
4. Google affiche sa page de connexion. L'utilisateur saisit son mot de passe sur le domaine de Google, jamais sur le site.
5. Google affiche l'écran de consentement. L'utilisateur accepte de partager son e-mail et son profil.
6. Google redirige le navigateur vers l'`redirect_uri` du site avec un `code` et le `state`.
7. Le site compare le `state` reçu à celui qu'il a stocké. Si les valeurs diffèrent, il rejette la requête.
8. Le serveur du site envoie le `code` à `https://oauth2.googleapis.com/token`. Il joint le `client_id`, le `client_secret`, le `redirect_uri` et le `code_verifier`.
9. Google répond avec un **jeton d'identité** (JWT) et un **jeton d'accès**.
10. Le site valide le jeton d'identité (voir ci-dessous).
11. Le site lit les informations de l'utilisateur dans le jeton.
12. Le site cherche un compte lié à cet identifiant. Il en crée un si aucun n'existe.
13. Le site ouvre sa propre session, généralement avec un cookie `HttpOnly` et `Secure`.

## Contenu du jeton d'identité

Le jeton d'identité est un JWT signé par Google. Il contient ces champs (« claims ») :

| Champ | Signification |
|---|---|
| `iss` | Émetteur : `https://accounts.google.com` |
| `aud` | Destinataire : le `client_id` du site |
| `sub` | Identifiant unique et stable de l'utilisateur |
| `exp` | Date d'expiration |
| `nonce` | Valeur générée à l'étape 2 |
| `email`, `email_verified` | Adresse e-mail et son état de vérification |
| `name`, `picture` | Nom et photo (scope `profile`) |

## Validation du jeton d'identité

Valide chaque point suivant avant de faire confiance au jeton :

1. Vérifie la signature avec les clés publiques de Google (JWKS : `https://www.googleapis.com/oauth2/v3/certs`).
2. Vérifie que `iss` vaut `https://accounts.google.com`.
3. Vérifie que `aud` est égal à ton `client_id`.
4. Vérifie que `exp` n'est pas dépassé.
5. Vérifie que `nonce` correspond à la valeur stockée.

Utilise une bibliothèque officielle ou reconnue. N'écris pas ta propre validation JWT.

## Bonnes pratiques de sécurité

- Utilise `sub` comme identifiant du compte. N'utilise pas `email`, car une adresse peut changer.
- Vérifie `email_verified` avant de faire confiance à l'adresse.
- Déclare des URI de redirection exactes, en HTTPS. Évite les jokers.
- Utilise toujours `state` pour bloquer les attaques CSRF.
- Utilise `nonce` pour bloquer le rejeu d'un jeton.
- Utilise PKCE, même avec un client confidentiel.
- Demande le minimum de scopes.
- Ne lie pas automatiquement un compte Google à un compte existant du même e-mail sans confirmation. Un attaquant pourrait prendre ce compte.

## Variante : Google Identity Services

Le bouton moderne de Google (bibliothèque JavaScript GIS, One Tap) simplifie le flux côté navigateur :

1. Le navigateur charge le script de Google et affiche le bouton.
2. Après la connexion, Google transmet directement un jeton d'identité (`credential`) au JavaScript du site.
3. Le front envoie ce jeton au serveur.
4. Le serveur valide le jeton comme décrit plus haut, puis ouvre la session.

Ce flux n'échange pas de `code` et n'utilise pas de `client_secret`. Il fournit l'identité, mais pas de jeton d'accès pour appeler d'autres API Google.

## Révocation

L'utilisateur retire l'accès du site depuis son compte Google, dans la section « Sécurité » puis « Connexion via Google ». Le site garde sa propre session jusqu'à son expiration. Les nouvelles connexions demandent de nouveau le consentement.
## Principe

« Se connecter avec Google » utilise le protocole **OpenID Connect (OIDC)**. OIDC ajoute une couche d'identité à **OAuth 2.0**. Le site ne reçoit jamais le mot de passe de l'utilisateur. Google authentifie l'utilisateur, puis il envoie au site une preuve signée de son identité.

## Les trois acteurs

| Acteur | Rôle |
|---|---|
| Utilisateur | Se connecte avec son compte Google |
| Site | Demande l'identité de l'utilisateur |
| Google | Authentifie l'utilisateur et émet les jetons |

## Déroulement (flux « code d'autorisation »)

1. L'utilisateur clique sur le bouton « Se connecter avec Google ».
2. Le site redirige le navigateur vers Google. L'URL contient `client_id`, `redirect_uri`, `scope` (par exemple `openid email profile`), `state` et `code_challenge`.
3. Google affiche sa page de connexion. L'utilisateur saisit ses identifiants et accepte le partage de ses informations.
4. Google redirige le navigateur vers la `redirect_uri` du site. L'URL contient un `code` à usage unique et le `state`.
5. Le serveur du site vérifie que le `state` correspond à celui de l'étape 2.
6. Le serveur du site envoie le `code`, son `client_secret` et le `code_verifier` à Google, directement, sans passer par le navigateur.
7. Google répond avec un **jeton d'identité** (ID token) et un **jeton d'accès**.
8. Le serveur du site vérifie le jeton d'identité, puis ouvre une session pour l'utilisateur.

## Contenu du jeton d'identité

Le jeton d'identité est un JWT signé par Google. Il contient ces champs (appelés « claims ») :

- `sub` : identifiant unique et stable de l'utilisateur chez Google
- `email` et `email_verified` : adresse e-mail et son état de vérification
- `name` et `picture` : nom et photo du profil
- `aud` : le `client_id` du site
- `iss` : l'émetteur, `https://accounts.google.com`
- `exp` : la date d'expiration

## Vérifications obligatoires côté site

Le serveur du site vérifie chaque point avant d'accepter le jeton d'identité :

- La signature correspond aux clés publiques de Google.
- `iss` et `aud` ont les bonnes valeurs.
- `exp` n'est pas dépassé.
- Le `nonce`, s'il existe, correspond à celui envoyé.

Utilise `sub` comme identifiant du compte, pas `email`. L'adresse e-mail peut changer, alors que `sub` reste identique.

## Protections contre les attaques

| Élément | Protège contre |
|---|---|
| `state` | Les attaques CSRF sur la redirection |
| PKCE (`code_challenge`) | Le vol du `code` en transit |
| `nonce` | Le rejeu d'un jeton d'identité |
| `redirect_uri` exacte | La redirection vers un site pirate |
| `client_secret` côté serveur | L'usurpation du site auprès de Google |

## Variante : Google Identity Services

Le bouton JavaScript de Google simplifie le flux. Le navigateur reçoit directement le jeton d'identité, puis le transmet au serveur du site. Le serveur applique les mêmes vérifications.
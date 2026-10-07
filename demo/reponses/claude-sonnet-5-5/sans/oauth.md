# Fonctionnement de « Se connecter avec Google »

Ce bouton repose sur les protocoles **OAuth 2.0** (autorisation) et **OpenID Connect** (OIDC, authentification, qui s'appuie sur OAuth 2.0). L'idée : le site ne gère pas ton mot de passe, il délègue la vérification de ton identité à Google.

## Les acteurs

- **L'utilisateur** : toi.
- **Le client (Relying Party)** : le site ou l'application qui affiche le bouton.
- **Le fournisseur d'identité (IdP)** : Google, qui authentifie l'utilisateur.

## Le déroulement (flux « Authorization Code »)

1. **Clic sur le bouton** : le site redirige ton navigateur vers Google avec plusieurs paramètres : son `client_id`, l'URL de retour (`redirect_uri`), les informations demandées (`scope`, par ex. `openid email profile`), et un paramètre `state` anti-falsification (CSRF).

2. **Authentification chez Google** : tu te connectes sur le domaine de Google (si tu ne l'es pas déjà), éventuellement avec la double authentification. Le site ne voit jamais ton mot de passe.

3. **Consentement** : Google t'indique quelles informations le site demande (nom, e-mail, photo…) et tu acceptes ou refuses.

4. **Retour vers le site** : Google te redirige vers le `redirect_uri` avec un **code d'autorisation** temporaire.

5. **Échange du code** : le serveur du site contacte directement Google (de serveur à serveur) avec ce code et son `client_secret`. Google renvoie :
   - un **ID token** (un JWT signé contenant l'identité : identifiant unique `sub`, e-mail, nom…),
   - un **access token** (pour appeler les API Google si besoin),
   - parfois un **refresh token**.

6. **Vérification et ouverture de session** : le site vérifie la signature de l'ID token, l'émetteur, l'audience et la date d'expiration. Il crée ou retrouve ton compte, puis ouvre une session classique (cookie).

## Pourquoi c'est sécurisé

- Le mot de passe reste chez Google.
- Le code d'autorisation est à usage unique et de courte durée.
- Le `state` protège contre les attaques CSRF, et PKCE protège contre l'interception du code (notamment pour les applications mobiles et les SPA).
- Les jetons sont signés cryptographiquement.
- L'`redirect_uri` doit être préenregistré auprès de Google, ce qui empêche les redirections vers des sites malveillants.

## Côté développeur

- Créer un projet dans la **Google Cloud Console**, puis des identifiants OAuth (client ID et secret).
- Déclarer les URI de redirection autorisées.
- Intégrer le bouton (Google Identity Services) ou une bibliothèque OAuth/OIDC.
- Côté serveur, valider l'ID token et lier l'identifiant `sub` à un compte utilisateur (plutôt que l'e-mail seul, qui peut changer).

## Avantages et limites

**Avantages** : inscription rapide, pas de mot de passe supplémentaire à retenir, sécurité déléguée à Google.

**Limites** : dépendance à Google (si ton compte est suspendu, tu perds l'accès), partage de certaines données personnelles, et suivi potentiel de tes usages.

Si tu veux, je peux détailler un exemple de code (Node.js, Python, etc.) ou expliquer la différence entre OAuth et OpenID Connect.
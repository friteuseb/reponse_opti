## Le principe

Le bouton utilise le protocole **OpenID Connect**, construit sur OAuth 2.0. Le site ne voit jamais ton mot de passe. Google authentifie l'utilisateur, puis donne au site une preuve de son identité.

## Le déroulement

1. L'utilisateur clique sur « Se connecter avec Google ».
2. Le site redirige le navigateur vers Google, avec son identifiant client et une URL de retour.
3. Google affiche sa page de connexion. L'utilisateur saisit son mot de passe et accepte de partager son profil.
4. Google redirige le navigateur vers le site, avec un **code d'autorisation** à usage unique dans l'URL.
5. Le serveur du site envoie ce code à Google, avec son **secret client**.
6. Google répond avec un **jeton d'identité** signé. Il contient l'identifiant unique de l'utilisateur (`sub`), son e-mail et son nom.
7. Le site vérifie la signature du jeton, puis ouvre une session pour l'utilisateur.

Le code transite par le navigateur, mais il ne sert à rien sans le secret client. Seul le serveur du site connaît ce secret. Un pirate qui intercepte le code ne peut donc pas obtenir de jeton.

## La limite principale

Le site dépend de Google. Si l'utilisateur perd l'accès à son compte Google ou si Google le suspend, il perd aussi l'accès au site. Pour limiter ce risque, beaucoup de sites proposent une seconde méthode de connexion.

Attention : le site doit identifier l'utilisateur par `sub`, pas par l'e-mail. L'e-mail peut changer, `sub` reste stable.
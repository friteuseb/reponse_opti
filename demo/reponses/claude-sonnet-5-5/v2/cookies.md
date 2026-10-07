# Cookies et RGPD : ce que doit faire un artisan avec un site vitrine

## Le principe

Un cookie est un petit fichier que votre site dépose dans le navigateur du visiteur. La règle tient en deux points :
- Les cookies indispensables au fonctionnement du site ne demandent pas d'accord.
- Tous les autres demandent l'accord du visiteur **avant** leur dépôt.

## Étape 1 : listez les cookies de votre site

1. Ouvrez votre site dans Chrome.
2. Appuyez sur F12.
3. Ouvrez l'onglet « Application », puis « Cookies ».
4. Notez le nom et l'origine de chaque cookie.

Un outil gratuit comme Cookiebot Scanner ou CookieMetrics fait le même travail. Si votre site n'utilise aucun service externe, la liste est souvent vide ou très courte.

## Étape 2 : triez les cookies

**Sans accord du visiteur :**
- Cookies de session ou de sécurité.
- Cookies de panier ou de langue.
- Mesure d'audience exemptée. Elle doit respecter 5 conditions :
  - Elle sert uniquement à mesurer l'audience du site.
  - Elle ne suit pas le visiteur sur d'autres sites.
  - Elle ne transmet pas les données à un tiers.
  - Le cookie dure 13 mois au plus.
  - Les données sont conservées 25 mois au plus.

Matomo (bien configuré) et Plausible respectent ces conditions. Google Analytics ne figure pas dans la liste d'exemption de la CNIL.

**Avec accord du visiteur :**
- Google Analytics.
- Pixel Facebook ou Instagram.
- Google Ads.
- Vidéos YouTube intégrées.
- Carte Google Maps intégrée.
- Boutons de partage de réseaux sociaux.
- Outils de statistiques comme Hotjar.

## Étape 3 : supprimez ce qui ne sert à rien

Chaque service supprimé enlève une obligation. Pour un site vitrine, ces options évitent souvent le bandeau :
- Remplacez Google Analytics par Matomo ou Plausible, configuré en mode exempté.
- Remplacez la carte intégrée par un lien vers l'adresse sur Google Maps.
- Remplacez la vidéo YouTube par un lien, ou utilisez `youtube-nocookie.com` (vérifiez ensuite qu'aucun cookie n'est déposé).

Si votre site ne dépose plus que des cookies exemptés, vous n'avez pas besoin de bandeau.

## Étape 4 : installez un bandeau si nécessaire

Le bandeau doit respecter ces règles :
- Il bloque les cookies concernés tant que le visiteur n'a pas répondu.
- Il propose « Accepter » et « Refuser » au même niveau, avec la même taille et la même couleur.
- Il ne coche aucune case à l'avance.
- Il ne considère pas qu'un défilement ou un clic ailleurs vaut accord.
- Il décrit chaque finalité en une phrase claire.
- Il enregistre la réponse comme preuve.
- Il redemande l'avis au bout de 6 mois au plus.

Ajoutez en bas de chaque page un lien « Gérer mes cookies ». Le visiteur doit pouvoir retirer son accord aussi facilement qu'il l'a donné.

Pour installer ce bandeau, utilisez un module de votre outil de création (WordPress, Wix, Jimdo, Shopify) ou une solution dédiée comme Axeptio, Tarteaucitron (gratuit) ou Klaro (gratuit).

## Étape 5 : rédigez la politique de cookies

Placez-la sur une page accessible depuis le bandeau et le pied de page. Elle indique :
- La liste des cookies, avec leur nom, leur origine et leur durée de vie.
- La finalité de chaque cookie.
- Le moyen de refuser ou de retirer son accord.

Vous pouvez l'intégrer à la politique de confidentialité.

## Étape 6 : vérifiez le reste du RGPD

Les cookies ne sont qu'une partie du sujet. Contrôlez aussi ces points :
- **Mentions légales :** nom, adresse, SIRET, contact et hébergeur.
- **Formulaire de contact :** indiquez qui reçoit les données, pourquoi, et combien de temps vous les gardez.
- **Droits des personnes :** indiquez une adresse e-mail pour exercer les droits d'accès, de rectification et de suppression.

## Étape 7 : testez

1. Ouvrez votre site en navigation privée.
2. Refusez les cookies dans le bandeau.
3. Rouvrez l'onglet « Cookies » (F12).
4. Vérifiez qu'aucun cookie soumis à accord n'apparaît.

Refaites ce test après chaque modification du site.

## Risques

La CNIL contrôle les sites et peut sanctionner. Pour une petite structure, elle commence en général par une mise en demeure. Corrigez vite si vous en recevez une.

Ne copiez pas le bandeau d'un autre site sans vérifier vos propres cookies. Un bandeau qui ne bloque rien reste non conforme.
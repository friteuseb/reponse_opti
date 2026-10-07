# Cookies et RGPD : ce que tu dois faire

## Le principe

Un cookie est un petit fichier que ton site dépose dans le navigateur du visiteur. Avant de déposer la plupart des cookies, tu dois obtenir l'accord du visiteur.

| Type de cookie | Exemple | Accord du visiteur |
|---|---|---|
| Fonctionnement du site | session, sécurité, panier | Non |
| Mesure d'audience limitée | Matomo configuré selon la CNIL, Plausible | Non |
| Mesure d'audience classique | Google Analytics | Oui |
| Publicité, réseaux sociaux | pixel Facebook, Google Ads | Oui |
| Contenu intégré | vidéo YouTube, carte Google Maps | Oui |

Si ton site dépose seulement des cookies de fonctionnement, tu n'as pas besoin de bandeau. Vérifie d'abord ce point.

## Procédure

1. Liste les cookies de ton site. Utilise un scanner gratuit (Cookieserve) ou demande la liste à ton webmaster.
2. Supprime les cookies inutiles. Retire le pixel Facebook si tu ne fais pas de publicité.
3. Remplace Google Analytics par Matomo ou Plausible si tu veux des statistiques sans bandeau.
4. Installe un bandeau de consentement pour les cookies restants. Tarteaucitron est gratuit. Axeptio est payant.
5. Affiche deux boutons de même taille et de même couleur : « Tout accepter » et « Tout refuser ».
6. Ne précoche aucune case.
7. Bloque tous les cookies non nécessaires avant le clic du visiteur.
8. Ajoute un lien « Gérer mes cookies » en bas de chaque page.
9. Rédige une page « Politique de cookies ». Indique pour chaque cookie son nom, son rôle, sa durée et son éditeur.
10. Redemande le consentement tous les 6 mois.
11. Teste ton site en navigation privée. Clique sur « Tout refuser ». Ouvre F12, onglet « Application », rubrique « Cookies ». Vérifie qu'aucun cookie non nécessaire n'apparaît.

## Avertissements

- N'écris pas « En poursuivant votre navigation, vous acceptez les cookies ». La CNIL n'accepte pas cette formule comme un accord valide.
- N'installe pas un bandeau décoratif. Un bandeau qui ne bloque aucun cookie ne protège pas ton site.
- Ne cache pas le bouton « Tout refuser » dans un sous-menu. Refuser doit demander autant d'effort qu'accepter.

## Autre point à vérifier

Si ton site a un formulaire de contact, ajoute sous le formulaire une mention courte. Elle indique qui reçoit les données, pourquoi, pendant combien de temps, et comment exercer les droits d'accès et de suppression.
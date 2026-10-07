# Cookies et RGPD : le guide pour un site vitrine d'artisan

## 1. Comprendre le principe

Un cookie est un petit fichier déposé sur l'appareil du visiteur. La règle est simple :

- **Les cookies strictement nécessaires** au fonctionnement du site ne demandent **aucun consentement**.
- **Tous les autres** (statistiques, publicité, réseaux sociaux, vidéos intégrées, etc.) demandent **le consentement préalable** du visiteur.

## 2. Faites l'inventaire de ce que fait votre site

Avant tout, listez ce qui est installé. Vous pouvez utiliser un outil gratuit comme **Cookiebot Scanner**, **Webcookies** ou l'outil **Cookieviz** de la CNIL. Les suspects habituels sont :

| Élément sur votre site | Cookie soumis au consentement ? |
|---|---|
| Google Analytics | **Oui** |
| Pixel Facebook / Meta, Google Ads | **Oui** |
| Vidéo YouTube intégrée | **Oui** (sauf mode « sans cookies » youtube-nocookie, à vérifier) |
| Google Maps intégrée | **Oui** |
| Boutons de partage / flux Instagram, Facebook | **Oui** |
| Cookie technique (session, panier, sécurité) | Non |
| Statistiques anonymes exemptées (voir plus bas) | Non |

## 3. Si vous utilisez des cookies soumis au consentement

Il vous faut un **bandeau cookies** conforme. Les règles de la CNIL sont les suivantes :

- **Aucun cookie non essentiel ne doit être déposé avant** que le visiteur ait accepté.
- Le bouton **« Refuser » doit être aussi visible et aussi simple** que « Accepter », au même niveau, sur le premier écran.
- **Pas de case pré-cochée.**
- **Continuer à naviguer, ou fermer le bandeau, ne vaut pas consentement.**
- Le visiteur doit pouvoir choisir **finalité par finalité** (statistiques, publicité, etc.).
- Il doit pouvoir **changer d'avis à tout moment**, grâce à un lien permanent du type « Gérer mes cookies » en bas de page.
- Son choix doit être **conservé** (preuve du consentement) et redemandé au plus tard **tous les 6 mois environ**.
- Les cookies déposés ne doivent pas durer plus de **13 mois**.

## 4. L'option la plus simple : ne pas avoir besoin de bandeau

Pour un site vitrine, c'est souvent la meilleure solution :

- **Supprimez Google Analytics**, ou remplacez-le par un outil de mesure d'audience **exempté de consentement** par la CNIL : Matomo (bien configuré), Plausible, Fathom, etc.
- **Remplacez Google Maps** par un simple lien « Voir sur la carte » ou une image cliquable.
- **Évitez les vidéos et widgets** de réseaux sociaux intégrés, ou faites-les charger seulement après clic.
- **Hébergez vos polices** (Google Fonts) sur votre propre serveur.

Si vous n'utilisez plus que des cookies techniques ou exemptés, **vous n'avez pas besoin de bandeau**. Vous devez quand même informer les visiteurs dans votre politique de confidentialité.

## 5. Les outils pour vous aider

- **WordPress** : Complianz, Real Cookie Banner, CookieYes
- **Tous types de sites** : Axeptio, Tarteaucitron.js (gratuit, développé par un Français), Cookiebot, Iubenda
- **Wix, Squarespace, Shopify, Webflow** : ils intègrent un module de gestion des cookies, à activer et à paramétrer correctement.

Attention : installer un bandeau ne suffit pas. **Il doit réellement bloquer les cookies** tant que le visiteur n'a pas accepté. Testez en navigation privée, avec les outils de développement de votre navigateur (onglet « Application » puis « Cookies »).

## 6. Les pages obligatoires

1. **Mentions légales** : votre identité, SIRET, adresse, contact, hébergeur.
2. **Politique de confidentialité** : quelles données vous collectez (formulaire de contact, par exemple), pourquoi, combien de temps, les droits des personnes (accès, suppression…), et comment vous contacter.
3. **Politique de cookies** (souvent intégrée à la précédente) : la liste des cookies, leur finalité et leur durée.

## 7. N'oubliez pas le formulaire de contact

Ce n'est pas un cookie, mais le RGPD s'applique aussi :

- Indiquez près du formulaire pourquoi vous collectez ces données et renvoyez vers la politique de confidentialité.
- Ne demandez que le nécessaire (nom, email, message).
- Ne gardez pas les messages indéfiniment.

## 8. Checklist rapide

- [ ] J'ai listé tous les cookies et traceurs de mon site
- [ ] J'ai supprimé ou remplacé ceux dont je n'ai pas besoin
- [ ] Si j'en garde : mon bandeau bloque les cookies avant consentement
- [ ] Les boutons « Accepter » et « Refuser » sont équivalents
- [ ] Un lien « Gérer mes cookies » reste accessible
- [ ] Mes mentions légales et ma politique de confidentialité sont à jour
- [ ] J'ai testé mon site en navigation privée

## 9. Quels risques ?

La CNIL contrôle surtout les gros sites, mais elle peut aussi réagir à des plaintes de particuliers ou de concurrents. Pour un petit site, cela commence en général par une mise en demeure, mais les sanctions sont possibles. En faisant simple (peu ou pas de traceurs), vous réduisez presque tout le risque.

**Conseil pratique** : pour un artisan, le plus efficace est souvent de retirer Google Analytics et Google Maps, et de n'avoir ainsi plus de bandeau à gérer. Mais si vous voulez suivre vos statistiques, passez par un outil exempté ou par un bandeau bien configuré.

Pour vérifier les détails, les ressources officielles de la CNIL (cnil.fr, rubrique « Cookies et traceurs ») sont claires et régulièrement mises à jour.
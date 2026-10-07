# Cookies et RGPD : ce que doit faire un artisan avec un site vitrine

## Le principe

Un cookie qui n'est pas indispensable au fonctionnement du site exige l'accord du visiteur **avant** son dépôt. Sans cookie de ce type, le site n'a pas besoin de bandeau.

| Type de cookie | Accord du visiteur | Exemples |
|---|---|---|
| Indispensable | Non | Sécurité, panier, choix de la langue |
| Mesure d'audience configurée selon les règles de la CNIL | Non | Matomo ou Plausible, configurés en mode exempté |
| Publicité, réseaux sociaux, Google Analytics | Oui | Pixel Facebook, bouton de partage, Google Analytics |

## Procédure

1. **Dresse la liste des cookies de ton site.** Ouvre le site dans le navigateur, puis appuie sur F12. Va dans « Application » (Chrome) ou « Stockage » (Firefox), puis dans « Cookies ». Note le nom et l'émetteur de chaque cookie.
2. **Repère les contenus tiers.** Une carte Google Maps, une vidéo YouTube, un widget Facebook ou Instagram et Google Analytics déposent souvent des cookies. Demande à ton webmaster si tu ne sais pas ce que contient ta page.
3. **Supprime ce qui ne sert pas.** Retire les widgets et les outils que tu n'utilises plus. Moins il y a de cookies, moins il y a d'obligations.
4. **Remplace ce qui peut l'être.**
   - Remplace Google Analytics par un outil de mesure d'audience exempté, avec la configuration recommandée par la CNIL.
   - Remplace la carte Google Maps par une image avec un lien vers la carte, ou par OpenStreetMap.
   - Intègre les vidéos YouTube avec le domaine `youtube-nocookie.com`, puis vérifie qu'aucun cookie n'apparaît avant la lecture.
5. **Installe un bandeau de consentement si des cookies soumis à accord restent.** Utilise une solution dédiée (Axeptio, Tarteaucitron, Cookiebot ou équivalent). Configure-la selon les règles de l'étape suivante.
6. **Respecte les règles du bandeau.**
   - Ne dépose aucun cookie avant le choix du visiteur.
   - Affiche « Tout refuser » aussi visiblement que « Tout accepter », dès le premier écran.
   - Ne précoche aucune case.
   - Ajoute un lien permanent (en bas de page) pour modifier le choix.
   - Conserve la preuve du consentement.
   - Redemande le choix au bout de 6 mois au plus.
7. **Rédige une page « Politique de confidentialité » ou « Cookies ».** Indique ton identité, la liste des cookies, leur rôle, leur durée de vie, la façon de retirer son accord et ton adresse de contact.
8. **Teste le site en navigation privée.** Ouvre le site et ne clique sur rien. Vérifie dans F12 qu'aucun cookie non indispensable n'est présent. Clique ensuite sur « Tout refuser » et vérifie de nouveau. Recommence avec « Tout accepter » pour contrôler que le bandeau fonctionne.
9. **Reprends le test tous les 6 mois et après chaque modification du site.** Une mise à jour ou un nouveau plugin peut ajouter des cookies sans que tu le saches.

## Mises en garde

- **Attention : un bandeau mal configuré ne protège pas.** Un bandeau qui affiche « J'accepte » mais laisse les cookies se déposer avant le clic reste non conforme.
- **Attention : refuser doit être aussi simple qu'accepter.** La CNIL a sanctionné des sites dont le bouton de refus était caché ou demandait plusieurs clics.
- **Attention : la CNIL peut te mettre en demeure, puis te sanctionner.** Elle contrôle aussi les petits sites, souvent après une plainte de visiteur.

## Si tu hésites

Si ton site n'a que du texte, des photos et un formulaire de contact, tu n'as probablement aucun cookie à déclarer. Fais quand même l'étape 1 pour le vérifier, et garde la page de confidentialité (étape 7) pour la gestion des données du formulaire.
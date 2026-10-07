# Diagnostiquer un site WordPress devenu lent

Comme la lenteur est apparue il y a une semaine, la question clé est : **qu'est-ce qui a changé à ce moment-là ?** Voici l'ordre que je suggère.

## 1. Chercher ce qui a changé
- Mises à jour récentes (plugins, thème, WordPress, PHP) ?
- Nouveau plugin installé ou nouvelle fonctionnalité ajoutée ?
- Pic de trafic, ou au contraire du trafic suspect (bots, attaque) ?
- Changement chez l'hébergeur (migration, changement d'offre, serveur surchargé) ?

## 2. Mesurer pour savoir où ça coince
- **GTmetrix**, **PageSpeed Insights** ou **WebPageTest** : regardez surtout le **TTFB** (temps de réponse du serveur).
  - **TTFB élevé** (> 600 ms) : problème côté serveur, PHP, base de données ou plugins.
  - **TTFB correct mais page lente** : problème côté front (images lourdes, scripts, polices, widgets externes).
- Pensez à tester plusieurs pages (accueil, article, page admin) pour voir si c'est global ou localisé.

## 3. Installer Query Monitor (gratuit)
Ce plugin montre les requêtes SQL lentes, les plugins qui consomment le plus, les erreurs PHP et les appels HTTP externes. C'est souvent là qu'on trouve le coupable.

## 4. Tester les plugins et le thème
- Désactivez tous les plugins (idéalement sur un site de préproduction), puis réactivez-les un par un en mesurant à chaque fois.
- Basculez temporairement sur un thème par défaut (Twenty Twenty-Four) pour écarter le thème.

## 5. Vérifier le serveur
- Dans l'espace hébergeur : utilisation CPU/RAM, limites atteintes, logs d'erreurs.
- Version de PHP (8.1 ou plus recommandé).
- Activez `WP_DEBUG_LOG` pour repérer les erreurs répétées.

## 6. Vérifier la base de données
- Table `wp_options` gonflée par des options en *autoload*.
- Révisions d'articles, transients expirés, spams de commentaires.
- Outil utile : **WP-Optimize** (faites une sauvegarde avant).

## 7. Chercher une cause externe ou malveillante
- Scan avec **Wordfence** ou **Sucuri** (malware, script de minage, spam injecté).
- Vérifiez les logs d'accès : un afflux de requêtes sur `xmlrpc.php` ou `wp-login.php` indique une attaque par force brute.
- Scripts tiers (pub, analytics, chat, réseaux sociaux) qui répondent lentement.

## 8. Vérifier la mise en cache et le CDN
- Un plugin de cache (WP Rocket, LiteSpeed Cache, W3 Total Cache) est-il actif et bien configuré ?
- Cloudflare ou un autre CDN peut aider, surtout pour les images et fichiers statiques.

---

**Pour que je vous aide plus précisément**, dites-moi :
- Votre type d'hébergement (mutualisé, VPS, infogéré…)
- Si la lenteur touche le **site public**, l'**admin**, ou les deux
- Le TTFB mesuré et les plugins principaux installés
- Ce qui a été modifié la semaine dernière, si vous vous en souvenez
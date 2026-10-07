# Diagnostiquer un WordPress devenu lent

**Danger : fais une sauvegarde complète (fichiers + base de données) avant toute modification.** Un changement sur la base ou sur les plugins peut provoquer une perte de données.

## 1. Mesurer le problème

1. Mesure le temps de réponse du serveur (TTFB) avec cette commande :
   ```
   curl -o /dev/null -s -w "TTFB : %{time_starttransfer} s\nTotal : %{time_total} s\n" https://ton-site.fr
   ```
2. Interprète le résultat :
   - **TTFB supérieur à 0,8 s** : le problème vient du serveur, de PHP ou de la base de données. Passe aux étapes 2 à 7.
   - **TTFB correct mais page lente** : le problème vient du front (images, scripts, polices). Lance PageSpeed Insights ou WebPageTest et traite les points signalés.
3. Compare plusieurs pages (accueil, article, wp-admin). Si seules certaines pages sont lentes, cherche le plugin ou le contenu qu'elles ont en commun.

## 2. Lister ce qui a changé il y a 7 jours

Vérifie chacun de ces points :

- mises à jour de plugins, du thème ou de WordPress ;
- changement de version PHP par l'hébergeur ;
- nouveau plugin, nouveau widget ou nouveau script tiers (analytics, chat, publicité) ;
- hausse du trafic ;
- import massif de contenu ou de produits.

Si un changement coïncide avec le début de la lenteur, annule-le d'abord sur un site de test (staging).

## 3. Vérifier les ressources du serveur

1. Ouvre une session SSH, puis lance `top` (ou `htop`). Repère les processus `php-fpm` et `mysqld` qui consomment plus de 80 % du CPU.
2. Lance `free -h`. Si le swap est utilisé de façon continue, le serveur manque de RAM.
3. Lance `df -h`. Si un disque dépasse 90 %, libère de l'espace.
4. Sans accès SSH, regarde les graphiques de ton hébergeur. Cherche un plafond de CPU, de RAM ou de processus PHP.

## 4. Chercher du trafic anormal

1. Consulte les logs d'accès du serveur web.
2. Repère les adresses IP avec un nombre de requêtes très élevé.
3. Vérifie les requêtes vers `wp-login.php` et `xmlrpc.php`. Une attaque par force brute sature souvent PHP.
4. Si tu trouves des bots abusifs, bloque-les avec le pare-feu, Cloudflare ou un plugin de sécurité.

## 5. Identifier le plugin ou la requête coupable

1. Installe le plugin **Query Monitor** (sur le staging si possible).
2. Ouvre une page lente et lis ces onglets :
   - **Requêtes par composant** : le plugin ou le thème qui génère les requêtes les plus lentes ;
   - **Appels HTTP** : les API externes qui répondent en plus de 1 s ;
   - **Hooks** : les fonctions coûteuses.
3. Si Query Monitor ne suffit pas, désactive les plugins un par un et mesure le TTFB après chaque désactivation.

**Attention : ne désactive pas un plugin de paiement ou de sécurité sur un site en production.** Le site peut perdre des commandes ou devenir vulnérable. Utilise le staging.

## 6. Contrôler la base de données

1. Vérifie la taille des options chargées automatiquement (`autoload`) :
   ```
   SELECT SUM(LENGTH(option_value)) / 1024 / 1024 AS autoload_mo
   FROM wp_options WHERE autoload = 'yes';
   ```
   Un résultat supérieur à 1 Mo est un signe de problème. Identifie les plus grosses options et leur plugin d'origine.
2. Compte les transients expirés et les révisions d'articles. Supprime-les avec WP-CLI ou un plugin de nettoyage.
3. Active le slow query log de MySQL (seuil : 1 s) et analyse les requêtes lentes.
4. Si une table est très grosse sans index, ajoute un index ou demande de l'aide au développeur du plugin.

## 7. Vérifier PHP et le cache

1. Vérifie la version de PHP. Utilise une version supportée (8.1 ou plus récente) si ton thème et tes plugins la gèrent.
2. Lis le log d'erreurs PHP. Des avertissements répétés ralentissent le site.
3. Vérifie que **OPcache** est activé.
4. Vérifie qu'un cache de pages est actif (plugin ou cache du serveur).
5. Si le site a beaucoup de requêtes dynamiques, installe un cache d'objets (Redis ou Memcached).
6. Contrôle `memory_limit` (256 Mo au minimum) et le nombre de workers PHP-FPM. Un nombre trop bas crée une file d'attente.

## 8. Exclure un piratage

1. Lance un scan avec Wordfence, Sucuri ou l'outil de ton hébergeur.
2. Cherche des fichiers PHP modifiés récemment dans `wp-content/uploads` et des utilisateurs administrateurs inconnus.

**Danger : si tu trouves un malware, isole le site et restaure une sauvegarde saine avant de continuer.** Le malware peut voler des données.

## 9. Contacter l'hébergeur

Si les étapes 1 à 8 ne donnent aucune cause, contacte le support avec :

- les valeurs de TTFB mesurées ;
- la date de début de la lenteur ;
- la liste des changements de l'étape 2.

Demande s'il y a eu une migration de serveur, une limite de ressources atteinte ou un voisin bruyant sur un hébergement mutualisé.

Si tu me donnes ton TTFB, ton type d'hébergement et la liste de tes plugins, je peux t'aider à cibler les étapes utiles.
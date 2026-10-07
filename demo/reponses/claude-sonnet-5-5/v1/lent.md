# Diagnostiquer un site WordPress lent

Commence par mesurer, puis cherche ce qui a changé il y a 7 jours.

## 1. Mesurer où le temps est perdu

1. Ouvre le panneau Réseau des outils de développement du navigateur.
2. Recharge une page en navigation privée.
3. Note le TTFB (délai avant le premier octet) de la requête principale.

| Résultat | Cause probable |
|---|---|
| TTFB > 600 ms | Serveur, PHP, base de données ou plugin |
| TTFB < 600 ms, page lente | Images, scripts, polices, services tiers |

## 2. Lister les changements de la semaine

1. Vérifie les mises à jour de WordPress, des plugins et du thème.
2. Vérifie la version de PHP chez l'hébergeur.
3. Vérifie le trafic dans les statistiques de l'hébergeur.
4. Vérifie les contenus ajoutés : pages lourdes, images non compressées, nouveaux scripts.

## 3. Lire les logs

1. Active `WP_DEBUG_LOG` dans `wp-config.php`.
2. Lis `wp-content/debug.log`.
3. Lis les logs d'erreurs PHP et du serveur web.
4. Cherche les erreurs répétées et les requêtes lentes.

## 4. Isoler un plugin

Fais une sauvegarde avant de continuer. Ne teste pas en production aux heures de pointe. Les visiteurs perdraient des fonctions.

1. Copie le site sur un environnement de préproduction.
2. Installe Query Monitor.
3. Identifie les plugins qui exécutent le plus de requêtes ou prennent le plus de temps.
4. Désactive tous les plugins avec `wp plugin deactivate --all`.
5. Mesure à nouveau le TTFB.
6. Réactive les plugins un par un. Mesure après chaque activation.

## 5. Vérifier le serveur

1. Lance `top` ou `htop` pendant une page lente.
2. Contrôle l'usage du CPU, de la RAM et du swap.
3. Contrôle l'espace disque avec `df -h`.
4. Cherche un pic de requêtes vers `wp-login.php` ou `xmlrpc.php` dans les logs d'accès. Ce schéma indique une attaque par force brute.

## 6. Vérifier la base de données

1. Active le slow query log de MySQL avec un seuil de 1 s.
2. Mesure le poids des options chargées automatiquement :

   ```sql
   SELECT SUM(LENGTH(option_value)) FROM wp_options WHERE autoload='yes';
   ```

3. Cherche un résultat supérieur à 1 Mo.
4. Compte les transients expirés et les révisions d'articles.
5. Supprime-les après la sauvegarde.

## 7. Vérifier le cache

1. Vérifie qu'un cache de page est actif.
2. Vérifie qu'OPcache est actif.
3. Vérifie la présence d'un cache objet (Redis ou Memcached) si le site reçoit beaucoup de trafic.

Si tu me donnes le TTFB mesuré et la liste des plugins mis à jour cette semaine, je peux cibler la cause plus vite.
# Diagnostiquer un site WordPress lent

Fais une sauvegarde complète (fichiers et base de données) avant de modifier quoi que ce soit. Une désactivation de plugin ou une optimisation de base peut casser le site.

## 1. Dater le changement

Une lenteur qui commence à une date précise a presque toujours une cause précise.

1. Liste ce qui a changé il y a 7 à 10 jours :
   - mise à jour de WordPress, d'un plugin ou du thème ;
   - nouveau plugin ;
   - changement de version de PHP ou d'offre d'hébergement ;
   - campagne, article viral ou pic de trafic.
2. Consulte **Outils > Santé du site** dans l'administration.
3. Consulte le journal de ton hébergeur (mises à jour automatiques, incidents, migrations).
4. Consulte les statistiques de trafic. Compare cette semaine à la précédente.

## 2. Mesurer où le temps passe

1. Teste la page d'accueil avec PageSpeed Insights, WebPageTest ou GTmetrix.
2. Mesure le TTFB (temps jusqu'au premier octet) depuis un terminal :

```bash
curl -o /dev/null -s -w "TTFB : %{time_starttransfer} s\nTotal : %{time_total} s\n" https://exemple.fr/
```

3. Interprète le résultat :
   - TTFB supérieur à 600 ms : le problème vient du serveur, de PHP ou de la base de données.
   - TTFB correct mais page lente : le problème vient du front (images, JavaScript, polices, scripts tiers).
4. Teste aussi `/wp-login.php`. Cette page n'utilise pas le cache de page. Si elle est lente, la cause est PHP, la base de données ou le serveur.

## 3. Vérifier les ressources du serveur

Sur un serveur dédié ou un VPS, connecte-toi en SSH. Sur un hébergement mutualisé, utilise le panneau de l'hébergeur.

```bash
top            # CPU et processus les plus gourmands
free -h        # RAM et swap
df -h          # espace disque
```

- Un swap très utilisé signale un manque de RAM.
- Un disque plein à plus de 90 % provoque des ralentissements et des erreurs.
- Lis le journal d'erreurs PHP (souvent `/var/log/php*-fpm.log` ou `error_log` dans le dossier du site).

## 4. Vérifier le trafic

Les robots et les attaques par force brute ralentissent un site sans que tu le voies dans les statistiques.

```bash
# 20 adresses IP les plus actives
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20

# Nombre d'appels aux points d'entrée les plus attaqués
grep -c "wp-login.php" /var/log/nginx/access.log
grep -c "xmlrpc.php" /var/log/nginx/access.log
```

Adapte le chemin du journal (Apache : `/var/log/apache2/access.log`).

Si le trafic anormal est confirmé, utilise l'une de ces mesures :
- activer un pare-feu applicatif (Cloudflare, Wordfence) ;
- bloquer `xmlrpc.php` si tu ne l'utilises pas ;
- installer fail2ban pour bannir les IP abusives.

## 5. Isoler le plugin ou le thème fautif

1. Installe le plugin **Query Monitor**.
2. Ouvre une page lente. Lis les onglets suivants :
   - **Queries by Component** : temps SQL par plugin ;
   - **HTTP API Calls** : appels à des services externes ;
   - **Hooks & Actions** : code lent par composant.
3. Si Query Monitor ne suffit pas, travaille sur une copie du site (staging). Ne teste pas en production.
4. Désactive tous les plugins :

```bash
wp plugin deactivate --all
```

5. Mesure à nouveau le TTFB.
6. Réactive les plugins un par un. Mesure après chaque réactivation.
7. Active un thème par défaut pour tester le thème :

```bash
wp theme activate twentytwentyfour
```

## 6. Vérifier la base de données

1. Mesure la taille des tables :

```bash
wp db size --tables --size_format=mb
```

2. Mesure le poids des options chargées à chaque page :

```sql
SELECT ROUND(SUM(LENGTH(option_value))/1024/1024, 2) AS mo
FROM wp_options
WHERE autoload IN ('yes','on','auto','auto-on');
```

Au-dessus de 1 Mo, cherche les options volumineuses laissées par d'anciens plugins.

3. Supprime les transients expirés :

```bash
wp transient delete --expired
```

4. Vérifie les tables `wp_postmeta`, `wp_options` et celles des plugins de logs ou de statistiques. Une table de plusieurs Go est suspecte.
5. Active le journal des requêtes lentes de MySQL (`slow_query_log`) si tu as accès au serveur.
6. Optimise les tables en dernier :

```bash
wp db optimize
```

## 7. Vérifier les appels externes et WP-Cron

Un service tiers lent bloque PHP en attendant sa réponse. Exemples : API de licence, flux RSS, polices, outils d'analyse.

1. Lis l'onglet **HTTP API Calls** de Query Monitor. Cherche les appels supérieurs à 1 s.
2. Liste les tâches planifiées :

```bash
wp cron event list
```

3. Cherche les tâches en retard ou en très grand nombre.
4. Si le trafic est élevé, désactive le WP-Cron intégré et utilise une tâche cron système :

```php
// wp-config.php
define('DISABLE_WP_CRON', true);
```

```bash
*/5 * * * * cd /chemin/du/site && wp cron event run --due-now
```

## 8. Vérifier PHP et le cache

1. Vérifie la version de PHP. Utilise 8.2 ou 8.3.
2. Vérifie qu'OPcache est actif (`php -i | grep opcache.enable`).
3. Vérifie qu'un cache de page est actif (WP Rocket, LiteSpeed Cache, WP Super Cache ou cache du serveur).
4. Vérifie si une mise à jour a vidé ou désactivé le cache, ou si une purge automatique se déclenche trop souvent.
5. Active un cache d'objet (Redis ou Memcached) si ton hébergeur le propose.

## 9. Exclure un piratage

Un site compromis ralentit souvent (minage, envoi de spam, redirections).

```bash
wp core verify-checksums
wp plugin verify-checksums --all
```

- Analyse le site avec Wordfence ou Sucuri.
- Cherche les fichiers PHP récents dans `wp-content/uploads`. Ce dossier ne doit pas en contenir.
- Vérifie la liste des comptes administrateurs.

## 10. Contacter l'hébergeur

Contacte le support si les étapes 2 à 9 ne montrent rien. Demande :
- l'utilisation CPU et RAM de ton compte sur 14 jours ;
- les limites atteintes (processus PHP, I/O) ;
- un changement de serveur ou de configuration récent.

## Résumé : symptôme et cause probable

| Symptôme | Cause probable |
|---|---|
| TTFB élevé, `/wp-login.php` lent | PHP, base de données ou serveur saturé |
| TTFB correct, page lente | Images, JavaScript ou scripts tiers |
| Pic de requêtes sur `wp-login.php` ou `xmlrpc.php` | Attaque par force brute |
| Lenteur après une mise à jour | Plugin ou thème incompatible |
| `wp_options` autoload supérieur à 1 Mo | Données d'anciens plugins |
| Appels HTTP supérieurs à 1 s | Service externe lent |
| Fichiers PHP inconnus dans `uploads` | Piratage |

Si tu me donnes ton hébergement (mutualisé, VPS), les plugins principaux et les résultats des étapes 2 et 3, je peux cibler la cause.
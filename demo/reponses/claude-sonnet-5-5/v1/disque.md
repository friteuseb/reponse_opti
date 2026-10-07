# Libérer de l'espace sur une partition pleine

## Règles de sécurité

- Ne supprime rien dans `/etc`, `/usr` ou `/var/lib` à la main. Les paquets et les services en dépendent.
- Ne lance pas `rm` sur un journal ouvert par un service. Le service garde l'espace occupé. Utilise `truncate -s 0`.
- N'ajoute pas `--volumes` à `docker system prune`. Cette option supprime des données.

## 1. Trouver la partition pleine

1. Affiche l'usage de chaque partition :

   ```bash
   df -h
   ```

2. Repère la partition à 100 %. Note son point de montage (par exemple `/` ou `/var`).
3. Vérifie les inodes :

   ```bash
   df -i
   ```

4. Si `IUse%` atteint 100 %, cherche les répertoires qui contiennent des millions de petits fichiers (sessions, cache, files de mails).

## 2. Trouver ce qui prend la place

1. Liste les 15 plus gros répertoires du premier niveau :

   ```bash
   sudo du -xh --max-depth=1 / 2>/dev/null | sort -rh | head -15
   ```

2. Descends dans le plus gros répertoire. Relance la même commande avec son chemin.
3. Répète jusqu'à trouver le fichier ou le répertoire responsable.
4. Liste les fichiers de plus de 100 Mo :

   ```bash
   sudo find / -xdev -type f -size +100M -exec ls -lh {} + 2>/dev/null
   ```

L'option `-x` (ou `-xdev`) limite la recherche à une seule partition.

## 3. Chercher les fichiers supprimés mais encore ouverts

Un processus peut garder ouvert un fichier supprimé. `df` compte alors l'espace, mais `du` ne le voit pas.

1. Liste ces fichiers :

   ```bash
   sudo lsof +L1
   ```

2. Note le processus et son PID.
3. Redémarre le service concerné :

   ```bash
   sudo systemctl restart nom-du-service
   ```

4. Vérifie avec `df -h` que l'espace est revenu.

## 4. Libérer l'espace

Commence par les actions les moins risquées.

**Cache des paquets (Debian, Ubuntu) :**

```bash
sudo apt clean
sudo apt autoremove --purge
```

**Journaux systemd :** limite-les à 500 Mo.

```bash
sudo journalctl --vacuum-size=500M
```

**Anciens journaux compressés :**

```bash
sudo find /var/log -type f -name "*.gz" -mtime +30 -delete
```

**Journal actif trop gros :** vide-le sans le supprimer.

```bash
sudo truncate -s 0 /var/log/nom-du-fichier.log
```

**Docker :** mesure d'abord, nettoie ensuite.

```bash
docker system df
docker system prune
```

La commande `prune` supprime les conteneurs arrêtés, les réseaux inutilisés et les images sans étiquette.

## 5. Vérifier le résultat

1. Relance `df -h`.
2. Confirme que la partition passe sous 85 %.
3. Vérifie que les services critiques tournent :

   ```bash
   systemctl --failed
   ```

## 6. Éviter le retour du problème

- Configure `logrotate` pour les journaux de tes applications.
- Ajoute une alerte à 80 % d'usage.
- Si la partition reste trop petite, agrandis-la ou déplace les données lourdes vers une autre partition.

Si tu me donnes la sortie de `df -h` et du `du` du premier niveau, je t'indique quoi nettoyer en priorité.
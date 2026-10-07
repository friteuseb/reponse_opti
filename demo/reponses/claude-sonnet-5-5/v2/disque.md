# Libérer de l'espace disque sur un serveur Linux

## 1. Identifier la partition pleine

1. Affiche l'usage de chaque partition :
   ```bash
   df -h
   ```
2. Repère la ligne à 100 % dans la colonne `Use%`. Note son point de montage (`/`, `/var`, `/home`…).
3. Vérifie aussi les inodes :
   ```bash
   df -i
   ```
   Si `IUse%` est à 100 %, la partition contient trop de petits fichiers. L'espace en Go n'est pas en cause. Passe à l'étape 3 et cherche les répertoires qui contiennent des milliers de fichiers (sessions, caches, files de mail).

## 2. Trouver les gros répertoires

1. Liste les 15 plus gros répertoires de premier niveau :
   ```bash
   sudo du -xh --max-depth=1 / 2>/dev/null | sort -h | tail -n 15
   ```
   L'option `-x` limite la recherche à la partition courante.
2. Descends dans le plus gros répertoire. Répète la commande avec son chemin, par exemple `/var`.
3. Continue jusqu'à trouver les fichiers responsables.

Alternative interactive : `ncdu`.
```bash
sudo apt install ncdu    # ou : sudo dnf install ncdu
sudo ncdu -x /
```

## 3. Trouver les gros fichiers

Liste les fichiers de plus de 500 Mo :
```bash
sudo find / -xdev -type f -size +500M -exec ls -lh {} + 2>/dev/null
```

## 4. Détecter les fichiers supprimés mais encore ouverts

Si `du` compte moins d'espace que `df`, un processus garde peut-être un fichier supprimé ouvert.

1. Liste ces fichiers :
   ```bash
   sudo lsof +L1
   ```
2. Note le PID et la taille du fichier.
3. Redémarre le service concerné. Le système libère alors l'espace :
   ```bash
   sudo systemctl restart nom_du_service
   ```
4. Si tu ne peux pas redémarrer le service, vide le fichier via son descripteur. Remplace `PID` et `FD` par les valeurs de `lsof` :
   ```bash
   sudo truncate -s 0 /proc/PID/fd/FD
   ```

## 5. Libérer l'espace sans risque

Commence par les sources suivantes. Elles se régénèrent ou n'ont aucun effet sur les données.

### Journal systemd

1. Mesure sa taille :
   ```bash
   journalctl --disk-usage
   ```
2. Limite-le à 500 Mo :
   ```bash
   sudo journalctl --vacuum-size=500M
   ```
   Ou garde 14 jours :
   ```bash
   sudo journalctl --vacuum-time=14d
   ```

### Cache des paquets

- Debian/Ubuntu :
  ```bash
  sudo apt clean
  sudo apt autoremove --purge
  ```
- RHEL/Fedora :
  ```bash
  sudo dnf clean all
  sudo dnf autoremove
  ```

Relis la liste que `autoremove` affiche avant de confirmer. Elle inclut les anciens noyaux.

### Snap

Les anciennes révisions occupent de la place. Liste-les :
```bash
snap list --all | grep désactivé
```
Supprime chacune :
```bash
sudo snap remove nom --revision=NUMERO
```

### Docker

1. Mesure l'usage :
   ```bash
   docker system df
   ```
2. Supprime les conteneurs arrêtés, les réseaux inutilisés et les images sans étiquette :
   ```bash
   docker system prune
   ```
3. Pour supprimer aussi toutes les images inutilisées, ajoute `-a`.

N'ajoute pas `--volumes` sans vérifier. Cette option supprime les volumes inutilisés, donc les données de conteneurs arrêtés.

### Logs dans `/var/log`

1. Supprime les logs anciens déjà compressés :
   ```bash
   sudo find /var/log -type f -name "*.gz" -mtime +30 -delete
   ```
2. Pour un log actif volumineux, vide-le :
   ```bash
   sudo truncate -s 0 /var/log/nom.log
   ```

Ne supprime pas un log actif avec `rm`. Le service garde le fichier ouvert et l'espace reste occupé.

### Caches utilisateur

Vérifie `~/.cache`, `/root/.cache` et `/var/cache`. Ces dossiers contiennent des données régénérables, mais vérifie le contenu avant de supprimer.

## 6. Ce qu'il ne faut pas supprimer

- Ne supprime rien dans `/var/lib` sans savoir ce que le dossier contient. Les bases de données (MySQL, PostgreSQL) y stockent leurs données.
- Ne touche pas à `/proc`, `/sys` et `/dev`. Ce sont des systèmes de fichiers virtuels.
- Ne supprime pas manuellement les fichiers de `/boot`. Utilise le gestionnaire de paquets.
- Ne lance jamais `rm -rf` avec un chemin que tu n'as pas relu. Teste d'abord avec `ls`.
- Ne supprime pas un fichier dont tu ignores l'usage. Déplace-le d'abord vers une autre partition, puis attends quelques jours.

## 7. Cas particuliers

- **Le disque est à 100 % et les commandes échouent.** Libère quelques Mo avec `sudo apt clean` ou `sudo journalctl --vacuum-size=100M`. Continue ensuite le diagnostic.
- **Rien à supprimer.** Étends la partition (LVM : `lvextend -r -L +10G /dev/vg/lv`) ou ajoute un disque.
- **Partition ext4 avec 5 % réservés à root.** Tu peux réduire cette réserve sur une partition de données. Utilise `sudo tune2fs -m 1 /dev/sdXN`. Ne le fais pas sur `/`.

## 8. Vérifier et prévenir

1. Relance `df -h`. Confirme que `Use%` est passé sous 80 %.
2. Vérifie que les services critiques tournent :
   ```bash
   systemctl --failed
   ```
3. Configure `logrotate` pour les logs qui grossissent trop (`/etc/logrotate.d/`).
4. Limite le journal de façon permanente. Dans `/etc/systemd/journald.conf`, définis `SystemMaxUse=500M`. Redémarre ensuite `systemd-journald`.
5. Ajoute une alerte à 80 % d'usage avec ton outil de supervision (Zabbix, Prometheus, Netdata).
# Libérer de l'espace disque sur un serveur Linux

## 1. Identifier la partition pleine

```bash
df -h          # espace par partition
df -i          # inodes (un disque peut être "plein" sans que les Go le soient)
```
Repérez la partition à 100 % (souvent `/`, `/var` ou `/home`).

## 2. Trouver ce qui prend la place

**Vue d'ensemble, dossier par dossier** (`-x` reste sur la même partition) :
```bash
sudo du -xh / --max-depth=1 2>/dev/null | sort -rh | head -15
```
Puis descendez dans le plus gros dossier :
```bash
sudo du -xh /var --max-depth=1 | sort -rh | head -15
```

**Les plus gros fichiers :**
```bash
sudo find / -xdev -type f -size +500M -exec ls -lh {} + 2>/dev/null
```

**Outil interactif** (très pratique) :
```bash
sudo apt install ncdu     # ou dnf / yum
sudo ncdu -x /
```

## 3. Les coupables habituels et comment les nettoyer sans risque

| Source | Commande / action |
|---|---|
| **Cache des paquets** | `sudo apt clean` et `sudo apt autoremove` (Debian/Ubuntu) ; `sudo dnf clean all` (RHEL/Fedora) |
| **Journaux systemd** | `journalctl --disk-usage` puis `sudo journalctl --vacuum-size=200M` (ou `--vacuum-time=7d`) |
| **Logs dans `/var/log`** | Vérifiez avec `ls -lhS /var/log`. Les `.gz` et anciens `.1` peuvent être supprimés. |
| **Docker** | `docker system df` puis `docker system prune` (voir l'avertissement ci-dessous) |
| **Anciens noyaux** | `sudo apt autoremove --purge` |
| **Snap (anciennes révisions)** | `snap list --all`, puis `sudo snap remove <nom> --revision=<n>` |
| **Corbeille / caches utilisateurs** | `~/.cache`, `~/.local/share/Trash` |
| **Vieux dumps, archives, backups** | Vérifiez à la main avant de supprimer |

## 4. Pièges à connaître

**Fichier supprimé mais espace non libéré.** Si un processus garde un fichier ouvert (typiquement un gros log), l'espace reste occupé :
```bash
sudo lsof +L1 | grep deleted
```
Redémarrez le service concerné pour libérer l'espace.

**Vider un log actif sans casser le service.** Ne le supprimez pas, tronquez-le :
```bash
sudo truncate -s 0 /var/log/gros-fichier.log
```

**Plus d'inodes disponibles** (`df -i` à 100 %) : il y a des millions de petits fichiers (sessions PHP, mails, cache). Repérez le dossier avec :
```bash
sudo find / -xdev -type f | cut -d/ -f1-3 | sort | uniq -c | sort -rn | head
```

## 5. Précautions pour ne rien casser

- **Ne supprimez jamais** au hasard dans `/usr`, `/lib`, `/etc`, `/boot`, ni les fichiers de bases de données dans `/var/lib/mysql`, `/var/lib/postgresql`, etc.
- **`docker system prune -a --volumes`** peut supprimer des données persistantes (volumes inutilisés). Sans `--volumes` ni `-a`, c'est bien plus sûr.
- **Évitez `rm -rf` avec des variables ou jokers** sans avoir vérifié le chemin avec `ls` d'abord.
- Si le disque est si plein que plus rien ne fonctionne, libérez d'abord quelques centaines de Mo (cache apt, vieux logs compressés) pour pouvoir travailler tranquillement.

## 6. Éviter que ça se reproduise

- Configurez **logrotate** pour vos applications (`/etc/logrotate.d/`).
- Limitez le journal systemd : `SystemMaxUse=500M` dans `/etc/systemd/journald.conf`.
- Mettez une **alerte de supervision** à 80 % d'occupation.
- Si le besoin est réel, **agrandissez le disque** (LVM : `lvextend -r`, ou extension du volume chez votre hébergeur).

---

Si vous me donnez la sortie de `df -h` et du `du` sur la partition concernée, je peux vous indiquer précisément quoi nettoyer.
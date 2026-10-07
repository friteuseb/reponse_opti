# Libérer de l'espace disque sur un serveur Linux

Ces étapes vont du diagnostic au nettoyage. Les premières ne modifient rien.

## 1. Identifier la partition pleine

```bash
df -h
```

Repère la ligne à 100 % dans la colonne `Use%`. Note son point de montage (`/`, `/var`, `/home`…).

Si `Use%` est bas mais que l'erreur persiste, les inodes sont épuisés :

```bash
df -i
```

Dans ce cas, cherche un répertoire qui contient des millions de petits fichiers (sessions, mails, caches).

## 2. Trouver ce qui prend la place

Liste les plus gros répertoires de la partition. L'option `-x` empêche `du` de quitter cette partition.

```bash
sudo du -xh --max-depth=1 / | sort -h | tail -15
```

Remplace `/` par le point de montage trouvé à l'étape 1. Descends ensuite dans le plus gros répertoire et relance la commande. Répète jusqu'à trouver le coupable.

Pour une vue interactive, installe `ncdu` :

```bash
sudo ncdu -x /
```

## 3. Vérifier les fichiers supprimés mais encore ouverts

Un fichier supprimé garde son espace tant qu'un processus l'ouvre. Dans ce cas, `du` ne voit rien, mais `df` affiche une partition pleine.

```bash
sudo lsof +L1
```

Redémarre le service qui tient le fichier, par exemple `sudo systemctl restart nom-du-service`. L'espace revient aussitôt.

## 4. Libérer l'espace

Commence par les sources les plus sûres.

**Journaux systemd.** Limite-les à 500 Mo :

```bash
sudo journalctl --vacuum-size=500M
```

**Cache des paquets.**

```bash
sudo apt clean          # Debian, Ubuntu
sudo dnf clean all      # Fedora, RHEL
```

**Anciens paquets inutiles.**

```bash
sudo apt autoremove     # Debian, Ubuntu
```

Lis la liste avant de confirmer. La commande peut retirer d'anciens noyaux, ce qui est normal.

**Docker.** Mesure d'abord, puis supprime seulement les objets inutilisés :

```bash
docker system df
docker system prune
```

**Journaux dans `/var/log`.** Pour un fichier actif et volumineux, vide-le sans le supprimer :

```bash
sudo truncate -s 0 /var/log/gros-fichier.log
```

Pour un fichier déjà archivé (`.gz`, `.1`), `rm` suffit.

## 5. Vérifier le résultat

```bash
df -h
```

Vise moins de 85 % d'occupation. Au-delà, le problème reviendra vite.

## Mises en garde

- **Danger : ne lance pas `docker system prune -a --volumes` sans vérifier.** Cette commande supprime les volumes inutilisés, donc parfois des données de base de données.
- **Danger : ne supprime rien à la main dans `/var/lib`, `/etc` ou `/boot`.** Ces répertoires contiennent l'état des services et du démarrage. Une erreur peut empêcher le serveur de redémarrer.
- **Attention : ne fais pas `rm` sur un journal actif.** Le service garde le fichier ouvert et l'espace n'est pas libéré. Utilise `truncate`.
- **Attention : lis chaque liste avant de confirmer.** `apt autoremove` et `prune` montrent ce qu'ils vont supprimer.

## Éviter la récidive

- Configure `SystemMaxUse=500M` dans `/etc/systemd/journald.conf` pour limiter les journaux.
- Vérifie que `logrotate` tourne pour les journaux applicatifs.
- Ajoute une alerte à 80 % d'occupation avec ton outil de supervision.
- Si la cause est un volume de données légitime, agrandis la partition ou ajoute un disque.
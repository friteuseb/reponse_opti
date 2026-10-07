# Configurer une connexion SSH par clé

Cette procédure utilise une clé Ed25519. Le **client** est ta machine locale. Le **serveur** est la machine distante.

## 1. Générer la paire de clés (sur le client)

```bash
ssh-keygen -t ed25519 -C "mon-client"
```

- Accepte l'emplacement par défaut (`~/.ssh/id_ed25519`), sauf si une clé existe déjà. Dans ce cas, choisis un autre nom pour ne pas l'écraser.
- Saisis une passphrase. Elle protège la clé privée si quelqu'un la copie.

La commande crée deux fichiers :
- `id_ed25519` : la clé privée.
- `id_ed25519.pub` : la clé publique.

**Danger : ne partage jamais la clé privée.** Elle donne accès à tous les serveurs qui acceptent ta clé publique.

## 2. Copier la clé publique vers le serveur

```bash
ssh-copy-id utilisateur@adresse-du-serveur
```

Le serveur te demande ton mot de passe une dernière fois. La commande ajoute ensuite la clé publique à `~/.ssh/authorized_keys` sur le serveur.

Si `ssh-copy-id` n'existe pas (Windows, par exemple), utilise cette commande :

```bash
cat ~/.ssh/id_ed25519.pub | ssh utilisateur@adresse-du-serveur "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

## 3. Tester la connexion

```bash
ssh utilisateur@adresse-du-serveur
```

La connexion doit réussir sans demander le mot de passe du serveur. Si tu as défini une passphrase, SSH te la demande. Un agent SSH (`ssh-add`) évite de la saisir à chaque connexion.

## 4. Désactiver le mot de passe (facultatif, recommandé)

Cette étape bloque les attaques par force brute sur le mot de passe.

**Danger : garde ta session SSH ouverte pendant toute cette étape.** Si la configuration est fausse, tu perds l'accès au serveur. Il faut alors une console physique ou celle de l'hébergeur.

1. Ouvre le fichier de configuration sur le serveur :
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
2. Vérifie ou modifie ces lignes :
   ```
   PubkeyAuthentication yes
   PasswordAuthentication no
   ```
3. Cherche aussi des fichiers dans `/etc/ssh/sshd_config.d/`. Ils peuvent remplacer ces valeurs.
4. Teste la syntaxe :
   ```bash
   sudo sshd -t
   ```
   Aucune sortie signifie que la syntaxe est correcte.
5. Recharge le service :
   ```bash
   sudo systemctl reload ssh
   ```
   Sur RHEL, Fedora et dérivés, le service s'appelle `sshd`.
6. Ouvre un **second** terminal et connecte-toi. Ferme la première session seulement si cette connexion réussit.

## 5. Simplifier la commande (facultatif)

Ajoute ce bloc dans `~/.ssh/config` sur le client :

```
Host monserveur
    HostName adresse-du-serveur
    User utilisateur
    IdentityFile ~/.ssh/id_ed25519
```

Tu te connectes alors avec `ssh monserveur`.

## Si le serveur demande encore le mot de passe

| Cause probable | Vérification ou correction |
|---|---|
| Permissions trop ouvertes | Sur le serveur : `chmod 700 ~/.ssh` et `chmod 600 ~/.ssh/authorized_keys`. |
| Dossier personnel ouvert en écriture au groupe | Sur le serveur : `chmod go-w ~`. |
| Mauvaise clé utilisée | Force la clé : `ssh -i ~/.ssh/id_ed25519 utilisateur@adresse-du-serveur`. |
| Clé publique mal copiée | Compare `authorized_keys` avec `id_ed25519.pub`. Une clé tient sur une seule ligne. |
| SELinux actif (RHEL, Fedora) | Sur le serveur : `restorecon -R ~/.ssh`. |

Pour trouver la cause, lance `ssh -v utilisateur@adresse-du-serveur` sur le client. Lis aussi les logs du serveur : `/var/log/auth.log` (Debian, Ubuntu) ou `journalctl -u sshd`.
# Configurer une connexion SSH par clé

## 1. Générer une paire de clés (sur ta machine locale)

```bash
ssh-keygen -t ed25519 -C "ton_email@exemple.com"
```

- Appuie sur Entrée pour accepter l'emplacement par défaut (`~/.ssh/id_ed25519`).
- Définis une **passphrase** (recommandé) : elle protège ta clé privée si on te la vole.

> Si ton serveur est très ancien et ne supporte pas Ed25519 : `ssh-keygen -t rsa -b 4096`

## 2. Copier la clé publique sur le serveur

**Méthode simple (Linux/macOS/Git Bash) :**

```bash
ssh-copy-id utilisateur@adresse_du_serveur
```

Si le serveur utilise un port spécifique :

```bash
ssh-copy-id -p 2222 utilisateur@adresse_du_serveur
```

**Méthode manuelle (si `ssh-copy-id` n'est pas disponible) :**

```bash
cat ~/.ssh/id_ed25519.pub | ssh utilisateur@adresse_du_serveur "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Sous Windows PowerShell :**

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh utilisateur@adresse_du_serveur "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 3. Tester la connexion

```bash
ssh utilisateur@adresse_du_serveur
```

Tu ne dois plus avoir à saisir le mot de passe du serveur (seulement la passphrase de ta clé, si tu en as défini une).

## 4. Désactiver l'authentification par mot de passe (optionnel mais recommandé)

⚠️ **Ne fais cette étape qu'après avoir vérifié que la connexion par clé fonctionne**, sinon tu risques de t'enfermer dehors. Garde aussi une session SSH ouverte pendant le test.

Sur le serveur, édite la configuration :

```bash
sudo nano /etc/ssh/sshd_config
```

Modifie ou ajoute :

```
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin prohibit-password
```

Vérifie aussi le dossier `/etc/ssh/sshd_config.d/` : certains fichiers peuvent écraser tes réglages.

Puis redémarre le service :

```bash
sudo systemctl restart ssh    # Debian/Ubuntu
sudo systemctl restart sshd   # CentOS/RHEL/Fedora
```

Ouvre un **nouveau terminal** pour tester avant de fermer l'ancienne session.

## 5. Simplifier avec un fichier de config (optionnel)

Dans `~/.ssh/config` sur ta machine :

```
Host monserveur
    HostName adresse_du_serveur
    User utilisateur
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Tu pourras alors te connecter avec simplement :

```bash
ssh monserveur
```

## Dépannage

- **La clé n'est pas acceptée** : vérifie les permissions sur le serveur :
  ```bash
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/authorized_keys
  ```
- **Voir ce qui se passe** : `ssh -v utilisateur@adresse_du_serveur`
- **Logs côté serveur** : `sudo journalctl -u ssh` ou `/var/log/auth.log`

Si tu me dis quel système tu utilises (client et serveur), je peux adapter les commandes.
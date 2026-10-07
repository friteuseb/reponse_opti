# Configurer une connexion SSH par clé

Dans ce guide, le **client** est ta machine locale. Le **serveur** est la machine distante.

## 1. Générer la paire de clés (sur le client)

```bash
ssh-keygen -t ed25519 -C "ton-email-ou-nom"
```

1. Accepte l'emplacement par défaut : `~/.ssh/id_ed25519`.
2. Saisis une passphrase. Elle protège la clé privée si quelqu'un la vole.

La commande crée deux fichiers :

| Fichier | Rôle |
|---|---|
| `~/.ssh/id_ed25519` | Clé privée. Elle reste sur le client. |
| `~/.ssh/id_ed25519.pub` | Clé publique. Elle va sur le serveur. |

Ne partage jamais la clé privée. Elle prouve ton identité.

Si le serveur est très ancien et refuse ed25519, utilise RSA :

```bash
ssh-keygen -t rsa -b 4096
```

## 2. Copier la clé publique sur le serveur

```bash
ssh-copy-id utilisateur@adresse-du-serveur
```

Options utiles :

- Port différent de 22 : `ssh-copy-id -p 2222 utilisateur@adresse-du-serveur`
- Clé précise : `ssh-copy-id -i ~/.ssh/id_ed25519.pub utilisateur@adresse-du-serveur`

Le serveur demande ton mot de passe une dernière fois.

### Sans `ssh-copy-id` (méthode manuelle)

```bash
cat ~/.ssh/id_ed25519.pub | ssh utilisateur@adresse-du-serveur \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Sous Windows PowerShell, `ssh-copy-id` n'existe pas. Utilise cette variante :

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh utilisateur@adresse-du-serveur "cat >> ~/.ssh/authorized_keys"
```

## 3. Tester la connexion par clé

```bash
ssh utilisateur@adresse-du-serveur
```

Le client demande la passphrase de la clé, pas le mot de passe du serveur. Si c'est le cas, la clé fonctionne.

## 4. Éviter de saisir la passphrase à chaque connexion (optionnel)

Charge la clé dans `ssh-agent` :

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

## 5. Créer un raccourci de connexion (optionnel)

Ajoute ce bloc dans `~/.ssh/config` sur le client :

```
Host monserveur
    HostName adresse-du-serveur
    User utilisateur
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Connecte-toi ensuite avec `ssh monserveur`.

## 6. Désactiver le mot de passe sur le serveur

**Ne ferme pas ta session SSH ouverte. Garde-la jusqu'à la fin du test.** Une erreur de configuration peut t'exclure du serveur.

1. Vérifie que la connexion par clé fonctionne (étape 3).
2. Ouvre le fichier de configuration :
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
3. Définis ces trois options :
   ```
   PubkeyAuthentication yes
   PasswordAuthentication no
   KbdInteractiveAuthentication no
   ```
4. Cherche des surcharges dans `/etc/ssh/sshd_config.d/`. Un fichier `*.conf` peut réactiver `PasswordAuthentication yes` :
   ```bash
   sudo grep -r "PasswordAuthentication" /etc/ssh/
   ```
5. Vérifie la syntaxe :
   ```bash
   sudo sshd -t
   ```
   Aucune sortie signifie aucune erreur.
6. Recharge le service :
   ```bash
   sudo systemctl reload ssh
   ```
   Sur RHEL, Fedora et dérivés, le service s'appelle `sshd` : `sudo systemctl reload sshd`.
7. Ouvre un **second terminal**. Teste la connexion par clé.
8. Teste le refus du mot de passe :
   ```bash
   ssh -o PubkeyAuthentication=no utilisateur@adresse-du-serveur
   ```
   Le serveur doit répondre `Permission denied (publickey)`.

Optionnel : bloque aussi la connexion de `root` par mot de passe avec `PermitRootLogin prohibit-password`.

## Dépannage

Le serveur demande encore le mot de passe ? Vérifie ces points.

1. **Permissions sur le serveur.** SSH ignore les clés si les droits sont trop larges :
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   chmod go-w ~
   ```
2. **Diagnostic côté client.** Lance `ssh -v utilisateur@adresse-du-serveur`. Utilise `-vvv` pour plus de détails.
3. **Logs côté serveur.**
   ```bash
   sudo journalctl -u ssh -n 50
   ```
   Sur certaines distributions, lis `/var/log/auth.log` ou `/var/log/secure`.
4. **SELinux (RHEL, Fedora).** Restaure les contextes :
   ```bash
   restorecon -R ~/.ssh
   ```
5. **Mauvaise clé proposée.** Si le client possède plusieurs clés, force la bonne : `ssh -i ~/.ssh/id_ed25519 utilisateur@adresse-du-serveur`.

## Sauvegarde

Sauvegarde la clé privée dans un endroit sûr, par exemple un gestionnaire de mots de passe. Si tu perds la clé et que le mot de passe est désactivé, tu perds l'accès au serveur. Prévois un accès de secours (console du fournisseur, par exemple).
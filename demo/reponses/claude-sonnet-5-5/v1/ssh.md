# Configurer une connexion SSH par clé

Le poste local est ta machine. Le serveur est la machine distante.

## 1. Générer la paire de clés sur le poste local

```bash
ssh-keygen -t ed25519 -C "mon-poste"
```

1. Appuie sur Entrée pour accepter l'emplacement par défaut (`~/.ssh/id_ed25519`).
2. Saisis une passphrase. Elle protège la clé privée si quelqu'un la vole.

Ne partage jamais le fichier `id_ed25519`. C'est ta clé privée. Seul le fichier `id_ed25519.pub` quitte ton poste.

## 2. Copier la clé publique vers le serveur

```bash
ssh-copy-id utilisateur@adresse-du-serveur
```

Saisis le mot de passe une dernière fois. La commande ajoute la clé publique dans `~/.ssh/authorized_keys` sur le serveur.

Si `ssh-copy-id` n'existe pas (Windows, par exemple), utilise cette commande :

```bash
cat ~/.ssh/id_ed25519.pub | ssh utilisateur@adresse-du-serveur "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

## 3. Tester la connexion par clé

```bash
ssh utilisateur@adresse-du-serveur
```

Le serveur doit demander la passphrase de la clé, pas le mot de passe du compte. Si ce n'est pas le cas, ne passe pas à l'étape 4.

## 4. Désactiver le mot de passe sur le serveur

Ne ferme pas ta session SSH ouverte avant la fin de l'étape 5. Une erreur de configuration te bloque l'accès.

1. Ouvre le fichier de configuration :
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
2. Modifie ou ajoute ces lignes :
   ```
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```
3. Enregistre le fichier.
4. Vérifie la syntaxe :
   ```bash
   sudo sshd -t
   ```
5. Recharge le service :
   ```bash
   sudo systemctl reload ssh
   ```
   Sur RHEL, Fedora et dérivés, le service s'appelle `sshd`.

## 5. Vérifier depuis une seconde session

1. Ouvre un nouveau terminal sur le poste local.
2. Connecte-toi : `ssh utilisateur@adresse-du-serveur`.
3. Vérifie que la connexion réussit avec la clé.

Pour confirmer que le mot de passe est refusé, force-le :

```bash
ssh -o PubkeyAuthentication=no utilisateur@adresse-du-serveur
```

Le serveur doit répondre `Permission denied (publickey)`.

## Dépannage

- **Le serveur demande encore le mot de passe.** Un fichier de `/etc/ssh/sshd_config.d/` peut remplacer ton réglage. Vérifie avec `sudo sshd -T | grep -i passwordauthentication`.
- **La clé est refusée.** Vérifie les droits sur le serveur : `~/.ssh` en `700`, `authorized_keys` en `600`.
- **Tu utilises plusieurs clés.** Précise la clé avec `ssh -i ~/.ssh/id_ed25519 utilisateur@adresse-du-serveur`.
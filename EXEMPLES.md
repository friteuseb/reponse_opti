# Exemples avant / après

Exemples rédigés à la main pour illustrer chaque règle. Pour des réponses réelles de modèle, voir la [page de démo](https://friteuseb.github.io/reponse_opti/demo/) et le dossier [`demo/reponses/`](demo/reponses/).

## 1. Explication : « C'est quoi un cache ? »

**Avant** (1 phrase, 46 mots)

> Un cache constitue essentiellement une couche de stockage à haute vitesse qui permet de conserver à portée de main les données fréquemment sollicitées, afin que votre application puisse récupérer ces informations considérablement plus vite plutôt que d'interroger de manière répétée la base de données sous-jacente.

**Après** (5 phrases, 11 mots au plus)

> Un **cache** est une mémoire petite et rapide. Il garde une copie des **données** que vous utilisez souvent. Quand vous demandez une **donnée**, le système lit d'abord le **cache**. C'est plus rapide que de lire la **base de données**. La **base de données** travaille moins.

Ce qui change : « données », « informations » et « base de données sous-jacente » désignaient deux choses avec trois noms. Il reste deux noms, un par chose.

## 2. Procédure : redémarrer un service

**Avant**

> Afin de procéder au redémarrage du service, il conviendrait dans un premier temps de s'assurer que les modifications de configuration ont bien été enregistrées, puis il sera nécessaire d'effectuer un rechargement de systemd avant de relancer le service en question.

**Après**

> 1. Enregistre le fichier de configuration.
> 2. Recharge systemd : `systemctl --user daemon-reload`.
> 3. Redémarre le service : `systemctl --user restart comfyui`.
> 4. Vérifie l'état : `systemctl --user status comfyui`.

Ce qui change : une action par étape, à l'impératif, dans l'ordre. La commande exacte remplace « le service en question ».

## 3. Avertissement

**Avant**

> Il est important de noter que la suppression de ce lien symbolique pourrait potentiellement entraîner des problèmes de synchronisation, dans la mesure où il est référencé dans le fichier .stignore.

**Après**

> Danger : ne supprime pas ce lien. Le fichier `.stignore` le référence : sans lui, Syncthing copie 14 Go de vidéos.

Ce qui change : l'ordre vient en premier. La conséquence est concrète et chiffrée.

## 4. Compte rendu

**Avant**

> Globalement, la migration s'est plutôt bien déroulée, même si quelques difficultés ont été rencontrées au niveau de certaines tables, ce qui a nécessité un certain nombre d'ajustements, mais au final les performances semblent nettement meilleures.

**Après**

> La migration est terminée. Deux tables (`orders`, `logs`) ont bloqué sur des index en double. J'ai supprimé les doublons, puis relancé la migration. Les requêtes de la page d'accueil passent de 820 ms à 140 ms.

Ce qui change : « quelques difficultés », « certaines tables » et « nettement meilleures » deviennent des noms et des chiffres.

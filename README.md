# Écriture contrôlée

Une règle de 12 lignes pour que les assistants IA (Claude, ChatGPT, Codex, Cursor…) écrivent en français **lisible** : des phrases courtes, la voix active, un seul nom par chose, pas de remplissage.

> Un **cache** est une mémoire petite et rapide. Il garde une copie des **données** que vous utilisez souvent. Quand vous demandez une **donnée**, le système lit d'abord le **cache**.

Au lieu de :

> Un cache constitue essentiellement une couche de stockage à haute vitesse qui permet de conserver à portée de main les données fréquemment sollicitées, afin que votre application puisse récupérer ces informations considérablement plus vite…

## D'où ça vient

Le 4 octobre 2026, Andrej Karpathy [a conseillé](https://x.com/karpathy/status/2105819303471976479) de demander aux LLM d'écrire en **ASD-STE100**. C'est l'anglais contrôlé des manuels de maintenance aéronautique : un mécanicien doit comprendre une consigne du premier coup, quelle que soit sa langue maternelle. Les LLM connaissent bien cette norme. Karpathy conseille aussi de l'appliquer « à 80 % », car la norme complète est très stricte.

Problème : ASD-STE100 ne concerne que l'anglais. Ce repo transpose ses principes au français, avec les tics propres au français : verbes vides (« procéder à »), chaînes de « de », formules creuses (« Il est important de noter que »).

## Les 12 règles

Le texte complet est dans [`REGLE.md`](REGLE.md). En résumé :

| # | Règle | Exemple |
|---|---|---|
| 1 | Une phrase, une idée : 20 mots au plus (procédure), 25 (explication) | |
| 2 | 6 phrases au plus par paragraphe | Au-delà : une liste |
| 3 | Voix active | « Le script copie le fichier » |
| 4 | Procédures à l'impératif, une action par étape | « Arrête le service. » |
| 5 | Un terme, un sens, sans synonymes pour varier | « serveur » partout, pas « machine » puis « hôte » |
| 6 | Mots courants | « avant », pas « préalablement à » |
| 7 | Pas de verbes vides | « vérifier », pas « procéder à la vérification » |
| 8 | Pas de remplissage | ~~« N'hésitez pas à »~~ |
| 9 | Pas plus de trois compléments en « de » à la suite | |
| 10 | Des chiffres, pas des adjectifs | « 3 s », pas « très rapide » |
| 11 | Avertissement : l'ordre d'abord, la raison ensuite | « Ne supprime pas ce lien. Syncthing le synchronise. » |
| 12 | Termes techniques exacts | La simplicité porte sur la phrase, pas sur le métier |

Quatre exemples avant / après (explication, procédure, avertissement, compte rendu) : [`EXEMPLES.md`](EXEMPLES.md).

## Installation

### Option 1 : règle permanente (recommandé)

Copiez le contenu de [`REGLE.md`](REGLE.md) dans le fichier de règles de votre outil :

| Outil | Fichier |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` (tous les projets) ou `CLAUDE.md` à la racine d'un projet |
| Codex, OpenCode | `AGENTS.md` |
| Cursor | `.cursor/rules/ecriture-controlee.mdc` |
| ChatGPT, Claude.ai | Paramètres → Instructions personnalisées |

En une commande, pour Claude Code :

```bash
curl -s https://raw.githubusercontent.com/friteuseb/reponse_opti/main/REGLE.md >> ~/.claude/CLAUDE.md
```

### Option 2 : skill Claude Code (à la demande)

Le skill ne s'active que si vous le demandez (« réécris ça en écriture contrôlée », « simplifie cette procédure »). Il vérifie aussi le texte avant de le rendre.

```bash
mkdir -p ~/.claude/skills/ecriture-controlee
curl -s https://raw.githubusercontent.com/friteuseb/reponse_opti/main/skills/ecriture-controlee/SKILL.md \
  -o ~/.claude/skills/ecriture-controlee/SKILL.md
```

### Option 3 : à la volée

Collez la règle en début de conversation, ou demandez simplement : « Réponds en écriture contrôlée, à 80 % d'ASD-STE100. »

## Quand ne pas l'utiliser

Cette règle vise le texte qu'on doit **comprendre** : explications, procédures, documentation, comptes rendus. Elle aplatit le texte qu'on doit **ressentir** : pages de vente, textes de marque, récits. La règle les exclut donc explicitement.

## Crédits

- [Andrej Karpathy](https://x.com/karpathy/status/2105819303471976479), pour l'idée.
- [ASD-STE100](https://www.asd-ste100.org/), la norme d'origine. Ce projet n'est pas affilié à l'ASD et ne prétend pas être conforme à la norme.
- [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html), qui contrôle la conformité STE en anglais et en chinois, et m'a donné envie de faire la version française.

## Licence

MIT. Copiez, adaptez, partagez.

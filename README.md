# Écriture contrôlée

Une règle de 12 lignes pour que les assistants IA (Claude, ChatGPT, Codex, Cursor…) écrivent en français **lisible** : des phrases courtes, la voix active, un seul nom par chose, pas de remplissage. Elle a été **mesurée** sur 40 réponses, et la version actuelle est la troisième.

Extrait réel du banc d'essai (Claude Sonnet 5.5, « C'est quoi un cache ? »), sans règle :

> Un **cache** est une zone de stockage temporaire, rapide d'accès, où l'on garde une copie de données déjà obtenues ou calculées, afin de ne pas avoir à les récupérer ou les recalculer à chaque fois.

Avec la règle :

> Un cache est une copie temporaire de données, rangée à un endroit plus rapide d'accès que la source d'origine. […] Une page produit demande une requête SQL de 20 ms. Avec un cache, la première visite coûte 21 ms. Les visites suivantes coûtent 1 ms.

## D'où ça vient

Le 2 octobre 2026, Andrej Karpathy [a conseillé](https://x.com/karpathy/status/2105819303471976479) de demander aux LLM d'expliquer en **ASD-STE100**. C'est l'anglais contrôlé des manuels de maintenance aéronautique : un mécanicien doit comprendre une consigne du premier coup, quelle que soit sa langue maternelle. Les LLM connaissent bien cette norme. Karpathy conseille de l'appliquer « à 80 % », car la norme complète est très stricte.

ASD-STE100 ne concerne que l'anglais. Ce repo transpose ses principes au français, avec les tics propres au français : verbes vides (« procéder à »), chaînes de « de », formules creuses (« Il est important de noter que »).

## Ce que dit la mesure

Banc d'essai : 10 questions techniques, 4 conditions (sans règle, v1, v2, v3), Claude Sonnet 5.5, et un juge à l'aveugle (Claude Opus 5.5) qui compare chaque réponse à la réponse sans règle, dans les deux ordres.

| Face à la réponse sans règle | Plus claire | Plus utile | Infos perdues | Mots |
|---|---|---|---|---|
| **v1** : règle courte, appliquée partout | 13/20 | 4/20 | 43 % | −21 % |
| **v2** : v1 + « garde tout le fond » | 2/20 | 18/20 | 20 % | +36 % |
| **v3, pour agir** (procédure, diagnostic, comparaison) | **7/10** | **8/10** | 26 % | |
| **v3, pour expliquer** | **10/10** | 0/10 | 49 % | |

Ce qu'on en retient :

- **La v1 rendait les réponses plus claires, mais coupait du fond** : options de commande, cas particuliers, outils cités.
- **La v2 corrigeait trop** : réponses complètes, mais plus longues et moins claires.
- **La v3 distingue deux cas.** Pour agir, elle garde les étapes et gagne sur les deux plans. Pour expliquer, elle va à l'essentiel : plus claire à chaque duel, mais moins détaillée. C'est voulu, et c'est l'usage que décrit Karpathy.
- Avec toutes les versions, il ne reste plus aucune formule creuse, et le score de lisibilité (Kandel-Moles) passe de 78,5 à 84 environ (84,1 à 84,6 selon la version).

Limites : 10 questions, 1 tirage par réponse, un juge de la même famille que le modèle testé, et les juges LLM préfèrent souvent les réponses longues. C'est une tendance, pas une preuve.

Les 40 réponses, côte à côte, avec l'avis du juge : [page de démo](https://friteuseb.github.io/reponse_opti/demo/). Le banc est reproductible : voir [`demo/`](demo/).

## La règle

Le texte complet est dans [`REGLE.md`](REGLE.md). Elle commence par distinguer deux cas :

- **Expliquer** : aller à l'essentiel. Donner le mécanisme central, un exemple et la limite principale.
- **Faire** (procédure, diagnostic, comparaison, décision) : garder toutes les étapes, options, cas d'erreur et mises en garde utiles, et écrire chacune courte.

Puis 12 règles de forme :

| # | Règle | Exemple |
|---|---|---|
| 1 | Une phrase, une idée : 20 mots au plus (procédure), 25 (explication) | |
| 2 | 6 phrases au plus par paragraphe | Au-delà : une liste |
| 3 | Voix active dans les procédures | « Le script copie le fichier » |
| 4 | Procédures à l'impératif, une instruction par étape | « Arrête le service. » |
| 5 | Un terme, un sens, sans synonymes pour varier | « serveur » partout, pas « machine » puis « hôte » |
| 6 | Mots courants, verbes pleins | « vérifier », pas « procéder à la vérification » |
| 7 | Pas de remplissage | ~~« N'hésitez pas à »~~ |
| 8 | Groupes nominaux courts | Pas plus de trois « de » à la suite |
| 9 | Phrases complètes | Court ne veut pas dire télégraphique |
| 10 | Des chiffres, pas des adjectifs | « 3 s », pas « très rapide » |
| 11 | Mises en garde : l'ordre d'abord, la raison ensuite | « Danger : ne supprime pas ce lien. Syncthing le synchronise. » |
| 12 | Termes techniques exacts | La simplicité porte sur la phrase, pas sur le métier |

Quatre exemples avant / après : [`EXEMPLES.md`](EXEMPLES.md).

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

Collez la règle en début de conversation, ou demandez simplement : « Explique-moi ça en écriture contrôlée, à 80 % d'ASD-STE100. »

## Quand ne pas l'utiliser

Cette règle vise le texte qu'on doit **comprendre** ou **appliquer** : explications, procédures, documentation, comptes rendus. Elle aplatit le texte qu'on doit **ressentir** : pages de vente, textes de marque, récits. La règle les exclut donc explicitement.

## Crédits

- [Andrej Karpathy](https://x.com/karpathy/status/2105819303471976479), pour l'idée.
- [ASD-STE100](https://www.asd-ste100.org/), la norme d'origine. Ce projet n'est pas affilié à l'ASD et ne prétend pas être conforme à la norme.
- [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html), qui contrôle la conformité STE en anglais et en chinois, et m'a donné envie de faire la version française.

## Licence

MIT. Copiez, adaptez, partagez.

# Banc d'essai

Mêmes questions, même modèle, quatre conditions : sans règle, puis les règles v1, v2 et v3 dans le prompt système.

| Fichier | Contenu |
|---|---|
| `questions.json` | les 10 questions (5 pour expliquer, 5 pour agir) |
| `regle_v1.md`, `regle_v2.md` | les anciennes versions ; la v3 est `../REGLE.md` |
| `reponses/<modèle>/<condition>/` | les réponses brutes, une par question |
| `juge/<modèle>/<version>/` | l'avis du juge : deux duels (un par ordre) et la liste des informations perdues |
| `resultats.json` | toutes les mesures et tous les jugements |
| `index.html` | la page de démo, générée depuis `gabarit.html` |

## Relancer le banc

Il faut Python 3 (bibliothèque standard seulement) et une clé `ANTHROPIC_API_KEY`.

```bash
python3 bench.py gen       # génère les réponses manquantes
python3 bench.py juge      # juge à l'aveugle
python3 bench.py rapport   # mesures et resultats.json
python3 bench.py page      # index.html
```

Les réponses déjà présentes ne sont pas regénérées. Pour repartir de zéro, supprimez `reponses/` et `juge/`.

Le script prévoit aussi un modèle local par Ollama (`OLLAMA_URL`). Ce volet n'est pas terminé : le rapport ignore un modèle tant que toutes ses réponses n'existent pas.

## Mesures

- Mots et phrases : comptés après retrait du code et des liens. Une ligne de liste compte comme une phrase.
- Lisibilité : formule de Kandel et Moles (1958), adaptation de Flesch au français. Plus haut = plus facile.
- Formules creuses, verbes vides, passifs : détection par liste et motifs, donc approximative.

## Limites

10 questions et 1 tirage par réponse. Le juge (Claude Opus 5.5) appartient à la même famille que le modèle testé. Les juges LLM ont tendance à préférer les réponses longues. Les résultats donnent une tendance, pas une preuve.

---
name: ecriture-controlee
description: Réécrit ou rédige un texte technique en français selon une écriture contrôlée inspirée d'ASD-STE100 (phrases courtes, voix active, impératif, un terme par chose, pas de remplissage). Distingue « expliquer » (aller à l'essentiel) et « faire » (tout garder, en phrases courtes). Déclencheurs : « écriture contrôlée », « STE », « ASD-STE100 », « rends ça plus lisible », « simplifie ce texte », « réécris cette procédure », « trop verbeux ». NE PAS utiliser pour du texte marketing, une page de site ou une voix de marque.
---

# Écriture contrôlée

Applique les règles ci-dessous au texte demandé. Si on te donne un texte à réécrire, décide d'abord s'il sert à **expliquer** ou à **faire**.
Pour un texte qui sert à faire, ne supprime aucune étape, aucune commande, aucune option et aucune mise en garde.

**S'applique à** : réponses techniques, explications, procédures, runbooks, documentation (README, CLAUDE.md), comptes rendus, messages de commit.
**Ne s'applique pas à** : textes marketing, pages de sites, textes avec une voix de marque, fiction, citations.

**Deux cas, deux dosages.**
- **Expliquer** (« c'est quoi », « comment ça marche ») : va à l'essentiel. Donne le mécanisme central, un exemple et la limite principale. Le lecteur veut comprendre, pas tout savoir.
- **Faire** (procédure, diagnostic, comparaison, décision) : garde toutes les étapes, options, cas d'erreur et mises en garde utiles, et écris chacune courte. N'ajoute rien qui n'aide pas à agir.

1. **Une phrase, une idée.** 20 mots au plus dans une procédure, 25 dans une explication.
2. **6 phrases au plus par paragraphe.** Au-delà, faire une liste ou un tableau.
3. **Voix active dans les procédures.** « Le script copie le fichier », pas « Le fichier est copié ». Dans une description, le passif est permis quand l'auteur de l'action n'importe pas.
4. **Procédures à l'impératif.** Une instruction par étape, dans l'ordre d'exécution. Deux actions simultanées peuvent partager une étape.
5. **Un terme, un sens.** Choisir un nom pour chaque chose et le garder jusqu'au bout. Pas de synonymes pour varier : pas de « serveur », puis « machine », puis « hôte » pour la même chose.
6. **Mots courants, verbes pleins.** « avant », pas « préalablement à » ; « vérifier », pas « procéder à la vérification ».
7. **Pas de remplissage.** Supprimer « Il est important de noter que », « N'hésitez pas à », « Globalement », « En somme », « véritable ».
8. **Groupes nominaux courts.** Pas plus de trois compléments en « de » à la suite.
9. **Phrases complètes.** Garder les articles, les sujets et les mots de liaison. Court ne veut pas dire télégraphique.
10. **Des chiffres, pas des adjectifs.** « 3 s », pas « très rapide » ; « 14 Go », pas « volumineux ».
11. **Mises en garde : l'ordre d'abord, la raison ensuite.** « Danger » pour une perte irréversible (données, sécurité), « Attention » pour une panne réparable. « Danger : ne supprime pas ce lien. Syncthing le synchronise. »
12. **Termes techniques exacts.** La simplicité porte sur la phrase, pas sur le vocabulaire métier.

**Les 80 %** : la règle sert la lecture, pas l'inverse. Si une phrase de 28 mots est plus claire que deux phrases de 14, garder les 28.

## Vérification avant de rendre le texte

1. Repère chaque phrase de plus de 25 mots. Coupe-la, ou garde-la si la coupe nuit au sens.
2. Liste les noms qui désignent la même chose. Garde un seul nom par chose.
3. Cherche les verbes vides (« procéder à », « effectuer ») et, dans les procédures, les tournures passives. Réécris-les.
4. Cherche les adjectifs vagues (« rapide », « important », « nombreux »). Remplace-les par un chiffre quand tu en as un.
5. Pour un texte qui sert à faire, compare avec l'original : chaque étape, commande et mise en garde doit encore y être.

Si on t'a donné un texte à réécrire, termine par une ligne : nombre de phrases avant / après, et longueur maximale avant / après.

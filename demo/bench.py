#!/usr/bin/env python3
"""Banc d'essai : mêmes questions, avec et sans la règle d'écriture contrôlée.

  python3 bench.py gen      # génère les réponses (mises en cache dans reponses/)
  python3 bench.py juge     # juge à l'aveugle + contrôle des informations perdues
  python3 bench.py rapport  # calcule les mesures et écrit resultats.json

Variables : ANTHROPIC_API_KEY, OLLAMA_URL (défaut http://gx10:11434).
"""
import json, os, re, sys, time, random, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ICI = Path(__file__).parent
REGLE = (ICI.parent / "REGLE.md").read_text()
QUESTIONS = json.loads((ICI / "questions.json").read_text())
OLLAMA = os.environ.get("OLLAMA_URL", "http://gx10:11434")
JUGE = "claude-opus-5-5"

MODELES = {
    "claude-sonnet-5-5": {"api": "anthropic", "nom": "Claude Sonnet 5.5"},
    "qwen3.8:27b": {"api": "ollama", "nom": "Qwen 3.8 27B (local)"},
}
BASE = "Tu es un assistant. Réponds en français."
# v1 : première version publiée. v2 : ajoute « Le fond d'abord » (la v1 faisait perdre du contenu).
# v3 : distingue « expliquer » (aller à l'essentiel) et « faire » (tout garder, en phrases courtes).
REGLE_V1 = (ICI / "regle_v1.md").read_text()
REGLE_V2 = (ICI / "regle_v2.md").read_text()
CONDITIONS = {"sans": BASE, "v1": BASE + "\n\n" + REGLE_V1, "v2": BASE + "\n\n" + REGLE_V2, "v3": BASE + "\n\n" + REGLE}
VARIANTES = ("v1", "v2", "v3")


def post(url, data, headers, timeout=600):
    req = urllib.request.Request(url, json.dumps(data).encode(), {"content-type": "application/json", **headers})
    for essai in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            if essai == 3:
                raise
            print(f"  nouvel essai ({e})", file=sys.stderr)
            time.sleep(5 * (essai + 1))


def claude(model, system, user, max_tokens=16000):
    t0 = time.time()
    r = post("https://api.anthropic.com/v1/messages",
             {"model": model, "max_tokens": max_tokens, "system": system,
              "messages": [{"role": "user", "content": user}]},
             {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
    texte = "".join(b.get("text", "") for b in r["content"])
    return texte, {"tokens_sortie": r["usage"]["output_tokens"], "arret": r.get("stop_reason"), "secondes": round(time.time() - t0, 1)}


def ollama(model, system, user):
    t0 = time.time()
    r = post(f"{OLLAMA}/api/chat",
             {"model": model, "think": False, "stream": False,
              "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}, {})
    return r["message"]["content"], {"tokens_sortie": r.get("eval_count"), "secondes": round(time.time() - t0, 1)}


def fichier(model, cond, qid):
    return ICI / "reponses" / model.replace(":", "_") / cond / f"{qid}.md"


# ---------- génération ----------

def generer(model, cond, q):
    f = fichier(model, cond, q["id"])
    if f.exists():
        return
    api = MODELES[model]["api"]
    texte, meta = (claude if api == "anthropic" else ollama)(model, CONDITIONS[cond], q["q"])
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(texte)
    f.with_suffix(".json").write_text(json.dumps(meta))
    print(f"  {model} / {cond} / {q['id']} : {meta}")


def cmd_gen():
    taches = [(m, c, q) for m in MODELES for c in CONDITIONS for q in QUESTIONS]
    # Claude en parallèle, le modèle local une requête à la fois.
    with ThreadPoolExecutor(4) as ex_claude, ThreadPoolExecutor(1) as ex_local:
        futs = [(ex_claude if MODELES[m]["api"] == "anthropic" else ex_local).submit(generer, m, c, q)
                for m, c, q in taches]
        for f in futs:
            f.result()


# ---------- juge ----------

PROMPT_DUEL = """Une personne a posé cette question à un assistant :

<question>{q}</question>

Voici deux réponses.

<reponse_A>
{a}
</reponse_A>

<reponse_B>
{b}
</reponse_B>

Compare-les du point de vue de la personne qui a posé la question.
- clarte : quelle réponse se lit et se comprend le plus facilement ?
- utilite : quelle réponse l'aide le mieux à comprendre ou à agir (exactitude, informations utiles, actionnable) ?

Réponds uniquement en JSON : {{"clarte": "A" | "B" | "egal", "utilite": "A" | "B" | "egal", "raison": "<une phrase>"}}"""

PROMPT_INFOS = """Question posée : <question>{q}</question>

<reponse_reference>
{ref}
</reponse_reference>

<reponse_a_verifier>
{cand}
</reponse_a_verifier>

1. Liste les informations utiles de la réponse de référence (faits, conseils, commandes, mises en garde). Ignore les formules de politesse et les répétitions.
2. Pour chacune, indique si la réponse à vérifier la contient (même formulée autrement).
3. Liste aussi les informations utiles présentes seulement dans la réponse à vérifier.

Réponds uniquement en JSON : {{"infos_reference": <nombre>, "manquantes": ["<info>", ...], "en_plus": ["<info>", ...]}}"""


def json_de(texte):
    return json.loads(re.search(r"\{.*\}", texte, re.S).group(0))


def demander_json(prompt, max_tokens):
    for essai in range(3):
        r, _ = claude(JUGE, "Tu es un évaluateur rigoureux et impartial. Tu réponds uniquement en JSON.", prompt, max_tokens)
        try:
            return json_de(r)
        except Exception:
            print(f"  JSON illisible (essai {essai + 1}) : {r[:300]!r}", file=sys.stderr)
    raise ValueError("le juge ne renvoie pas de JSON")


def juger(model, q, variante):
    sortie = ICI / "juge" / model.replace(":", "_") / variante / f"{q['id']}.json"
    if sortie.exists():
        return
    sans, avec = (fichier(model, c, q["id"]).read_text() for c in ("sans", variante))
    duels = []
    for ordre in (("sans", "avec"), ("avec", "sans")):  # les deux ordres, pour neutraliser le biais de position
        textes = {"sans": sans, "avec": avec}  # « avec » = la variante jugée
        v = demander_json(PROMPT_DUEL.format(q=q["q"], a=textes[ordre[0]], b=textes[ordre[1]]), 8000)
        traduire = {"A": ordre[0], "B": ordre[1], "egal": "egal"}
        duels.append({"ordre": ordre, "clarte": traduire[v["clarte"]], "utilite": traduire[v["utilite"]], "raison": v["raison"]})
    infos = demander_json(PROMPT_INFOS.format(q=q["q"], ref=sans, cand=avec), 12000)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"duels": duels, "infos": infos}, ensure_ascii=False, indent=1))
    print(f"  jugé : {model} / {variante} / {q['id']}")


def cmd_juge():
    with ThreadPoolExecutor(5) as ex:
        list(ex.map(lambda t: juger(*t), [(m, q, v) for m in MODELES for v in VARIANTES for q in QUESTIONS]))


# ---------- mesures ----------

MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+)*")
CREUSES = ["il est important", "il est essentiel", "il est crucial", "il est primordial", "il convient de",
           "il est à noter", "n'hésitez pas", "n’hésitez pas", "en somme", "globalement", "en résumé",
           "en conclusion", "véritable", "essentiellement", "en effet", "dans le cadre de", "au niveau de",
           "afin de", "permet de", "permettent de", "notamment", "bien sûr", "en d'autres termes"]
VIDES = re.compile(r"\b(procéd\w*|effectu\w*|réalis\w*)\s+(à\s+|un\w*\s+|la\s+|le\s+|l['’]|les\s+|des\s+)", re.I)
PASSIF = re.compile(r"\b(est|sont|était|étaient|sera|seront|serait|a été|ont été|être|soit|soient)\s+(\w+\s+)?"
                    r"\w+(é|ée|és|ées)\b", re.I)


def nettoyer(md):
    md = re.sub(r"```.*?```", " ", md, flags=re.S)          # blocs de code
    md = re.sub(r"`[^`]*`", "X", md)                        # code en ligne = un mot
    md = re.sub(r"^\s*\|?\s*:?-{3,}.*$", "", md, flags=re.M)  # séparateurs de tableau
    md = re.sub(r"https?://\S+", "X", md)
    md = re.sub(r"[*_#>|]", " ", md)
    return md


def phrases(md):
    out = []
    for ligne in nettoyer(md).splitlines():                  # une ligne de liste ou un titre = au moins une phrase
        ligne = re.sub(r"^\s*(\d+[.)]|[-+•])\s+", "", ligne)  # puces et numéros de liste
        for p in re.split(r"(?<=[.!?…])\s+|\s+[–—]\s+(?=[A-ZÀ-Ö])", ligne):
            mots = MOT.findall(p)
            if mots:
                out.append(mots)
    return out


def syllabes(mot):
    m = mot.lower()
    n = len(re.findall(r"[aeiouyàâäéèêëîïôöùûüœæ]+", m))
    if n > 1 and re.search(r"[^aeiouy](e|es|ent)$", m):
        n -= 1
    return max(n, 1)


def mesures(md):
    ph = phrases(md)
    mots = [w for p in ph for w in p]
    longueurs = [len(p) for p in ph]
    bas = md.lower()
    n_mots = max(len(mots), 1)
    return {
        "mots": len(mots),
        "phrases": len(ph),
        "mots_par_phrase": round(len(mots) / max(len(ph), 1), 1),
        "phrase_max": max(longueurs, default=0),
        "phrases_plus_25": sum(l > 25 for l in longueurs),
        "formules_creuses": sum(bas.count(c) for c in CREUSES),
        "verbes_vides": len(VIDES.findall(md)),
        "passifs": len(PASSIF.findall(md)),
        # Kandel & Moles (1958), adaptation de Flesch au français : plus haut = plus facile.
        "kandel_moles": round(207 - 1.015 * len(mots) / max(len(ph), 1) - 73.6 * sum(map(syllabes, mots)) / n_mots, 1),
    }


def mediane(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else round((v[n // 2 - 1] + v[n // 2]) / 2, 1)


GROUPES = {"tout": lambda q: True, "expliquer": lambda q: q["type"] == "explication",
           "faire": lambda q: q["type"] != "explication"}


def cmd_rapport():
    res = {"juge": JUGE, "questions": QUESTIONS, "modeles": {}, "detail": []}
    for m, info in MODELES.items():
        # Un modèle n'entre dans le rapport que si toutes ses réponses existent.
        if not all(fichier(m, c, q["id"]).exists() for c in CONDITIONS for q in QUESTIONS):
            print(f"{m} : réponses incomplètes, ignoré")
            continue
        lignes = []
        for q in QUESTIONS:
            ligne = {"modele": m, **q, "reponses": {}, "juge": {}}
            for c in CONDITIONS:
                f = fichier(m, c, q["id"])
                ligne["reponses"][c] = {"texte": f.read_text(), "mesures": mesures(f.read_text())}
            for v in VARIANTES:
                jf = ICI / "juge" / m.replace(":", "_") / v / f"{q['id']}.json"
                if jf.exists():
                    ligne["juge"][v] = json.loads(jf.read_text())
            lignes.append(ligne)
        conditions = {}
        for c in CONDITIONS:
            ms = [l["reponses"][c]["mesures"] for l in lignes]
            conditions[c] = {
                "medianes": {k: mediane([x[k] for x in ms]) for k in ("mots", "mots_par_phrase", "phrase_max", "kandel_moles")},
                "totaux": {k: sum(x[k] for x in ms) for k in ("phrases_plus_25", "formules_creuses", "verbes_vides", "passifs")},
            }
        variantes = {}
        for v in VARIANTES:
            variantes[v] = {}
            for g, garde in GROUPES.items():
                js = [l["juge"][v] for l in lignes if garde(l) and v in l["juge"]]
                ref = sum(x["infos"]["infos_reference"] for x in js)
                man = sum(len(x["infos"]["manquantes"]) for x in js)
                variantes[v][g] = {
                    "duels": 2 * len(js),
                    "clarte": sum(d["clarte"] == "avec" for x in js for d in x["duels"]),
                    "utilite": sum(d["utilite"] == "avec" for x in js for d in x["duels"]),
                    "infos_reference": ref, "manquantes": man,
                    "en_plus": sum(len(x["infos"]["en_plus"]) for x in js),
                    "perdues_pct": round(100 * man / ref) if ref else None,
                }
        res["modeles"][m] = {"nom": info["nom"], "conditions": conditions, "variantes": variantes}
        res["detail"] += lignes
        print(f"\n## {info['nom']}")
        for c, r in conditions.items():
            print(f"  {c:5} {r['medianes']}  {r['totaux']}")
        for v, gs in variantes.items():
            for g, r in gs.items():
                print(f"  {v} {g:9} clarté {r['clarte']}/{r['duels']}  utilité {r['utilite']}/{r['duels']}  perdues {r['perdues_pct']} %")
    (ICI / "resultats.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


def cmd_page():
    """Assemble la page de démo : index.html (page complète, pour GitHub Pages) et le fragment pour un artefact."""
    donnees = (ICI / "resultats.json").read_text().replace("</", "<\\/")
    fragment = (ICI / "gabarit.html").read_text().replace("__DONNEES__", donnees)
    (ICI / "index.html").write_text('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
                                    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                                    + fragment.replace("<main", "</head>\n<body>\n<main", 1) + "\n</body>\n</html>\n")
    sortie = Path(os.environ.get("FRAGMENT", ICI / "fragment.html"))
    sortie.write_text(fragment)
    print(f"index.html et {sortie} écrits")


if __name__ == "__main__":
    {"gen": cmd_gen, "juge": cmd_juge, "rapport": cmd_rapport, "page": cmd_page}[sys.argv[1]]()

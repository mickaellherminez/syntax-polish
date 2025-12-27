# 📘 Instructions – Syntax Polish (Alfred Workflow)

## 1. Objectif du projet

**Syntax Polish** est un workflow Alfred permettant de reformuler, corriger ou améliorer un texte
(en particulier du texte sélectionné) en s’appuyant sur **différents fournisseurs d’IA**  
(ex. : DeepSeek, OpenAI, Anthropic, etc.).

🎯 Objectifs clés :
- Être **simple à installer** pour les utilisateurs Alfred
- Être **100 % sécurisé** (aucune clé API partagée ou stockée en clair)
- Être **extensible multi-IA**
- Être **maintenable et open-source friendly**

---

## 2. Principe général de fonctionnement

### Flux utilisateur

1. L’utilisateur sélectionne du texte (ou saisit une entrée)
2. Il déclenche le workflow Alfred (raccourci clavier / mot-clé)
3. Le workflow :
   - détecte le fournisseur d’IA actif
   - récupère la clé API **depuis le Keychain macOS**
   - envoie le texte à l’API sélectionnée
4. La réponse est :
   - affichée dans Alfred
   - et/ou copiée automatiquement dans le presse-papier

---

## 3. Sécurité – RÈGLES ABSOLUES 🔒

### ❌ Interdictions strictes
- ❌ Aucune clé API **codée en dur**
- ❌ Aucune clé API dans :
  - le code source
  - `info.plist`
  - les variables par défaut Alfred
  - le dépôt GitHub
- ❌ Aucun log affichant une clé ou un token

### ✅ Règles obligatoires
- ✅ Les clés API sont **stockées exclusivement dans le Keychain macOS**
- ✅ Chaque utilisateur configure **sa propre clé**
- ✅ Le workflow refuse de s’exécuter si la clé est absente
- ✅ Les requêtes réseau utilisent TLS par défaut (ne jamais désactiver la vérification SSL/TLS, ex. pas de `verify=False`)

---

## 4. Gestion des clés API (Keychain macOS)

### Principe
Chaque fournisseur d’IA possède un **service Keychain dédié**.

Exemples :
- `syntax-polish-deepseek`
- `syntax-polish-openai`
- `syntax-polish-anthropic`

### Comportement attendu du code
- Lire la clé via la commande `security find-generic-password`
- Ne jamais afficher la clé, même en debug
- Retourner une erreur claire si la clé n’existe pas

---

## 5. Support multi-IA (obligatoire)

### Architecture attendue

- Chaque fournisseur IA est implémenté dans un **module isolé**
- Chaque module expose une interface commune :
  - `send_request(text, options) -> response`

### Exemples de providers
- DeepSeek
- OpenAI
- Anthropic
- (extensible sans modifier le cœur du workflow)

### Sélection du provider
- Par variable Alfred (`AI_PROVIDER`)
- Ou par défaut documenté dans le README
- Jamais codé en dur dans la logique métier

---

## 6. Structure générale du projet

```
src/
├─ python/
│  ├─ main.py              # Point d’entrée du workflow
│  ├─ providers/           # Implémentations IA
│  │  ├─ deepseek.py
│  │  ├─ openai.py
│  │  └─ __init__.py
│  ├─ utils/
│  │  ├─ keychain.py       # Accès sécurisé aux clés
│  │  ├─ alfred.py         # Helpers Alfred
│  │  ├─ clipboard.py
│  │  └─ __init__.py
│  └─ lib/                 # Dépendances éventuelles vendorisées
workflow/
├─ info.plist
├─ icon.png
└─ scripts/
dist/
└─ Syntax-Polish.alfredworkflow

```

---

## 7. Style de code Python (obligatoire)

- Conformité **PEP 8**
- Formatage automatique recommandé : **Black**
- Linting recommandé : **Ruff**
- Typage Python (`typing`) fortement conseillé
- Fonctions courtes, lisibles, testables
- Docstrings obligatoires pour les modules publics

---

## 8. Gestion des erreurs & UX

### Principes
- Toujours **fail fast** (échouer vite)
- Toujours **fail clearly** (échouer clairement)
- Jamais de stack trace brute dans Alfred

### Exemples d’erreurs gérées
- Clé API manquante
- Provider inconnu
- Erreur réseau / timeout
- Réponse API invalide

---

## 9. Logging & Debug

- Mode debug activable via variable (`DEBUG=1`)
- Logs :
  - informatifs
  - jamais verbeux par défaut
  - jamais sensibles
- Aucun log persistant obligatoire

---

## 10. Données utilisateur & confidentialité

- Le texte envoyé à l’IA provient :
  - soit de la sélection utilisateur
  - soit d’un input volontaire
- Aucun texte n’est stocké localement
- Aucun tracking, analytics ou télémétrie

📄 Une page `docs/privacy.md` doit expliquer clairement ce point.

---

## 11. Distribution

### Méthode officielle
- Dépôt GitHub public
- GitHub Releases avec :
  - `.alfredworkflow`
  - `SHA256SUMS.txt`
  - changelog

### Versioning
- SemVer (`MAJOR.MINOR.PATCH`)
- Changelog obligatoire à chaque release

---

## 12. Contributions

- Toute contribution doit :
  - respecter ces instructions
  - respecter les règles Cursor
  - ne jamais introduire de secret
- Toute PR violant les règles de sécurité sera refusée

---

## 13. Philosophie du projet

> Simple pour l’utilisateur  
> Sécurisé par défaut  
> Extensible sans dette technique  
> Lisible pour l’humain avant tout  

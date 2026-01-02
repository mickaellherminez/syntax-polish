# Changelog

Le projet suit **SemVer** : `MAJOR.MINOR.PATCH`.

## [1.2.2] - 2026-01-02

### Changed
- Clarification UX autour du raccourci clavier Alfred :
  - la procédure pour définir soi‑même un raccourci (bloc Hotkey dans Alfred) est détaillée pas à pas ;
  - le readme interne du workflow (`workflow/info.plist`) est aligné pour indiquer qu’il faut choisir un raccourci après import.

## [1.2.1] - 2026-01-02

### Changed
- Documentation des clés API améliorée :
  - ajout des commandes `security find-generic-password` (sans afficher la valeur de la clé) et `security delete-generic-password` pour vérifier / supprimer une clé dans le Trousseau ;
  - section README enrichie pour expliquer comment gérer les clés DeepSeek / OpenAI / Anthropic dans le Keychain macOS.

## [1.2.0] - 2026-01-02

### Changed
- Amélioration des messages d’erreur lorsque la clé API est manquante :
  - le message indique explicitement le service Keychain concerné ;
  - des instructions claires expliquent comment ajouter la clé via `sp setup` dans Alfred ;
  - une commande `security add-generic-password` prête à adapter est fournie pour un ajout manuel en ligne de commande.

## [1.1.0] - 2026-01-01

### Changed
- Ajustements internes de préparation à la release 1.2.0 (aucun changement fonctionnel majeur documenté).

## [1.0.0] - 2025-12-31

### Added
- Architecture **multi‑providers** unifiée via `providers.get_provider` (DeepSeek / OpenAI / Anthropic).
- Providers **OpenAI** et **Anthropic** :
  - même prompt de correction que DeepSeek,
  - lecture des clés API depuis le Trousseau (`syntax-polish-openai`, `syntax-polish-anthropic`),
  - support complet de la variable `AI_PROVIDER` (`deepseek`, `openai`, `anthropic`).

### Changed
- Intégration Anthropic :
  - passage à l’API `v1/messages` avec format `content` correct et `max_tokens` explicite,
  - modèle configurable, par défaut `claude-opus-4-5-20251101` (ou autre modèle compatible).
- Ajout d’un **mode debug** commun (`DEBUG=1`) pour tous les providers :
  - logs `[DEBUG] ... raw response` en cas de succès,
  - logs `[DEBUG] ... HTTP <code> body` en cas d’erreur HTTP,
  - sans jamais exposer les clés API.
- Documentation mise à jour (`README.md`) :
  - description du support multi‑IA (DeepSeek, OpenAI, Anthropic),
  - explication détaillée de `AI_PROVIDER` et du mode `DEBUG`.

## [0.15.0] - 2025-12-27

### Added
- Infrastructure de tests unitaires automatisés :
  - ajout de `pytest` dans `requirements-dev.txt`,
  - dossier `tests/` avec des tests pour `main.py`, `providers/deepseek.py` et `utils/keychain.py`,
  - script `scripts/test.sh` pour lancer facilement la suite de tests.

## [0.14.0] - 2025-12-27

### Changed
- DeepSeek :
  - Ajout / affinage d’un **prompt système** dédié à la correction de texte (conservation du sens et du ton, détection automatique de la langue, réponse sans explications).
- Documentation :
  - Ajout d’une section **“Comment fonctionne la correction”** dans le `README` (prompt DeepSeek, détection de langue, sortie sans explications).
  - Explication détaillée de la variable Alfred **`AI_PROVIDER`** (création, valeurs possibles, provider par défaut).
  - Précision sur le comportement lorsque plusieurs clés API sont enregistrées dans le Trousseau (sélection via `AI_PROVIDER`, `deepseek` par défaut).
  - Enrichissement de `docs/privacy.md` (données traitées, non‑stockage local, rôle du Keychain et des providers tiers).

## [0.11.0] - 2025-12-27

### Changed
- Amélioration de l’expérience d’installation Alfred :
  - panneau d’import enrichi (readme, description, instructions claires),
  - mot-clé `sp setup` sans argument (un simple `Entrée` lance l’assistant Keychain).
- Ajout d’un prompt de correction explicite pour DeepSeek :
  - message système spécialisé “correction / amélioration de texte”,
  - détection automatique de la langue et réponse dans la même langue,
  - sortie limitée au texte corrigé, sans explications.
- Mise à jour de la documentation (`README.md`) pour détailler la configuration `sp setup`,
  la sécurité des clés (Keychain macOS) et le comportement de correction.

## [0.1.0] - 2025-12-27

### Added
- Base du workflow Alfred (hotkey + clipboard).
- Support DeepSeek (Keychain macOS).
- Commande `sp setup` pour configurer les clés dans le Keychain via UI macOS.



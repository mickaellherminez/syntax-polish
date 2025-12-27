# Changelog

Le projet suit **SemVer** : `MAJOR.MINOR.PATCH`.

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



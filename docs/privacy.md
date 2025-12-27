# Confidentialité (Privacy)

Cette section décrit comment **Syntax Polish** traite vos données lorsque vous utilisez le workflow.

## 1. Données traitées

- Le texte que vous sélectionnez ou saisissez manuellement dans Alfred.
- Aucune autre donnée personnelle n’est collectée par le workflow lui‑même.

## 2. Ce que fait le workflow avec votre texte

- Le texte est :
  - lu localement par le script Python,
  - envoyé **uniquement** au fournisseur d’IA configuré (par défaut DeepSeek),
  - remplacé par la version corrigée dans le presse‑papiers.
- Le workflow **ne stocke pas** votre texte sur disque.
- Il n’y a **aucun tracking**, aucune télémétrie ni analytics.

## 3. Clés API & sécurité

- Les clés API sont **enregistrées exclusivement dans le Trousseau macOS (Keychain)**.
- Aucune clé n’est stockée dans :
  - le code source,
  - le fichier `.alfredworkflow`,
  - les préférences Alfred.
- Les requêtes vers l’API passent par **HTTPS** avec vérification TLS standard du système.

## 4. Journaux et erreurs

- En mode normal :
  - seuls des messages d’erreur génériques sont renvoyés à Alfred (ex. “Erreur : clé API manquante”),
  - aucune partie de votre texte ni de votre clé API n’est affichée.
- Un mode debug optionnel peut être ajouté à terme, mais il devra **ne jamais journaliser de contenu sensible**.

## 5. Fournisseurs d’IA tiers

- Quand vous utilisez Syntax Polish, le texte est transmis au fournisseur d’IA sélectionné
  (par exemple : DeepSeek, et plus tard éventuellement OpenAI / Anthropic).
- Ces fournisseurs appliquent leurs **propres politiques de confidentialité** et conditions d’utilisation.
- Il est de votre responsabilité de vérifier que ces politiques vous conviennent,
  en particulier si vous traitez des données sensibles ou soumises à une contrainte réglementaire.

---

En résumé :  
**Syntax Polish ne stocke pas vos textes, ne trace pas votre activité et ne conserve jamais vos clés API en clair.**  
Les seules données envoyées à un tiers sont celles nécessaires au fonctionnement de l’IA que vous avez choisie.

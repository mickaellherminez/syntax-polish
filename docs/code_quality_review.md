# Code Quality Review

## Vue d'ensemble
Le workflow Python est concis et facile à suivre, mais l'implémentation actuelle reste très minimale (un seul provider) et manque de garde-fous autour des appels réseau, de la sélection de fournisseur et du reporting d'erreurs. Les points suivants priorisent les risques pour la stabilité, la sécurité et la maintenabilité.

## Points positifs
- Lecture d'entrée flexible via arguments ou stdin, utile pour Alfred selon la configuration du Script Action. 【F:src/python/main.py†L5-L24】
- Utilisation du trousseau macOS pour récupérer la clé API DeepSeek, conforme aux consignes de sécurité. 【F:src/python/providers/deepseek.py†L7-L27】【F:src/python/utils/keychain.py†L5-L28】

## Points à améliorer (priorisés)
1. **Surface provider limitée et structure rigide** : seul DeepSeek est supporté et la sélection se fait via un `if` unique. L'ajout d'un provider impose de modifier `main.py` plutôt que d'utiliser un registre extensible. 【F:src/python/main.py†L27-L38】
2. **Gestion des erreurs réseau insuffisante** : l'appel HTTP DeepSeek ne gère pas les codes d'erreur, les timeouts de connexion/lecture distincts, ni les exceptions `URLError`/`HTTPError`; une réponse inattendue provoque un crash générique capté en haut de pile. 【F:src/python/providers/deepseek.py†L15-L27】【F:src/python/main.py†L29-L44】
3. **Validation de réponse absente** : le code suppose `choices[0].message.content` toujours présent; un body partiel renverra une `KeyError` peu explicite. 【F:src/python/providers/deepseek.py†L25-L27】
4. **Manque d'observabilité contrôlée** : aucun mode debug ou log structuré n'est disponible; en cas de défaut, seuls des messages génériques sont imprimés, compliquant le diagnostic côté utilisateur. 【F:src/python/main.py†L29-L44】
5. **Robustesse Keychain perfectible** : une absence de binaire `security` ou un code de retour non géré produit une `RuntimeError` générique; aucun hint de résolution n'est donné (ex. nom de service attendu). 【F:src/python/utils/keychain.py†L9-L28】
6. **Absence de tests automatisés** : aucun test unitaire ou d'intégration pour le parsing d'entrée, la sélection de provider ou le formatage de requête, ce qui fragilise l'évolution multi-IA.

## Recommandations
- Introduire une interface de provider (ex. protocole ou ABC) et un registre déclaratif pour ajouter/sélectionner des fournisseurs sans modifier `main.py`.
- Durcir `send_request` : gestion explicite de `HTTPError`/`URLError`, timeouts différenciés connexion/lecture, et messages d'erreur contextualisés pour Alfred.
- Valider la réponse DeepSeek avant d'accéder aux champs (`choices`, `message`, `content`) et renvoyer une erreur utilisateur claire en cas de format inattendu.
- Ajouter un mode `DEBUG` activable par variable d'environnement pour logguer les étapes clés (provider choisi, appel lancé, statut HTTP), en veillant à ne jamais exposer de secrets ou de texte sensible.
- Améliorer `get_api_key` avec des messages de dépannage (service manquant, Keychain inaccessible) et éventuellement un wrapper d'erreur dédié.
- Couvrir `_get_input_text`, la sélection de provider, et la sérialisation DeepSeek avec des tests unitaires pour sécuriser les évolutions futures.

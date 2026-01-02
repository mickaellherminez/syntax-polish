# Sécurité – état actuel

## Points positifs
- **Absence de secrets en clair** : les clés API sont lues depuis le Trousseau macOS via `security find-generic-password` et ne sont jamais stockées dans le dépôt.
- **TLS systématique** : toutes les requêtes passent par HTTPS sans désactivation de la validation TLS.
- **Mode debug limité** : les journaux se limitent désormais à des métadonnées (taille, clés principales) et n’incluent pas le contenu utilisateur.

## Renforcements ajoutés
- **Validation stricte des réponses** : chaque provider vérifie la présence des champs attendus et retourne des erreurs explicites en cas de format inattendu.
- **Gestion d’erreurs réseau** : les erreurs HTTP, réseau et de décodage JSON sont capturées avec des messages clairs, évitant des traces brutes dans Alfred.

## Risques / améliorations restantes
- **Modèles codés en dur** : les identifiants de modèles restent statiques dans les providers ; un paramétrage via variables d’environnement ou fichier de config faciliterait les mises à jour de sécurité/compliance.
- **Portabilité limitée** : le workflow dépend du Trousseau macOS ; prévoir un mécanisme explicite pour les environnements non macOS (message dédié ou variable de contournement sécurisée) faciliterait les tests et la CI.
- **Résilience réseau** : aucun retry/backoff n’est implémenté ; un mécanisme de retry limité avec jitter réduirait les échecs transitoires sans exposer davantage de données.

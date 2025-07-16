# 📖 dkprun — Mode d’emploi

`dkprun` est un utilitaire universel pour exécuter, tester, vérifier, transférer et préparer des scripts et projets multi-langages, avec détection automatique de l’OS et gestion intelligente des dépendances et fichiers !

---

## 🚀 Usage rapide

```bash
dkprun [OPTIONS] <extension> <fichier>
```
ou pour certaines commandes :
```bash
dkprun [OPTIONS] <commande> [arguments...]
```

---

## 🛠️ Extensions supportées

| Extension | Langage / Outil       | Commande utilisée         |
|-----------|----------------------|--------------------------|
| -py       | Python               | python                   |
| -js       | JavaScript (Node.js) | node                     |
| -sh       | Bash                 | bash                     |
| -rb       | Ruby                 | ruby                     |
| -php      | PHP                  | php                      |
| -c        | C                    | gcc                      |
| -cpp      | C++                  | g++                      |
| -bat      | Batch (Windows)      | cmd                      |
| -ps1      | PowerShell (Win)     | powershell               |
| -c#       | C# (.NET)            | dotnet/csc               |
| -html     | HTML                 | xdg-open/browser         |
| -java     | Java                 | javac/java               |
| -go       | Go                   | go                       |
| -rs       | Rust                 | rustc                    |
| -swift    | Swift                | swift                    |
| -kt       | Kotlin               | kotlinc                  |

---

## ⚡ Commandes & options principales

- `-r`  
  **Exécuter** le fichier selon l’extension spécifiée (ex : compilation + exécution pour C/C++/Java).
- `-noerror`  
  Ignore les erreurs d’exécution (continue même si une étape échoue).
- `-anasyntax <ext> <fichier>`  
  Analyse la **syntaxe** du fichier donné, selon l’extension (Python, JS, Bash, C, etc).
- `-checkinterpreters`  
  Vérifie la présence des interpréteurs principaux (node, npm, php, gcc, etc) et suggère leur installation.
- `-installdependencies <fichier>`  
  Installe les dépendances du projet en détectant le gestionnaire adapté (requirements.txt, package.json, etc).
- `-autoinstalldependencies <ext> <fichier>`  
  Analyse le code source pour détecter et installer automatiquement les modules externes (pip/npm).
- `-automakelib <ext> <fichier>`  
  Crée automatiquement un squelette de package (actuellement supporté pour Python uniquement).
- `-install <paquet>`  
  Installe un paquet système (via apt, yum, dnf, brew, choco… selon l’OS).
- `-install -preconfigure <repo>`  
  Clone et configure un dépôt GitHub Python préconfiguré dans un environnement virtuel.
- `-log <fichier>`  
  Active le logging dans un fichier.
- `-verbose`  
  Mode verbeux (logging DEBUG).
- `-color`  
  Colorisation des sorties console.
- `-clean`  
  Nettoie les fichiers temporaires/build.
- `-docker <fichier|dossier>`  
  Exécute dans un conteneur Docker adapté.
- `-test`  
  Lance les tests du projet (pytest, npm test, etc).
- `-gitstatus`  
  Affiche le statut git du projet.
- `-gitcommit <message>`  
  Fait un commit rapide.
- `-listdependencies <fichier>`  
  Liste les dépendances détectées.
- `-gendoc`  
  Génère la documentation du projet.
- `-updatedependencies`  
  Met à jour toutes les dépendances.
- `-runurl <url_script>`  
  Télécharge et exécute un script distant.
- `-interactive`  
  Mode interactif CLI.
- `-profile`  
  Affiche le temps et mémoire d’exécution.
- `-zip <fichier|répertoire>`  
  Zippe le projet/répertoire.
- `-unzip <fichier.zip> [dossier]`  
  Dézippe une archive dans le dossier courant ou un dossier spécifié.
- `-startserver [-port <n>] [-psswd <motdepasse>]`  
  Démarre un serveur de transfert de fichiers (optionnel : port, mot de passe).
- `-sendserver <fichier> -ip <adresse_ip> [-port <n>] [-psswd <motdepasse>]`  
  Envoie un fichier à un serveur dkprun.
- `-takeserver <fichier> -ip <adresse_ip> [-port <n>] [-saveas <nom>] [-psswd <motdepasse>]`  
  Récupère un fichier depuis un serveur dkprun.
- `-closeall <dossier>`  
  Termine les processus utilisant un dossier (pour forcer la suppression).
- `-help`  
  Affiche cette aide.

---

## 🎓 Exemples d’utilisation

- Exécuter un script Python :  
  `dkprun -r -py mon_script.py`

- Compiler et exécuter un programme C++ :  
  `dkprun -r -cpp main.cpp`

- Vérifier la syntaxe d’un script Bash :  
  `dkprun -anasyntax -sh script.sh`

- Installer les dépendances Node.js :  
  `dkprun -installdependencies app.js`

- Installer automatiquement les modules Python importés :  
  `dkprun -autoinstalldependencies -py script.py`

- Vérifier les interpréteurs présents :  
  `dkprun -checkinterpreters`

- Installer wget (Linux/Mac/Windows) :  
  `dkprun -install wget`

- Préconfigurer un dépôt Python Discord :  
  `dkprun -install -preconfigure discord_v2`

- **Transfert de fichiers sécurisé** (avec mot de passe) :  
  - Côté serveur :  
    `dkprun -startserver -psswd azerty`
  - Côté client (envoi) :  
    `dkprun -sendserver secret.txt -ip 192.168.1.42 -psswd azerty`
  - Côté client (récupérer un fichier) :  
    `dkprun -takeserver secret.txt -ip 192.168.1.42 -psswd azerty`

- Dézipper une archive :
  `dkprun -unzip monarchive.zip`

- Fermer les processus bloquant un dossier :
  `dkprun -closeall ./mon_projet`

---

## ℹ️ Remarques

- L’option `-r` est requise pour toute exécution de fichier.
- Certaines commandes nécessitent les droits administrateur (sudo/choco/brew…).
- L’installation automatique des dépendances est supportée pour Python et JavaScript.
- Pour ouvrir un fichier HTML, le navigateur par défaut sera utilisé.
- Les commandes de transfert de fichier (serveur/client) peuvent utiliser le paramètre `-psswd` pour plus de sécurité (mot de passe transmis en clair, usage LAN recommandé).

---

## 🧑‍💻 Astuce

Tape simplement `dkprun` sans arguments pour afficher l’aide à jour !

---

**Auteur : AutoDKP / MJVhack**

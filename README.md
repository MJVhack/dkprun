# 📖 dkprun — Mode d’emploi

`dkprun` est un utilitaire universel pour exécuter, tester, vérifier et préparer des scripts et projets multi-langages, avec détection automatique de l’OS et gestion intelligente des dépendances !

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

---

## 🎓 Exemples d’utilisation

- Exécuter un script Python :  
  `dkprun -r -py mon_script.py`

- Compiler et exécuter un programme C++ :  
  `dkprun -r -cpp main.cpp`

- Vérifier la syntaxe d’un script Bash :  
  `dkprun -sh -anasyntax script.sh`

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

---

## ℹ️ Remarques

- L’option `-r` est requise pour toute exécution de fichier.
- Certaines commandes nécessitent les droits administrateur (sudo/choco/brew…).
- Pour l’installation automatique des dépendances, seuls Python et JavaScript sont supportés.
- Pour ouvrir un fichier HTML, le navigateur par défaut sera utilisé.

---

## 🧑‍💻 Astuce

Tape simplement `dkprun` sans arguments pour afficher l’aide à jour !

---

**Auteur : AutoDKP / MJVhack**

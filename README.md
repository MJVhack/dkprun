📖 **dkprun — Mode d’emploi modernisé**

`dkprun` est un outil universel pour exécuter, analyser, tester, préparer et transférer des projets multi-langages (Python, Node.js, Java, Bash, etc.). Il détecte automatiquement le système d'exploitation et gère intelligemment les dépendances et fichiers.

---

## 🚀 Usage rapide

```
dkprun [OPTIONS] -<extension> <fichier>
dkprun [OPTIONS] <commande> [arguments...]
```

---

## 🛠️ Extensions supportées

| Extension | Langage / Outil   | Commande utilisée     |
| --------- | ----------------- | --------------------- |
| `-py`     | Python            | `python`              |
| `-js`     | JavaScript (Node) | `node`                |
| `-sh`     | Bash              | `bash`                |
| `-rb`     | Ruby              | `ruby`                |
| `-php`    | PHP               | `php`                 |
| `-c`      | C                 | `gcc`                 |
| `-cpp`    | C++               | `g++`                 |
| `-bat`    | Batch (Windows)   | `cmd`                 |
| `-ps1`    | PowerShell        | `powershell`          |
| `-c#`     | C# (.NET)         | `dotnet` ou `csc`     |
| `-html`   | HTML              | navigateur par défaut |
| `-java`   | Java              | `javac` puis `java`   |
| `-go`     | Go                | `go run`              |
| `-rs`     | Rust              | `rustc`               |
| `-swift`  | Swift             | `swift`               |
| `-kt`     | Kotlin            | `kotlinc`             |

---

## ⚡ Commandes principales

* `-r` : Exécute le fichier selon l’extension (compilation si nécessaire)
* `-noerror` : Ignore les erreurs d’exécution
* `-anasyntax <ext> <fichier>` : Analyse la syntaxe du fichier
* `-checkinterpreters` : Vérifie les interpréteurs/installations disponibles
* `-installdependencies <fichier>` : Installe les dépendances du projet
* `-autoinstalldependencies <ext> <fichier>` : Installe auto. les modules externes (Python/Node)
* `-automakelib <ext> <fichier>` : Génère un squelette de package (ex: Python)
* `-install <paquet>` : Installe un paquet système via `apt`, `brew`, `choco`, etc.
* `-install -preconfigure <repo>` : Clone un repo GitHub et configure l’env. virtuel
* `-log <fichier>` : Active le logging dans un fichier
* `-verbose` : Affiche les logs détaillés (DEBUG)
* `-color` : Active la colorisation console
* `-clean` : Supprime les fichiers temporaires ou de build
* `-docker <cible>` : Exécute le script/dossier dans un conteneur Docker
* `-test` : Lance les tests du projet (pytest, npm test...)
* `-gitstatus` / `-gitcommit <msg>` : Outils Git rapides
* `-listdependencies <fichier>` : Liste les dépendances détectées
* `-gendoc` : Génère la documentation du projet
* `-updatedependencies` : Met à jour les dépendances automatiquement
* `-runurl <url>` : Télécharge et exécute un script distant
* `-interactive` : Mode terminal interactif
* `-profile` : Affiche le temps et la mémoire d’exécution
* `-zip <fichier|répertoire>` : Crée une archive ZIP
* `-unzip <fichier.zip> [dossier]` : Extrait une archive ZIP
* `-startserver [-port] [-psswd]` : Lance un serveur de transfert
* `-sendserver <f> -ip <ip> [...]` : Envoie un fichier
* `-takeserver <f> -ip <ip> [...]` : Reçoit un fichier
* `-closeall <dossier>` : Termine les processus bloquant un dossier
* `-help` : Affiche l’aide

---

## 🎓 Exemples d’utilisation

```bash
# Exécuter un script Python
$ dkprun -r -py mon_script.py

# Compiler et lancer du C++
$ dkprun -r -cpp main.cpp

# Vérifier la syntaxe d'un script Bash
$ dkprun -anasyntax -sh script.sh

# Installer les dépendances Node
$ dkprun -installdependencies app.js

# Auto-installer les modules Python importés
$ dkprun -autoinstalldependencies -py script.py

# Vérifier les interpréteurs installés
$ dkprun -checkinterpreters

# Installer wget
$ dkprun -install wget

# Préconfigurer un repo Discord
$ dkprun -install -preconfigure discord_v2

# Transfert sécurisé LAN
$ dkprun -startserver -psswd azerty
$ dkprun -sendserver secret.txt -ip 192.168.1.42 -psswd azerty
$ dkprun -takeserver secret.txt -ip 192.168.1.42 -psswd azerty
```

---

## ℹ️ Remarques utiles

* L’option `-r` est **obligatoire** pour exécuter un script
* Certaines commandes peuvent exiger les droits administrateur (sudo/choco)
* L’installation automatique de modules est supportée pour Python/Node uniquement
* Les fichiers HTML s’ouvrent dans le navigateur
* Les commandes de transfert supportent `-psswd` pour la sécurité (transmis en clair en LAN)

---

## 🧑‍💻 Astuce :

Tape simplement `dkprun` sans arguments pour afficher l'aide interactive !

---

**Auteur :** AutoDKP / [@MJVhack](https://github.com/MJVhack)

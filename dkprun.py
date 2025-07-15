#!/usr/bin/env python3
import sys
import subprocess
import os
import ast
import shutil

EXT_TO_COMMAND = {
    "-py": "python",
    "-js": "node",
    "-sh": "bash",
    "-rb": "ruby",
    "-php": "php"
}

def print_help():
    print("📜 Utilisation : dkprun -r -<ext> fichier OU -traceia fichier.py [options]")
    print("Extensions supportées :")
    for ext in EXT_TO_COMMAND:
        print(f"  {ext.ljust(5)} → {EXT_TO_COMMAND[ext]}")
    print("\nOptions :")
    print("  -noerror     Ignore les erreurs d'exécution du script appelé")
    print("  -installdependencies <fichier> Installe les dépendances du projet selon l'extension")
    print("\nExemples :")
    print("  dkprun -r -py mon_script.py")
    print("  dkprun -r -py mon_script.py -noerror")
    print("  dkprun -traceia mon_script.py")
    print("  dkprun -installdependencies mon_script.py")

def check_and_install_interpreters():
    interpreters = {
        "node": "Node.js (node) : https://nodejs.org/",
        "npm": "NPM (npm) : inclus avec Node.js",
        "composer": "Composer (php) : https://getcomposer.org/",
        "php": "PHP (php) : https://www.php.net/",
        "ruby": "Ruby (ruby) : https://www.ruby-lang.org/fr/",
        "bundle": "Bundler (bundle) : gem install bundler",
        "bash": "Bash (bash) : généralement présent sur Linux/Mac"
    }
    missing = []
    for exe, help_txt in interpreters.items():
        if shutil.which(exe) is None:
            missing.append(help_txt)
    if missing:
        print("⚠️ Interpréteurs/managers manquants :")
        for m in missing:
            print(f"  ➤ {m}")
        print("\nInstalle-les manuellement avant de continuer.")
    else:
        print("✅ Tous les interpréteurs principaux sont installés.")

def install_all_dependencies():
    print("🔎 Vérification des interpréteurs...")
    check_and_install_interpreters()
    print("\n🔧 Installation automatique des dépendances des différents environnements...")
    # Python (ignore, comme demandé)
    # Node.js
    if os.path.exists("package.json"):
        print("→ Installation des dépendances Node.js (npm)...")
        subprocess.run(["npm", "install"])
    # PHP
    if os.path.exists("composer.json"):
        print("→ Installation des dépendances PHP (composer)...")
        subprocess.run(["composer", "install"])
    # Ruby
    if os.path.exists("Gemfile"):
        print("→ Installation des dépendances Ruby (bundle)...")
        subprocess.run(["bundle", "install"])
    print("✅ Installation automatique terminée.")

def analyse_python_code(file_path):
    # ... (inchangé)
    # 1. Vérification de syntaxe
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)
        print("✅ Syntaxe valide.")
    except SyntaxError as e:
        print("❌ Erreur de syntaxe détectée :")
        print(f"  ➤ Ligne {e.lineno} : {e.text.strip() if e.text else ''}")
        print(f"  ➤ {e.msg}")
        return
    # ... (reste inchangé)

def install_dependencies(filename):
    ext = None
    for k in EXT_TO_COMMAND:
        if filename.endswith(k.replace("-", ".")):
            ext = k
            break
    if ext == "-py":
        # Python : requirements.txt ou pip install -r
        req_file = "requirements.txt"
        if not os.path.exists(req_file):
            print("Aucun requirements.txt trouvé.")
        else:
            print(f"Installation des dépendances Python depuis {req_file}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file])
    elif ext == "-js":
        # Node : package.json
        if not os.path.exists("package.json"):
            print("Aucun package.json trouvé.")
        else:
            print("Installation des dépendances Node.js (npm)...")
            subprocess.run(["npm", "install"])
    elif ext == "-php":
        # PHP : composer.json
        if not os.path.exists("composer.json"):
            print("Aucun composer.json trouvé.")
        else:
            print("Installation des dépendances PHP (composer)...")
            subprocess.run(["composer", "install"])
    elif ext == "-rb":
        # Ruby : Gemfile
        if not os.path.exists("Gemfile"):
            print("Aucun Gemfile trouvé.")
        else:
            print("Installation des dépendances Ruby (bundle)...")
            subprocess.run(["bundle", "install"])
    elif ext == "-sh":
        print("Pas de gestion automatique des dépendances pour Bash.")
    else:
        print("Extension non reconnue ou pas de gestion des dépendances.")
    print("✅ Installation terminée.")

def main():
    args = sys.argv[1:]

    if not args:
        print_help()
        return

    # Détection de -noerror (et retrait de la liste)
    noerror = False
    if "-noerror" in args:
        noerror = True
        args.remove("-noerror")

    if args and args[0] == "-traceia":
        if len(args) < 2:
            print("❌ Fichier à analyser manquant.")
            return
        filename = args[1]
        if not os.path.exists(filename):
            print(f"❌ Fichier introuvable : {filename}")
            return
        analyse_python_code(filename)
        return
    
    if args and args[0] == "-checkinterpreters":
        check_and_install_interpreters()
        return

    # Ajout de la commande -installdependencies
    if args and args[0] == "-installdependencies":
        if len(args) < 2:
            print("❌ Fichier cible manquant pour -installdependencies.")
            return
        filename = args[1]
        if not os.path.exists(filename):
            print(f"❌ Fichier introuvable : {filename}")
            return
        install_dependencies(filename)
        return

    # Mode exécution standard
    if "-r" not in args:
        print("❌ Erreur : option -r requise pour exécuter")
        print_help()
        return

    ext_flag = next((arg for arg in args if arg in EXT_TO_COMMAND), None)
    if not ext_flag:
        print("❌ Erreur : aucune extension valide spécifiée.")
        print_help()
        return

    try:
        file_index = args.index(ext_flag) + 1
        filename = args[file_index]
    except IndexError:
        print(f"❌ Erreur : aucun fichier fourni après {ext_flag}")
        return

    if not os.path.exists(filename):
        print(f"❌ Fichier introuvable : {filename}")
        return

    command = EXT_TO_COMMAND[ext_flag]
    print(f"🚀 Exécution de : {command} {filename}\n")
    if noerror:
        try:
            result = subprocess.run([command, filename], stderr=subprocess.DEVNULL)
            sys.exit(0)
        except Exception:
            sys.exit(0)
    else:
        subprocess.run([command, filename])

if __name__ == "__main__":
    main()
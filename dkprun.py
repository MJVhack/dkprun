#!/usr/bin/env python3
import sys
import subprocess
import os 
import ast
import shutil
import platform 
import webbrowser

def detect_os():
    system = platform.system().lower()
    if system == "linux":
        distro = ""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.strip().split("=")[1].strip('"')
                        break
        except FileNotFoundError:
            distro = "linux"
        return f"linux-{distro}"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"
detected_os = detect_os()

print(f"🔍 Système détecté : {detected_os}")

EXT_TO_COMMAND = {
    "-py": "python",
    "-js": "node",
    "-sh": "bash",
    "-rb": "ruby",
    "-php": "php",
    "-c": "gcc",
    "-bat": "cmd",        
    "-ps1": "powershell",
    "-c#": "dotnet",
    "-html": "xdg-open", 
}

def print_help():
    print("📜 Utilisation : dkprun [options]")
    print("Extensions supportées :")
    for ext in EXT_TO_COMMAND:
        print(f"  {ext.ljust(7)} → {EXT_TO_COMMAND[ext]}")
    print("\nOptions :")
    print("  -noerror     Ignore les erreurs d'exécution du script appelé")
    print("  -installdependencies <fichier> Installe les dépendances du projet selon l'extension")
    print("  -install <cible> [-preconfigure <repo>] Installe un paquet ou configure un repo GitHub")
    print("  -traceia fichier.py Analyse la syntaxe Python")
    print("  -checkinterpreters Vérifie les interpréteurs")
    print("\nExemples :")
    print("  dkprun -r -py mon_script.py")
    print("  dkprun -install wget")
    print("  dkprun -install -preconfigure dkpshell")
    print("  dkprun -install python3 -preconfigure discord_v2")

def check_and_install_interpreters():
    interpreters = {
        "node": "Node.js (node) : https://nodejs.org/",
        "npm": "NPM (npm) : inclus avec Node.js",
        "composer": "Composer (php) : https://getcomposer.org/",
        "php": "PHP (php) : https://www.php.net/",
        "ruby": "Ruby (ruby) : https://www.ruby-lang.org/fr/",
        "bundle": "Bundler (bundle) : gem install bundler",
        "bash": "Bash (bash) : généralement présent sur Linux/Mac",
        "cmd": "Batch (cmd) : présent sur Windows",
        "powershell": "PowerShell : présent sur Windows",
        "gcc": "GCC (C) : https://gcc.gnu.org/ (MinGW-w64 sur Windows)"
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
    if os.path.exists("package.json"):
        print("→ Installation des dépendances Node.js (npm)...")
        subprocess.run(["npm", "install"])
    if os.path.exists("composer.json"):
        print("→ Installation des dépendances PHP (composer)...")
        subprocess.run(["composer", "install"])
    if os.path.exists("Gemfile"):
        print("→ Installation des dépendances Ruby (bundle)...")
        subprocess.run(["bundle", "install"])
    print("✅ Installation automatique terminée.")

def analyse_python_code(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        ast.parse(code)
        print("✅ Syntaxe valide.")
    except SyntaxError as e:
        print("❌ Erreur de syntaxe détectée :")
        print(f"  ➤ Ligne {e.lineno} : {e.text.strip() if e.text else ''}")
        print(f"  ➤ {e.msg}")
        return

def install_dependencies(filename):
    ext = None
    for k in EXT_TO_COMMAND:
        if filename.endswith(k.replace("-", ".")):
            ext = k
            break
    if ext == "-py":
        req_file = "requirements.txt"
        if not os.path.exists(req_file):
            print("Aucun requirements.txt trouvé.")
        else:
            print(f"Installation des dépendances Python depuis {req_file}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file])
    elif ext == "-js":
        if not os.path.exists("package.json"):
            print("Aucun package.json trouvé.")
        else:
            print("Installation des dépendances Node.js (npm)...")
            subprocess.run(["npm", "install"])
    elif ext == "-php":
        if not os.path.exists("composer.json"):
            print("Aucun composer.json trouvé.")
        else:
            print("Installation des dépendances PHP (composer)...")
            subprocess.run(["composer", "install"])
    elif ext == "-rb":
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

def install_python_repo(repo_name, git_url):
    print(f"→ Installation des dépendances de {repo_name}...")
    cwd = os.getcwd()
    os.makedirs(repo_name, exist_ok=True)
    os.chdir(repo_name)
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    venv_python = "venv\\Scripts\\python.exe" if os.name == "nt" else "venv/bin/python"
    print(f"→ Clonage du repo {repo_name} depuis {git_url}...")
    subprocess.run(["git", "clone", git_url])
    repo_dir = git_url.split('/')[-1]
    if repo_dir.endswith('.git'):
        repo_dir = repo_dir[:-4]
    os.chdir(repo_dir)
    if os.path.exists("requirements.txt"):
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("Aucun requirements.txt trouvé dans le repo.")
    if os.name == "nt":
        print("Pour activer le venv : venv\\Scripts\\activate")
    else:
        print("Pour activer le venv : source venv/bin/activate")
    os.chdir(cwd)

def install_package(target):
    print(f"🚀 Installation de : {target}")
    system = platform.system().lower()
    if system == "linux":
        if shutil.which("apt"):
            print("→ Installation via APT")
            subprocess.run(["sudo", "apt", "install", "-y", target])
        elif shutil.which("dnf"):
            print("→ Installation via DNF")
            subprocess.run(["sudo", "dnf", "install", "-y", target])
        elif shutil.which("yum"):
            print("→ Installation via YUM")
            subprocess.run(["sudo", "yum", "install", "-y", target])
        else:
            print("❌ Aucun gestionnaire de paquets Linux trouvé (apt, dnf, yum).")
    elif system == "darwin":
        if shutil.which("brew"):
            print("→ Installation via Homebrew")
            subprocess.run(["brew", "install", target])
        else:
            print("❌ Homebrew (brew) n'est pas installé sur ce Mac.")
    elif system == "windows":
        if shutil.which("choco"):
            print("→ Installation via Chocolatey")
            subprocess.run(["choco", "install", target, "-y"])
        else:
            print("❌ Chocolatey (choco) n'est pas installé sur ce Windows.")
    else:
        # fallback : téléchargement direct
        print("→ Téléchargement direct via wget/curl")
        url = f"https://example.com/{target}.sh"
        if shutil.which("wget"):
            subprocess.run(["wget", url])
        elif shutil.which("curl"):
            subprocess.run(["curl", "-O", url])
        else:
            print("❌ wget ou curl non trouvé.")
    print("✅ Installation terminée.")

def main():
    args = sys.argv[1:]

    if not args:
        print_help()
        return

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
    
    # Gestion robuste de la commande -install
    if args and args[0] == "-install":
        preconfigure = False
        repo_name = None
        target = None
        # analyse des args pour -install et -preconfigure
        for i, arg in enumerate(args[1:]):
            if arg == "-preconfigure":
                preconfigure = True
                if i + 2 < len(args):
                    repo_name = args[i + 2]
            elif not arg.startswith("-"):
                target = arg
        if not preconfigure and target:
            install_package(target)
            return
        # Option -preconfigure spécifique au repo
        if preconfigure and repo_name:
            repo_map = {
                "dkpshell": ("dkpshell", "https://github.com/MJVhack/Dkpshell"),
                "discord_v2": ("discord.py_v2", "https://github.com/MJVhack/discord.py_v2"),
                "discord_modif_2": ("discord_modif_2", "https://github.com/MJVhack/discord_modif_2"),
            }
            key = repo_name.lower()
            if key in repo_map:
                install_python_repo(*repo_map[key])
            else:
                print(f"Aucune préconfiguration définie pour le repo {repo_name}")
            print("✅ Préconfiguration terminée.")
            return
        print("❌ Usage : dkprun -install <paquet> OU dkprun -install -preconfigure <repo>")
        return

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

    # Execution logic for each language

    if ext_flag == "-html":
        print(f"🌐 Ouverture du fichier HTML dans le navigateur : {filename}")
        abs_path = os.path.abspath(filename)
        system = platform.system().lower()
        if system == "linux" and shutil.which("xdg-open"):
            subprocess.run(["xdg-open", abs_path])
        elif system == "windows":
            subprocess.run(["start", abs_path], shell=True)
        elif system == "darwin":
            subprocess.run(["open", abs_path])
        else:
            print("Aucune commande système trouvée, ouverture via webbrowser Python…")
            webbrowser.open(f'file://{abs_path}')
        return


    if ext_flag == "-c#":
        print(f"🚀 Compilation et exécution d'un script C# : {filename}")
        if shutil.which("csc"):
            exe_file = os.path.splitext(filename)[0] + ".exe"
            subprocess.run(["csc", filename])
            subprocess.run([exe_file])
        elif shutil.which("dotnet"):
            subprocess.run(["dotnet", "run", filename])
        else:
            print("❌ Aucun compilateur C# trouvé (csc ou dotnet). Installe .NET SDK.")
        return
    if ext_flag == "-c":
        print(f"🚀 Compilation et exécution d'un script C : {filename}")
        if shutil.which("gcc") is None:
            print("❌ gcc n'est pas installé ou pas dans le PATH. Installe MinGW-w64 sur Windows.")
            return
        exe_file = os.path.splitext(filename)[0] + ".exe" if os.name == "nt" else os.path.splitext(filename)[0]
        subprocess.run(["gcc", filename, "-o", exe_file])
        subprocess.run([exe_file])
    elif ext_flag == "-bat":
        print(f"🚀 Exécution d'un script Batch (cmd) : {filename}")
        if shutil.which("cmd") is None:
            print("❌ cmd n'est pas disponible sur ce système.")
            return
        subprocess.run(["cmd", "/c", filename])
    elif ext_flag == "-ps1":
        print(f"🚀 Exécution d'un script PowerShell : {filename}")
        if shutil.which("powershell") is None:
            print("❌ powershell n'est pas disponible sur ce système.")
            return
        subprocess.run(["powershell", "-File", filename])
    else:
        command = EXT_TO_COMMAND[ext_flag]
        print(f"🚀 Exécution de : {command} {filename}\n")
        if noerror:
            try:
                subprocess.run([command, filename], stderr=subprocess.DEVNULL)
                sys.exit(0)
            except Exception:
                sys.exit(0)
        else:
            subprocess.run([command, filename])

if __name__ == "__main__":
    main()
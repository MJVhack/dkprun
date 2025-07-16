#!/usr/bin/env python3
import sys
import subprocess
import os
import ast
import shutil
import platform
import webbrowser
import re
import time
import zipfile
import logging
from datetime import datetime
import psutil
import socket
import urllib.request



try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False

EXT_TO_COMMAND = {
    "-py": "python",
    "-js": "node",
    "-sh": "bash",
    "-rb": "ruby",
    "-php": "php",
    "-c": "gcc",
    "-cpp": "g++",
    "-bat": "cmd",
    "-ps1": "powershell",
    "-c#": "dotnet",
    "-html": "xdg-open",
    "-java": "java",
    "-go": "go",
    "-rs": "rustc",
    "-swift": "swift",
    "-kt": "kotlinc",
}

REPO_PRESETS = {
    "dkpshell": ("dkpshell", "https://github.com/MJVhack/Dkpshell"),
    "discord_v2": ("discord.py_v2", "https://github.com/MJVhack/discord.py_v2"),
    "discord_modif_2": ("discord_modif_2", "https://github.com/MJVhack/discord_modif_2"),
}

def setup_logging(logfile=None, verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(levelname)s: %(message)s'
    if logfile:
        logging.basicConfig(filename=logfile, level=log_level, filemode='w', format=log_format)
    else:
        logging.basicConfig(stream=sys.stdout, level=log_level, format=log_format)

def log(msg, level='info', color=None):
    if COLOR_SUPPORT and color:
        print(color + msg + Style.RESET_ALL)
    else:
        print(msg)
    if hasattr(logging, level):
        getattr(logging, level)(msg)
    else:
        logging.info(msg)

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
        except Exception:
            distro = "linux"
        return f"linux-{distro}"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def get_desktop():
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        b = os.path.join(os.path.expanduser("~"), "Bureau")
        return b if os.path.exists(b) else os.path.join(os.path.expanduser("~"), "Desktop")

def print_help():
    help_txt = f"""
📘 dkprun - Utilitaire universel multi-langages

Exécute, teste, analyse et prépare tes projets en Python, JavaScript, Java, C, Bash, Ruby, etc. avec détection automatique de l’OS, gestion des dépendances, packaging, Docker et bien plus.

────────────────────────────────────────────

🔧 Syntaxe de base :
  dkprun -r -<ext> <fichier>                 Exécute un fichier selon son extension
  dkprun -<commande> [options]               Lance une commande utilitaire

────────────────────────────────────────────

🧠 Extensions supportées :
  -py     → Python            | python
  -js     → JavaScript (Node) | node
  -sh     → Bash              | bash
  -rb     → Ruby              | ruby
  -php    → PHP               | php
  -c      → C                 | gcc
  -cpp    → C++               | g++
  -java   → Java              | javac + java
  -c#     → C# (.NET)         | dotnet / csc
  -ps1    → PowerShell        | powershell
  -bat    → Batch (cmd)       | cmd
  -go     → Go                | go
  -rs     → Rust              | rustc
  -kt     → Kotlin            | kotlinc
  -swift  → Swift             | swift
  -html   → HTML              | navigateur

────────────────────────────────────────────

⚙️ Commandes principales :

  -r                          → Exécuter le fichier
  -noerror                    → Ignore les erreurs d’exécution
  -checkinterpreters          → Vérifie les outils nécessaires
  -installdependencies <f>    → Installe les dépendances du fichier
  -autoinstalldependencies    → Analyse et installe auto. (JS / Python)
  -automakelib <ext> <f>      → Génère un squelette de bibliothèque
  -install <pkg>              → Installe un paquet système
  -install -preconfigure <r>  → Clone & configure un repo Git
  -anasyntax <ext> <f>        → Analyse la syntaxe d’un script

────────────────────────────────────────────

🧰 Outils additionnels :

  -docker <fichier>           → Exécute dans un conteneur Docker
  -clean                      → Supprime les fichiers temporaires
  -zip <cible>                → Crée une archive zip du projet
  -unzip <fichier.zip> [dest] → Dézippe une archive
  -gitstatus / -gitcommit     → Git rapide
  -gendoc                     → Génère la documentation (Sphinx)
  -test                       → Lance les tests (pytest, npm test…)
  -updatedependencies         → Met à jour les dépendances
  -interactive                → Mode terminal interactif
  -profile                    → Affiche temps + RAM d’exécution
  -osinfo / -getip            → Infos système et IP
  -wifiips                    → IPs du réseau local
  -startserver                → Lance un serveur de transfert
  -sendserver <f> -ip <ip>    → Envoie un fichier
  -takeserver <f> -ip <ip>    → Récupère un fichier

────────────────────────────────────────────

🧪 Exemples :
  dkprun -r -py script.py
  dkprun -anasyntax -js app.js
  dkprun -install git
  dkprun -install -preconfigure dkpshell
  dkprun -interactive

────────────────────────────────────────────

Tape simplement `dkprun` ou `dkprun -help` pour réafficher ce guide.

"""
    print(help_txt)

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
        "gcc": "GCC (C) : https://gcc.gnu.org/",
        "g++": "G++ (C++) : https://gcc.gnu.org/",
        "go": "Go : https://golang.org/",
        "rustc": "Rust : https://www.rust-lang.org/",
        "swift": "Swift : https://swift.org/",
        "kotlinc": "Kotlin : https://kotl.in/"
    }
    missing = []
    for exe, help_txt in interpreters.items():
        if shutil.which(exe) is None:
            missing.append(help_txt)
    if missing:
        log("⚠️ Interpréteurs/managers manquants :", "warning", Fore.YELLOW)
        for m in missing:
            log(f"  ➤ {m}", "warning", Fore.YELLOW)
        print("\nInstalle-les manuellement avant de continuer.")
    else:
        log("✅ Tous les interpréteurs principaux sont installés.", "info", Fore.GREEN)

def clean_project():
    patterns = [
        "__pycache__", ".pytest_cache", ".mypy_cache",
        "*.class", "*.o", "*.exe", "*.out", "node_modules", "venv", ".env", ".DS_Store"
    ]
    nb_cleaned = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for d in dirs:
            if d in patterns or d.startswith("build"):
                try:
                    shutil.rmtree(os.path.join(root, d))
                    nb_cleaned += 1
                    log(f"🧹 Dossier supprimé: {os.path.join(root, d)}", "info", Fore.CYAN)
                except Exception:
                    pass
        for f in files:
            for pat in patterns:
                if re.fullmatch(pat.replace("*", ".*"), f):
                    try:
                        os.remove(os.path.join(root, f))
                        nb_cleaned += 1
                        log(f"🧹 Fichier supprimé: {os.path.join(root, f)}", "info", Fore.CYAN)
                    except Exception:
                        pass
    log(f"✅ Nettoyage terminé. Eléments nettoyés: {nb_cleaned}", "info", Fore.GREEN)

def os_info():
    import platform
    import socket
    import getpass

    log("🖥️ Informations sur le système :", "info", Fore.CYAN)
    try:
        print(f"Nom d'utilisateur : {getpass.getuser()}")
        print(f"Nom de la machine : {socket.gethostname()}")
        print(f"Adresse IP locale : {socket.gethostbyname(socket.gethostname())}")
        print(f"Système : {platform.system()}")
        print(f"Nom complet OS : {platform.platform()}")
        print(f"Version : {platform.version()}")
        print(f"Version détaillée : {platform.uname().version}")
        print(f"Architecture : {platform.machine()}")
        print(f"Processeur : {platform.processor()}")
        print(f"Python : {platform.python_version()} ({platform.python_implementation()})")
        print(f"Chemin Python : {platform.python_executable if hasattr(platform, 'python_executable') else sys.executable}")
        print(f"Répertoire courant : {os.getcwd()}")
        print(f"Dossier utilisateur : {os.path.expanduser('~')}")
        # RAM et CPU si psutil dispo
        try:
            import psutil
            print(f"RAM totale : {round(psutil.virtual_memory().total/(1024**3),2)} Go")
            print(f"RAM dispo : {round(psutil.virtual_memory().available/(1024**3),2)} Go")
            print(f"CPU logique : {psutil.cpu_count()}")
            print(f"CPU physique : {psutil.cpu_count(logical=False)}")
        except ImportError:
            print("(psutil non installé : infos RAM/CPU limitées)")
    except Exception as e:
        log(f"Erreur d'affichage des infos OS : {e}", "error", Fore.RED)

def start_file_server(port=5001, dest_dir=None):
    """
    Démarre un serveur TCP qui reçoit ou envoie un fichier selon la requête du client.
    """
    import socket
    import threading

    dest_dir = dest_dir or os.getcwd()
    print(f"📦 [Serveur] Prêt sur le port {port}... (Ctrl+C pour arrêter)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        while True:
            try:
                conn, addr = s.accept()
            except KeyboardInterrupt:
                print("\nArrêt du serveur.")
                break
            print(f"🔔 Connexion de {addr}")
            t = threading.Thread(target=handle_file_server_request, args=(conn, dest_dir))
            t.daemon = True
            t.start()

def get_wifi_ips():
    """
    Affiche toutes les IPs de machines connectées au même réseau local (table ARP).
    Fonctionne sur Windows, Linux, Mac.
    """

    log("🔎 IPs détectées sur le réseau local :", "info", Fore.CYAN)
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("arp -a", shell=True, encoding="utf-8")
            # Les lignes contenant une IP (xxx.xxx.xxx.xxx)
            pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
            ips = set()
            for line in output.splitlines():
                match = pattern.search(line)
                if match:
                    ips.add(match.group(1))
        else:
            output = subprocess.check_output(["arp", "-a"], encoding="utf-8")
            pattern = re.compile(r"\((\d+\.\d+\.\d+\.\d+)\)")
            ips = set(pattern.findall(output))
        # Affichage
        for ip in sorted(ips):
            print(f" - {ip}")
    except Exception as e:
        log(f"❌ Impossible de récupérer la liste des IPs : {e}", "error", Fore.RED)

def handle_file_server_request(conn, dest_dir):
    with conn:
        try:
            # Reçoit la commande (première ligne)
            command_line = b""
            while not command_line.endswith(b"\n"):
                byte = conn.recv(1)
                if not byte:
                    return
                command_line += byte
            command = command_line.strip().decode(errors='replace')
            if command.startswith("SEND:"):
                # Reception d'un fichier
                filename = command[5:]
                dest_path = os.path.join(dest_dir, os.path.basename(filename))
                with open(dest_path, "wb") as f:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        f.write(data)
                print(f"✅ Fichier reçu : {dest_path}")
            elif command.startswith("TAKE:"):
                # Envoi d'un fichier
                filename = command[5:]
                file_path = os.path.join(dest_dir, os.path.basename(filename))
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        while True:
                            data = f.read(4096)
                            if not data:
                                break
                            conn.sendall(data)
                    print(f"✅ Fichier envoyé : {file_path}")
                else:
                    conn.sendall(b"")
                    print(f"❌ Fichier demandé non trouvé : {file_path}")
        except Exception as e:
            print(f"❌ Erreur serveur : {e}")

def take_file_from_server(file_name, ip, port=5001, save_as=None):
    """
    Demande à un serveur dkprun le fichier `file_name` et le récupère.

    Args:
        file_name (str): Nom du fichier à demander.
        ip (str): Adresse IP du serveur.
        port (int): Port du serveur.
        save_as (str): Chemin local de sauvegarde (défaut: même nom).
    """
    import socket

    save_as = save_as or os.path.basename(file_name)
    try:
        with socket.socket() as s:
            s.connect((ip, port))
            s.sendall(f"TAKE:{file_name}\n".encode())
            with open(save_as, 'wb') as f:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    f.write(data)
        log(f"✅ Fichier '{file_name}' récupéré depuis {ip}:{port} vers '{save_as}'", "info", Fore.GREEN)
    except Exception as e:
        log(f"❌ Erreur lors de la récupération du fichier : {e}", "error", Fore.RED)

def send_file_to_server(file_path, ip, port=5001):
    """
    Envoie un fichier à un serveur dkprun (startserver) sur l'IP et port donnés.

    Args:
        file_path (str): Chemin du fichier à envoyer.
        ip (str): Adresse IP du serveur.
        port (int): Port du serveur (défaut 5001).
    """
    import socket

    if not os.path.exists(file_path):
        log(f"❌ Fichier à envoyer introuvable : {file_path}", "error", Fore.RED)
        return
    try:
        with socket.socket() as s:
            s.connect((ip, port))
            # Envoie de la commande et du nom du fichier
            s.sendall(f"SEND:{os.path.basename(file_path)}\n".encode())
            # Puis envoie du contenu
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    s.sendall(data)
        log(f"✅ Fichier '{file_path}' envoyé à {ip}:{port}", "info", Fore.GREEN)
    except Exception as e:
        log(f"❌ Erreur lors de l'envoi du fichier : {e}", "error", Fore.RED)

def run_in_docker(target):
    """
    Exécute un script ou projet dans un conteneur Docker adapté selon son extension.
    """
    import subprocess
    import os

    ext_map = {
        ".py": ("python:3.12", "python"),
        ".js": ("node:20", "node"),
        ".sh": ("ubuntu:latest", "bash"),
        ".rb": ("ruby:latest", "ruby"),
        ".php": ("php:latest", "php"),
        ".c": ("gcc:latest", "gcc"),
        ".cpp": ("gcc:latest", "g++"),
        ".java": ("openjdk:latest", "java"),
        ".go": ("golang:latest", "go run"),
        ".rs": ("rust:latest", "rustc"),
        # Ajoute d'autres extensions/images si besoin
    }

    ext = os.path.splitext(target)[1].lower()
    docker_image, docker_cmd = ext_map.get(ext, (None, None))
    if not docker_image:
        log(f"❌ Extension non supportée pour Docker: {ext}", "error", Fore.RED)
        return

    abs_target = os.path.abspath(target)
    workdir = os.path.dirname(abs_target)
    filename = os.path.basename(abs_target)

    log(f"🚢 Exécution dans {docker_image} : {docker_cmd} {filename}", "info", Fore.MAGENTA)

    # Construction de la commande Docker
    docker_args = [
        "docker", "run", "--rm",
        "-v", f"{workdir}:/app",
        "-w", "/app",
        docker_image
    ]
    if ext in [".c", ".cpp"]:
        # Compilation puis exécution
        exe = filename.rsplit('.', 1)[0]
        docker_args += [docker_cmd, filename, "-o", exe, "&&", f"./{exe}"]
    elif ext == ".java":
        classname = filename.rsplit('.', 1)[0]
        docker_args += ["bash", "-c", f"javac {filename} && java {classname}"]
    else:
        docker_args += [docker_cmd, filename]

    try:
        subprocess.run(docker_args)
    except Exception as e:
        log(f"❌ Erreur d'exécution Docker : {e}", "error", Fore.RED)


def get_wifi_ips():
    """
    Affiche toutes les IPs de machines connectées au même réseau local (table ARP).
    Fonctionne sur Windows, Linux, Mac.
    """
    import subprocess
    import platform
    import re

    log("🔎 IPs détectées sur le réseau local :", "info", Fore.CYAN)
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("arp -a", shell=True, encoding="latin1")
            # Les lignes contenant une IP (xxx.xxx.xxx.xxx)
            pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
            ips = set()
            for line in output.splitlines():
                match = pattern.search(line)
                if match:
                    ips.add(match.group(1))
        else:
            output = subprocess.check_output(["arp", "-a"], encoding="utf-8")
            pattern = re.compile(r"\((\d+\.\d+\.\d+\.\d+)\)")
            ips = set(pattern.findall(output))
        # Affichage
        for ip in sorted(ips):
            print(f" - {ip}")
    except Exception as e:
        log(f"❌ Impossible de récupérer la liste des IPs : {e}", "error", Fore.RED)

def unzip_project(zip_path, extract_to=None):
    """
    Décompresse un fichier zip dans le dossier courant ou un dossier donné.

    Args:
        zip_path (str): Chemin du fichier zip à décompresser.
        extract_to (str, optional): Dossier cible. Si None, extrait dans le dossier courant.
    """
    if not os.path.exists(zip_path):
        log(f"❌ Fichier zip introuvable : {zip_path}", "error", Fore.RED)
        return
    if extract_to is None:
        extract_to = os.getcwd()
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        log(f"✅ Fichier décompressé dans : {extract_to}", "info", Fore.GREEN)
    except Exception as e:
        log(f"❌ Erreur lors de la décompression : {e}", "error", Fore.RED)

def run_tests():
    if os.path.exists("pytest.ini") or any(f.endswith("_test.py") for f in os.listdir(".")):
        log("🧪 Lancement des tests pytest...", "info", Fore.MAGENTA)
        subprocess.run(["pytest"])
    elif os.path.exists("package.json"):
        log("🧪 Lancement des tests npm...", "info", Fore.MAGENTA)
        subprocess.run(["npm", "test"])
    elif os.path.exists("Gemfile"):
        log("🧪 Lancement des tests Ruby...", "info", Fore.MAGENTA)
        subprocess.run(["bundle", "exec", "rake", "test"])
    else:
        log("❌ Aucun système de test détecté.", "error", Fore.RED)

def git_status():
    if shutil.which("git") is None:
        log("❌ Git n'est pas installé.", "error", Fore.RED)
        return
    subprocess.run(["git", "status"])

def git_commit(msg):
    if shutil.which("git") is None:
        log("❌ Git n'est pas installé.", "error", Fore.RED)
        return
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", msg])
    log("✅ Git commit effectué.", "info", Fore.GREEN)

def list_dependencies(filename):
    ext_flag = None
    for k in EXT_TO_COMMAND:
        if filename.endswith(k.replace("-", ".")):
            ext_flag = k
            break
    deps = set()
    if ext_flag == "-py":
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        imports = set(re.findall(r'^\s*import (\w+)|^\s*from (\w+)', code, re.MULTILINE))
        for imp in imports:
            deps.update([x for x in imp if x])
    elif ext_flag == "-js":
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        imports = set(re.findall(r'require\([\'"]([\w\-]+)[\'"]\)|import .* from [\'"]([\w\-]+)[\'"]', code))
        for imp in imports:
            deps.update([x for x in imp if x])
    log(f"📦 Dépendances détectées : {', '.join(sorted(deps))}", "info", Fore.MAGENTA)

def closeall(target_path):
    target_path = os.path.abspath(target_path).lower()
    found = False
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'open_files', 'cwd']):
        try:
            is_relevant = False
            cwd = proc.info.get('cwd')
            if cwd and target_path in cwd.lower():
                is_relevant = True
            for f in proc.info.get('open_files') or []:
                if target_path in f.path.lower():
                    is_relevant = True
            if is_relevant:
                found = True
                print(f"{Fore.YELLOW}[CloseAll] Arrêt du processus {proc.info['name']} (PID {proc.info['pid']}){Fore.RESET}")
                proc.terminate()
        except Exception:
            pass
    if not found:
        print(f"{Fore.GREEN}[CloseAll] Aucun processus bloquant trouvé pour {target_path}{Fore.RESET}")

def gendoc():
    if os.path.exists("conf.py"):
        log("🔎 conf.py trouvé, génération de la doc avec Sphinx...", "info", Fore.CYAN)
        subprocess.run(["sphinx-build", ".", "_build"])
        log("✅ Documentation Sphinx générée dans ./_build", "info", Fore.GREEN)
    else:
        log("⌛ Aucun conf.py Sphinx trouvé dans ce dossier. Lancement 'sphinx-quickstart' pour initialiser la doc.", "info", Fore.CYAN)
        result = subprocess.run(["sphinx-quickstart"])
        if result.returncode == 0 and os.path.exists("conf.py"):
            subprocess.run(["sphinx-build", ".", "_build"])
            log("✅ Documentation Sphinx générée dans ./_build", "info", Fore.GREEN)
        else:
            log("❌ La génération de la doc a échoué ou a été annulée.", "error", Fore.RED)

def update_dependencies():
    if os.path.exists("requirements.txt"):
        log("⬆️ Mise à jour des paquets pip...", "info", Fore.CYAN)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])
    elif os.path.exists("package.json"):
        log("⬆️ Mise à jour des paquets npm...", "info", Fore.CYAN)
        subprocess.run(["npm", "update"])
    elif os.path.exists("composer.json"):
        log("⬆️ Mise à jour des paquets composer...", "info", Fore.CYAN)
        subprocess.run(["composer", "update"])
    else:
        log("❌ Aucun gestionnaire de dépendances détecté.", "error", Fore.RED)

def run_url(url):
    ext = os.path.splitext(url)[1]
    filename = f"temp_script{ext}"
    try:
        import requests
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)
        log(f"🌐 Script téléchargé depuis {url}", "info", Fore.CYAN)
        main(["-r", f"-{ext[1:]}", filename])
    except Exception as e:
        log(f"❌ Erreur téléchargement/exécution : {e}", "error", Fore.RED)
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def interactive_mode():
    log("Bienvenue en mode interactif ! (tape 'exit' pour quitter)", "info", Fore.CYAN)
    while True:
        try:
            cmd = input("> ")
            if cmd.strip().lower() == "exit":
                break
            main(cmd.strip().split())
        except KeyboardInterrupt:
            print()
            break

def profile_execution(cmd_fn, *args, **kwargs):
    import tracemalloc
    tracemalloc.start()
    start = time.time()
    result = cmd_fn(*args, **kwargs)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    log(f"⏱️ Temps d’exécution : {end - start:.3f}s | Mémoire max : {peak / 1024:.1f} Ko", "info", Fore.YELLOW)
    return result

def zip_project(target):
    zipname = f"{os.path.basename(target).rstrip(os.sep)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zf:
        if os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                for f in files:
                    zf.write(os.path.join(root, f))
        else:
            zf.write(target)
    log(f"✅ Projet zippé : {zipname}", "info", Fore.GREEN)

def automakelib_py(file_path):
    basename = os.path.splitext(os.path.basename(file_path))[0]
    desktop = get_desktop()
    package_dir = os.path.join(desktop, basename)
    log(f"🛠️ Création du package Python sur le Bureau : {package_dir}/", "info", Fore.CYAN)
    if os.path.exists(package_dir):
        log("⚠️ Le dossier existe déjà, suppression…", "warning", Fore.YELLOW)
        shutil.rmtree(package_dir)
    os.makedirs(os.path.join(package_dir, basename), exist_ok=True)
    shutil.copy(file_path, os.path.join(package_dir, basename, "__init__.py"))
    setup_py = f"""from setuptools import setup, find_packages
setup(
    name="{basename}",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="AutoDKP",
    description="Auto-generated lib from {file_path}"
)"""
    with open(os.path.join(package_dir, "setup.py"), "w", encoding="utf-8") as f:
        f.write(setup_py)
    log("✅ Squelette de package Python créé.", "info", Fore.GREEN)

def autoinstall_dependencies(filename, ext_flag):
    log(f"🔎 Analyse automatique des dépendances dans {filename} ({ext_flag})", "info", Fore.CYAN)
    if ext_flag == "-py":
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        imports = set(re.findall(r'^\s*import (\w+)|^\s*from (\w+)', code, re.MULTILINE))
        modules = set()
        for imp in imports:
            modules.update([x for x in imp if x])
        externals = []
        for mod in modules:
            try:
                __import__(mod)
            except ImportError:
                externals.append(mod)
        if externals:
            log(f"📦 Modules externes détectés : {', '.join(externals)}", "info", Fore.MAGENTA)
            log("→ Installation via pip…", "info", Fore.MAGENTA)
            for mod in externals:
                subprocess.run([sys.executable, "-m", "pip", "install", mod])
        else:
            log("✅ Aucun module externe à installer.", "info", Fore.GREEN)
        return
    elif ext_flag == "-js":
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        imports = set(re.findall(r'require\([\'"]([\w\-]+)[\'"]\)|import .* from [\'"]([\w\-]+)[\'"]', code))
        modules = set()
        for imp in imports:
            modules.update([x for x in imp if x])
        node_builtins = {"fs", "path", "http", "os", "crypto", "events", "stream", "util", "url", "child_process", "net", "zlib", "dns", "tls", "process"}
        externals = [mod for mod in modules if mod not in node_builtins]
        if externals:
            log(f"📦 Modules npm détectés : {', '.join(externals)}", "info", Fore.MAGENTA)
            log("→ Installation via npm…", "info", Fore.MAGENTA)
            for mod in externals:
                subprocess.run(["npm", "install", mod])
        else:
            log("✅ Aucun module npm externe à installer.", "info", Fore.GREEN)
        return
    else:
        log("❌ Installation automatique non supportée pour cette extension.", "error", Fore.RED)

def get_ip():
    log("🌐 Informations IP :", "info", Fore.CYAN)
    # IP locale
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"IP locale : {local_ip}")
    except Exception as e:
        print(f"IP locale : Erreur ({e})")
    # IP publique
    try:
        with urllib.request.urlopen('https://api.ipify.org') as response:
            public_ip = response.read().decode()
        print(f"IP publique : {public_ip}")
    except Exception as e:
        print(f"IP publique : Erreur ({e})")

def analyse_syntax(filename, ext_flag):
    if ext_flag == "-py":
        try:
            with open(filename, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            log("✅ Syntaxe Python OK", "info", Fore.GREEN)
        except Exception as e:
            log(f"❌ Erreur de syntaxe Python : {e}", "error", Fore.RED)
    elif ext_flag == "-js":
        result = subprocess.run(["node", "--check", filename])
        log("✅ Syntaxe JavaScript OK" if result.returncode == 0 else "❌ Erreur JS", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-sh":
        result = subprocess.run(["bash", "-n", filename])
        log("✅ Syntaxe Bash OK" if result.returncode == 0 else "❌ Erreur Bash", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-rb":
        result = subprocess.run(["ruby", "-c", filename])
        log("✅ Syntaxe Ruby OK" if result.returncode == 0 else "❌ Erreur Ruby", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-php":
        result = subprocess.run(["php", "-l", filename])
        log("✅ Syntaxe PHP OK" if result.returncode == 0 else "❌ Erreur PHP", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-java":
        result = subprocess.run(["javac", filename])
        log("✅ Syntaxe Java OK" if result.returncode == 0 else "❌ Erreur Java", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-c":
        result = subprocess.run(["gcc", "-fsyntax-only", filename])
        log("✅ Syntaxe C OK" if result.returncode == 0 else "❌ Erreur C", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    elif ext_flag == "-cpp":
        result = subprocess.run(["g++", "-fsyntax-only", filename])
        log("✅ Syntaxe C++ OK" if result.returncode == 0 else "❌ Erreur C++", "info" if result.returncode == 0 else "error", Fore.GREEN if result.returncode == 0 else Fore.RED)
    else:
        log("❌ Analyse syntaxique non supportée pour ce type de fichier.", "error", Fore.RED)

def install_dependencies(filename):
    ext = None
    for k in EXT_TO_COMMAND:
        if filename.endswith(k.replace("-", ".")):
            ext = k
            break
    if ext == "-py":
        req_file = "requirements.txt"
        if not os.path.exists(req_file):
            log("Aucun requirements.txt trouvé.", "warning", Fore.YELLOW)
        else:
            log(f"Installation des dépendances Python depuis {req_file}...", "info", Fore.CYAN)
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file])
    elif ext == "-js":
        if not os.path.exists("package.json"):
            log("Aucun package.json trouvé.", "warning", Fore.YELLOW)
        else:
            log("Installation des dépendances Node.js (npm)...", "info", Fore.CYAN)
            subprocess.run(["npm", "install"])
    elif ext == "-php":
        if not os.path.exists("composer.json"):
            log("Aucun composer.json trouvé.", "warning", Fore.YELLOW)
        else:
            log("Installation des dépendances PHP (composer)...", "info", Fore.CYAN)
            subprocess.run(["composer", "install"])
    elif ext == "-rb":
        if not os.path.exists("Gemfile"):
            log("Aucun Gemfile trouvé.", "warning", Fore.YELLOW)
        else:
            log("Installation des dépendances Ruby (bundle)...", "info", Fore.CYAN)
            subprocess.run(["bundle", "install"])
    elif ext == "-sh":
        log("Pas de gestion automatique des dépendances pour Bash.", "info", Fore.YELLOW)
    else:
        log("Extension non reconnue ou pas de gestion des dépendances.", "error", Fore.RED)
    log("✅ Installation terminée.", "info", Fore.GREEN)

def install_python_repo(repo_name, git_url):
    log(f"→ Installation des dépendances de {repo_name}...", "info", Fore.CYAN)
    cwd = os.getcwd()
    os.makedirs(repo_name, exist_ok=True)
    os.chdir(repo_name)
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    venv_dir = os.path.join(os.getcwd(), "venv")
    if os.name == "nt":
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")
    log(f"→ Clonage du repo {repo_name} depuis {git_url}...", "info", Fore.CYAN)
    subprocess.run(["git", "clone", git_url])
    repo_dir = git_url.split('/')[-1]
    if repo_dir.endswith('.git'):
        repo_dir = repo_dir[:-4]
    os.chdir(repo_dir)
    if not os.path.exists(venv_python):
        log(f"❌ Python venv introuvable à : {venv_python}", "error", Fore.RED)
        log("Vérifie que la création du venv a bien fonctionné.", "error", Fore.RED)
        os.chdir(cwd)
        return
    if os.path.exists("requirements.txt"):
        try:
            subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        except FileNotFoundError as e:
            log(f"❌ Erreur : Fichier ou exécutable introuvable.\n  ➤ {e}", "error", Fore.RED)
        except subprocess.CalledProcessError as e:
            log(f"❌ Erreur lors de l'installation des dépendances : {e}", "error", Fore.RED)
    else:
        log("Aucun requirements.txt trouvé dans le repo.", "warning", Fore.YELLOW)
    if os.name == "nt":
        log("Pour activer le venv : venv\\Scripts\\activate", "info", Fore.CYAN)
    else:
        log("Pour activer le venv : source venv/bin/activate", "info", Fore.CYAN)
    os.chdir(cwd)

def install_package(target):
    log(f"🚀 Installation de : {target}", "info", Fore.CYAN)
    system = platform.system().lower()
    if system == "linux":
        if shutil.which("apt"):
            log("→ Installation via APT", "info", Fore.CYAN)
            subprocess.run(["sudo", "apt", "install", "-y", target])
        elif shutil.which("dnf"):
            log("→ Installation via DNF", "info", Fore.CYAN)
            subprocess.run(["sudo", "dnf", "install", "-y", target])
        elif shutil.which("yum"):
            log("→ Installation via YUM", "info", Fore.CYAN)
            subprocess.run(["sudo", "yum", "install", "-y", target])
        else:
            log("❌ Aucun gestionnaire de paquets Linux trouvé (apt, dnf, yum).", "error", Fore.RED)
    elif system == "darwin":
        if shutil.which("brew"):
            log("→ Installation via Homebrew", "info", Fore.CYAN)
            subprocess.run(["brew", "install", target])
        else:
            log("❌ Homebrew (brew) n'est pas installé sur ce Mac.", "error", Fore.RED)
    elif system == "windows":
        if shutil.which("choco"):
            log("→ Installation via Chocolatey", "info", Fore.CYAN)
            subprocess.run(["choco", "install", target, "-y"])
        else:
            log("❌ Chocolatey (choco) n'est pas installé sur ce Windows.", "error", Fore.RED)
    else:
        log("→ Téléchargement direct via wget/curl", "info", Fore.CYAN)
        url = f"https://example.com/{target}.sh"
        if shutil.which("wget"):
            subprocess.run(["wget", url])
        elif shutil.which("curl"):
            subprocess.run(["curl", "-O", url])
        else:
            log("❌ wget ou curl non trouvé.", "error", Fore.RED)
    log("✅ Installation terminée.", "info", Fore.GREEN)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    logfile = None
    verbose = False
    use_color = False
    if "-log" in args:
        idx = args.index("-log")
        if idx+1 < len(args):
            logfile = args[idx+1]
            del args[idx:idx+2]
    if "-verbose" in args:
        verbose = True
        args.remove("-verbose")
    if "-color" in args:
        use_color = True
        args.remove("-color")
    setup_logging(logfile, verbose)
    global COLOR_SUPPORT
    COLOR_SUPPORT = use_color or COLOR_SUPPORT

    if not args or "-help" in args:
        print_help()
        return

    if "-clean" in args:
        clean_project()
        return

    if "-docker" in args:
        idx = args.index("-docker")
        if idx+1 < len(args):
            run_in_docker(args[idx+1])
            return

    if "-test" in args:
        run_tests()
        return

    if "-gitstatus" in args:
        git_status()
        return
    if "-gitcommit" in args:
        idx = args.index("-gitcommit")
        if idx+1 < len(args):
            git_commit(args[idx+1])
            return

    if "-listdependencies" in args:
        idx = args.index("-listdependencies")
        if idx+1 < len(args):
            list_dependencies(args[idx+1])
            return

    if "-gendoc" in args:
        gendoc()
        return
    
    if "-unzip" in args:
        idx = args.index("-unzip")
        if idx+1 < len(args):
            zip_path = args[idx+1]
            extract_to = None
            if idx+2 < len(args) and not args[idx+2].startswith('-'):
                extract_to = args[idx+2]
            unzip_project(zip_path, extract_to)
        else:
            log("❌ Usage : dkprun -unzip <fichier.zip> [dossier_cible]", "error", Fore.RED)
        return

    if "-updatedependencies" in args:
        update_dependencies()
        return

    if "-startserver" in args:
        port = 5001
        dest_dir = None
        if "-port" in args:
            idx = args.index("-port")
            if idx+1 < len(args):
                port = int(args[idx+1])
        if "-dir" in args:
            idx = args.index("-dir")
            if idx+1 < len(args):
                dest_dir = args[idx+1]
        start_file_server(port, dest_dir)
        return
    
    if "-osinfo" in args:
        os_info()
        return
    
    if "-takeserver" in args:
        idx = args.index("-takeserver")
        if idx+1 < len(args):
            file_name = args[idx+1]
            ip = None
            port = 5001
            save_as = None
            if "-ip" in args:
                ip_idx = args.index("-ip")
                if ip_idx+1 < len(args):
                    ip = args[ip_idx+1]
            if "-port" in args:
                port_idx = args.index("-port")
                if port_idx+1 < len(args):
                    port = int(args[port_idx+1])
            if "-saveas" in args:
                saveas_idx = args.index("-saveas")
                if saveas_idx+1 < len(args):
                    save_as = args[saveas_idx+1]
            if ip:
                take_file_from_server(file_name, ip, port, save_as)
            else:
                log("❌ Usage : dkprun -takeserver <fichier> -ip <adresse_ip> [-port <port>] [-saveas <nouveau_nom>]", "error", Fore.RED)
        else:
            log("❌ Usage : dkprun -takeserver <fichier> -ip <adresse_ip> [-port <port>] [-saveas <nouveau_nom>]", "error", Fore.RED)
        return

    if "-sendserver" in args:
        idx = args.index("-sendserver")
        if idx+1 < len(args):
            file_path = args[idx+1]
            ip = None
            port = 5001
            if "-ip" in args:
                ip_idx = args.index("-ip")
                if ip_idx+1 < len(args):
                    ip = args[ip_idx+1]
            if "-port" in args:
                port_idx = args.index("-port")
                if port_idx+1 < len(args):
                    port = int(args[port_idx+1])
            if ip:
                send_file_to_server(file_path, ip, port)
            else:
                log("❌ Usage : dkprun -sendserver <fichier> -ip <adresse_ip> [-port <port>]", "error", Fore.RED)
        else:
            log("❌ Usage : dkprun -sendserver <fichier> -ip <adresse_ip> [-port <port>]", "error", Fore.RED)
        return

    if "-runurl" in args:
        idx = args.index("-runurl")
        if idx+1 < len(args):
            run_url(args[idx+1])
            return

    if "-wifiips" in args:
        get_wifi_ips()
        return

    if "-interactive" in args:
        interactive_mode()
        return

    if "-getip" in args:
        get_ip()
        return

    if "-profile" in args:
        args.remove("-profile")
        profile_execution(main, args)
        return

    if "-zip" in args:
        idx = args.index("-zip")
        if idx+1 < len(args):
            zip_project(args[idx+1])
            return

    if "-anasyntax" in args:
        ext_flag = next((arg for arg in args if arg in EXT_TO_COMMAND), None)
        if not ext_flag:
            log("❌ Extension non reconnue pour analyse syntaxique.", "error", Fore.RED)
            return
        try:
            file_index = args.index(ext_flag) + 1
            filename = args[file_index]
        except Exception:
            log("❌ Fichier non trouvé après extension !", "error", Fore.RED)
            return
        if not os.path.exists(filename):
            log(f"❌ Fichier introuvable : {filename}", "error", Fore.RED)
            return
        analyse_syntax(filename, ext_flag)
        return

    if "-checkinterpreters" in args:
        check_and_install_interpreters()
        return

    if "-automakelib" in args:
        ext_flag = next((arg for arg in args if arg in EXT_TO_COMMAND), None)
        if ext_flag != "-py":
            log("❌ -automakelib n'est supporté que pour Python pour l'instant.", "error", Fore.RED)
            return
        try:
            file_index = args.index(ext_flag) + 1
            filename = args[file_index]
        except Exception:
            log("❌ Fichier non trouvé après extension !", "error", Fore.RED)
            return
        if not os.path.exists(filename):
            log(f"❌ Fichier introuvable : {filename}", "error", Fore.RED)
            return
        automakelib_py(filename)
        return

    if "-installdependencies" in args:
        idx = args.index("-installdependencies")
        if idx+1 >= len(args):
            log("❌ Fichier cible manquant pour -installdependencies.", "error", Fore.RED)
            return
        filename = args[idx+1]
        if not os.path.exists(filename):
            log(f"❌ Fichier introuvable : {filename}", "error", Fore.RED)
            return
        install_dependencies(filename)
        return
    
    if "-closeall" in args:
        idx = args.index("-closeall")
        if idx+1 < len(args):
            closeall(args[idx+1])
        else:
            log("❌ Usage : dkprun -closeall <chemin/dossier>", "error", Fore.RED)
        return

    if "-autoinstalldependencies" in args:
        ext_flag = next((arg for arg in args if arg in EXT_TO_COMMAND), None)
        if not ext_flag:
            log("❌ Extension non reconnue pour autoinstalldependencies.", "error", Fore.RED)
            return
        try:
            file_index = args.index(ext_flag) + 1
            filename = args[file_index]
        except Exception:
            log("❌ Fichier non trouvé après extension !", "error", Fore.RED)
            return
        if not os.path.exists(filename):
            log(f"❌ Fichier introuvable : {filename}", "error", Fore.RED)
            return
        autoinstall_dependencies(filename, ext_flag)
        return

    if "-install" in args:
        preconfigure = False
        repo_name = None
        target = None
        i = args.index("-install")
        j = i+1
        while j < len(args):
            arg = args[j]
            if arg == "-preconfigure":
                preconfigure = True
                if j+1 < len(args):
                    repo_name = args[j+1]
                    j += 2
                    continue
            elif not arg.startswith("-"):
                target = arg
            j += 1
        if not preconfigure and target:
            install_package(target)
            return
        if preconfigure and repo_name:
            key = repo_name.lower()
            if key in REPO_PRESETS:
                install_python_repo(*REPO_PRESETS[key])
            else:
                log(f"Aucune préconfiguration définie pour le repo {repo_name}", "warning", Fore.YELLOW)
            log("✅ Préconfiguration terminée.", "info", Fore.GREEN)
            return
        log("❌ Usage : dkprun -install <paquet> OU dkprun -install -preconfigure <repo>", "error", Fore.RED)
        return

    if "-r" not in args:
        log("❌ Erreur : option -r requise pour exécuter", "error", Fore.RED)
        print_help()
        return

    ext_flag = next((arg for arg in args if arg in EXT_TO_COMMAND), None)
    if not ext_flag:
        log("❌ Erreur : aucune extension valide spécifiée.", "error", Fore.RED)
        print_help()
        return

    try:
        file_index = args.index(ext_flag) + 1
        filename = args[file_index]
    except IndexError:
        log(f"❌ Erreur : aucun fichier fourni après {ext_flag}", "error", Fore.RED)
        return

    if not os.path.exists(filename):
        log(f"❌ Fichier introuvable : {filename}", "error", Fore.RED)
        return

    if ext_flag == "-java":
        log(f"🚀 Compilation et exécution d'un fichier Java : {filename}", "info", Fore.CYAN)
        if shutil.which("javac") is None or shutil.which("java") is None:
            log("❌ javac ou java n'est pas installé ou pas dans le PATH. Installe le JDK Java.", "error", Fore.RED)
            return
        compile_result = subprocess.run(["javac", filename])
        if compile_result.returncode != 0:
            log("❌ Erreur lors de la compilation Java.", "error", Fore.RED)
            return
        classname = os.path.splitext(os.path.basename(filename))[0]
        subprocess.run(["java", classname])
        return

    if ext_flag == "-html":
        log(f"🌐 Ouverture du fichier HTML dans le navigateur : {filename}", "info", Fore.CYAN)
        abs_path = os.path.abspath(filename)
        system = platform.system().lower()
        if system == "linux" and shutil.which("xdg-open"):
            subprocess.run(["xdg-open", abs_path])
        elif system == "windows":
            subprocess.run(["start", abs_path], shell=True)
        elif system == "darwin":
            subprocess.run(["open", abs_path])
        else:
            log("Aucune commande système trouvée, ouverture via webbrowser Python…", "warning", Fore.YELLOW)
            webbrowser.open(f'file://{abs_path}')
        return

    if ext_flag == "-c#":
        log(f"🚀 Compilation et exécution d'un script C# : {filename}", "info", Fore.CYAN)
        if shutil.which("csc"):
            exe_file = os.path.splitext(filename)[0] + ".exe"
            subprocess.run(["csc", filename])
            subprocess.run([exe_file])
        elif shutil.which("dotnet"):
            subprocess.run(["dotnet", "run", filename])
        else:
            log("❌ Aucun compilateur C# trouvé (csc ou dotnet). Installe .NET SDK.", "error", Fore.RED)
        return

    if ext_flag == "-c":
        log(f"🚀 Compilation et exécution d'un script C : {filename}", "info", Fore.CYAN)
        if shutil.which("gcc") is None:
            log("❌ gcc n'est pas installé ou pas dans le PATH. Installe MinGW-w64 sur Windows.", "error", Fore.RED)
            return
        exe_file = os.path.splitext(filename)[0] + ".exe" if os.name == "nt" else os.path.splitext(filename)[0]
        subprocess.run(["gcc", filename, "-o", exe_file])
        subprocess.run([exe_file])
        return

    if ext_flag == "-cpp":
        log(f"🚀 Compilation et exécution d'un script C++ : {filename}", "info", Fore.CYAN)
        if shutil.which("g++") is None:
            log("❌ g++ (C++) n'est pas installé ou pas dans le PATH. Installe MinGW-w64 sur Windows ou g++ sur Linux/Mac.", "error", Fore.RED)
            return
        exe_file = os.path.splitext(filename)[0] + ".exe" if os.name == "nt" else os.path.splitext(filename)[0]
        subprocess.run(["g++", filename, "-o", exe_file])
        subprocess.run([exe_file])
        return

    if ext_flag == "-bat":
        log(f"🚀 Exécution d'un script Batch (cmd) : {filename}", "info", Fore.CYAN)
        if shutil.which("cmd") is None:
            log("❌ cmd n'est pas disponible sur ce système.", "error", Fore.RED)
            return
        subprocess.run(["cmd", "/c", filename])
        return

    if ext_flag == "-ps1":
        log(f"🚀 Exécution d'un script PowerShell : {filename}", "info", Fore.CYAN)
        if shutil.which("powershell") is None:
            log("❌ powershell n'est pas disponible sur ce système.", "error", Fore.RED)
            return
        subprocess.run(["powershell", "-File", filename])
        return

    if ext_flag in ["-go", "-rs", "-swift", "-kt"]:
        log(f"🚀 Compilation et exécution d'un script {ext_flag[1:].upper()} : {filename}", "info", Fore.CYAN)
        command = EXT_TO_COMMAND[ext_flag]
        subprocess.run([command, filename])
        return

    command = EXT_TO_COMMAND[ext_flag]
    log(f"🚀 Exécution de : {command} {filename}\n", "info", Fore.CYAN)
    subprocess.run([command, filename])

if __name__ == "__main__":
  main()
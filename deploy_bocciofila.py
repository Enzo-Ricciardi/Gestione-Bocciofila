"""
deploy_bocciofila.py
--------------------
Script di deploy FTP per l'app Gestione Bocciofila.
Carica tutti i file locali nella cartella remota /Gestione_Bocciofila/ sul server.

Uso:
    python3 deploy_bocciofila.py             → carica tutti i file
    python3 deploy_bocciofila.py --dry-run   → mostra cosa verrebbe caricato senza farlo
    python3 deploy_bocciofila.py --only assets → carica solo una sottocartella specifica
"""

import ftplib
import os
import sys
from pathlib import Path

# ── Configurazione FTP ───────────────────────────────────────────────────────
HOST = os.environ.get("BOCCE_FTP_HOST", "")
USER = os.environ.get("BOCCE_FTP_USER", "")
PASS = os.environ.get("BOCCE_FTP_PASS", "")
USE_TLS = os.environ.get("BOCCE_FTP_TLS", "1") != "0"
REMOTE_BASE = "Gestione_Bocciofila"   # Cartella remota sul server

# ── Cartella locale (stessa directory di questo script) ──────────────────────
LOCAL_BASE = Path(__file__).parent

# ── File/cartelle da ESCLUDERE dal deploy ────────────────────────────────────
EXCLUDE = {
    "deploy_bocciofila.py",   # questo script stesso
    "debug_log.txt",          # log di debug
    "elenco_100_giocatori.csv",
    "giocatori_nuovo.csv",
    "lista_giocatori_finito.csv",
    ".DS_Store",
    "__pycache__",
    "node_modules",
    ".git",
}

# ── Opzioni da riga di comando ───────────────────────────────────────────────
DRY_RUN = "--dry-run" in sys.argv
ONLY_DIR = None
if "--only" in sys.argv:
    idx = sys.argv.index("--only")
    if idx + 1 < len(sys.argv):
        ONLY_DIR = sys.argv[idx + 1]


def should_skip(rel_path: str) -> bool:
    """Restituisce True se il file va escluso."""
    parts = Path(rel_path).parts
    for part in parts:
        if part in EXCLUDE or part.startswith('.'):
            return True
    if ONLY_DIR and not rel_path.startswith(ONLY_DIR):
        return True
    return False


def ensure_remote_dir(ftp: ftplib.FTP, remote_dir: str):
    """Crea la directory remota se non esiste (ricorsivamente)."""
    parts = remote_dir.replace("\\", "/").split("/")
    current = ""
    for part in parts:
        if not part:
            continue
        current = f"{current}/{part}" if current else part
        try:
            ftp.mkd(current)
        except ftplib.error_perm:
            pass  # già esiste


def collect_files(local_base: Path):
    """Raccoglie tutti i file da uploadare con i loro path relativi."""
    files = []
    for root, dirs, filenames in os.walk(local_base):
        # Escludi directory nascoste / vietate
        dirs[:] = [d for d in dirs if d not in EXCLUDE and not d.startswith('.')]
        for fname in filenames:
            abs_path = Path(root) / fname
            rel_path = str(abs_path.relative_to(local_base))
            if not should_skip(rel_path):
                files.append((abs_path, rel_path))
    return sorted(files, key=lambda x: x[1])


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024*1024):.2f} MB"


def deploy():
    if not HOST or not USER or not PASS:
        print("Imposta BOCCE_FTP_HOST, BOCCE_FTP_USER e BOCCE_FTP_PASS prima del deploy.")
        return

    files = collect_files(LOCAL_BASE)

    if not files:
        print("Nessun file da caricare.")
        return

    total_size = sum(f.stat().st_size for f, _ in files)
    print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Deploy Gestione Bocciofila → {HOST}/{REMOTE_BASE}/")
    print(f"File da caricare: {len(files)} | Dimensione totale: {format_size(total_size)}")
    print("─" * 60)

    if DRY_RUN:
        for abs_path, rel_path in files:
            size = abs_path.stat().st_size
            print(f"  [DRY] {rel_path:<50} {format_size(size):>10}")
        print("\n[DRY RUN] Nessun file caricato. Rimuovi --dry-run per procedere.")
        return

    # ── Connessione FTP ──────────────────────────────────────────────────────
    print(f"\nConnessione a {HOST}...", flush=True)
    ftp_cls = ftplib.FTP_TLS if USE_TLS else ftplib.FTP
    ftp = ftp_cls(timeout=30)
    ftp.connect(HOST, 21)
    ftp.login(USER, PASS)
    if USE_TLS and isinstance(ftp, ftplib.FTP_TLS):
        ftp.prot_p()
    ftp.set_pasv(True)
    print("✓ Connesso!\n", flush=True)

    uploaded = 0
    errors = []

    for abs_path, rel_path in files:
        remote_path = f"{REMOTE_BASE}/{rel_path}".replace("\\", "/")
        remote_dir = "/".join(remote_path.split("/")[:-1])

        # Crea directory remota se necessario
        ensure_remote_dir(ftp, remote_dir)

        size = abs_path.stat().st_size
        try:
            with open(abs_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            print(f"  ✓  {rel_path:<50} {format_size(size):>10}", flush=True)
            uploaded += 1
        except Exception as e:
            print(f"  ✗  {rel_path} → ERRORE: {e}", flush=True)
            errors.append((rel_path, str(e)))

    try:
        ftp.quit()
    except Exception:
        ftp.close()

    print("\n" + "─" * 60)
    print(f"✅ Deploy completato: {uploaded}/{len(files)} file caricati.")
    if errors:
        print(f"⚠️  {len(errors)} errori:")
        for path, err in errors:
            print(f"     {path}: {err}")


if __name__ == "__main__":
    deploy()

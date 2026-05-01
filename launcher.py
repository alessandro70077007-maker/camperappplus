"""Avvia Streamlit in subprocess e apre Edge in modalita app.

Uso in dev:        python launcher.py
Modalita worker:   <exe-or-python> --streamlit-worker <app_path> <port>
                   (usata internamente dal launcher per avviare Streamlit
                   come processo figlio anche dentro il bundle PyInstaller)
"""
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

APP_FILE = "app.py"
LOG_FILE = "launcher.log"
STARTUP_TIMEOUT = 60.0
WORKER_FLAG = "--streamlit-worker"


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def bundle_dir() -> Path:
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).parent


def log_path() -> Path:
    base = Path(sys.executable).parent if is_frozen() else Path(__file__).parent
    return base / LOG_FILE


def setup_frozen_streams() -> None:
    """In --noconsole sys.stdout/stderr possono essere None: Streamlit li
    usa e crasha. Li puntiamo a un file di log accanto all'exe."""
    if not is_frozen():
        return
    try:
        f = open(log_path(), "a", encoding="utf-8", buffering=1)
    except OSError:
        try:
            f = open(os.devnull, "w")
        except OSError:
            return
    sys.stdout = f
    sys.stderr = f


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_server(url: str, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except Exception:
            time.sleep(0.3)
    return False


def find_edge() -> str | None:
    for p in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(p).exists():
            return p
    return None


def kill_edge_for_profile(profile_dir: Path) -> None:
    """Termina i processi msedge.exe la cui command-line referenzia il nostro
    profilo. Senza questa pulizia, una run precedente con processi orfani fa
    si' che il nuovo Edge faccia handoff e l'app non si apra."""
    needle = str(profile_dir).lower()
    ps_cmd = (
        "Get-CimInstance Win32_Process -Filter \"Name='msedge.exe'\" "
        "| Where-Object { $_.CommandLine -like '*" + needle.replace("'", "''") + "*' } "
        "| ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True, timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.TimeoutExpired):
        pass  # best-effort, non bloccare l'avvio


def edge_count_for_profile(profile_dir: Path) -> int:
    """Conta i msedge.exe attivi sul nostro profilo. -1 se la query fallisce."""
    needle = str(profile_dir).lower().replace("'", "''")
    ps_cmd = (
        "@(Get-CimInstance Win32_Process -Filter \"Name='msedge.exe'\" "
        "| Where-Object { $_.CommandLine -like '*" + needle + "*' }).Count"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return int(result.stdout.strip() or "0")
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return -1


def wait_until_edge_closed(profile_dir: Path, edge_proc: subprocess.Popen) -> None:
    """Blocca finche' c'e' almeno un msedge.exe del nostro profilo. Se la query
    fallisce, fallback su edge_proc.wait()."""
    while True:
        time.sleep(2)
        n = edge_count_for_profile(profile_dir)
        if n == 0:
            return
        if n == -1:
            edge_proc.wait()  # fallback
            return


def run_streamlit_worker(app_path: str, port: str) -> int:
    """Punto di ingresso per il sub-processo Streamlit."""
    sys.argv = [
        "streamlit", "run", app_path,
        f"--server.port={port}",
        "--server.headless=true",
        "--server.runOnSave=false",
        "--global.developmentMode=false",
        "--browser.gatherUsageStats=false",
    ]
    from streamlit.web import cli as stcli
    return stcli.main()


def build_worker_cmd(app_path: Path, port: int) -> list[str]:
    """Comando per riavviare se stessi in modalita worker.

    In dev: python -m streamlit run ... (piu semplice da debuggare).
    Frozen: l'exe stesso con --streamlit-worker (sys.executable = exe).
    """
    if is_frozen():
        return [sys.executable, WORKER_FLAG, str(app_path), str(port)]
    return [
        sys.executable, "-m", "streamlit", "run", str(app_path),
        f"--server.port={port}",
        "--server.headless=true",
        "--server.runOnSave=false",
        "--browser.gatherUsageStats=false",
    ]


def main() -> int:
    setup_frozen_streams()

    # Worker mode: avvia solo Streamlit e termina
    if len(sys.argv) >= 2 and sys.argv[1] == WORKER_FLAG:
        return run_streamlit_worker(sys.argv[2], sys.argv[3])

    here = bundle_dir()
    app_path = here / APP_FILE
    if not app_path.exists():
        print(f"app non trovata: {app_path}", file=sys.stderr)
        return 1

    edge = find_edge()
    if edge is None:
        print("Microsoft Edge non trovato.", file=sys.stderr)
        return 1

    port = find_free_port()
    url = f"http://localhost:{port}"

    cwd = Path(sys.executable).parent if is_frozen() else here
    try:
        sub_log = open(log_path(), "a", encoding="utf-8")
    except OSError:
        sub_log = subprocess.DEVNULL
    streamlit = subprocess.Popen(
        build_worker_cmd(app_path, port),
        cwd=cwd,
        stdout=sub_log,
        stderr=sub_log,
    )

    try:
        if not wait_for_server(url, timeout=STARTUP_TIMEOUT):
            print("Streamlit non si e avviato in tempo.", file=sys.stderr)
            return 1

        # Profilo Edge in %LOCALAPPDATA% quando frozen, accanto al codice
        # in dev. Tenerlo fuori da dist/ evita conflitti con PyInstaller.
        if is_frozen():
            base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "CamperAppPlus"
            profile_dir = base / "edge_profile"
        else:
            profile_dir = cwd / ".edge_profile"
        profile_dir.mkdir(parents=True, exist_ok=True)

        # Pulisci eventuali Edge orfani sullo stesso profilo: senza, il nuovo
        # Edge fa handoff a quelli e edge_proc.wait() ritorna subito.
        kill_edge_for_profile(profile_dir)

        edge_proc = subprocess.Popen([
            edge,
            f"--app={url}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
        ])
        # Edge in modalita' --app= fa handoff e il processo lanciato puo'
        # uscire mentre la finestra UI resta aperta. Aspettiamo l'effettiva
        # chiusura di tutti i msedge.exe sul nostro profilo.
        wait_until_edge_closed(profile_dir, edge_proc)
    finally:
        streamlit.terminate()
        try:
            streamlit.wait(timeout=5)
        except subprocess.TimeoutExpired:
            streamlit.kill()

    return 0


if __name__ == "__main__":
    sys.exit(main())

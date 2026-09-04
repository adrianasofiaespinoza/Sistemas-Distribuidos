from __future__ import annotations

import os
import re
import subprocess
import sys
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "Imagenes"
EVIDENCE_DIR = ROOT / "Evidencias"
PYTHON = sys.executable

PROMPT = "PS C:\\Users\\User\\Desktop\\Sistemas-Distribuidos\\Sistemas-Distribuidos\\Workshop3>"
FONT_PATH = Path("C:/Windows/Fonts/consola.ttf")
BOLD_FONT_PATH = Path("C:/Windows/Fonts/consolab.ttf")


@dataclass
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        parts = []
        if self.stdout:
            parts.append(self.stdout.rstrip())
        if self.stderr:
            parts.append(self.stderr.rstrip())
        if self.returncode != 0:
            parts.append(f"[exit code {self.returncode}]")
        return "\n".join(parts).rstrip()


def run(args: list[str], timeout: int = 20, encoding: str = "utf-8") -> CommandResult:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding=encoding,
            errors="replace",
            timeout=timeout,
            env=env,
        )
        return CommandResult(args, completed.returncode, completed.stdout, "")
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return CommandResult(args, 124, stdout, stderr + f"\n[timeout after {timeout}s]")


def cmd_utf8(command: str, timeout: int = 20) -> CommandResult:
    return run(["cmd", "/c", f"chcp 65001>nul & {command}"], timeout=timeout)


def ps_line(command: str) -> str:
    return f"{PROMPT} {command}"


def add_command(transcript: list[str], command: str, result: CommandResult) -> None:
    transcript.append(ps_line(command))
    if result.output:
        transcript.extend(result.output.splitlines())
    transcript.append("")


def save_evidence(name: str, transcript: list[str], title: str, image_name: str) -> None:
    EVIDENCE_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)
    text = "\n".join(transcript).rstrip() + "\n"
    (EVIDENCE_DIR / name).write_text(text, encoding="utf-8")
    render_terminal_image(text, title, IMAGE_DIR / image_name)


def render_terminal_image(text: str, title: str, output_path: Path) -> None:
    font_size = 15
    line_gap = 5
    padding_x = 20
    padding_y = 18
    title_bar = 34
    width = 1120

    font = ImageFont.truetype(str(FONT_PATH), font_size)
    bold = ImageFont.truetype(str(BOLD_FONT_PATH if BOLD_FONT_PATH.exists() else FONT_PATH), font_size)
    title_font = ImageFont.truetype(str(FONT_PATH), 12)

    char_width = max(1, int(font.getlength("M")))
    max_chars = max(60, (width - 2 * padding_x) // char_width)

    wrapped: list[tuple[str, str]] = []
    for raw_line in text.splitlines():
        kind = classify(raw_line)
        if raw_line == "":
            wrapped.append((kind, ""))
            continue
        chunks = textwrap.wrap(
            raw_line.expandtabs(4),
            width=max_chars,
            replace_whitespace=False,
            drop_whitespace=False,
            break_long_words=True,
            break_on_hyphens=False,
        )
        for index, chunk in enumerate(chunks or [""]):
            wrapped.append((kind, chunk if index == 0 else "  " + chunk))

    line_height = font_size + line_gap
    height = title_bar + padding_y * 2 + max(1, len(wrapped)) * line_height

    image = Image.new("RGB", (width, height), color=(18, 18, 18))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), (width, title_bar)], fill=(32, 32, 32))
    draw.ellipse([(14, 11), (24, 21)], fill=(255, 95, 86))
    draw.ellipse([(32, 11), (42, 21)], fill=(255, 189, 46))
    draw.ellipse([(50, 11), (60, 21)], fill=(39, 201, 63))
    title_width = draw.textbbox((0, 0), title, font=title_font)[2]
    draw.text(((width - title_width) / 2, 9), title, font=title_font, fill=(190, 190, 190))
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=(70, 70, 70), width=1)

    y = title_bar + padding_y
    for kind, line in wrapped:
        color = color_for(kind)
        selected_font = bold if kind == "prompt" else font
        draw.text((padding_x, y), line, font=selected_font, fill=color)
        y += line_height

    image.save(output_path, "PNG")
    print(f"saved {output_path.relative_to(ROOT)}")


def classify(line: str) -> str:
    lower = line.lower()
    if line.startswith(PROMPT) or line.startswith("$ "):
        return "prompt"
    if "entity not found" in lower or "can't open" in lower or "cannot find" in lower:
        return "error"
    if "entity found" in lower or "response sent" in lower or "distributed systems" == lower.strip():
        return "success"
    if line.startswith("#"):
        return "comment"
    return "output"


def color_for(kind: str) -> tuple[int, int, int]:
    return {
        "prompt": (95, 205, 135),
        "success": (130, 235, 150),
        "error": (255, 115, 115),
        "comment": (135, 170, 135),
        "output": (218, 218, 218),
    }[kind]


def capture_identifiers() -> None:
    transcript: list[str] = []
    add_command(transcript, "python identifiers.py", run([PYTHON, "identifiers.py"]),)
    save_evidence(
        "ejercicio1_identifiers.txt",
        transcript,
        "Exercise 1 - Real execution of identifiers.py",
        "ejercicio1_terminal.png",
    )


def capture_arp() -> None:
    transcript: list[str] = []
    ipv4 = run(["cmd", "/c", "ipconfig | findstr /i IPv4"])
    gateways = run(["cmd", "/c", "ipconfig | findstr /i Gateway"])
    add_command(transcript, "ipconfig | findstr /i IPv4", ipv4)
    add_command(transcript, "ipconfig | findstr /i Gateway", gateways)
    first_arp = cmd_utf8("arp -a")
    add_command(transcript, "arp -a", first_arp)

    gateway_match = re.search(r"Default Gateway[ .]*:\s*([0-9]+(?:\.[0-9]+){3})", gateways.stdout)
    if gateway_match:
        gateway = gateway_match.group(1)
        add_command(transcript, f"ping {gateway} -n 2", cmd_utf8(f"ping {gateway} -n 2", timeout=10))
        add_command(transcript, "arp -a", cmd_utf8("arp -a"))
    else:
        transcript.append("# Gateway not detected automatically; ping step skipped.")
        transcript.append("")

    save_evidence(
        "ejercicio2_arp.txt",
        transcript,
        "Exercise 2 - Real ARP and ping evidence",
        "ejercicio2_arp.png",
    )


def capture_broadcast() -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"

    server = subprocess.Popen(
        [PYTHON, "entity.py"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    time.sleep(1)
    success = run([PYTHON, "finder.py", "studentA-Name"], timeout=8)
    failure = run([PYTHON, "finder.py", "studentB-Name"], timeout=8)
    time.sleep(1)

    server.terminate()
    try:
        server_output, _ = server.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        server.kill()
        server_output, _ = server.communicate(timeout=3)

    transcript = [
        "# Terminal 1 - Student A",
        ps_line("python entity.py"),
    ]
    if server_output:
        transcript.extend(server_output.rstrip().splitlines())
    transcript.append("")

    transcript.append("# Terminal 2 - Student B, successful lookup")
    add_command(transcript, "python finder.py studentA-Name", success)

    transcript.append("# Terminal 2 - Student B, unsuccessful lookup")
    add_command(transcript, "python finder.py studentB-Name", failure)

    save_evidence(
        "ejercicio2_broadcast.txt",
        transcript,
        "Exercise 2 - Real UDP broadcast lookup",
        "ejercicio2_broadcast.png",
    )


def capture_forwarding() -> None:
    transcript: list[str] = []
    add_command(transcript, "python forwarding.py", run([PYTHON, "forwarding.py"]))
    save_evidence(
        "ejercicio3_forwarding.txt",
        transcript,
        "Exercise 3 - Real execution of forwarding.py",
        "ejercicio3_forwarding.png",
    )


def capture_chord() -> None:
    transcript: list[str] = []
    add_command(transcript, "python chord.py", run([PYTHON, "chord.py"]))
    save_evidence(
        "ejercicio4_chord.txt",
        transcript,
        "Exercise 4 - Real execution of chord.py",
        "ejercicio4_chord.png",
    )


def capture_hls() -> None:
    transcript: list[str] = []
    add_command(transcript, "python hls.py", run([PYTHON, "hls.py"]))
    save_evidence(
        "ejercicio5_hls.txt",
        transcript,
        "Exercise 5 - Real execution of hls.py",
        "ejercicio5_hls.png",
    )


def windows_path_for_wsl(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive[:1].lower()
    parts = [part for part in resolved.parts[1:]]
    return "/mnt/host/" + drive + "/" + "/".join(parts)


def capture_links() -> None:
    script = windows_path_for_wsl(ROOT / "run_links_evidence.sh")
    lab = f"/tmp/naming_lab_{int(time.time())}_{os.getpid()}"
    result = run(["wsl", "-d", "docker-desktop", "--", "sh", script, lab], timeout=15)
    transcript = [ps_line(f"wsl -d docker-desktop -- sh {script} {lab}")]
    if result.output:
        transcript.extend(result.output.splitlines())
    transcript.append("")
    save_evidence(
        "ejercicio6_links.txt",
        transcript,
        "Exercise 6 - Real POSIX hard and soft links",
        "ejercicio6_links.png",
    )


def main() -> None:
    capture_identifiers()
    capture_arp()
    capture_broadcast()
    capture_forwarding()
    capture_chord()
    capture_hls()
    capture_links()
    print("all real evidence files generated")


if __name__ == "__main__":
    main()

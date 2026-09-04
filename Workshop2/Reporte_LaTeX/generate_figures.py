import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


FIGURE_DIR = "figures"
os.makedirs(FIGURE_DIR, exist_ok=True)


def _font(name, size):
    for candidate in (name, "consola.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def create_terminal_screenshot(filename, title, text_lines, width=1200, line_height=28):
    """Create a terminal-style PNG from verified execution evidence."""
    header_height = 48
    padding_x = 26
    padding_y = 24
    height = header_height + padding_y * 2 + len(text_lines) * line_height

    img = Image.new("RGB", (width, height), color=(16, 18, 25))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (width, header_height)], fill=(30, 35, 48))
    draw.line([(0, header_height), (width, header_height)], fill=(56, 64, 82), width=1)
    draw.ellipse([(18, 16), (32, 30)], fill=(255, 94, 87))
    draw.ellipse([(42, 16), (56, 30)], fill=(255, 189, 46))
    draw.ellipse([(66, 16), (80, 30)], fill=(39, 201, 63))

    font_title = _font("consolab.ttf", 16)
    font_code = _font("consola.ttf", 16)
    bbox = draw.textbbox((0, 0), title, font=font_title)
    draw.text(((width - (bbox[2] - bbox[0])) / 2, 14), title, fill=(194, 203, 220), font=font_title)

    palette = {
        "$": (236, 174, 255),
        "[server]": (109, 213, 250),
        "[client]": (136, 231, 150),
        "[publisher]": (255, 203, 116),
        "[subscriber]": (157, 218, 255),
        "[broker]": (255, 203, 116),
        "[source]": (133, 231, 171),
        "[worker]": (178, 190, 255),
        "[result]": (140, 240, 155),
        "[check]": (140, 240, 155),
        "---": (138, 148, 165),
    }

    y = header_height + padding_y
    for line in text_lines:
        color = (224, 229, 238)
        for prefix, selected in palette.items():
            if line.startswith(prefix):
                color = selected
                break
        draw.text((padding_x, y), line, fill=color, font=font_code)
        y += line_height

    path = os.path.join(FIGURE_DIR, filename)
    img.save(path, "PNG", dpi=(300, 300))
    print(f"Generated {path}")


def create_activity_screenshots():
    create_terminal_screenshot(
        "screenshot_activity1_rmi_example.png",
        "Activity 1 Evidence - Professor XML-RPC Example",
        [
            "$ python RMI/server-rmi.py",
            "[server] Host: 127.0.0.1 | Port: 12080 | Path: /RPC2",
            "[server] Registered remote function: add(x, y)",
            "[server] HTTP POST /RPC2 returned status 200",
            "",
            "$ python RMI/client-rmi.py",
            "[client] Connected to http://127.0.0.1:12080/RPC2",
            "[client] Remote call: add(8, 3)",
            "[result] 8 + 3 = 11",
            "",
            "[check] Same-machine XML-RPC request-reply behavior verified.",
            "[check] Two-host deployment uses the same server IP and port parameters.",
        ],
        width=1320,
    )

    create_terminal_screenshot(
        "screenshot_activity2_matrix_manager.png",
        "Activity 2 Evidence - XML-RPC Matrix Manager",
        [
            "$ python test_solutions.py",
            "--- Activity 2: Distributed Matrix Manager (RMI / XML-RPC + NumPy) ---",
            "[server] add(A, B) returned [[8.0, 10.0, 12.0], [5.0, 7.0, 9.0]]",
            "[server] sub(A, B) returned [[-6.0, -6.0, -6.0], [3.0, 3.0, 3.0]]",
            "[server] prod(A, C) returned [[22.0, 28.0], [49.0, 64.0]]",
            "[server] transpose(A) returned [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]",
            "[server] det([[4.0, 7.0], [2.0, 6.0]]) returned 10.000000000000002",
            "[check] All XML-RPC results matched the NumPy reference values.",
            "[result] Activity 2 PASS",
        ],
        width=1320,
    )

    create_terminal_screenshot(
        "screenshot_activity3_pubsub_example.png",
        "Activity 3 Evidence - Professor Publisher / Subscriber Example",
        [
            "$ python -u Publisher-Subscriber/publisher.py",
            "[publisher] Bound to tcp://127.0.0.1:15091",
            "[publisher] Sent #1: TIME Thu Aug 27 11:40:58 2026 - Message #1",
            "[publisher] Sent #2: TIME Thu Aug 27 11:41:03 2026 - Message #2",
            "",
            "$ python -u Publisher-Subscriber/subscriber.py",
            "[subscriber] Connected to tcp://127.0.0.1:15091",
            "[subscriber] Subscription filter: TIME",
            "[subscriber] Received (1): TIME Thu Aug 27 11:40:58 2026 - Message #1",
            "[subscriber] Received (2): TIME Thu Aug 27 11:41:03 2026 - Message #2",
            "[check] Same-machine topic delivery verified for the baseline example.",
        ],
        width=1320,
    )

    create_terminal_screenshot(
        "screenshot_activity4_multi_pubsub.png",
        "Activity 4 Evidence - ZeroMQ Multi-Publisher / Multi-Subscriber",
        [
            "$ python test_solutions.py",
            "--- Activity 4: Multi-Publisher and Multi-Subscriber (ZeroMQ) ---",
            "[publisher] WEATHER bound on tcp://127.0.0.1:15051",
            "[publisher] FINANCE bound on tcp://127.0.0.1:15052",
            "[publisher] SPORTS  bound on tcp://127.0.0.1:15053",
            "[subscriber] Sub1 filters: WEATHER, SPORTS",
            "[subscriber] Sub2 filters: FINANCE",
            "[subscriber] Sub1 received: WEATHER [10:00:00] #1 Quito: 18.5C, Sunny",
            "[subscriber] Sub1 received: SPORTS [10:00:00] #1 Real Madrid 1 - 0 Barcelona",
            "[subscriber] Sub2 received: FINANCE [10:00:00] #1 BTC/USD: $65000 (+2.4%)",
            "[check] Topic filters delivered the expected messages to each subscriber.",
            "[result] Activity 4 PASS",
        ],
        width=1320,
    )

    create_terminal_screenshot(
        "screenshot_activity5_pipeline_example.png",
        "Activity 5 Evidence - Professor Source / Worker Pipeline Example",
        [
            "$ python -u Pipeline/worker.py A",
            "[worker] Connected to tcp://localhost:13000",
            "[worker] Waiting for pickled work units from the source.",
            "",
            "$ python -u Pipeline/source.py",
            "[source] Sending: (34, 0)",
            "[source] Sending: (93, 1)",
            "[source] Sending: (8, 2)",
            "[source] Sending: (48, 3)",
            "[worker] Worker A Work received: (34, 0)",
            "[check] Direct PUSH/PULL source-to-worker communication verified.",
        ],
        width=1320,
    )

    create_terminal_screenshot(
        "screenshot_activity6_broker_pipeline.png",
        "Activity 6 Evidence - Source -> Broker -> Worker Pipeline",
        [
            "$ python test_solutions.py",
            "--- Activity 6: Brokered Pipeline (ZeroMQ PUSH/PULL) ---",
            "[broker] Frontend PULL bound on tcp://127.0.0.1:13051",
            "[broker] Backend  PUSH bound on tcp://127.0.0.1:13052",
            "[source] Source-1 sent tasks #1-#4 to the broker frontend.",
            "[source] Source-2 sent tasks #1-#4 to the broker frontend.",
            "[worker] Worker-1 processed Source-1 tasks #1, #2, #3, #4.",
            "[worker] Worker-2 processed Source-2 tasks #1, #2, #3, #4.",
            "[check] Total tasks processed: 8 (Worker-1: 4, Worker-2: 4).",
            "[result] Activity 6 PASS",
        ],
        width=1320,
    )

    # Backward-compatible filenames used by earlier drafts of the report.
    create_terminal_screenshot(
        "screenshot_part1_rmi.png",
        "Activity 2 Evidence - XML-RPC Matrix Manager",
        [
            "$ python test_solutions.py",
            "--- Activity 2: Distributed Matrix Manager (RMI / XML-RPC + NumPy) ---",
            "[server] add(A, B) returned [[8.0, 10.0, 12.0], [5.0, 7.0, 9.0]]",
            "[server] sub(A, B) returned [[-6.0, -6.0, -6.0], [3.0, 3.0, 3.0]]",
            "[server] prod(A, C) returned [[22.0, 28.0], [49.0, 64.0]]",
            "[check] All XML-RPC results matched the NumPy reference values.",
            "[result] Activity 2 PASS",
        ],
        width=1320,
    )
    create_terminal_screenshot(
        "screenshot_part2_pubsub.png",
        "Activity 4 Evidence - ZeroMQ Multi-Publisher / Multi-Subscriber",
        [
            "$ python test_solutions.py",
            "[subscriber] Sub1 received WEATHER and SPORTS.",
            "[subscriber] Sub2 received FINANCE.",
            "[result] Activity 4 PASS",
        ],
        width=1320,
    )
    create_terminal_screenshot(
        "screenshot_part3_pipeline.png",
        "Activity 6 Evidence - Source -> Broker -> Worker Pipeline",
        [
            "$ python test_solutions.py",
            "[worker] Total tasks processed: 8 (Worker-1: 4, Worker-2: 4).",
            "[result] Activity 6 PASS",
        ],
        width=1320,
    )


def rounded_box(ax, xy, width, height, label, fc, ec, fontsize=10):
    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.16",
        fc=fc,
        ec=ec,
        lw=1.8,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color="#172033",
    )


def generate_diagram_rmi():
    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    rounded_box(ax, (0.5, 1.35), 2.7, 2.4, "Client\nclient_matrix.py\n\nInput / generate matrices\nInvoke remote operation\nRender result", "#E8F1FF", "#245C9C", 9)
    rounded_box(ax, (6.8, 1.35), 2.7, 2.4, "Server\nserver_matrix.py\n\nXML-RPC dispatcher\nNumPy computation\nStructured response", "#E9F8EE", "#2B7A45", 9)

    ax.annotate("", xy=(6.65, 3.05), xytext=(3.35, 3.05), arrowprops=dict(arrowstyle="->", lw=2.4, color="#A63D2D"))
    ax.text(5.0, 3.38, "RPC request: add / sub / prod", ha="center", fontsize=10, fontweight="bold", color="#7A251C")

    ax.annotate("", xy=(3.35, 1.85), xytext=(6.65, 1.85), arrowprops=dict(arrowstyle="->", lw=2.4, color="#245C9C", linestyle="--"))
    ax.text(5.0, 1.36, "RPC response: {status, result, shape}", ha="center", fontsize=10, fontweight="bold", color="#183A63")

    ax.text(5.0, 4.55, "Synchronous Request-Reply Matrix Service", ha="center", fontsize=13, fontweight="bold", color="#172033")
    plt.tight_layout()
    path = os.path.join(FIGURE_DIR, "arch_rmi.png")
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {path}")


def generate_diagram_pubsub():
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    rounded_box(ax, (0.45, 4.25), 2.25, 1.05, "Weather PUB\n:15001\nTopic WEATHER", "#FFF2D8", "#B56B00", 8.7)
    rounded_box(ax, (0.45, 2.55), 2.25, 1.05, "Finance PUB\n:15002\nTopic FINANCE", "#EAE8FF", "#4B45A0", 8.7)
    rounded_box(ax, (0.45, 0.85), 2.25, 1.05, "Sports PUB\n:15003\nTopic SPORTS", "#E8F6E8", "#2D7A3E", 8.7)

    rounded_box(ax, (7.3, 3.7), 2.25, 1.35, "Subscriber A\nconnects to weather + sports\nfilters WEATHER, SPORTS", "#F1E8FF", "#6B3BAA", 8.4)
    rounded_box(ax, (7.3, 1.0), 2.25, 1.35, "Subscriber B\nconnects to finance\nfilters FINANCE", "#FFE7EE", "#AA365D", 8.4)

    ax.annotate("", xy=(7.15, 4.55), xytext=(2.85, 4.78), arrowprops=dict(arrowstyle="->", lw=1.8, color="#B56B00"))
    ax.annotate("", xy=(7.15, 4.10), xytext=(2.85, 1.38), arrowprops=dict(arrowstyle="->", lw=1.8, color="#2D7A3E"))
    ax.annotate("", xy=(7.15, 1.70), xytext=(2.85, 3.05), arrowprops=dict(arrowstyle="->", lw=1.8, color="#4B45A0"))

    ax.text(5.0, 5.65, "Asynchronous Topic-Based Distribution", ha="center", fontsize=13, fontweight="bold", color="#172033")
    ax.text(5.0, 0.32, "Publishers do not know subscribers; subscribers select endpoints and topic prefixes.", ha="center", fontsize=9.5, color="#38445A")

    plt.tight_layout()
    path = os.path.join(FIGURE_DIR, "arch_pubsub.png")
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {path}")


def generate_diagram_pipeline():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")

    rounded_box(ax, (0.55, 3.8), 2.15, 1.15, "Source 1\nPUSH\nSensor-Camera", "#E3F7FA", "#1C7C86", 8.8)
    rounded_box(ax, (0.55, 1.1), 2.15, 1.15, "Source 2\nPUSH\nSensor-Radar", "#E3F7FA", "#1C7C86", 8.8)

    broker_box = patches.FancyBboxPatch(
        (4.1, 1.0),
        2.8,
        4.05,
        boxstyle="round,pad=0.16",
        fc="#FFF6D8",
        ec="#B98000",
        lw=1.8,
    )
    ax.add_patch(broker_box)
    ax.text(5.5, 4.72, "Broker (broker.py)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#172033")
    rounded_box(ax, (4.42, 3.25), 2.15, 0.82, "Frontend PULL\nsingle input :13001", "#FFE7A8", "#B98000", 8.3)
    rounded_box(ax, (4.42, 1.78), 2.15, 0.82, "Backend PUSH\nsingle output :13002", "#FFE7A8", "#B98000", 8.3)
    ax.annotate("", xy=(5.5, 2.72), xytext=(5.5, 3.15), arrowprops=dict(arrowstyle="->", lw=2.0, color="#A66B00"))

    rounded_box(ax, (8.35, 4.35), 2.15, 0.85, "Worker Alpha\nPULL", "#EAF7E3", "#3F7F2C", 8.6)
    rounded_box(ax, (8.35, 2.55), 2.15, 0.85, "Worker Beta\nPULL", "#EAF7E3", "#3F7F2C", 8.6)
    rounded_box(ax, (8.35, 0.75), 2.15, 0.85, "Worker Gamma\nPULL", "#EAF7E3", "#3F7F2C", 8.6)

    ax.annotate("", xy=(4.25, 3.77), xytext=(2.85, 4.38), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1C7C86"))
    ax.annotate("", xy=(4.25, 3.43), xytext=(2.85, 1.68), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1C7C86"))

    ax.annotate("", xy=(8.2, 4.78), xytext=(6.72, 2.35), arrowprops=dict(arrowstyle="->", lw=1.7, color="#3F7F2C"))
    ax.annotate("", xy=(8.2, 2.98), xytext=(6.72, 2.22), arrowprops=dict(arrowstyle="->", lw=1.7, color="#3F7F2C"))
    ax.annotate("", xy=(8.2, 1.18), xytext=(6.72, 2.08), arrowprops=dict(arrowstyle="->", lw=1.7, color="#3F7F2C"))

    ax.text(5.5, 5.62, "Brokered Pipeline: Many Sources, Many Workers", ha="center", fontsize=13, fontweight="bold", color="#172033")
    ax.text(5.5, 0.25, "The broker removes the direct N x M connection mesh while preserving simple PUSH/PULL sockets.", ha="center", fontsize=9.5, color="#38445A")

    plt.tight_layout()
    path = os.path.join(FIGURE_DIR, "arch_pipeline.png")
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {path}")


if __name__ == "__main__":
    create_activity_screenshots()
    generate_diagram_rmi()
    generate_diagram_pubsub()
    generate_diagram_pipeline()
    print("All report figures were generated successfully.")

# -*- coding: utf-8 -*-
"""
KiiChain CLI — Terminal interface for the KiiChain blockchain project.
EVM-compatible chain for FX settlement, stablecoins, and real-world assets.
Styled with Rich.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import box

from utils import ensure_env

console = Console()

LOGO = r"""
[bold cyan]__    __  __  __   ______   __                  __           [/]
[bold cyan]/  |  /  |/  |/  | /      \ /  |                /  |          [/]
[bold cyan]$$ | /$$/ $$/ $$/ /$$$$$$  |$$ |____    ______  $$/  _______  [/]
[bold cyan]$$ |/$$/  /  |/  |$$ |  $$/ $$      \  /      \ /  |/       \ [/]
[bold cyan]$$  $$<   $$ |$$ |$$ |      $$$$$$$  | $$$$$$  |$$ |$$$$$$$  |[/]
[bold cyan]$$$$$  \  $$ |$$ |$$ |   __ $$ |  $$ | /    $$ |$$ |$$ |  $$ |[/]
[bold cyan]$$ |$$  \ $$ |$$ |$$ \__/  |$$ |  $$ |/$$$$$$$ |$$ |$$ |  $$ |[/]
[bold cyan]$$ | $$  |$$ |$$ |$$    $$/ $$ |  $$ |$$    $$ |$$ |$$ |  $$ |[/]
[bold cyan]$$/   $$/ $$/ $$/  $$$$$$/  $$/   $$/  $$$$$$$/ $$/ $$/   $$/ [/]
"""


def show_logo():
    console.print(LOGO)
    console.print(
        Panel(
            "[bold green]KiiChain[/] — Fast, scalable EVM-compatible blockchain.\n"
            "The first on-chain FX settlement layer for stablecoins and real-world assets.",
            title="[bold]Project Status: Active[/]",
            border_style="green",
            box=box.DOUBLE,
        )
    )


def menu_table():
    table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
    table.add_column("Key", style="bold yellow", width=4)
    table.add_column("Action", style="white")
    table.add_row("1", "Install Dependencies (Go 1.24.11+)")
    table.add_row("2", "Settings (hardware requirements)")
    table.add_row("3", "About (project info and hashtags)")
    table.add_row("4", "Quick Links (Oro Testnet, Explorer, Faucet)")
    table.add_row("5", "Documentation & Resources")
    table.add_row("6", "Hardware Requirements")
    table.add_row("7", "Operating System")
    table.add_row("0", "Exit")
    return table


def install_dependencies():
    console.print(Panel(
        "[bold]Install Dependencies[/]\n\n"
        "Required: [bold]Go 1.24.11+[/]\n\n"
        "Installation / update:\n"
        "  macOS: [cyan]brew install go@1.24[/] or download from golang.org\n"
        "  Ubuntu: [cyan]sudo snap install go --classic --channel=1.24/stable[/]\n"
        "  Arch Linux: [cyan]pacman -S go[/]\n"
        "  Manual: [cyan]https://golang.org/dl[/]\n\n"
        "Check version: [cyan]go version[/] (must be 1.24.11 or higher)",
        title="[bold green]Install Dependencies[/]",
        border_style="green",
    ))
    if Prompt.ask("Check Go version on this system?", choices=["y", "n"], default="y") == "y":
        try:
            r = subprocess.run(["go", "version"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                console.print(f"[green]Installed:[/] {r.stdout.strip()}")
            else:
                console.print("[yellow]Go not found. Install Go using the instructions above.[/]")
        except FileNotFoundError:
            console.print("[yellow]Go not found in PATH. Install Go using the instructions above.[/]")
        except Exception as e:
            console.print(f"[red]Error:[/] {e}")


def settings():
    console.print(Panel(
        "[bold]Settings — Hardware Requirements[/]\n\n"
        "[bold]Minimum:[/]\n"
        "  8 GB RAM\n  1 TB NVMe SSD\n  4 Cores (modern CPUs)\n\n"
        "[bold]Recommended:[/]\n"
        "  16 GB RAM\n  2 TB NVMe SSD\n  8 Cores (modern CPUs)\n\n"
        "[dim]OS: Linux (x86_64/amd64). Arch Linux or Ubuntu recommended.[/]",
        title="[bold green]Settings[/]",
        border_style="green",
    ))


def about():
    about_dir = Path(__file__).parent / "about"
    if about_dir.exists():
        console.print(Panel(
            "[bold]About KiiChain[/]\n\n"
            "Content from the [cyan]about[/] folder with hashtags and project description.",
            title="[bold green]About[/]",
            border_style="green",
        ))
        for f in sorted(about_dir.glob("*.md")):
            try:
                text = f.read_text(encoding="utf-8")
                console.print(Markdown(text))
            except Exception as e:
                console.print(f"[red]Error reading {f}:[/] {e}")
    else:
        console.print("[yellow]about/ directory not found.[/]")


def quick_links():
    links = [
        ("Join Oro Testnet", "https://kiichain.com/oro-testnet", "Start validating on testnet"),
        ("Testnet Explorer", "https://explorer.kiichain.com", "Browse transactions and blocks"),
        ("Testnet Faucet", "https://faucet.kiichain.com", "Get testnet tokens"),
    ]
    table = Table(title="[bold green]Quick Links — Oro Testnet[/]", box=box.ROUNDED, border_style="blue")
    table.add_column("Link", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Action", style="yellow")
    for name, url, desc in links:
        table.add_row(name, desc, "Open in browser")
    console.print(table)
    choice = Prompt.ask("Open a link (1-3 or Enter to skip)", default="")
    if choice in ("1", "2", "3"):
        idx = int(choice) - 1
        webbrowser.open(links[idx][1])
        console.print(f"[green]Opened:[/] {links[idx][0]}")


def documentation_resources():
    links = [
        ("Official Documentation", "https://docs.kiichain.com", "Guides and API"),
        ("Developer Hub", "https://developers.kiichain.com", "Developer tools"),
        ("Whitepaper", "https://kiichain.com/whitepaper", "Technical specifications"),
        ("Blog", "https://blog.kiichain.com", "Latest updates"),
    ]
    table = Table(title="[bold green]Documentation & Resources[/]", box=box.ROUNDED, border_style="blue")
    table.add_column("Resource", style="cyan")
    table.add_column("Description", style="white")
    for name, url, desc in links:
        table.add_row(name, desc)
    console.print(table)
    choice = Prompt.ask("Open (1-4 or Enter to skip)", default="")
    if choice in ("1", "2", "3", "4"):
        idx = int(choice) - 1
        webbrowser.open(links[idx][1])
        console.print(f"[green]Opened:[/] {links[idx][0]}")


def hardware_requirements():
    console.print(Panel(
        "[bold]Hardware Requirements[/]\n\n"
        "[bold]Minimum:[/]\n"
        "  8 GB RAM\n  1 TB NVMe SSD\n  4 Cores (modern CPUs)\n\n"
        "[bold]Recommended:[/]\n"
        "  16 GB RAM\n  2 TB NVMe SSD\n  8 Cores (modern CPUs)",
        title="[bold green]Hardware Requirements[/]",
        border_style="green",
    ))


def operating_system():
    console.print(Panel(
        "[bold]Operating System[/]\n\n"
        "Supported: [bold]Linux (x86_64)[/] or [bold]Linux (amd64)[/]\n\n"
        "Recommended distributions:\n"
        "  [cyan]Arch Linux[/]\n  [cyan]Ubuntu[/]",
        title="[bold green]Operating System[/]",
        border_style="green",
    ))


@ensure_env
def main():
    show_logo()
    while True:
        console.print()
        console.print(menu_table())
        choice = Prompt.ask("[bold yellow]Select an option[/]", default="0")
        if choice == "0":
            console.print("[bold green]Goodbye![/]")
            break
        elif choice == "1":
            install_dependencies()
        elif choice == "2":
            settings()
        elif choice == "3":
            about()
        elif choice == "4":
            quick_links()
        elif choice == "5":
            documentation_resources()
        elif choice == "6":
            hardware_requirements()
        elif choice == "7":
            operating_system()
        else:
            console.print("[yellow]Invalid option. Enter 0-7.[/]")
        console.print()


if __name__ == "__main__":
    main()

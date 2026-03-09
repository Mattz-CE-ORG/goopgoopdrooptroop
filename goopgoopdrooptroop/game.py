"""Main game loop for GoopGoopDroopTroop."""

from __future__ import annotations

import random
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box

from .art import BANNER, get_art, IDLE_LINES
from .goop import Goop, Troop
from .missions import Mission, run_mission

console = Console()


def show_banner():
    console.print(Text(BANNER, style="bold green"))
    console.print(
        Panel(
            "[bold cyan]Command your goop soldiers. Send them on missions.\n"
            "Feed them. Train them. Watch them droop.[/bold cyan]\n\n"
            "[dim]Type a number to select an option. Type 'q' to quit.[/dim]",
            title="[bold yellow]~ Welcome to GoopGoopDroopTroop ~[/bold yellow]",
            border_style="green",
        )
    )


def show_troop_overview(troop: Troop):
    table = Table(
        title="🫠 Your Goop Troop",
        box=box.DOUBLE_EDGE,
        border_style="green",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="bold cyan", min_width=15)
    table.add_column("Lvl", justify="center", style="yellow")
    table.add_column("HP", justify="center")
    table.add_column("ATK", justify="center", style="red")
    table.add_column("DEF", justify="center", style="blue")
    table.add_column("Goop%", justify="center", style="green")
    table.add_column("Droop%", justify="center", style="magenta")
    table.add_column("Mood", justify="center")
    table.add_column("Power", justify="center", style="bold yellow")

    for i, g in enumerate(troop.goops):
        mood = g.mood
        mood_emoji = {
            "ecstatic": "🤩", "happy": "😊", "content": "😐",
            "droopy": "😢", "miserable": "😭", "dead": "💀",
        }.get(mood, "❓")

        hp_color = "green" if g.hp > g.max_hp * 0.5 else "yellow" if g.hp > g.max_hp * 0.25 else "red"

        table.add_row(
            str(i + 1),
            g.name if g.alive else f"[strike]{g.name}[/strike]",
            str(g.level),
            f"[{hp_color}]{g.hp}/{g.max_hp}[/{hp_color}]",
            str(g.attack),
            str(g.defense),
            str(g.goopiness),
            str(g.droopiness),
            f"{mood_emoji} {mood}",
            str(g.power) if g.alive else "---",
        )

    console.print(table)
    console.print(
        f"  [bold yellow]GoopBucks:[/bold yellow] {troop.goop_bucks}  "
        f"[bold magenta]Reputation:[/bold magenta] {troop.reputation}  "
        f"[bold cyan]Missions:[/bold cyan] {troop.total_missions}  "
        f"[bold green]Troop Power:[/bold green] {troop.troop_power}"
    )
    console.print()


def show_goop_detail(goop: Goop):
    art = get_art(goop.mood)
    info = (
        f"[bold cyan]{goop.name}[/bold cyan] "
        f"(Lvl {goop.level}, XP: {goop.xp}/{goop.level * 25})\n\n"
        f"HP: {goop.hp}/{goop.max_hp}  ATK: {goop.attack}  DEF: {goop.defense}\n"
        f"Goopiness: {goop.goopiness}  Droopiness: {goop.droopiness}\n"
        f"Hunger: {goop.hunger}/100  Morale: {goop.morale}/100\n"
        f"Mood: {goop.mood}  Power: {goop.power}\n"
        f"Missions: {goop.missions_completed}  Kills: {goop.kills}\n"
        f"Status: {'🟢 Alive' if goop.alive else '💀 Deceased'}"
    )
    panels = [
        Panel(art, title="Portrait", border_style="green", width=30),
        Panel(info, title="Stats", border_style="cyan", width=50),
    ]
    console.print(Columns(panels))


def select_squad(troop: Troop) -> list[Goop] | None:
    alive = troop.alive_goops
    if not alive:
        console.print("[red]No living goops to send on a mission![/red]")
        return None

    console.print("[bold]Select goops for the mission (comma-separated numbers, or 'all'):[/bold]")
    for i, g in enumerate(alive):
        console.print(f"  [{i + 1}] {g.name} (Lvl {g.level}, Power {g.power})")

    choice = console.input("[bold yellow]Squad> [/bold yellow]").strip().lower()
    if choice == "all":
        return alive
    if choice in ("q", "back", "b"):
        return None

    try:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        squad = [alive[i] for i in indices if 0 <= i < len(alive)]
        if not squad:
            console.print("[red]No valid goops selected![/red]")
            return None
        return squad
    except (ValueError, IndexError):
        console.print("[red]Invalid selection![/red]")
        return None


def main_menu(troop: Troop) -> str:
    console.print(Panel(
        "[1] 📋 View Troop\n"
        "[2] 🫠 Inspect a Goop\n"
        "[3] 🍖 Feed a Goop\n"
        "[4] 💪 Train a Goop\n"
        "[5] 😴 Rest a Goop\n"
        "[6] ⚔️  Go on a Mission\n"
        "[7] 🆕 Recruit a Goop\n"
        "[8] 🎲 Random Event\n"
        "[9] 💾 Save & Quit",
        title="[bold green]~ Command Center ~[/bold green]",
        border_style="green",
    ))
    return console.input("[bold yellow]Command> [/bold yellow]").strip()


def pick_goop(troop: Troop, action: str) -> Goop | None:
    alive = troop.alive_goops
    if not alive:
        console.print("[red]No living goops![/red]")
        return None
    console.print(f"[bold]Select a goop to {action}:[/bold]")
    for i, g in enumerate(alive):
        console.print(f"  [{i + 1}] {g.name}")
    choice = console.input("[bold yellow]Goop #> [/bold yellow]").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(alive):
            return alive[idx]
    except ValueError:
        pass
    console.print("[red]Invalid choice![/red]")
    return None


def random_event(troop: Troop):
    events = [
        ("goop_rain", "☔ A goop rain falls! All goops gain goopiness!"),
        ("tax", "💰 The Goop Tax Collector arrives! -15 GoopBucks."),
        ("gift", "🎁 A mysterious blob leaves a gift! +30 GoopBucks!"),
        ("droop_wave", "😢 A droop wave hits! All goops get droopier."),
        ("morale_boost", "🎉 A traveling goop bard sings! Morale boost!"),
        ("wild_goop", "🫠 A wild goop appears and wants to join!"),
        ("earthquake", "🌋 A slime quake! Some goops take damage!"),
        ("feast", "🍖 You find a cache of goop food! Hunger reduced!"),
    ]
    event_id, message = random.choice(events)
    console.print(Panel(message, title="[bold magenta]~ Random Event ~[/bold magenta]", border_style="magenta"))

    if event_id == "goop_rain":
        for g in troop.alive_goops:
            g.goopiness = min(100, g.goopiness + random.randint(3, 10))
    elif event_id == "tax":
        troop.goop_bucks = max(0, troop.goop_bucks - 15)
    elif event_id == "gift":
        troop.goop_bucks += 30
    elif event_id == "droop_wave":
        for g in troop.alive_goops:
            g.droopiness = min(100, g.droopiness + random.randint(5, 15))
            g.morale = max(0, g.morale - random.randint(3, 8))
    elif event_id == "morale_boost":
        for g in troop.alive_goops:
            g.morale = min(100, g.morale + random.randint(10, 20))
    elif event_id == "wild_goop":
        if len(troop.goops) < 10:
            wild = Goop(
                name=f"Wild {random.choice(['Splorp', 'Gloob', 'Drizzbert', 'Oozwald'])}",
                level=random.randint(1, 3),
                attack=random.randint(8, 18),
                defense=random.randint(3, 12),
                goopiness=random.randint(50, 90),
            )
            troop.goops.append(wild)
            console.print(f"  [green]{wild.name} joined your troop![/green]")
        else:
            console.print("  [yellow]Your troop is full! The wild goop wanders off sadly.[/yellow]")
    elif event_id == "earthquake":
        for g in troop.alive_goops:
            if random.random() < 0.5:
                dmg = random.randint(5, 15)
                g.take_damage(dmg)
    elif event_id == "feast":
        for g in troop.alive_goops:
            g.hunger = max(0, g.hunger - random.randint(15, 30))


def run_game():
    show_banner()
    troop = Troop.load()

    if not troop.goops:
        console.print("\n[bold yellow]Your troop is empty! Let's recruit your first goop![/bold yellow]")
        name = console.input("[bold cyan]Name your first goop (or press Enter for random): [/bold cyan]").strip()
        goop = troop.recruit(name if name else None)
        console.print(f"\n[bold green]Welcome, {goop.name}![/bold green]")
        show_goop_detail(goop)
        troop.save()

    while True:
        console.print()
        idle = random.choice(IDLE_LINES)
        console.print(f"[dim italic]{idle}[/dim italic]\n")

        troop.tick_all()
        choice = main_menu(troop)

        if choice == "1":
            show_troop_overview(troop)

        elif choice == "2":
            goop = pick_goop(troop, "inspect")
            if goop:
                show_goop_detail(goop)

        elif choice == "3":
            goop = pick_goop(troop, "feed")
            if goop:
                result = goop.feed()
                console.print(f"[green]{result}[/green]")

        elif choice == "4":
            goop = pick_goop(troop, "train")
            if goop:
                result = goop.train()
                console.print(f"[cyan]{result}[/cyan]")

        elif choice == "5":
            goop = pick_goop(troop, "rest")
            if goop:
                result = goop.rest()
                console.print(f"[blue]{result}[/blue]")

        elif choice == "6":
            if not troop.alive_goops:
                console.print("[red]No living goops! Recruit or revive first.[/red]")
                continue
            mission = Mission.generate(troop.troop_power)
            console.print(Panel(
                f"[bold]{mission.name}[/bold]\n\n"
                f"{mission.description}\n\n"
                f"Difficulty: {'💀' * mission.difficulty}\n"
                f"Reward: {mission.reward_bucks} GoopBucks, {mission.reward_xp} XP\n"
                f"Reputation: +{mission.reputation_gain}",
                title="[bold red]~ Mission Available ~[/bold red]",
                border_style="red",
            ))
            accept = console.input("[bold]Accept mission? (y/n): [/bold]").strip().lower()
            if accept in ("y", "yes"):
                squad = select_squad(troop)
                if squad:
                    won, log = run_mission(troop, squad, mission)
                    color = "green" if won else "red"
                    console.print(Panel(
                        "\n".join(log),
                        title=f"[bold {color}]~ Mission Report ~[/bold {color}]",
                        border_style=color,
                    ))

        elif choice == "7":
            cost = 20 + len(troop.goops) * 10
            console.print(f"[yellow]Recruitment costs {cost} GoopBucks. You have {troop.goop_bucks}.[/yellow]")
            if troop.goop_bucks >= cost:
                name = console.input("[bold cyan]Name (Enter for random): [/bold cyan]").strip()
                try:
                    goop = troop.recruit(name if name else None)
                    console.print(f"\n[bold green]{goop.name} has joined the troop![/bold green]")
                    show_goop_detail(goop)
                except ValueError as e:
                    console.print(f"[red]{e}[/red]")
            else:
                console.print("[red]Not enough GoopBucks![/red]")

        elif choice == "8":
            random_event(troop)

        elif choice in ("9", "q", "quit", "exit"):
            troop.save()
            console.print("[bold green]Troop saved! Your goops will wait for you... droopily.[/bold green]")
            console.print("[dim]Goodbye, Commander. 🫡[/dim]")
            break

        else:
            console.print("[red]Unknown command! Try a number 1-9.[/red]")

        troop.save()

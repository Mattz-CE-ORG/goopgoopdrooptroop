# 🫠 GoopGoopDroopTroop

> *Command your goop soldiers. Send them on missions. Feed them. Train them. Watch them droop.*

A terminal-based tamagotchi squad manager where you recruit, train, and command a troop of ASCII goop creatures on increasingly absurd missions.

```
   ██████╗  ██████╗  ██████╗ ██████╗  ██████╗  ██████╗  ██████╗ ██████╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗
  ██║  ███╗██║   ██║██║   ██║██████╔╝██║  ███╗██║   ██║██║   ██║██████╔╝
  ██║   ██║██║   ██║██║   ██║██╔═══╝ ██║   ██║██║   ██║██║   ██║██╔═══╝
  ╚██████╔╝╚██████╔╝╚██████╔╝██║     ╚██████╔╝╚██████╔╝╚██████╔╝██║
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝
```

## Features

- **Recruit** goop soldiers with randomly generated names like *Splorington* or *Dribblezilla*
- **Train** your goops in attack, defense, and raw goopiness
- **Feed** them or watch their morale (and body mass) deteriorate
- **Send them on missions** to places like *The Sludge Pits of Despair* and *Operation: Maximum Goop*
- **Random events** keep things spicy - goop rain, tax collectors, wild goops joining your squad
- **Persistent saves** - your troop remembers you (and their grudges)
- **ASCII art** mood-based portraits for every goop

## Install

```bash
pip install .
# or
uv pip install .
```

## Run

```bash
goopgoopdrooptroop
# or the shorter alias
ggdt
# or
python -m goopgoopdrooptroop
```

## Stats

Each goop has:
- **HP** - health, obviously
- **ATK / DEF** - combat stats
- **Goopiness** - how goop they are (higher = better)
- **Droopiness** - how droop they are (lower = better)
- **Hunger** - feed your goops or they get sad
- **Morale** - the vibe. droopy goops fight poorly

## Save Data

Saved to `~/.goopgoopdrooptroop/troop.json`. Delete to start fresh.

## License

WTFPL - Do What The F*** You Want To Public License

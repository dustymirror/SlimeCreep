# SlimeCreep
Slime Creep - A triple- duo channel chaotic CV generator for EuroPi, inspired by NLC Sloth.

![Version](https://img.shields.io/badge/version-1.11-blue)
![EuroPi](https://img.shields.io/badge/EuroPi-compatible-green)

## Features

- Three independent chaos generators: **Creep**, **Ooze**, **Smear**
- 6 CV outputs (X/Y per channel), 0–10V range
- Speed control per channel (0.3–10x)
- Depth control per channel (0.05–2.0)
- External CV coupling via Ain input
- DIN trigger input for chaos perturbation
- OLED display with real-time trajectory visualization
- 5-second boot animation (snail crawling with `;@-` / `;@ ~`)

## Installation

1. Connect your EuroPi to your computer via USB
2. Copy `slime_creep.py` to the EuroPi contrib 
3. add ["Slime Creep", "contrib.slime_creep.SlimeCreep"], to the menu.py

## Controls

| Control | Function                |
|---------|-------------------------|
| K1      | Adjust Speed (0.3–10.0) |
| K2      | Adjust Depth (0.05–2.0) |
| B1      | Previous creeper        |
| B2      | Next creeper            |
| B1+B2   | Back to sys menu        |
| DIN     | Perturb all channels    |
| AIN     | Coupling strength in    |

## Output Mapping

| Channel | X Output | Y Output |
|---------|----------|----------|
| Creep   | CV1      | CV4      |
| Ooze    | CV2      | CV5      |
| Smear   | CV3      | CV6      |

## Display

┌─────────────────────────────┐
│Creep                        │  ← Currently selected creeper
│                             │
│  [X Trace]                  │  ← Current creeper X trajectory
│  [Y Trace]                  │  ← Current creeper Y Trajectory 
│                             │
│X2.5   D0.78   D.  A=        │  ← Current creeper Status
└─────────────────────────────┘

Bottom Status Bar Description:
X2.5           Speed value for the current creeper (0.3–10.0)    X0.3 (slowest) – X10.0 (fastest)
D0.78          Depth value for the current creeper (0.05–2.0)    D0.05 (shallow) – D2.00 (deep)
D. or D*       Disturbance indicator: D* indicates a recent DIN trigger (flashing)    D* is displayed for approximately 0.5 seconds after triggering
A= A- A# A@    Ain coupling strength indicator: _ → - → = → # → @ represents 0%–100% The higher the external CV, the denser the symbols

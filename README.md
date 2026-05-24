# SlimeCreep
Slime Creep - A triple- duo channel chaotic CV generator for EuroPi, inspired by NLC Sloth.

![Version](https://img.shields.io/badge/version-1.11-blue)
![EuroPi](https://img.shields.io/badge/EuroPi-compatible-green)

<img width="461" height="517" alt="截屏2026-05-24 12 03 48" src="https://github.com/user-attachments/assets/4aa9f9cb-5166-4998-93bd-b85f34a6611a" />



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
| AIN     | Coupling strength       |

## Output Mapping

| Channel | X Output | Y Output |
|---------|----------|----------|
| Creep   | CV1      | CV4      |
| Ooze    | CV2      | CV5      |
| Smear   | CV3      | CV6      |

## Bottom Status Bar Description:

X:Speed value for the current creeper (0.3–10.0)

D:Depth value for the current creeper (0.05–2.0)

D. or D* Disturbance indicator: 
D* indicates a recent DIN trigger (flashing)

A= A- A# A@  Ain coupling strength indicator:
_ → - → = → # → @ represents 0%–100% The higher the external CV

Enjoy the sludge...... 🐌

<img width="595" height="455" alt="截屏2026-05-24 12 04 03" src="https://github.com/user-attachments/assets/3e45c6ce-dc3b-440a-933f-b35a159c51f6" />

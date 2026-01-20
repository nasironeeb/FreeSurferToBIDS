# FreeSurfer to BIDS Converter

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
[![Pylint](https://github.com/nasironeeb/FreeSurferToBIDS/actions/workflows/pylint.yml/badge.svg)](https://github.com/nasironeeb/FreeSurferToBIDS/actions/workflows/pylint.yml)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/alexf/FreeSurferToBIDS/issues)


---

## 🧠 Overview

This module provides a lightweight Python utility to **convert FreeSurfer output directories** into a **BIDS-compatible structure **.  
It reorganizes nested FreeSurfer data, verifies integrity through size checks, and supports both dry-run and move/copy modes.

This tool helps researchers working with FreeSurfer outputs standardize their data within a consistent **BIDS derivatives** hierarchy such as:

```txt
derivatives/
├── freesurfer_v7.1.1/
│    ├── sub-00001/
│    │      ├── ses-001/
│    │      │    ├── channels.txt
│    │      │    ├── label/
│    │      │    ├── mri/
│    │      │    ├── scripts/
│    │      │    ├── stats/
│    │      │    ├── surf/
│    │      │    ├── tmp/
│    │      │    ├── touch/
│    │      │    ├── trash/
│    │      │    ├── xhemi/
│    │      │    └── xhemi-textures.npy
│    │      ├── ses-002/
│    │      └── ses-003/
│    ├── sub-00002/
│    └── sub-00003/
```

---

## ⚙️ Installation

### Requirements
- Python **3.8+**
- Standard library modules only:
  - `logging`
  - `pathlib`
  - `shutil`

No external dependencies are required.

### Clone this repository

```bash
git clone https://github.com/nasirone/FreeSurferToBIDS.git
cd FreeSurferToBIDS
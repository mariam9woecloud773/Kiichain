# Kiichain
KiiChain CLI — Terminal interface for KiiChain EVM-compatible blockchain with faucet claims, token transfers, smart contract deployment, staking operations, cross-chain FX settlement for stablecoins and RWA, validator management, and Rich-styled command menu
<div align="center">

```
 __    __  __  __   ______   __                  __           
/  |  /  |/  |/  | /      \ /  |                /  |          
$$ | /$$/ $$/ $$/ /$$$$$$  |$$ |____    ______  $$/  _______   
$$ |/$$/  /  |/  |$$ |  $$/ $$      \  /      \ /  |/       \ 
$$  $$<   $$ |$$ |$$ |      $$$$$$$  | $$$$$$  |$$ |$$$$$$$  |
$$$$$  \  $$ |$$ |$$ |   __ $$ |  $$ | /    $$ |$$ |$$ |  $$ |
$$ |$$  \ $$ |$$ |$$ \__/  |$$ |  $$ |/$$$$$$$ |$$ |$$ |  $$ |
$$ | $$  |$$ |$$ |$$    $$/ $$ |  $$ |$$    $$ |$$ |$$ |  $$ |
$$/   $$/ $$/ $$/  $$$$$$/  $$/   $$/  $$$$$$$/ $$/ $$/   $$/ 
```

# KiiChain CLI

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![KiiChain](https://img.shields.io/badge/KiiChain-Blockchain-00D4AA?style=for-the-badge)](https://kiichain.io)
[![EVM](https://img.shields.io/badge/EVM-Compatible-627EEA?style=for-the-badge&logo=ethereum&logoColor=white)](https://ethereum.org)
[![Rich](https://img.shields.io/badge/Rich-CLI-5C87C2?style=for-the-badge)](https://github.com/Textualize/rich)

**Terminal CLI for KiiChain — fast, scalable EVM-compatible blockchain and first on-chain FX settlement layer for stablecoins and RWA.**

[Features](#features) • [Getting Started](#getting-started) • [Configuration](#configuration) • [Usage](#usage) • [Project Structure](#project-structure) • [FAQ](#faq)

</div>

---

## Official Links

| Resource | URL |
|----------|-----|
| **KiiChain** | https://kiichain.io |
| **Documentation** | https://docs.kiiglobal.io |
| **KiiChain Overview** | https://docs.kiiglobal.io/docs/learn/kiichain |
| **Whitepaper** | https://docs.kiiglobal.io/docs/learn/kiichain/whitepaper |
| **Testnet Explorer** | https://explorer.kiichain.io |
| **Testnet Faucet** | https://explorer.kiichain.io/faucet |
| **Testnet Faucet (Docs)** | https://docs.kiiglobal.io/docs/build-on-kiichain/developer-tools/testnet-faucet |
| **GitHub** | https://github.com/KiiChain/kiichain |

---

## Features

<table>
<tr>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Install Dependencies (Go 1.24.11+) | ✓ |
| Settings & hardware requirements | ✓ |
| About KiiChain & hashtags | ✓ |
| Quick Links (Oro Testnet, Explorer, Faucet) | ✓ |
| Documentation & Resources | ✓ |
| Hardware requirements guide | ✓ |

</td>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Operating system support info | ✓ |
| Rich terminal UI (panels, tables) | ✓ |
| Open links in browser | ✓ |
| Go version check | ✓ |
| Markdown rendering (about/) | ✓ |
| Interactive CLI menu | ✓ |

</td>
</tr>
</table>

---

## Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **pip** (Python package manager)

### Installation

```bash
# Clone or download the project
git clone <repository-url>
cd Kiichain

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python main.py
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Rich terminal UI, panels, tables, Markdown |

---

## Configuration

The CLI reads content from the `about/` folder. Customize displayed information by editing the Markdown files:

**`about/project.md`** — KiiChain overview and features:

```markdown
# KiiChain — About

**KiiChain** — fast, scalable blockchain on CometBFT, EVM-compatible.
First on-chain FX settlement layer for stablecoins and RWA.

## Features
- 100% EVM Compatible — Solidity, full EVM infrastructure
- High performance — up to 12,000 TPS, ~1 sec block time
- Interoperability — 100+ blockchain ecosystems
- Custom modules — Oracle, Gas Abstraction, Token Factory
```

**`about/testnet.md`** — Oro Testnet links:

```markdown
# Oro Testnet

- Join Oro Testnet — start validation
- Testnet Explorer — view transactions and blocks
- Testnet Faucet — get test tokens
```

**`about/tech.md`** — Hardware and OS requirements:

```markdown
# Technical Requirements

**Dependencies:** Go 1.24.11+
**OS:** Linux (x86_64/amd64). Arch Linux or Ubuntu recommended.
**Minimum:** 8 GB RAM, 1 TB NVMe SSD, 4 cores
**Recommended:** 16 GB RAM, 2 TB NVMe SSD, 8 cores
```

---

## Usage

Run the main application:

```bash
python main.py
```

### CLI Menu

```
╭──────────────────────────────────────────────────────────────────╮
│                    KiiChain CLI — Main Menu                       │
├────┬─────────────────────────────────────────────────────────────┤
│  1 │ Install Dependencies (Go 1.24.11+)                         │
│  2 │ Settings (hardware requirements)                            │
│  3 │ About (project info & hashtags from about/)                  │
│  4 │ Quick Links (Oro Testnet, Explorer, Faucet)                  │
│  5 │ Documentation & Resources                                    │
│  6 │ Hardware Requirements                                        │
│  7 │ Operating System                                             │
│  0 │ Exit                                                         │
╰────┴─────────────────────────────────────────────────────────────╯

Select option [0]:
```

**Typical workflow:**

1. **Install Dependencies** → Verify Go 1.24.11+ for validator setup
2. **Settings** → Check hardware (8–16 GB RAM, 1–2 TB NVMe, 4–8 cores)
3. **Quick Links** → Join Oro Testnet, open Explorer or Faucet
4. **Documentation** → Access official docs, whitepaper, developer hub

---

## Project Structure

```
Kiichain/
├── main.py              # Entry point, Rich CLI, menu logic
├── requirements.txt     # Python dependencies (rich)
├── README.md            # This file
├── README_CLI.md        # Original CLI description (Russian)
├── tags.txt             # GitHub topics
└── about/
    ├── project.md       # KiiChain overview, features, hashtags
    ├── resources.md     # Documentation, whitepaper, developer hub
    ├── tech.md          # Go, OS, hardware requirements
    └── testnet.md       # Oro Testnet, explorer, faucet
```

---

## FAQ

<details>
<summary><b>What is KiiChain?</b></summary>

KiiChain is a fast, scalable blockchain built on CometBFT with 100% EVM compatibility. It is the first on-chain FX settlement layer for stablecoins and real-world assets (RWA). Key features: up to 12,000 TPS, ~1 second block time, interoperability with 100+ blockchain ecosystems, and custom modules for Oracle, Gas Abstraction, Token Factory, and RWA/DeFi applications.
</details>

<details>
<summary><b>What is Oro Testnet?</b></summary>

Oro Testnet is KiiChain's test network (chain ID: `oro_1336-1`) for validation and development. You can join as a validator, use the Testnet Explorer to view blocks and transactions, and obtain test KII tokens via the Explorer Faucet or Discord commands (`$request`, `$balance`, `$faucet_status`).
</details>

<details>
<summary><b>What does this CLI do?</b></summary>

This is a terminal helper for KiiChain. It provides setup instructions (Go, hardware, OS), quick links to official resources (Explorer, Faucet, docs), and displays project information from the `about/` folder. It does not run a node or validator — it guides you through the setup process.
</details>

<details>
<summary><b>What are the hardware requirements for running a KiiChain node?</b></summary>

**Minimum:** 8 GB RAM, 1 TB NVMe SSD, 4 CPU cores. **Recommended:** 16 GB RAM, 2 TB NVMe SSD, 8 CPU cores. Supported OS: Linux (x86_64/amd64). Recommended distros: Arch Linux, Ubuntu.
</details>

<details>
<summary><b>Which Go version is required?</b></summary>

Go 1.24.11 or higher. Install via: macOS `brew install go@1.24`, Ubuntu `snap install go --classic --channel=1.24/stable`, Arch `pacman -S go`, or download from golang.org/dl. Use `go version` to verify.
</details>

<details>
<summary><b>How do I get testnet tokens?</b></summary>

Use the Explorer Faucet at https://explorer.kiichain.io/faucet (connect MetaMask or Keplr to Testnet Oro first), or request via Discord: `$request {your_address}`. Tokens can be requested every 24 hours.
</details>

<details>
<summary><b>Is this official KiiChain software?</b></summary>

No. This is an independent, community-built CLI tool for KiiChain. It is not affiliated with KiiChain, Kii Global, or the official KiiChain team. Use at your own risk.
</details>

---

## Disclaimer

This software is provided for **educational and testnet purposes** only. It is a helper CLI for accessing KiiChain resources and setup guides. The authors assume no liability for any damages, lost funds, or violations of KiiChain's terms. Always verify information on official documentation and use responsibly.

---

<div align="center">

**Support development**

ETH: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1`

If this project helped you, consider giving it a ⭐

</div>

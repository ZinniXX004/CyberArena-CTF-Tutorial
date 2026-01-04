# 🚩 Cyber Arena: CTF & Attack-Defense Game

![Rust](https://img.shields.io/badge/Rust-server-orange)
![Python](https://img.shields.io/badge/Python-exploits-blue)
![C](https://img.shields.io/badge/C-binary-00599C)
![C#](https://img.shields.io/badge/C%23-GUI-green)
![C++](https://img.shields.io/badge/C++-Hybrid-blueviolet)
![License](https://img.shields.io/badge/License-Educational-green)

**Cyber Arena** is a hands-on cybersecurity simulation designed to teach the fundamentals of **Capture The Flag (CTF)** competitions and **Attack & Defense** mechanics.

It features a custom high-performance **Scoreboard Server** (Rust), **Binary Exploitation** challenges (C), **Web Application** vulnerabilities (Python/Flask), and modern **Interactive Dashboards**.

---

## 📂 Project Structure

```text
/
├── engine/           # The Game Server (Rust + Axum)
├── clients/          # Interactive Dashboards [NEW]
│   ├── gui-win/      # Modern Admin Console (C# WPF)
│   └── cli-unix/     # Hybrid Terminal Client (Rust + C++)
├── challenges/       # Vulnerable source code
│   ├── 01-binary-pwn # Buffer Overflow Challenge (C)
│   └── 02-web-sqli   # SQL Injection Challenge (Python)
├── solutions/        # Automated exploit scripts (Python)
└── scripts/          # Build tools and Game Launchers
```

## 🛠️ Prerequisites

Before running the simulation, ensure you have the following installed:

*   **Rust**: [Install Rust](https://www.rust-lang.org/tools/install)
*   **Python 3**: [Install Python](https://www.python.org/downloads/)
*   **.NET SDK 6.0+**: [Install .NET](https://dotnet.microsoft.com/en-us/download) (Required for Windows GUI)
*   **GCC Compiler**:
    *   **Windows**: Install [MinGW-w64](https://www.mingw-w64.org/) or [w64devkit](https://github.com/skeeto/w64devkit). *Make sure to add it to your PATH.*
    *   **Linux/Mac**: Run `sudo apt install base-devel`

---

## 🚀 How to Play

### 1. Build the Environment
We provide automated scripts to compile the C binaries, patch the vulnerabilities, and install Python dependencies.

**Windows:**
```cmd
cd scripts
build_challenge.bat
```

**Linux/Mac:**
```bash
cd scripts
chmod +x build_challenge.sh
./build_challenge.sh
```

### 2. Start the Game Engine
This script launches the Rust Scoreboard, the Vulnerable Web App, and a Simulation Bot (Game Admin) that generates traffic.

> **Note:** This will open new terminal windows for the Server and Web App. **Keep them open!**

**Windows:**
```cmd
cd scripts
start_game.bat
```

**Linux/Mac:**
```bash
cd scripts
chmod +x start_game.sh
./start_game.sh
```

### 3. Visualization (Interactive Clients)
Instead of looking at raw server logs, you can run a dedicated dashboard to monitor the game.

**Option A: Windows GUI (C# WPF)**
A modern, "Hacker-themed" graphical dashboard.
```cmd
cd clients/gui-win/CyberAdmin
dotnet run
```

**Option B: Hybrid CLI (Rust + C++)**
A terminal-based interface powered by a custom Rust library linked into C++.
*   **Windows Build:** Run `clients/cli-unix/build_win.bat` -> Run `cyber_term.exe`
*   **Linux Build:** Run `clients/cli-unix/build_linux.sh` -> Run `./cyber_term`

### 4. Run the Exploits (The "Hacker" Mode)
Now that everything is running, open a **new** terminal and run the solution scripts to attack the challenges and capture flags.

#### Phase 1: Binary Exploitation (Buffer Overflow)
This script detects your OS, finds the vault binary, brute-forces the memory offset, and submits the flag.

```bash
cd solutions
python exploit_vault.py
```

#### Phase 2: Web Exploitation (SQL Injection)
This script attacks the running Web App (`localhost:5000`), bypasses the login, steals the flag, and submits it.

```bash
cd solutions
python exploit_web.py
```

---

## 🏆 Scoring

Check the **CyberAdmin Dashboard** or the Server logs to see your live score!

| Challenge Type | Vulnerability | Points |
| :--- | :--- | :--- |
| **Binary** | Buffer Overflow | **300** |
| **Web** | SQL Injection | **500** |

---

## 🛡️ Important Note

This project is intended for **educational purposes only**. The authors are not responsible for any misuse of the techniques demonstrated in this repository.

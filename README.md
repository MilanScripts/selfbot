# MilanScripts Selfbot (Discord)

A custom Python based selfbot for Discord featuring fun commands, moderation utilities, and mocking features. Designed with extensibility and owner-only permissions in mind.

> ⚠️ **Disclaimer:** Selfbots are against Discord's Terms of Service. Use at your own risk. This project is for educational purposes only.

---

## Features

### 🎉 General Commands
- `!time` – Get the current time.
- `!ping` – Show bot latency.
- `!hello` – Friendly greeting.
- `!coinflip` / `!flip` – Flip a coin.
- `!roll [sides]` – Roll a dice (default: 6).
- `!joke` – Receive a random programmer joke.
- `!fact` – Fun trivia facts.
- `!catfact` / `!dogfact` – Random animal facts.
- `!advice` – Get a life tip.
- `!inspire` – Inspirational quotes.
- `!rps` – Rock, Paper, Scissors game.
- `!play` – Join your voice channel and play `sound.mp3`.

### 👑 Owner Commands
- `!addowner [user]` – Add an owner by mention, ID, or name.
- `!removeowner [user]` – Remove an owner.
- `!listowners` – View all owners.
- `!mock @user` – Repeat what a user says.
- `!stopmock [@user]` – Stop mocking a user (or all).
- `!listmocks` – List all mocked users.
- `!version` – Show current bot version.
- `!purge [amount]` – Delete recent bot messages.
- `!remove [message_id]` – Delete a message by ID.

---

## Getting Started

### ✅ Requirements
- Python 3.5.3+
- `discord.py` library (not maintained, use forks like `py-cord` or `nextcord` if needed)
- FFmpeg (must be installed and added to your system PATH)

### 📦 Installation
1. Clone this repo:
   ```bash
   git clone https://github.com/milanscripts/selfbot.git
   cd selfbot

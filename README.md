# 🔊 JoinToCreate – Discord Bot

A fully functional **Join to Create Voice Channel System** for Discord written in Python using `discord.py`.  
This bot allows users to automatically generate personal voice channels and manage them via an intuitive control panel.

---

## 📦 Features

- ➕ **Auto VC Creation** – Join the `➕ Create VC` channel to instantly generate a personal voice channel.
- 🎛️ **Interactive Control Panel** – Manage your VC with interactive buttons:
  - 🔒 Lock / 🔓 Unlock
  - 👁 Hide / 👁‍🗨 Unhide
  - 👥 Limit user count
  - ✏️ Rename channel
  - 👑 Transfer ownership
  - 🚫 Delete VC
- 🧠 **Ownership Tracking** – Only VC owners can use the controls.
- 🧹 **Auto Cleanup** – Voice channels are automatically deleted when empty.

---

## ⚙️ Setup Instructions

### 1. Requirements

- Python 3.8+
- `discord.py` 2.x

```bash
pip install -U discord.py

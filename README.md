# 🔊 JoinToCreate – Discord Bot
A fully functional Join to Create Voice Channel System for Discord written in Python using discord.py. This bot lets users create private temporary voice channels by joining a special VC and provides a user-friendly interface for managing those channels.

📦 Features
➕ Auto VC Creation – Join the ➕ Create VC channel to auto-generate a personal voice channel.

🎛️ Interactive Control Panel – Use buttons to manage VC:

🔒 Lock / 🔓 Unlock
👁 Hide / 👁‍🗨 Unhide 
👥 Limit user count
✏️ Rename channel 
👑 Transfer ownership
🚫 Delete the VC
🧠 Ownership Tracking – Only VC owners can use controls.
🧹 Auto Cleanup – Channels are deleted when empty.

⚙️ Setup Instructions
1. Requirements
Python 3.8+

discord.py (2.x)
bash
Copy
Edit
pip install -U discord.py
2. Configuration
Edit the bot token:

python
Copy
Edit
TOKEN = "YOURBOTTOKENS"  # Replace with your bot token
3. Running the Bot
Run the script:

bash
Copy
Edit
python bot.py
4. Set Up the System
Use the /setup command:

bash
Copy
Edit
/setup type: jtc
This will automatically create:

A category: Join to Create

A voice channel: ➕ Create VC

A text channel: 🍾・interface (contains control buttons)

📁 File Structure
bash
Copy
Edit
join_to_create/
│
├── bot.py               # Main bot file
├── README.md            # Project description
└── requirements.txt     # (Optional) Dependency list
💡 Example Use Case
A user joins ➕ Create VC.

Bot creates a personal VC for them.

User uses buttons in 🍾・interface to manage:
Rename VC to "Team RxDev"
Lock or limit it to 4 users
Hide/unhide as needed
When the VC is empty, it auto-deletes.

🔐 Permissions Required
Ensure the bot has the following permissions:

Manage Channels
Move Members
Manage Roles
Read/Send Messages
Use Application Commands (Slash commands)

🧠 Future Improvements
Persistent storage of VC ownership (via database or JSON)

Logging events
Custom channel name templates
Localization (multi-language support)

🤝 Credits
Developed by @notritik.exe
Iconic UI inspired by modern VC management systems.
Free for personal or educational use.

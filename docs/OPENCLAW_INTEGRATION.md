# OpenClaw Integration for BLADE-AI

Control your BLADE-AI application through natural language commands - either within the app's chatbot or from external apps like WhatsApp, Telegram, or Discord via OpenClaw.

## 🎯 What This Does

This integration adds **action execution** to the BLADE-AI chatbot, allowing you to:

- ✅ Remove packages by typing "Remove Facebook"
- ✅ Scan for bloatware with "Scan my phone"
- ✅ Get package analysis via "Analyze com.facebook.katana"
- ✅ Create backups by saying "Create backup"
- ✅ All with natural language - no clicking needed!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  Your Commands (Natural Language)          │
│  "Remove Facebook bloatware"                │
└───────────────┬─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│  In-App Chatbot OR OpenClaw (External)     │
└───────────────┬─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│  Command Parser (openclaw_integration.py)   │
│  • Intent Recognition                       │
│  • Entity Extraction                        │
│  • Safety Checks                            │
└───────────────┬─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│  Action Executor                            │
│  • Confirmation Dialog                      │
│  • ADB Operations                           │
│  • Result Feedback                          │
└───────────────┬─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│  Android Device (via ADB)                   │
└─────────────────────────────────────────────┘
```

## 🚀 Setup Options

### Option 1: In-App Chatbot (Already Integrated!)

The chatbot inside BLADE-AI now automatically detects and executes commands.

**No additional setup needed!** Just use the app's chatbot.

**Example commands:**
- "Remove all Facebook apps"
- "Scan for bloatware"
- "Create a backup first"
- "Analyze com.instagram.android"

### Option 2: External Control via OpenClaw

Control BLADE-AI from WhatsApp, Telegram, Discord, or any chat app via OpenClaw.

#### Prerequisites
- OpenClaw installed and running ([https://openclaw.ai](https://openclaw.ai))
- BLADE-AI application running
- Android device connected via ADB

#### Installation Steps

1. **Install OpenClaw** (if not already done):
   ```powershell
   iwr -useb https://openclaw.ai/install.ps1 | iex
   ```

2. **Copy the Skill**:
   ```powershell
   # The skill file is in: openclaw-skill/debloat-controller.py
   # Copy to OpenClaw's skills directory
   # (OpenClaw will show you where this is during setup)
   ```

3. **Connect Your Chat App**:
   - Follow OpenClaw docs to connect WhatsApp, Telegram, etc.
   - OpenClaw guides you through this during first run

4. **Start Using**:
   ```
   You (via WhatsApp): "Hey, scan my phone for bloatware"
   OpenClaw: 🔍 Scanning... Found 15 packages!
   
   You: "Remove Facebook"
   OpenClaw: ⚠️ Confirm removal of com.facebook.katana?
   
   You: "Yes, confirm"
   OpenClaw: ✅ Successfully removed!
   ```

## 📝 Supported Commands

### Scanning & Discovery
- "Scan my phone for bloatware"
- "Show all packages"
- "List system apps"
- "What bloatware is on my device?"

### Package Removal
- "Remove Facebook"
- "Uninstall Instagram"
- "Delete com.facebook.katana"
- "Get rid of all Facebook apps"

### Package Analysis
- "Analyze com.facebook.katana"
- "Is Facebook safe to remove?"
- "Tell me about com.instagram.android"

### Backup & Restore
- "Create a backup"
- "Create backup before removing anything"
- "Restore com.facebook.katana"

### Device Info
- "Show my device info"
- "What phone is connected?"
- "Check battery level"

## 🔒 Safety Features

### Automatic Confirmations
All destructive actions (uninstall, etc.) require confirmation:

```
You: Remove Facebook

Bot: ⚠️ Confirm Action
     Package: com.facebook.katana
     Action: Uninstall (3 packages)
     
     Packages:
     • com.facebook.katana
     • com.facebook.system
     • com.facebook.services
     
     [Cancel] [Confirm]
```

### Risk Assessment
The system automatically classifies packages:
- 🟢 **Safe**: Third-party apps, easy to reinstall
- 🟡 **Caution**: OEM apps, may affect features
- 🟠 **Expert**: System dependencies, advanced users only
- 🔴 **Dangerous**: Critical system components, don't remove!

### Backup Prompts
Before major operations, the bot can suggest creating backups.

## 🛠️ Technical Details

### Backend Components

**1. Command Parser** (`backend-python/openclaw_integration.py`)
- Uses regex patterns for intent recognition
- Extracts package names and entities
- Confidence scoring

**2. Action Executor**
- Safely executes ADB commands
- Manages confirmation workflows
- Returns structured results

**3. Main Backend** (`backend-python/main.py`)
- Added `parse_chat_command` endpoint
- Added `execute_action` endpoint
- Integrated with existing ADB operations

### Frontend Components

**1. Updated ChatBot** (`frontend/src/components/ChatBot.tsx`)
- Detects actionable messages
- Shows confirmation dialogs
- Displays action results

**2. API Layer** (`frontend/src/utils/api.ts`)
- `parseChatCommand()` - Analyze message intent
- `executeAction()` - Execute confirmed actions

**3. Electron IPC** (`electron/main.js`, `electron/preload.js`)
- New IPC handlers for OpenClaw integration
- Bridges frontend ↔ backend

## 📊 Command Flow Example

**User**: "Remove all Facebook apps"

1. **Parse** → Intent: `uninstall`, Entities: `{target: "facebook"}`
2. **Search** → Find matching packages: `com.facebook.*`
3. **Confirm** → Show dialog with 3 matching packages
4. **Execute** → Run `adb uninstall` for each package
5. **Result** → "✅ Removed 3/3 packages successfully"

## 🔧 Customization

### Add More Intents

Edit `backend-python/openclaw_integration.py`:

```python
self.intent_patterns = {
    'uninstall': [...],
    'scan': [...],
    # Add your own:
    'freeze': [
        r'\b(freeze|disable)\s+(.+)',
    ],
}
```

### Modify Safety Checks

```python
def _is_likely_bloatware(self, package_name: str) -> bool:
    bloatware_indicators = [
        'facebook', 'tiktok', 'instagram',
        # Add your patterns:
        'games', 'weather',
    ]
    ...
```

## 🐛 Troubleshooting

### Commands Not Being Executed

**Check:**
1. Backend logs - Look for parsing errors
2. Confidence score - May be too low (< 0.8)
3. Pattern matching - Package name format

**Fix:**
```python
# Increase confidence threshold or improve patterns
if match:
    return {'intent': intent, 'confidence': 0.9}  # Higher confidence
```

### Confirmation Not Showing

**Check:**
- `requires_confirmation` flag in executor
- Frontend state management (`pendingAction`)

### External OpenClaw Not Working

**Check:**
1. BLADE-AI app is running
2. Android device connected
3. OpenClaw skill installed correctly
4. IPC communication working

## 📚 Examples Gallery

### Basic Usage
```
User: Hey, what bloatware is on my phone?
Bot: 🔍 Found 15 packages [shows list]

User: Remove Facebook
Bot: ⚠️ Confirm: Remove 3 Facebook packages?
User: Yes
Bot: ✅ Removed successfully!
```

### Advanced Workflow
```
User: Create backup first
Bot: 💾 Backup created: backup_2026-02-20.json

User: Now scan for bloatware
Bot: 🔍 Found 20 packages...

User: Remove all social media apps
Bot: ⚠️ Found: Facebook, Instagram, TikTok, Snapchat
     Remove all 4?
User: Confirm
Bot: ✅ Removed 4/4 apps!
```

### Via WhatsApp (with OpenClaw)
```
WhatsApp → OpenClaw → BLADE-AI

You: "Remove bloatware from my Samsung"
Claw: *triggers BLADE-AI scan*
Claw: Found 18 Samsung bloatware apps
      Remove all? (yes/no)
You: yes
Claw: ✅ Done! Removed 18 apps.
```

## 🎓 Next Steps

1. **Try It** - Open the BLADE-AI chatbot and try commands
2. **Install OpenClaw** - For external control (optional)
3. **Customize** - Add your own command patterns
4. **Share** - Tell others about this integration!

## 📄 License

MIT License - Same as BLADE-AI

## 🤝 Contributing

Have ideas for new commands or improvements? Open an issue or PR!

---

**Made with ❤️ for the BLADE-AI community**

# Safety Interlock UI Method Documentation

## Purpose
The Safety Interlock UI Method is a defensive workflow that prevents accidental or unsafe device modifications when the user issues system-level commands via chat. It combines a global "Action Mode" gate with a per-command confirmation card inside the chat stream, ensuring that destructive actions are only executed after explicit user consent.

This document describes the exact flow in the current codebase, identifies the components involved, and outlines improvements that would make the method more robust and patent-ready.

## Core Idea (Design Summary)
A chat-based system administration interface intercepts destructive commands, performs independent verification, and presents a Pending Action Card that requires Action Mode to be enabled and a confirmation click before execution.

## Code Map (Where It Lives)
- UI and workflow state: [frontend/src/components/ChatBot.tsx](frontend/src/components/ChatBot.tsx)
- Command parsing and action staging: [backend-python/openclaw_integration.py](backend-python/openclaw_integration.py)
- AI safety analysis (per-package): [backend-python/ai_advisor.py](backend-python/ai_advisor.py)
- Backend command routing: [backend-python/main.py](backend-python/main.py)
- Safety mode documentation: [docs/ACTION_MODE_SAFETY.md](docs/ACTION_MODE_SAFETY.md)

## System Actors
- User: Enters chat instructions (e.g., "Remove Facebook")
- UI Client: React chat interface that maintains Action Mode state and pending actions
- Backend Service: Parses commands, collects targets, and executes ADB operations
- AI Advisor: Optional safety analysis service for packages

## End-to-End Workflow
1) User enters a command in the chat input.
2) The UI sends the message to the backend parse endpoint.
3) Backend parses the message and determines intent plus target packages.
4) Backend returns an action payload with `requires_confirmation` and package list.
5) UI stores the payload in `pendingAction` and displays the Pending Action Card.
6) UI requests an Action Mode token from backend (time-limited) when Action Mode is enabled.
7) UI optionally requests AI risk analysis for each package and displays risk badges.
8) If Action Mode is disabled or token is expired, the UI prevents execution.
9) When user confirms, the UI sends the action plus Action Mode token for execution.
10) Backend validates the token, executes the ADB operation, and logs the safety event.
11) UI clears the pending action and appends a result message.

## Detailed UI Behavior
### Action Mode Toggle
- Location: Header toggle in the chat window.
- Default: Off.
- When Off:
  - The system is read-only.
  - Commands can be parsed and explained but not executed.
- When On:
  - Actions can be executed, but only after explicit confirmation.
  - Backend issues a short-lived Action Mode token that must accompany execution.

Implementation detail:
- State is stored in `actionModeEnabled`.
- Preference is persisted in local storage (`chat_action_mode`).

### Pending Action Card
- Triggered when backend returns `requires_confirmation: true`.
- Displays:
  - Action summary message.
  - List of matched packages (limited in UI).
  - Risk badges per package when AI analysis is available.
  - Confirm / Cancel buttons.
- Confirm action requires explicit click.
- Cancel action clears the pending card.

Implementation detail:
- State is stored in `pendingAction`.
- Rendering happens in the "Input Area" section of ChatBot.

### Execution Guardrails
- UI blocks execution when Action Mode is disabled.
- UI clears pending actions when Action Mode is turned off.
- Backend rejects execution when Action Mode token is missing or expired.
- Dangerous actions require typing a confirmation phrase ("DELETE").

## Backend Behavior
### Command Parsing
- `CommandParser` uses regex rules to map natural language to intent.
- `ActionExecutor` handles each intent.
- `uninstall` intent returns `requires_confirmation: True`.

### Action Execution
- UI sends the confirmed action to backend.
- Backend executes via ADB and returns a success or error message.
- Backend logs each action (including risk levels and confirmation result).

## Data Contracts (Simplified)
### Parse Result
```
{
  "success": true,
  "action": "uninstall",
  "requires_confirmation": true,
  "data": {
    "packages": [
      { "packageName": "com.example.app" }
    ],
    "count": 1
  },
  "message": "Found 1 package(s) to remove. Confirm to proceed."
}
```

### Execution Request
```
{
  "command": "execute_action",
  "args": {
    "executionResult": { ...parseResult },
    "confirmed": true,
    "actionModeToken": "<token>",
    "confirmationPhrase": "DELETE"
  }
}
```

## Safety Log
Each confirmed or cancelled action is appended to a local JSON log file for auditability.
- Default location: `~/BladeAI/logs/action_safety_log.json`
- Logged fields: action, packages, risk levels, confirmation status, and result message

## What Makes This "Safety Interlock"
The interlock is a two-step requirement:
1) Global Action Mode must be enabled.
2) A per-action confirmation must be explicitly accepted.

An additional protective layer enforces a time-limited Action Mode token and a typed confirmation phrase for dangerous actions.

This prevents accidental or scripted command execution and requires user intent to be asserted twice in different contexts.

## Current Risk Verification Layer
The UI triggers AI analysis for each package in destructive actions and displays risk badges (Safe/Caution/Expert/Dangerous). If the AI analysis fails, a local safety level is used as fallback.

## Recommended Improvements (Patent-Strengthening)
These are additive and do not change the core behavior.

1) Add AI Risk Badges to the Pending Action Card
- After parsing, run AI analysis for each package or for the entire action.
- Display a `Safe/Caution/Dangerous` badge next to each package.
- This turns a generic "Are you sure?" into a context-aware safety dialog.

2) Add Risk-Based Confirmation Rules
- Example: If risk is Dangerous, require a second explicit confirmation or typed acknowledgement.
- This creates an adaptive, safety-weighted interlock.

3) Log and Explain Safety Decisions
- Add a short explanation on why the action is risky.
- Store the risk summary in a log entry alongside the action.

4) Tie Execution to the Action Mode State Token
- Generate a short-lived "Action Mode token" when user enables it.
- Require the token in the execution request.
- This hardens the system against stale or replayed confirmations.

## Suggested Patent-Oriented Claim (Aligned to Current Code)
"A method for preventing accidental system modification in a chat interface comprising: intercepting a command parsed from a user message; displaying a pending execution widget within the chat stream that includes a list of target software packages; disabling execution unless a global action mode toggle is enabled; and executing the command only after a user confirmation interaction within said widget."

## Suggested Patent-Oriented Claim (If You Add Risk Badges)
"A method for preventing accidental system modification in a chat interface comprising: intercepting a command parsed from a user message; obtaining a safety classification for each target software package; rendering a pending execution widget that visually encodes said safety classifications; disabling execution unless a global action mode toggle is enabled; and executing the command only after user confirmation."

## Verification Checklist
- Action Mode toggle present and stored in local storage
- Pending action card appears for destructive commands
- Execution blocked when Action Mode is off
- Confirmation required for each destructive action

## Notes
This document reflects the code as of February 25, 2026. If you change the flow or add risk badges, update the "Gaps" and "Improvements" sections accordingly.

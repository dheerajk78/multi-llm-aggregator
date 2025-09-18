# Minimal Viable Open-Source LLM Aggregator — Spec

## 1. Core Features
Feature	Description
  - User API Key Management (BYOK)	Users securely add API keys for multiple LLM providers (OpenAI, Anthropic, etc.). Keys are stored locally or encrypted. No server-side storage unless explicitly opted-in.
  - Unified Query Interface	User inputs prompt once, selects or auto-routes to provider(s), sees response(s) in a unified UI.
Cost & Usage Tracking	Show token usage and estimated cost per provider per request (using provider pricing info). Helps users optimize usage.
Provider Selection & Routing	Manual selection or simple rules (e.g., cheapest, fastest). No heavy orchestration initially.
History & Favorites	Save queries, mark favorites, and reload past prompts. Optional local storage.
Open Source & Self-Hosting Friendly	Runs in browser + lightweight backend (optional). Easily deployable locally or on personal cloud (e.g., Docker).
2. Security & Privacy
API keys stored only on user device or encrypted with a master password if backend is used.
No data sent to external servers without explicit user consent.
Open-source code so users can verify no key leakage or logging.
Clear warnings about risks of key sharing and best practices.
3. Tech Stack Suggestions
Layer	Technology Options
Frontend	React / Vue / Svelte (modern, user-friendly UI)
Local Storage & Encryption	IndexedDB + Crypto API / localForage / libsodium for encryption
Backend (Optional)	Node.js with Express or FastAPI (Python) — only if user opts-in for cloud syncing or multi-device support
Deployment	Docker for easy local/self-hosted setup
API Clients	Wrap official SDKs or direct REST calls to providers’ APIs
4. User Workflow
User opens app, adds API keys (OpenAI key, Anthropic key, etc.).
User enters prompt, selects provider(s) or chooses “auto-route”.
App sends request(s) to selected provider(s) using stored keys.
Results display side-by-side or merged.
Usage and cost info shown for transparency.
User saves favorites or query history locally.
User can export/import keys and history if desired.
5. Documentation & Best Practices
How to generate API keys for each provider.
Security guidelines for storing and handling keys.
How to monitor costs and set usage limits.
Disclaimer about usage policy compliance.
How to contribute to the project.

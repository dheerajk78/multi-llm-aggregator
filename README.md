# multi-llm-aggregator
Open-source app to manage and query multiple LLM providers with cost tracking and secure key storage.

# Multi-LLM Aggregator
An open-source app that lets you manage and query multiple large language model (LLM) providers — all from one simple interface.

## Why This Project?

Many AI developers and enthusiasts use multiple LLM providers (OpenAI, Anthropic, etc.) but struggle to manage API keys, optimize costs, and keep usage organized. This app empowers you to:

- Bring your own API keys (BYOK) and keep them secure  
- Query multiple LLMs without switching apps or interfaces  
- Track token usage and estimated costs for better budgeting  
- Save your query history and favorites locally  
- Self-host or run locally with full control over your data

## Features

- Simple UI for adding, viewing, and deleting API keys  
- Unified prompt interface with selectable LLM providers  
- Real-time token usage and cost estimation  
- Local encrypted storage of keys and history  
- Open-source and community-driven

## Getting Started

### Prerequisites

- Node.js 16+  
- API keys from your chosen LLM providers (OpenAI, Anthropic, etc.)

### Installation

```bash
git clone https://github.com/yourusername/multi-llm-aggregator.git
cd multi-llm-aggregator
yarn install
yarn start

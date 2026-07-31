# Autonomous Local Web Research Agent

An autonomous research assistant built in Python that takes a user query, searches the web, reads multiple websites, and uses a local Large Language Model (via LM Studio) to synthesize a comprehensive research report. It features both a Command-Line Interface (CLI) and a Telegram Bot interface.

## Features
* **Live Web Research**: Uses Tavily API to search the live web for relevant sources.
* **Deep Reading (Jina)**: Extracts and parses raw text from multiple URLs simultaneously.
* **Local LLM Summarization**: Processes the combined web context securely and locally using LM Studio.
* **Dual Interface**: Operate the agent from the terminal or deploy it as a Telegram Bot.
* **Database Tracking**: All tasks and generated markdown reports are saved to a local SQLite database (SQLModel).
* **Corporate SSL Bypass**: Native sledgehammer bypass for restrictive corporate firewalls and self-signed certificates.

## Architecture
* **Framework**: Python, `python-telegram-bot`
* **Database**: SQLite & SQLModel
* **LLM Provider**: LM Studio (Local)
* **Search/Scraping**: Tavily API, Jina AI

## Setup

1. **Prerequisites**
   * Python 3.10+
   * LM Studio running locally
   * A Telegram Bot Token from [@BotFather](https://t.me/botfather)

2. **Installation**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   TELEGRAM_BOT_TOKEN="your_telegram_token"
   ```

4. **Run the Agent**
   * Terminal Mode: `python main.py --query "What is the capital of France?"`
   * Telegram Mode: `python main.py --telegram`

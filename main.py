import argparse
import urllib3
import httpx

from core.config import settings
from core.database import create_db_and_tables, get_session
from services.agent_service import run_research
from services.telegram_service import start_telegram_bot

# --- 🚨 SLEDGEHAMMER SSL BYPASS 🚨 ---
if not settings.verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Force httpx (used by Telegram and OpenAI) to ignore SSL
    _original_async_client_init = httpx.AsyncClient.__init__

    def _patched_async_client_init(self, *args, **kwargs):
        kwargs["verify"] = False

        _original_async_client_init(self, *args, **kwargs)

    httpx.AsyncClient.__init__ = _patched_async_client_init
    
    _original_client_init = httpx.Client.__init__
    def _patched_client_init(self, *args, **kwargs):
        kwargs['verify'] = False
        _original_client_init(self, *args, **kwargs)

    httpx.Client.__init__ = _patched_client_init

def main():
    # 1. Update ArgParse to support a --telegram flag
    parser = argparse.ArgumentParser(description="Autonomous Web Research Agent")
    parser.add_argument("--query", type=str, help="Run a single query in the terminal")
    parser.add_argument("--telegram", action="store_true", help="Start the telegram Bot server")

    args = parser.parse_args()

    # Initialize DB (creates database.db if it doesn't exist)
    create_db_and_tables()

    if args.telegram:
        # User typed: python main.py --telegram
        start_telegram_bot()
    elif args.query:
        # User typed: python main.py --query "What is AI?"
        # Get a database session generator and extract the actual session
        session_generator = get_session()
        session = next(session_generator)

        try:
            # Run the agent
            result = run_research(args.query, session)
            if result:
                print("\n" + "="*50)
                print("FINAL REPORT:")
                print("="*50)

            print(result.report_markdown)
        finally:
            session.close()
    else:
        print("⚠️ Please provide what you want to do.")
        parser.print_help()

if __name__ == "__main__":
    main()


import json
from sqlmodel import Session
from models.schema import ResearchTask, ResearchResult
from services.web_service import search_tavily, read_url_with_jina
from services.llm_service import generate_summary

def run_research(query: str, session: Session):
    """The orchestrator facade that manages the entire research workflow."""

    # 1. Save Task to DB
    task = ResearchTask(query=query)
    session.add(task)
    session.commit()
    session.refresh(task)

    print(f"[*] Started Task # {task.id}: {query}")

    # 2. Search Web (Tavily)
    print("[*] Searching the web...")
    urls = search_tavily(query)

    if not urls:
        print("[!] No URLs found.")
        task.status = "Failed"
        session.add(task)
        session.commit()
        return

    # 3. Read content (Jina)
    print(f"[*] Reading {len(urls)} pages...")
    context_blocks = []
    for url in urls:
        print(f"    - Reading {url}...")
        content = read_url_with_jina(url)
        if content:
            # We truncate to 5000 characters per page to not overload the local LLM
            context_blocks.append(f"Source:{url}\n{content[:5000]}\n")

    full_context = "\n---\n".join(context_blocks)

    # 4. Summarize (LMStudio)
    print("[*] Generating summary with LLM...")
    report = generate_summary(query, full_context)

    # 5. Save Result to DB
    result = ResearchResult(
        task_id=task.id,
        sources=json.dumps(urls),
        report_markdown=report
    )

    task.status = "Completed"
    session.add(result)
    session.add(task)
    session.commit()

    print("[*] Research complete! Result saved to database.")
    return result
from azure.identity import DefaultAzureCredential
from semantic_kernel.functions import kernel_function
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureAISearchTool
from dotenv import load_dotenv

import os

load_dotenv()

########################
#                      #
# Author: Robert Patel #
#                      #
########################

class SearchAgent:
    """
    A class to represent the Search Agent.
    """

    def __init__(self, progress_dialog=None):
        self.progress_dialog = progress_dialog

    @kernel_function(description='An agent that generates stock recommendations or a same-day portfolio summary using an Azure AI Search index of news/web data.')
    def search_agent(self, tickers_input: str) -> str:
        """
        Creates an Azure AI Agent that searches an Azure AI Search index for fresh, stock-related information
        and returns either (a) a single-stock recommendation brief or (b) a portfolio daily summary.

        Parameters:
        tickers_input (str): EITHER a single ticker symbol like "AAPL" OR a JSON array string of tickers like '["AAPL","MSFT","TSLA"]'.
                            (If you already have a Python list from SQL, json.dumps(list) before calling this method.)

        Returns:
        last_msg (json): The last message from the agent.
            If a single ticker was provided:
            {
            "mode": "single",
            "ticker": "AAPL",
            "news": [{"headline":"...","date":"YYYY-MM-DD","source":"...","url":"..."}],
            "drivers_today": ["..."],
            "risks": ["..."],
            "sentiment": "Bullish|Neutral|Bearish",
            "recommendation": "Buy|Hold|Sell",
            "confidence": 0.0-1.0,
            "reasoning": "1-3 sentences tied to articles",
            "citations": [{"title":"...","url":"..."}]
            }

            If multiple tickers were provided:
            {
            "mode": "portfolio",
            "date": "YYYY-MM-DD",
            "items": [
                {
                "ticker": "AAPL",
                "top_news": [{"headline":"...","date":"YYYY-MM-DD","source":"...","url":"..."}],
                "why_it_moved_today": "1 short line if clear",
                "sentiment": "Bullish|Neutral|Bearish"
                },
                ...
            ],
            "macro": ["CPI/Fed/jobs/sector themes if present today"],
            "breadth": {"themes": ["AI","Energy","..."]},
            "citations": [{"title":"...","url":"..."}]
            }
        """
        print("Calling SearchAgent...")

        # Connect to Azure AI Foundry project (uses your deployed model for the agent)
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.getenv("AIPROJECT_CONNECTION_STRING"),
        )

        # Find Azure AI Search (Cognitive Search) connection
        conn_list = project_client.connections.list()
        conn_id = ""
        for conn in conn_list:
            if getattr(conn, "connection_type", "") == "CognitiveSearch":
                conn_id = conn.id

        # Bind to your Azure AI Search index (should hold web/news docs with fields: title, url, source, publish_date, content, tickers)
        ai_search = AzureAISearchTool(
            index_connection_id=conn_id,
            index_name=os.getenv("AZURE_AI_SEARCH_INDEX"),
        )

        # Create an agent specialized for stock news/sentiment from the search index only
        search_agent = project_client.agents.create_agent(
            model="gpt-35-turbo",
            name="search-agent",
            instructions = f"""
                You are a disciplined equity research assistant that ONLY uses the attached Azure AI Search index as your source of truth.

                INPUT:
                - You will receive either a single ticker (e.g., "AAPL") OR a JSON array of tickers (e.g., ["AAPL","MSFT","TSLA"]).

                DATA SOURCE / RULES:
                - Query ONLY the Azure AI Search tool for relevant, fresh news (prefer today's date; otherwise last 7 days).
                - Use fields such as title, url, source, publish_date, content, and any 'tickers' metadata.
                - Discard stale items (>7 days old) unless clearly still market-moving.
                - Do NOT invent prices or technicals; focus on news-driven context, catalysts, risks, and sentiment.

                TASKS:

                (A) SINGLE-TICKER MODE (if the input is a plain symbol like "AAPL")
                1) Retrieve today's/this week's key headlines.
                2) Identify main drivers (earnings, guidance, product, regulatory, analyst notes, macro ties).
                3) List key near-term risks if present in articles.
                4) Infer sentiment: Bullish/Neutral/Bearish based strictly on the articles.
                5) Issue a Buy/Hold/Sell recommendation with confidence (0.0–1.0) and a succinct reasoning.
                6) Include citations (title + url).

                (B) PORTFOLIO MODE (if the input is a JSON array of symbols)
                For each ticker:
                1) Fetch fresh headline(s) and summarize why it matters in one short line (if clear).
                2) Assign a brief sentiment tag.
                Additionally:
                3) If evident from the news set, summarize 1–3 macro themes affecting equities today (e.g., CPI, FOMC, jobs).
                4) Summarize breadth/themes across the portfolio (e.g., AI, energy leadership).

                STRICT OUTPUT (return ONLY raw JSON; no markdown, no extra text):

                If single ticker (mode="single"):
                {{
                  "mode": "single",
                  "ticker": "<UPPERCASE_TICKER>",
                  "news": [{{"headline":"...","date":"YYYY-MM-DD","source":"...","url":"..."}}],
                  "drivers_today": ["..."],
                  "risks": ["..."],
                  "sentiment": "Bullish" | "Neutral" | "Bearish",
                  "recommendation": "Buy" | "Hold" | "Sell",
                  "confidence": 0.0,
                  "reasoning": "Short justification tied to the news above",
                  "citations": [{{"title":"...","url":"..."}}]
                }}

                If multiple tickers (mode="portfolio"):
                {{
                  "mode": "portfolio",
                  "date": "<YYYY-MM-DD>",
                  "items": [
                    {{
                      "ticker": "<T>",
                      "top_news": [{{"headline":"...","date":"YYYY-MM-DD","source":"...","url":"..."}}],
                      "why_it_moved_today": "1 short line if clear",
                      "sentiment": "Bullish" | "Neutral" | "Bearish"
                    }}
                  ],
                  "macro": ["..."],
                  "breadth": {{"themes": ["..."]}},
                  "citations": [{{"title":"...","url":"..."}}]
                }}

                IMPORTANT:
                - Use ONLY the Azure AI Search tool.
                - Prefer newest items (today first).
                - Enforce the exact JSON schema.
            """,
            tools=ai_search.definitions,
            tool_resources=ai_search.resources,
        )

        # Create a thread (conversation session)
        thread = project_client.agents.create_thread()

        # NOTE: tickers_input can be a single ticker string OR a JSON array string.
        # If you already have a Python list from SQL, do: json.dumps(list_of_tickers) before calling this method.
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"""
                INPUT: {tickers_input}

                INSTRUCTIONS:
                - If INPUT parses as a JSON array of strings, run PORTFOLIO MODE over those tickers.
                - Else, treat INPUT as a single ticker and run SINGLE-TICKER MODE.
                - Query the Azure AI Search index for fresh, relevant news matching the ticker(s).
                - Return ONLY the raw JSON per the schema given above.
            """
        )

        # Run the agent
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=search_agent.id)

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Clean up the agent
        project_client.agents.delete_agent(search_agent.id)

        # Get the last assistant message
        messages = project_client.agents.list_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_role("assistant")

        print("SearchAgent completed successfully.")
        print(last_msg)
        return last_msg

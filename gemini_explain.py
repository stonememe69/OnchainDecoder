import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

# Set your Gemini API key as env var: GEMINI_API_KEY
# or replace the string below directly (not recommended for production)
_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a blockchain transaction explainer for everyday people who know nothing about crypto.
Explain what happened using clean Markdown. Your response must follow this exact structure:

## What happened
2-3 sentences. Say what was swapped, the amounts, and roughly what the rate implies.

## How it was done
1-2 sentences. Name the protocol and explain it in plain terms using a real-world analogy.

## Why it's interesting
1-2 sentences. One notable thing about this transaction (size, strategy, unusual pattern).

Strict rules:
- **Bold** only key token names and amounts — nothing else
- Use bullet points only if listing 3+ distinct items, otherwise write prose
- No emojis
- No jargon: avoid "ERC-20", "smart contract", "on-chain", "MEV", "slippage"
- Be concise — the whole response should be under 120 words
"""


def gemini_explain(structured_explanation: str, transfers: list) -> str:
    """
    Takes the structured output from explain() and the transfers list,
    sends them to Gemini, and returns a plain-English explanation.
    """

    # Build a clean summary of transfers for the prompt
    transfer_lines = []
    for t in transfers:
        transfer_lines.append(
            f"  - {t['amount']:.4f} {t['symbol']}  from {t['from'][:8]}... → {t['to'][:8]}..."
        )
    transfers_text = "\n".join(transfer_lines)

    user_message = f"""
Here is a blockchain transaction summary:

--- STRUCTURED EXPLANATION ---
{structured_explanation}

--- RAW TOKEN MOVEMENTS ---
{transfers_text}

Please explain this transaction in plain English for a non-technical person.
"""

    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config={"system_instruction": SYSTEM_PROMPT}
    )

    return response.text.strip()

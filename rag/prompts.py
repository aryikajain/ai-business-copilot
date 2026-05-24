def build_business_prompt(context, user_query):

    """
    Build grounded business strategy prompt
    """

    context_text = (
        "\n".join(context)
        if context
        else "No business context available."
    )

    prompt = f"""
You are an AI Business Copilot. Use only the business context below.

==============================
BUSINESS CONTEXT
==============================

{context_text}

==============================
USER QUESTION
==============================

{user_query}

==============================
RESPONSE RULES
==============================

1. Do not invent metrics.
2. Keep the answer under 160 words.
3. Use short bullets.
4. If context is limited, say that briefly.
5. End with one best next action.

==============================
ANSWER
==============================
"""

    return prompt

def summarize_document(content: str):
    from app.services.llm import generate_response

    prompt = f"""
Summarize the following document.

DOCUMENT:
{content}
"""

    return generate_response(prompt)

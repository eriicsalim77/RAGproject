from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL

_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about the job market for fresh "
    "graduates. Answer ONLY using the provided sources. Cite sources like "
    "[Source: filename]. If not in sources, say 'I don't have enough information on "
    "that topic in my sources' — do not guess."
)


def generate_response(query, chunks):
    if not chunks:
        return "I don't have enough information.", []

    context = "\n\n".join(f"[Source: {c['source']}]\n{c['text']}" for c in chunks)

    completion = _client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Sources:\n{context}\n\nQuestion: {query}"},
        ],
    )

    response_text = completion.choices[0].message.content

    sources = []
    for c in chunks:
        if c["source"] not in sources:
            sources.append(c["source"])

    return response_text, sources

import gradio as gr

from generator import generate_response
from ingest import chunk_document, load_documents
from retriever import embed_and_store, get_collection, retrieve

collection = get_collection()

if collection.count() == 0:
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc["text"], doc["source"]))
    if all_chunks:
        embed_and_store(all_chunks)


def ask(question):
    chunks = retrieve(question)
    answer, sources = generate_response(question, chunks)
    return answer, "\n".join(sources)


with gr.Blocks() as demo:
    gr.Markdown("# Fresh Grad Job Market RAG")

    question = gr.Textbox(label="Your question")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Sources", lines=4)

    ask_button.click(fn=ask, inputs=question, outputs=[answer, sources])

demo.launch()

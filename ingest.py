import os

from config import CHUNK_SIZE, DOCS_FOLDER, MIN_CHUNK_LENGTH, OVERLAP


def load_documents():
    documents = []
    for filename in os.listdir(DOCS_FOLDER):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(DOCS_FOLDER, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        source = os.path.splitext(filename)[0]
        documents.append({"source": source, "text": text})

    print(f"Loaded {len(documents)} documents")
    return documents


def chunk_document(text, source_name):
    chunks = []
    step = CHUNK_SIZE - OVERLAP
    chunk_id = 0

    for start in range(0, len(text), step):
        chunk_text = text[start:start + CHUNK_SIZE]
        if len(chunk_text) < MIN_CHUNK_LENGTH:
            continue
        chunks.append({
            "text": chunk_text,
            "source": source_name,
            "chunk_id": f"{source_name}_{chunk_id}",
        })
        chunk_id += 1

    return chunks


if __name__ == "__main__":
    docs = load_documents()

    if docs:
        first_doc_chunks = chunk_document(docs[0]["text"], docs[0]["source"])
        print(f"First document produced {len(first_doc_chunks)} chunks")

    total_chunks = 0
    all_chunks = []
    for doc in docs:
        doc_chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(doc_chunks)
        total_chunks += len(doc_chunks)

    print(f"Total chunks across all documents: {total_chunks}")

    if all_chunks:
        print("First chunk:")
        print(all_chunks[0])

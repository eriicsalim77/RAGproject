from ingest import load_documents, chunk_document

docs = load_documents()
all_chunks = []
for d in docs:
    all_chunks.extend(chunk_document(d['text'], d['source']))

# Get one chunk from each unique source
seen_sources = set()
samples = []
for c in all_chunks:
    if c['source'] not in seen_sources:
        samples.append(c)
        seen_sources.add(c['source'])
    if len(samples) >= 5:
        break

for i, c in enumerate(samples, 1):
    print(f"--- Sample Chunk #{i} (Source: {c['source']}, {len(c['text'])} chars) ---")
    print(c['text'])
    print()
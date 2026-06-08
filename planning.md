# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? --> 
An unofficial guide to job hunr reality as a fresh grad in 2026.
There are thousands of college fresh grad that is currently navigating the transition, it is definitely one of the toughest period since it involves a lot of uncertainty. This domain willbe valuable to those audience and help them understand the landscape better, gain practical tips from peers or professionals, and give a sense of support in this period.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Book | A book that talks about the whole entire career in a bigger picture and help us think through the decision that we should make.  | docs/02_Book_80000hours.txt |
| 2 | Reddit  | Average experience reddit for fresh grad hunting a job  |docs/01_Reddit_AvgExperience.txt |
| 3 | Reddit | CS Major POV for hunting a job in 2026 as a fresh grad | C:\Users\USER\OneDrive\Documents\CodePath\01_Project_RAG\docs\03_Reddit_CSMajor.txt |
| 4 | Reddit | Tech job landscape open thread for fresh grad in 2025 | docs/04_Reddit_TechJob.txt |
| 5 | Reddit | Advice proffesional gave for a fresh grad in 2026  |docs/05_Reddit_Advice.txt |
| 6 | Reddit | H1B Visa applicant POV entering job market in the US | docs/06_Reddit_H1BPOV.txt |
| 7 | Reddit | Nurse POV entering a job market as fresh grad in 2026 | docs/07_Reddit_nursePOV.txt |
| 8 | Reddit | Networking as a leverage to navigate the job market in the US | docs/08_Reddit_Networking.txt |
| 9 | Reddit | H1B landing a job in the US |docs/09_Reddit_H1BLandscape.txt|
| 10 |Reddit | Fresh grad open thread reddit experiencing diffculty getting a job | docs/10_Reddit_TheGrind.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
300

**Overlap:**
50 

**Reasoning:**

This strategy is chosen because 90% of the source are threads with variety of writing and 10% is a book source with really high load of contents that. Using fixed size chunking will ensure that the chunk process is good enough to serve every kind of text.

This chunking strategy has also been used before in rulesbot project and it works well.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:**
5

**Production tradeoff reflection:**
1. Verifier : If cost wasn't a constraint I would optimize the answer with a verifier where each chunk could be added with an added author score or engagement to ensure that the model will always skew towards highest quality response.
2. Secutity : With every added feature there's always be a loophole, including adding that verified method to the model. I would add an added security filter that can ensure every response is generated from real human and not a bot or anything fake.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do fresh grad say about the job market in 2026 | The market is tough and rough, many students have done what is necessary (apply, networking, interviews) but have not heard anything back from recruiters and in high stress period. |
| 2 | What should students do to naviagate the job market in 2026 | Note: there's high variety of answer for this question. However, all answer is expected to be solution oriented rather than mental blocking. This includes practical solution to improve their skills, focus on projects, network, and polish their resume. |
| 3 | Is it easy to navigate the job market in 2026 | The answer should lean towards no or highly negative, the job market is really tough for high majority of people in 2026 based on all the sources listed. |
| 4 | How many job applications have the average fresh grad sent in 2026  | There is no right specific answer to this but roughly above 50 with the average around 150+ |
| 5 | How long is the average fresh grad took to get a jonb in 2025  | Months (3 months is the average) or most grad have not been able to land a job |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. High-context source bias: The load of each content is highly varies. Some sources have higher amount of chunks than the other and it might influence the generated results.

2. Off-topic retrieval: There's only 10 sources that this model use for RAG and the amount of queries asked for topic is limitless. When there's is not enough chunk retrived for a certain type of query, the model might hallucinate.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---
layout: elk
---
flowchart LR
    %% Step 1: Ingestion
    subgraph Ingestion["Ingestion"]
        direction TB
        I1["📄 Source: /docs"]
        I2["📚 10 documents (PDF, text, books)"]
    end

    %% Step 2: Chunking
    subgraph Chunking["Chunking"]
        direction TB
        C1["✂️ Fixed chunk size: 300 chars"]
        C2["🔁 Overlap: 50 chars"]
    end

    %% Step 3: Embedding + Vector
    subgraph Embedding_Vector["Embedding + Vector Store"]
        direction TB
        E1["🤖 Model: all-MiniLM-L6-v2 (Sentence Transformer)"]
        EM["🧩 Embedding generated"]
        E2["💾 Vector Store: ChromaDB"]
    end

    %% Step 4: Retrieval
    subgraph Retrieval["Retrieval"]
        direction TB
        R1["🔍 Query: Top-K search (K=5)"]
        R2["📦 Retrieve from ChromaDB"]
    end

    %% Step 5: Generation
    subgraph Generation["Generation"]
        direction TB
        G1["🤖 LLM: Groq llama-3.3-70b-versatile"]
        G2["🪄 Generate context-aware answer"]
        G3["📦 References from ChromaDB"]
    end

    %% Data Flow
    I2 -->|"Text data"| C1
    C2 -->|"Chunked text"| EM
    EM -->|"Embeddings stored"| E2
    E2 -->|"Vectors searched"| R1
    R2 -->|"Retrieved context"| G1
    G2 -->|"Final response"| G3

    %% Classes for color
    classDef indigo stroke:#818cf8,fill:#eef2ff;
    classDef teal stroke:#2dd4bf,fill:#f0fdfa;
    classDef violet stroke:#a78bfa,fill:#f5f3ff;
    classDef orange stroke:#fb923c,fill:#fff7ed;
    classDef green stroke:#4ade80,fill:#f0fdf4;

    %% Assign colors
    class Ingestion indigo;
    class Chunking teal;
    class Embedding_Vector violet;
    class Retrieval orange;
    class Generation green;
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Claude 
I'll Input the Domain, Documents, and Chunking Strategy and I will ask AI to :
- implement code to load documents () os.listdir() + file reading for document loading process )
- Document dicts
- Sliding Window 
- Chunk IDs
- Configuration Constraints

**Milestone 4 — Embedding and retrieval:**
Claude
I'll input the embedding and retrieval process descriptions including the model and reasoning behind.

I'll ask AI to write code and implement:
- Sentence transformer
- ChromeDB PersistentClient
- _collection.add() to embed and store in one cal
- And implement skip-in-ingested so it doesnt re-embed every restar 

**Milestone 5 — Generation and interface:**
Claude

I'll input the generation model that we use and interface design vision.

I'll ask AI to write code and help build the interface
- Implement generation model that match and align with the prior process for higher-quality generation.
- Built a lightweight modern aesthetic good UX interface to interact with the model.

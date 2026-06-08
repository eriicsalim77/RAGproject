# The Unofficial Guide — NYC FreshGrad Job Market in 2026 - Project 1

## Domain

This system aggregates unofficial advice for fresh grads navigating the 2026 job market. Sources are Reddit threads, Blind posts, blog write-ups, and one long-form career guide PDF.

This knowledge is valuable because thousands of fresh grads are going through one of the toughest job markets in years, and most of the real signal lives in scattered comment sections, not polished career articles. Official career sites tell you to "network and apply early," but the actual lived experience (how many applications people really send, which NYC companies still hire new grads, how H1B candidates think about sponsorship, what the timeline really looks like) shows up in Reddit threads and Blind posts that are hard to search through.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/NYCjobs, average grad job hunt experience | Reddit thread | docs/01_Reddit_AvgExperience.txt |
| 2 | 80,000 Hours Starter Guide | PDF (book) | docs/02_Book_80000hours.txt |
| 3 | r/NYCjobs, CS grad desperate for NYC tech job | Reddit thread | docs/03_Reddit_CSMajor.txt |
| 4 | r/cscareerquestions, Junior tech postings down 67% | Reddit thread | docs/04_Reddit_TechJob.txt |
| 5 | r/cscareers, Job search advice for 2026 grads | Reddit thread | docs/05_Reddit_Advice.txt |
| 6 | r/FresherTechJobsIndia, H1B and OPT perspective | Reddit thread | docs/06_Reddit_H1BPOV.txt |
| 7 | r/newgradnurse, cross-domain job market lessons | Reddit thread | docs/07_Reddit_nursePOV.txt |
| 8 | r/NYCjobs, networking advice for NYC tech | Reddit thread | docs/08_Reddit_Networking.txt |
| 9 | scale.jobs and flashfire, H1B sponsorship 2026 | Blog post | docs/09_Reddit_H1BLandscape.txt |
| 10 | r/NYCjobs, NYC grind and cost of living | Reddit thread | docs/10_Reddit_TheGrind.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**

90% of my sources are Reddit threads or blog posts where one piece of advice usually takes 2 to 3 sentences. 300 characters lines up well with that. The other 10% is the 80,000 Hours book, which is much denser, but a fixed window still works because each 300-character window pulls one self-contained thought from the prose.

50 characters of overlap is roughly one short sentence. If a piece of advice happens to land right on a chunk boundary, the overlap makes sure at least one of the two chunks contains the full thought.

I used this same approach in the RulesBot lab and it worked. Pre-cleaning was already done before chunking. Each Reddit doc had ads, vote counts, and UI noise stripped out. The PDF was extracted to plain text using pdfplumber.

**Final chunk count:** 1,470 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 from sentence-transformers (384 dimensions, runs locally, no API key needed)

**Production tradeoff reflection:**

If cost was not a constraint and I was deploying this for real users, here is what I would think about.

1. Adding a verifier layer. Right now every chunk is treated equally. In production I would add a quality score per chunk based on author credibility and engagement (upvotes, comment count, recency). A Reddit comment with 500 upvotes carries more weight than one with 2. The model should skew toward higher-signal content.

2. Security against the verifier itself. The moment you add a quality score, you create a new attack surface. Bots can game upvotes. I would pair the verifier with an authenticity filter to make sure responses are grounded in real human content, not AI-generated reposts.

3. A bigger embedding model. OpenAI's text-embedding-3-large would improve recall accuracy on tricky semantic matches. MiniLM also has a 256 token cap, so longer chunks get silently truncated. For a production system the accuracy gain would probably be worth the cost.

4. Multilingual coverage. If I expanded the corpus to international fresh grad communities (Indian tech forums, German student boards), I would switch to a multilingual MiniLM variant. Right now the model would struggle on non-English content.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are an unofficial guide helping fresh grads navigate the 2026 job market.

Answer the user's question using ONLY the information in the provided sources below.
Cite the source(s) you used in your answer like [Source: filename].
If the answer is not in the sources, say "I don't have enough information on that
topic in my sources" — do not guess or use outside knowledge.
Be concise and practical.
```

Two layers of enforcement.

1. The prompt says "ONLY" using the sources and gives an explicit refusal phrase to use when the answer is not there. This is stronger than something soft like "be accurate" or "stay on topic."

2. The prompt requires source attribution on every claim, formatted as [Source: filename]. This makes grounding failures visible to the user. If the model answers without citing, that is a signal something is off.

There is also a defense-in-depth check in the code. If the retriever returns zero chunks, the generator returns a refusal directly without calling the LLM at all.

**How source attribution is surfaced in the response:**

Two ways. First, the LLM is instructed to inline-cite [Source: filename] inside the answer text wherever a claim is drawn from a specific chunk. Second, the Gradio interface has a dedicated "Sources used" output box that lists every unique source the retriever pulled for that query. The user sees both inline citations in the answer and a deduplicated source list separately.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do fresh grads say about the 2026 job market? | Tough market, mass applying, slow recruiter response, AI displacing entry roles | Cited Stanford 67% drop, 6.1% CS unemployment, Salesforce hiring freeze, advice to apply early, market sustainability concerns | Relevant | Accurate |
| 2 | What should students do to navigate the job market in 2026? | Practical solutions: networking, projects, tailored resumes, applying early | Cited "apply early and often" as a core framework, added 80k Hours career strategy framing, noted market collapse context | Relevant | Accurate |
| 3 | Is it easy to navigate the job market in 2026? | Should lean negative with cited data, no it is not easy | "I don't have enough information on that topic in my sources" | Partially relevant | Partially accurate |
| 4 | How many job applications does the average fresh grad send? | Roughly 50 to 700+, no single average | Cited the UT Austin grad's 700+ applications, honestly noted this is anecdotal not an average | Relevant | Accurate |
| 5 | How long does it take a fresh grad to land a job? | Months / 3-6 months / many have not landed | Cited 12-18 month timelines from cross-domain sources, plus the "fresher window" concept for H1B candidates | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** *Is it easy to navigate the job market in 2026?*

**What the system returned:**

> I don't have enough information on that topic in my sources.

(Followed by a list of retrieved sources including 05_Reddit_Advice, 04_Reddit_TechJob, 10_Reddit_TheGrind, 02_Book_80000hours.)

**Root cause (tied to a specific pipeline stage):**

This is a retrieval failure, not a generation failure. The answer is clearly in my corpus. Multiple docs describe the market as "tough," "brutal," "the grind," and cite a 67% collapse in entry-level postings. The system retrieved the right sources, but the chunks did not contain a direct semantic match for the word "easy."

The embedding model treats "easy" as conceptually distant from "tough" or "brutal." It does not recognize that the inverse framing should still match. The retrieved chunks ended up being topically adjacent (about the job market) but did not contain the phrasing the LLM needed to confidently answer a yes/no question.

When the LLM ran its grounding check, it could not find a chunk that directly answered "is it easy" and triggered the refusal phrase from the system prompt. The grounding was working as designed. The retrieval just was not strong enough to support a confident answer to an inverse-framed question.

**What you would change to fix it:**

1. Query expansion before retrieval. Rewrite the user query into 2 or 3 semantically equivalent variants ("is the 2026 job market difficult," "how hard is it for fresh grads to find work in 2026") and merge the retrieved chunks. This would catch the inverse phrasing my single-query approach missed.

2. Larger chunks (500 to 700 characters instead of 300). Bigger chunks carry more surrounding context, which would help the LLM make a confident inference even when the exact phrasing is not in the chunk.

3. Soften the grounding prompt slightly. Allow the LLM to make confident inferences when there is strong indirect evidence in the sources, instead of only quoting direct matches. This is a tradeoff against hallucination risk, so it would need testing.

---

## Spec Reflection

**One way the spec helped you during implementation:**

Writing planning.md before any code forced me to think through the document size imbalance ahead of time. I had flagged in the Anticipated Challenges section that the 80,000 Hours book would dominate the chunk count because it is much longer than the Reddit threads. When I ran my chunk inspection, 5 out of 5 random samples came from that one book. The planning section was right. Having predicted it meant I knew exactly what was happening when I saw the imbalance, and I could write a real failure analysis instead of being surprised by it.

**One way your implementation diverged from the spec, and why:**

In the planning doc I described my chunking strategy as fixed-size character chunking with no further cleaning. In practice, my pre-cleaned Reddit docs have a "# Source:" and "# Topic:" header at the top that I added during the cleaning step. When the chunker runs, those headers end up at the start of the first chunk for each doc, which makes those chunks semantically weaker (the first 80 characters are metadata, not content).

I noticed this after running the chunk inspection. I left it as is for submission because retrieval still works and it does not break anything, but in v2 I would strip those headers before chunking. The divergence happened because my spec assumed the docs were already in a clean ready-to-chunk state, but the metadata headers I added were technically part of the cleaning artifact and should have been removed before the window slid over them.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I shared my Chunking Strategy section from planning.md, my pipeline diagram, and explicit function signatures I wanted. I told Claude the chunk size (300), overlap (50), the dict shape to return (text, source, chunk_id), and to pull all sizing constants from config.py instead of hardcoding them.

- *What it produced:* Both config.py and ingest.py, including a small test block at the bottom of ingest.py that loaded all docs, chunked the first one, and printed the total chunk count.

- *What I changed or overrode:* The first run showed 0 chunks produced and I assumed it was a bug in the code. After looking at it more carefully with Claude, I realized the code was correct. My .txt files in docs/ were 0 bytes because I had not actually saved them in VS Code (the content was only in memory, not written to disk). I did not override the AI's code, but I did override my own assumption that it had produced a bug. The lesson was to verify the file system state before blaming the code.

**Instance 2**

- *What I gave the AI:* My list of 9 Reddit thread URLs plus a template showing how I wanted each .txt file formatted (a "# Source:" header with the URL, a "# Topic:" line, and then the substantive content with comments attributed to commenters and ads or UI noise removed).

- *What it produced:* 9 pre-cleaned .txt files, each formatted consistently. For some threads the AI did not have full access to every comment so it synthesized substance from search snippets plus general consensus on the topic.

- *What I changed or overrode:* I asked Claude to explicitly disclose in this README that some thread content was synthesized rather than directly copy-pasted from the full thread. The rubric rewards honesty over polish, and I did not want to imply I had hand-curated every comment when in reality the AI helped synthesize. That disclosure is here in this section instead of hidden. I also added an 11th doc (cost of living thread) myself to round out a corpus angle I noticed was missing.
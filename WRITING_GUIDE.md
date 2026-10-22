# Writing Guide: How People and AI Share the Work

[中文](写作指南.md)

> This English version is an AI-assisted translation of [写作指南.md](写作指南.md), which is the original. It is waiting for review by a native speaker.

This guide is for everyone who writes for *Stories about Bitcoin*. The Chronicle chapters and [Garden](garden/) submissions follow the same rules: **people write the key scenes and the people in them; AI researches the sources, checks the timeline and drafts translations.** For submissions, credit and licensing, see [garden/README.md](garden/README.md).

## 1. The principle in one line

> **People write the heart. AI builds the scaffolding, runs the errands and finds the faults. AI does not write finished paragraphs into the text.**

The "heart" is what a reader remembers afterwards: the images, the people, the attitude. The "scaffolding" is everything that holds the heart up: sources, dates, citations, translations, formatting. When you are not sure who should do something, ask: if someone else wrote this passage, would it come out differently? If yes, it is a person's job.

## 2. Why split it this way

You cannot add a human voice by polishing. It comes from three things AI cannot give you:

1. **Why you care.** Faced with the same history, different people stop at different places.
2. **Details only you know.** The forum post that made you sigh; what your phone showed the day you got liquidated.
3. **What you are willing to cut.** AI is good at adding and bad at cutting.

The book already has two examples:

- **Telling the reader what it means.** Chapter 04 says: "This was the classic cypherpunk tactic: use a loophole in the law to protect the freedom of code." That sentence draws the conclusion for the reader. What moves people is Finney's own line: the fan was too noisy, so he turned it off.
- **Details that drift.** Chapter 04 has Finney "typing two words, Running bitcoin"; chapter 36 says he "wrote three characters". After many AI rewrites, the details no longer come from one person's memory.

So people take care of those three things, and AI does all the rest of the labour and guards the facts.

## 3. Who does what

| Task | Who | Output |
| --- | --- | --- |
| Opening image, closing line, heartbeat scenes | Person | Text |
| People: which quote to use, which moment to write | Person | Text |
| The author's attitude, jokes, favourites, doubts | Person | Text, author's note |
| What to cut, what to keep | Person | Final draft |
| Research, finding quotes and their sources | AI, person spot-checks | Research pack in `sources/` |
| Checking the timeline and details across chapters | AI drafts the table, person confirms | Fact-check table |
| Translation | AI first draft, native speaker reviews and is credited | Translation |
| Editorial questions | AI only asks; person decides | List of questions |
| Purely informational transitions | AI may draft, person reviews | Text (disclosed) |
| Typos, consistent terms, formatting | AI | Final draft |
| Video and audio adaptations, first screening of submissions | AI, person approves | Derived works |

## 4. Six steps for one piece

1. **Research pack (AI).** Start from primary material: a timeline, quotes with links, points of dispute and opposing views. Prompt: section 8 A.
2. **Why me (person).** Write 3–5 lines: what moved you about this story? Where do you want the reader to stop? Not for publication; it sets your direction.
3. **Rough draft (person).** Write it yourself, or talk into your phone and transcribe. Write only the 2–3 scenes you most want to write, and hold the rest with one-line placeholders such as "[explain the 2010 price here]". It can be ugly.
4. **Editorial questions (AI).** AI reads the draft like an editor and only asks questions; it rewrites nothing. Prompt: section 8 B.
5. **Revision (person).** You revise the heart. AI may draft the informational placeholders; you review them and count them in your disclosure.
6. **Fact-check and proofread (AI drafts, person confirms).** Claim-by-claim check, consistent terms, typos, plus a list of every sentence that explains the meaning, for you to keep or cut. Prompt: section 8 C.

The last step is always **reading it aloud yourself**.

### Shorter versions by type

| Type | Required steps | Notes |
| --- | --- | --- |
| Chronicle chapter | All six + author's note | Rewrite one scene at a time, not a whole chapter |
| Portrait, historical fiction | All six | Fiction needs a research pack too; the background must be right |
| Oral history | 2–6 | The interviewee's words are primary material; check any public events they mention |
| Memoir | 2–5, plus 6 if public events are involved | Personal experience needs no source |
| Letter, poem, lyrics | 3–5 | You can skip AI entirely |

**Author's note in the Chronicle:** 3–5 lines at the start of each chapter, written by the author: why this chapter, and what surprised you most while researching it. When rewriting the Chronicle, start with chapter 04, "The First Believer", and fix Finney's details in chapter 36 at the same time.

## 5. What a person must write

All of these must come from you, even if you only say them into your phone and AI transcribes:

- **The first image and the last line.**
- **1–2 heartbeat scenes per piece.** The moment Finney turns off the fan; the moment Laleh hides her seed on a small slip of paper.
- **Choices about people.** The research pack may hold ten quotes. Which one you use, and which day of their life you write, is your call.
- **Your attitude.** Jokes, favourites, doubts, uncertainty. "I still haven't figured this out" is a very good sentence.
- **What to cut.** Before the final draft, go through every meaning-explaining sentence AI flagged. The default is to cut.

How to tell whether a sentence belongs here: if cutting it costs the reader information, AI can handle it. If it costs them a feeling, it is yours.

## 6. AI's three main jobs

### 6.1 Research

The output is one research pack per chapter, `sources/XX_章名.md`; a Garden piece keeps its own `sources.md`. It is raw material for the author to choose from, not an article.

- **Primary sources only.** Original posts, emails, forum archives, court filings, on-chain transactions, interviews from the time. Secondary articles are only for finding leads; when citing, trace them back to what they cite.
- **A link for every fact.** The link must be a page that was actually opened, not a search snippet. Use an archive.org copy if the page is gone.
- **Quotes stay verbatim.** No rewording, no stitching. Translations go in a separate column, marked as translations.
- **List, don't choose.** No comments like "this is the most moving part".
- **Include disputes and opposing views.** If something cannot be found, say so; do not fill the gap.

A research pack always has seven sections (format in section 11): timeline; people and their words; key numbers; primary material and scene details; common myths and corrections; disputed or not found; source list.

### 6.2 Checking the timeline

Before the final draft, AI pulls out every checkable claim in the text and rates each one:

| Rating | Meaning |
| --- | --- |
| ✅ | Supported by a primary or reliable source |
| ⚠️ | Broadly right, but details are wrong or disputed |
| ❓ | No source found; cannot be confirmed or refuted |
| ❌ | Contradicted by the sources |

Beyond the single piece, two more checks:

- **Consistency across chapters.** How do other chapters describe the same person or event? Flag any mismatch, such as whether "Running bitcoin" was two words or three characters.
- **Working out dates.** When the author writes a date from memory, work it out from known events. "I bought at around nine thousand, and not long after came March 12": March 12 is 12 March 2020, so the purchase was in early 2020.

The table only raises questions and suggests fixes; the author decides. The model is [sources/00_引子.md](sources/00_引子.md).

### 6.3 Translation

- **AI drafts; a native-speaking volunteer reviews and is credited as translator.** Only reviewed translations go into an anthology.
- **Quotes go back to the original.** Finney's words, translated into Chinese and back into English, will drift. The English version uses his original words.
- **Use one multilingual glossary.** Private key, seed phrase, node, block: one translation per language. The glossary does not exist yet; it is on the to-do list.
- **Translate the voice, not just the meaning.** Reviewers read the translation aloud. When the author's joke does not carry over, use a local equivalent and explain it in a translator's note.

## 7. What AI does not do (red lines)

1. **No invented quotes from real people.** Anything in quotation marks must be findable in a source. Historical fiction with invented dialogue says "This story is fiction" on its first line.
2. **No sentences that explain the meaning.** Don't close a paragraph by telling the reader what it means; leave the conclusion to them.
3. **No rewriting of the parts a person wrote.** Ask, flag, suggest; never hand over a replacement version.
4. **No scoring, no pass/fail decisions.** Model scores push writing to sound more like AI.
5. **No choosing material for the author.** The research pack lists everything; the author chooses.
6. **No exposing private information.** Real names, addresses, links between wallets and identities, unless already public or agreed in writing.

The Garden does not accept pieces generated by AI without substantial rewriting by the author.

## 8. Prompts you can copy

These prompts are not tied to any model; use any AI that can search the web. Replace the text in square brackets.

### A. Build a research pack

```text
I'm writing a piece about [person or event]. Please build a research pack for me. Do not write the piece.

Rules:
1. Primary sources only: original posts, emails, forum archives, court filings, on-chain transactions, interviews from the time. Use secondary articles only to find leads.
2. Give a link you actually opened for every fact.
3. Keep quotes verbatim in the original language, no rewording or stitching; put any translation in a separate column.
4. List material only. Do not say which part is the most moving.
5. If you cannot find something, write "not found". Do not fill the gap.

Output these seven sections: Timeline | People and their words | Key numbers | Primary material and scene details | Common myths and corrections | Disputed or not found | Source list.
Rate every fact: ✅ reliable source / ⚠️ details wrong or disputed / ❓ not found / ❌ contradicted by sources.
```

### B. Ask questions like an editor

```text
Below is my rough draft. Read it like a strict editor. Only ask questions. Do not rewrite any sentence and do not offer replacement versions.

Focus on questions like:
- What did you yourself think here?
- Is there a source for this detail?
- This sentence explains the meaning for the reader. Can it go?
- Where are you moving too fast, before the reader can see the scene?
- After reading this, which single image will I remember?

Quote the sentence each question is about. At most 10 questions, most important first.

[paste draft]
```

### C. Check claim by claim

```text
Pull every checkable claim (dates, numbers, names, quotes, cause and effect) out of the piece below and put them in a table:
# | Claim in the text | Rating | What the source actually says | Source link | Suggested fix

Ratings: ✅ / ⚠️ / ❓ / ❌. Sources must be pages you actually opened.
Then list separately:
1. Every sentence that ends a paragraph by explaining its meaning. List them; do not delete them.
2. Details that may not match other chapters of the book.
3. Terminology and typos.

[paste piece]
```

### D. First-draft translation

```text
Translate the piece below from [source language] into [target language]. This is a first draft; a native speaker will review it.

Rules:
1. If a quote was originally said in the target language, use the speaker's original words instead of translating back. If unsure, mark it [check original].
2. Use this glossary for terms: [paste glossary, or "none yet"].
3. Keep the author's spoken tone and jokes. Where something does not carry over, add a [translator's note] instead of improvising.
4. Do not add explanations that are not in the original.

[paste piece]
```

## 9. Disclosing AI's part

Every piece, including every Chronicle chapter, states at the bottom of its page how much AI was involved; Garden pieces also fill in `ai_assistance` in `meta.yml`. Disclosure is a form of honesty, in the same spirit as "Don't trust, verify".

| Label | Meaning |
| --- | --- |
| `human` | Written by a person; AI only researched, fact-checked or proofread |
| `human-led` | Written by a person; AI drafted some transitions or suggested structure |
| `ai-assisted` | AI drafted; a person rewrote it paragraph by paragraph |

Translations are labelled separately, e.g. `ai-draft, human-reviewed`, with the reviewer named.

When unsure, compare with these:

- You spoke it into your phone; AI transcribed it and only fixed the word order: `human`.
- AI asked editor's questions and you changed three things yourself: `human`.
- AI drafted three "[explain … here]" placeholders: `human-led`.
- Existing Chronicle chapters, before they are rewritten: `ai-assisted`. Each rewritten chapter gets a new label.

Watching the labels change from `ai-assisted` to `human`, chapter by chapter, is a story of its own.

## 10. How to tell it is done

People decide, not models. The GPT / DeepSeek scoring in this repository becomes a tool for finding errors, no longer a pass/fail bar.

- [ ] **Read-aloud test.** Read it out loud yourself. Wherever it feels awkward, the human voice is missing.
- [ ] **Three human test readers.** A Bitcoin veteran (for technical errors), a friend who knows nothing about it (can they follow it?), and a sceptic (does it only move believers?).
- [ ] **One question.** Which image did the reader remember? If they can't say, the piece isn't finished.
- [ ] **No unresolved ❌ in the fact-check table.** ❓ can stay, but the text must sound uncertain there.
- [ ] **Disclosure label filled in.**

## 11. Appendix: formats and samples

### Research pack `sources/XX_章名.md`

```markdown
# Chapter XX "Title" · Research pack

Compiled: YYYY-MM-DD | By: [name] + AI
Ratings: ✅ reliable source | ⚠️ details wrong or disputed | ❓ not found | ❌ contradicted by sources

## 1. Timeline
| Date | Event | Rating | Source |

## 2. People and their words
| Who | Role at the time | Quote (original language) | Translation | Source |

## 3. Key numbers
| Number | What it counts | Rating | Source |

## 4. Primary material and scene details
(Posts, emails, interviews, photos. List only, no commentary; the author chooses.)

## 5. Common myths and corrections
| Myth | What actually happened | Source | In the old text? |

## 6. Disputed or not found

## 7. Source list
```

### Garden pieces

Copy [garden/_template/](garden/_template/); it has templates for `meta.yml`, the story and `sources.md`.

### Samples

- **Fact-check table:** [sources/00_引子.md](sources/00_引子.md), 15 checks of the three true stories in the prologue.
- **Research pack:** the chapter 08 pack is being built in the seven-section format and will go into `sources/` when ready.
- **Editorial questions:** to come. The first round of questions from the chapter 04 rewrite will go here as a sample.

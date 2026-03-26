# Contributing to Stories about Bitcoin

Thank you for your interest in contributing to **Stories about Bitcoin** (比特币那些事儿) -- an open-source bilingual Bitcoin history book covering 1976-2024 in 36 chapters, with a React website and free ebooks.

Whether you're a translator, historian, developer, or designer, there's a way for you to help. This guide will get you started.

## Quick Start

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Stories-about-Bitcoin.git
cd Stories-about-Bitcoin

# 2. Create a branch for your work
git checkout -b your-branch-name

# 3. Make your changes, then commit
git add <files>
git commit -m "Brief description of changes"

# 4. Push and open a Pull Request on GitHub
git push origin your-branch-name
```

## Ways to Contribute

### 1. Translation (most needed)

The book is written in Chinese and translated into English. Translations that read like natural, literary prose are far more valuable than literal word-for-word conversions.

**Proofread existing English translations:**

1. Compare files in `en/` with the Chinese originals in `正文/` (the source of truth).
2. Look for mistranslations, awkward phrasing, or missing nuance.
3. Open a PR with your improvements.

**Add a new language:**

1. Fork the repo and create a new directory (e.g., `ja/` for Japanese, `es/` for Spanish).
2. Copy the structure from `en/` -- each chapter has a corresponding file.
3. Translate the chapters, preserving the literary narrative tone.
4. Add a `SUMMARY.md` listing all translated chapters.
5. Open a PR. One reviewer must approve before merge.

**Translation guidelines:**

- Use the glossary at `scripts/content_pipeline/glossary.json` for consistent terminology.
- Maintain the book's storytelling voice -- this is narrative history, not a textbook.
- Proper nouns, technical terms, and dates must be accurate.
- Each PR should cover complete chapters (not partial translations).

### 2. Fact-Checking

Bitcoin history involves specific dates, numbers, and people. Accuracy matters.

**How to report an error:**

- Open a GitHub Issue with: the chapter name, the incorrect claim, and a source citation (link, paper, or book reference).

**How to fix it directly:**

- Edit the source file in `正文/` (not `zh/` -- that directory is auto-generated).
- Include your source citation in the PR description.
- Reference materials are maintained in `资料/` (not on GitHub), but you can cite any reputable external source.

### 3. Website Development

The website is a React SPA with HonKit-powered ebooks.

**Setup:**

```bash
cd new-website
npm install
npm run dev          # Dev server at localhost:5173
```

**Stack:** React + Vite + Tailwind CSS + Framer Motion

**Before submitting a PR:**

```bash
npm run lint         # Must pass
npm run test:run     # Must pass
npm run build        # Must succeed
```

**Key conventions:**

- Bilingual strings use `{ zh: '中文', en: 'English' }` objects.
- Components receive a `lang` prop for internationalization.
- Custom Tailwind tokens: `bitcoin-orange`, `bitcoin-gold`, `historical-parchment`.
- Check GitHub Issues for items labeled `good first issue`.

### 4. Design

**Chapter illustrations:**

- See [Issue #11](https://github.com/beihaili/Stories-about-Bitcoin/issues/11) for the style guide.
- Submit source files to `img/` (PNG format).
- Resized variants are generated automatically: `img_800px/` (via `sips -Z 800`) and `img_webp/` (via `cwebp -q 80`).

**OG share images:**

- Dimensions: 1200 x 630 px
- Use Bitcoin orange (`#F7931A`) as the primary accent color.
- Submit to `new-website/public/og/`.

### 5. Content Improvements

- Fix typos, improve wording, tighten prose.
- **Always edit `正文/`, never `zh/` directly.** The `zh/` directory is built from `正文/` by `scripts/build_zh.py` and CI.
- `en/` can be edited directly for English-only fixes.

## Commit Messages

- Write in English.
- Keep the first line concise (under 72 characters).
- Use the imperative mood: "Fix date in chapter 12", not "Fixed date in chapter 12".

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Be respectful and constructive in all interactions.

## Questions?

- **GitHub Issues**: [Open an issue](https://github.com/beihaili/Stories-about-Bitcoin/issues) for bugs, suggestions, or questions.
- **Discord**: [Join our community server](https://discord.gg/TTFuH9de).

## License

- **Content** (chapters, translations): [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (website, scripts): [MIT](LICENSE)

By contributing, you agree that your contributions will be licensed under these terms.

---

Thank you for helping tell Bitcoin's story.

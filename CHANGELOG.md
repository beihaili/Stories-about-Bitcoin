# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [v2.2] - 2026-03-25

### Changed
- Typography upgrade for PDF ebooks (improved readability)
- Added chapter numbering (第X章) to ebook builds
- Short paragraph merging to reduce visual fragmentation
- Fixed EPUB build issues

## [v2.0] - 2026-03-24

### Added
- Full English retranslation of all 36 chapters using Claude Opus
- GitHub Release with 6 ebook files (zh/en PDF + EPUB + sample)
- Bitcoin orange theme for ebook typesetting

### Changed
- Repository consolidation (正文/ as single source of truth)
- Complete rewrite of `chapters.js` with all 9 periods
- Fixed all chapter links across zh/ and en/

## [v1.0] - 2026-03-23

### Added
- First ebook release
- Pandoc + XeLaTeX PDF generation (ctexbook, B5 paper)
- HonKit EPUB generation

## [v0.9] - 2026-03-22

### Added
- Website monetization: BTC and Lightning donation addresses
- Content polish pass on 8 chapters

## [v0.1] - 2025-02

### Added
- Initial website launch
- React SPA homepage (Vite + Tailwind + Framer Motion)
- HonKit bilingual ebook (zh/ and en/)

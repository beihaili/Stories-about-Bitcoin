# Civil War and Independence: Bitcoin Independence Day

Two years.

Two years of arguments, accusations, personal attacks, forum schisms. Big blocks or small blocks, on-chain scaling or layer-two scaling, miners calling the shots or developers — the Bitcoin community had torn itself to pieces in the Scaling War.

By the spring of 2017, every participant was exhausted. Miners refused to activate SegWit. The entrepreneurs' compromise proposal, SegWit2x, satisfied neither side. Bitcoin Core developers waited. Users waited. Everyone waited.

Then someone nobody had ever heard of stepped forward.

---

## A Hat

The GitHub username: Shaolinfry. Real identity: unknown. To this day, nobody knows.

In February 2017, this anonymous developer posted an article on a technical forum proposing an idea that sounded a little crazy: User Activated Soft Fork — UASF.

In plain English: miners won't activate SegWit? Fine. Users will activate it themselves.

The method was simple and dangerous: starting August 1st, every node running the UASF software would reject any block that did not support SegWit. Miners could choose not to follow — but if the majority of exchanges, wallets, and merchants ran UASF, then blocks without SegWit support would go unrecognized. Unrecognized blocks meant no economic value. No economic value meant mining for nothing.

It was a game of chicken. Users were saying: we are taking this road. You can refuse to follow, but if you don't follow, the coins you mine will be worthless.

The miners' reaction? Fury. Bitmain's Jihan Wu publicly called UASF "an attack on Bitcoin." Many technical experts shook their heads too: what if not enough people supported UASF? What about a network split?

But Shaolinfry's idea struck a nerve that had been taut for two years — users had had enough. Enough of being held hostage by miners who wouldn't allow upgrades. Enough of sitting in the audience while entrepreneurs and miners played their games. UASF gave them a tool: stop waiting for someone else to decide, and do it yourself.

BIP 148 — the specific technical proposal behind UASF — garnered massive support within weeks. Not because it was technically flawless (it genuinely carried risks), but because of what it represented: the power over Bitcoin belongs to users.

Then the hats appeared.

Someone designed a baseball cap with "UASF" printed on the front. White letters on a black background, clean and forceful. Within weeks, that cap showed up at Bitcoin meetups around the world. New York, London, Tokyo, San Francisco — people wearing UASF hats could spot each other in a crowd at a glance.

A hat became a banner.

This detail matters. From the day it was born, Bitcoin had been a purely digital entity — code, algorithms, numbers on a screen. But the UASF hat was physical. You could touch it, wear it on your head, nod at the stranger across the room who was wearing one too. In a dispute about a software protocol, a cloth cap became the most powerful weapon.

---

## August 1st

The UASF threat hadn't even taken formal effect before the miners blinked.

On July 21, 2017, BIP 91 — the miners' hastily assembled compromise — was activated. In substance, it meant that before the UASF deadline of August 1st arrived, miners would voluntarily start requiring all blocks to signal SegWit support. In plain language: the miners saw that UASF was unstoppable and decided to jump before they were pushed.

SegWit activation was thus locked in. The users had won.

But the story wasn't over.

August 1, 2017. 1:16 PM, UTC.

Thousands of block explorer pages around the world refreshed simultaneously. Reddit's r/Bitcoin was flooded to the point of server meltdown. At Bitcoin meetups in dozens of cities, people huddled around screens, staring at the block height.

478,558.

The next block did not come from the Bitcoin main chain. A new chain forked off from block 478,558. The first Bitcoin Cash block was born. Block size: 1.9 MB — far exceeding Bitcoin's 1 MB limit. The big-block camp had left. They weren't driven out — they chose a different road.

The reaction at the meetups was complicated. Some applauded — SegWit was locked in, the war was over. Some fell silent — the community had split after all, and some of those who left were old friends who had walked the journey together. Someone raised a cap printed with "UASF" and said nothing.

Bitcoin won the Scaling War. The price was a schism.

---

## The Taste of Victory

What did SegWit's activation mean?

First, it fixed the transaction malleability bug — a technical problem that had plagued Bitcoin for years, finally resolved. Without that fix, the Lightning Network could never have worked. Without the Lightning Network, Bitcoin would have been trapped forever at the bottleneck of roughly seven transactions per second.

Second, without changing the block size limit, it effectively boosted network capacity by about 40%. Not through brute force (enlarging blocks), but through ingenuity (separating signature data from transaction data).

The deeper significance was that it paved the way for every future upgrade. The 2021 Taproot upgrade, future Schnorr signature optimizations — all of these were built on SegWit's technical foundation.

But the most important legacy of August 1st was not technical.

It was the establishment of a principle: in the world of Bitcoin, users hold the final say.

Not miners. Not developers. Not entrepreneurs. Users — the people who run nodes, the people who transact in bitcoin, the people who stood at meetups wearing UASF hats. When enough users said "we want SegWit," even the most powerful miners had no choice but to follow. Because the coins miners produce need buyers, and the buyers are users.

This principle was thereafter written into Bitcoin's unwritten constitution: code may propose, miners may execute, but users — by running the software they choose — hold the veto.

When Satoshi Nakamoto designed Bitcoin in 2008, he wrote "peer-to-peer" — peers among equals. Not "peer-to-miner," not "peer-to-corporation." On August 1, 2017, users reminded everyone of that original promise through action.

---

## After the Split

Bitcoin Cash took its big-block dream and went its own way. 8 MB blocks — later expanded to 32 MB — were large enough to accommodate far more transactions. Its supporters believed on-chain scaling was the right path, that Bitcoin should be a cheap, fast payment tool, not some kind of "digital gold."

Their conviction was not without merit. The title of Satoshi's white paper is "A Peer-to-Peer Electronic Cash System" — cash, not gold. From that angle, Bitcoin Cash was arguably more faithful to the original vision than Bitcoin itself.

But the market rendered its own verdict. In the months after the fork, Bitcoin Cash's price and hash rate both trailed far behind Bitcoin. By the end of 2018, BCH underwent yet another fork of its own (BSV), fragmenting the community further. The big-block path did not die, but the market marginalized it.

Bitcoin chose a different road: keep the base layer simple and secure, and delegate complex functionality to layer-two networks. The Lightning Network was the first fruit of that path.

Two years of war, one day of separation. From then on, Bitcoin's narrative gradually shifted from "electronic cash" to "digital gold" — a store of value, not a means of daily payment. Was this shift an active choice or a forced concession? That depends on whom you ask. But either way, it defined Bitcoin's direction for the next decade.

The Scaling War was over. The price frenzy was about to begin. SegWit gave the market confidence, the technical bottleneck had been opened, and Bitcoin began its sprint toward twenty thousand dollars.

---

*Shaolinfry remains anonymous to this day. After UASF succeeded, he — or she — gradually faded from public view, never gave a single interview, never sold a single licensing right to the hat design, never founded a company. An anonymous person proposed an idea, changed Bitcoin's fate, and then vanished. Does that pattern remind you of anyone?*

# Future Promise: The Inscription Storm

![配图](img/ch32.png)

![status](https://img.shields.io/badge/status-completed-success)
![author](https://img.shields.io/badge/author-beihaili-blue)

> 💡 In November 2021, Bitcoin completed its most significant protocol upgrade since SegWit — Taproot. Almost nobody noticed. A year later, a programmer who had once worked at Mr. Rags clothing store and called himself "a very very minor ex-Bitcoin Core contributor" used the door Taproot had opened to etch a pixel skull permanently into the Bitcoin blockchain. Then everyone noticed. The war of 2017 was about how big the blocks should be. The war of 2023 was about what went inside them.
>
> Follow me on Twitter: [@bhbtc1337](https://twitter.com/bhbtc1337)
>
> Join our WeChat group: [Form link](https://forms.gle/QMBwL6LwZyQew1tX8)
>
> This article is open source on GitHub: [Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3)

November 14, 2021. 5:15 AM, UTC.

Tens of thousands of Bitcoin full nodes scattered across the globe, without anyone pressing any button, simultaneously activated a new set of consensus rules. Block height 709,632. Taproot. Bitcoin's largest protocol upgrade since SegWit in 2017.

No press conference. No Twitter wars. No hats.

If you remember the scene four years earlier when SegWit activated — UASF hats, miner standoffs, the Bitcoin Cash fork, people at meetups around the world staring at block explorers and holding their breath — then Taproot's activation was like a graduation ceremony nobody attended. A few hundred celebratory posts appeared on Twitter. Jimmy Song tweeted "Good job #Bitcoin core devs and everyone who helped make Taproot happen!" And then — nothing.

The silence itself was a story.

---

## A Party No One Came To

The story begins in January 2018.

Bitcoin Core developer Gregory Maxwell posted a message to the bitcoin-dev mailing list proposing a technical concept called Taproot. A year later, on May 6, 2019, Blockstream co-founder Pieter Wuille — one of the principal authors of SegWit — published three draft BIPs on GitHub: BIP 340 (Schnorr Signatures), BIP 341 (Taproot), and BIP 342 (Tapscript). The inspiration reportedly came from a lunch conversation with Maxwell and Andrew Poelstra.

What the three BIPs did, in a single sentence: make Bitcoin transactions more private, more flexible, and cheaper.

Schnorr signatures could merge multiple signatures in a multisig transaction into one, making it impossible for outsiders to tell how many parties were behind it. Taproot made complex conditional payments look identical to ordinary transfers on-chain. Tapscript removed the limits on script size and opcode count, letting Bitcoin's scripting language do far more.

From proposal in 2018 to activation in 2021, the entire process took over three years. The only ripple along the way was the choice of activation mechanism: BIP 9 or BIP 8? Should the LOT (lock-in-on-timeout) parameter be set? Should activation be forced after timeout — a replay of 2017's UASF?

In the end, the community settled on a compromise: Speedy Trial. Give miners roughly three months to signal; 90% support locks it in, anything less means failure. No coercion, no standoff, no flipping the table.

June 12, 2021. Block 687,284. During the second difficulty adjustment period, miner signaling crossed the 90% threshold. Taproot locked in. Five months later, on November 14, it activated on schedule.

The whole process was so smooth it was almost boring.

Why? The answer isn't complicated. SegWit had touched interests — block size was directly tied to miners' revenue models, the power dynamics of the entire industry, the very definition of what Bitcoin was. That had been an existential war over "what is Bitcoin?" Taproot moved no one's cheese. Better privacy, higher efficiency, more flexible scripting — who was going to oppose that?

SegWit in 2017 was the product of civil war. Taproot in 2021 was a peaceful upgrade. Same network, four years apart. One left scars. The other barely left a memory.

But Taproot did one thing that nobody noticed at the time.

Tapscript removed the script size limit. Combined with SegWit's witness data discount — witness data counted at 1 weight unit, non-witness data at 4 — in theory, you could stuff nearly 4 MB of arbitrary content into the witness data section of a single transaction. Images, text, code — anything.

That door opened quietly. Then it waited a year.

---

## The Skull

Casey Rodarmor was not the kind of person who gave keynote speeches at conferences.

Before becoming a programmer, his life trajectory was thoroughly random: he'd worked at Mr. Rags clothing store, projected films at a Berkeley cinema, tested games during the Gameboy Advance era. Later he got his GED — the American equivalent of a high school diploma — taught himself to code, went to Google, then spent a stint at Chaincode Labs doing Bitcoin Core development. He later described himself as "a very very minor ex-Bitcoin Core contributor."

That self-assessment was probably accurate. In the Bitcoin developer community, he was no celebrity. Co-host of the SF Bitcoin BitDevs meetup, co-presenter of a podcast with someone called Aaron Redwing — where they discussed Bitcoin, fiat collapse, and backyard chicken farming.

But Rodarmor had one particular quality: he hated boredom. He'd said it himself — "I'm the kind of person that if I'm not working on something, I'm often bored and kind of depressed."

In late 2021, he started turning over an idea.

Could every individual satoshi — one hundred-millionth of a bitcoin — be tracked separately? In Bitcoin's original design, all satoshis were identical, like coins in your pocket: a dollar is a dollar, and nobody cares which one it is. But what if you numbered every coin, in the order it was mined? The first satoshi of the Genesis Block is number 0, the second is number 1, and so on.

He called the system Ordinals. The project was initially named bitcoin-atoms; in January 2022 it was renamed ord.

Numbering was only the first step. The second step was the one that truly changed the game: inscriptions.

The door that Taproot had opened found its purpose here. The technical mechanism of inscriptions worked in two stages — commit and reveal. First, create a Taproot output that commits content to a script; then spend that output, revealing the content on-chain. The content was wrapped in a structure called an "envelope": OP_FALSE OP_IF opens the envelope, data is pushed in, OP_ENDIF closes it. At the script level, this envelope was a no-op — it did nothing — so it broke none of the existing transaction logic.

Elegant? Elegant. And the key point: it was entirely rule-compliant. It did not modify a single Bitcoin consensus rule. It simply used what the rules already allowed.

December 14, 2022. 8:32 PM, UTC. Rodarmor created the first inscription on Bitcoin's mainnet — inscription #0.

He typed the final command into his terminal and pressed Enter. Then he waited. The cursor blinked on the screen; the only sounds in the room were the hum of a fan and his own breathing. Ten minutes later — roughly one block's time — the transaction confirmed. He switched to a block explorer and refreshed. A pixel skull appeared on the screen. Black and white, rough, Día de los Muertos style. From that moment on, it was etched into the Bitcoin blockchain. Forever.

He posted two words on Twitter: "probably nothing."

That "probably nothing" would reshape Bitcoin's landscape over the next year.

---

## The Flood

On January 20, 2023, Rodarmor formally announced that inscriptions were ready for mainnet. Ord version 0.4.0 was released. The first month was relatively calm — programmers and geeks testing the waters, inscribing small images, probing technical limits, showing each other their work on Twitter.

Then things accelerated.

February 1, 2023. The Luxor mining pool mined block 774,628. Size: 3.96 MB. Inside was a 3.94 MB hand-drawn wizard image, occupying 99.5% of the block's space. Sixty-three transactions squeezed into the remaining 0.04 MB. The block served a single purpose: to prove that SegWit plus Taproot's witness discount really could push a block to the theoretical ceiling of nearly 4 MB.

Taproot Wizards. A group of people used one drawing to push Bitcoin's "1 MB limit" — well, effectively ~4 MB after SegWit — to the absolute edge.

If you remember the Scaling War of 2015 to 2017 — two years of arguments, schisms, hats, forks — the core issue was exactly how big a block should be. The big-block camp said 8 MB, 32 MB. The small-block camp said 1 MB was enough, that bigger blocks would harm decentralization. In the end the small-blockers won, SegWit activated, and Bitcoin Cash forked off with its big-block dream.

Six years later, a hand-drawn wizard filled a block to 3.96 MB. No rules were changed.

In March, Yuga Labs — the parent company of the Bored Ape Yacht Club — released TwelveFold, a Bitcoin Ordinals collection. The auction received 3,246 bids; 288 won, for a total of 735.7 BTC — roughly $16.5 million. The highest single bid was 7.1159 BTC, about $159,600.

NFTs — or as Rodarmor preferred to call them, "digital artifacts" — had officially landed on Bitcoin. He hated the term NFT, calling it "too financial for something that's actually quite fun and quite artistic — the name is practically a negation, and it sucks."

The real frenzy began after March 8.

An anonymous developer going by domo — beyond the username and a Twitter account, nobody knew who they were — published the BRC-20 standard. If Ordinals meant inscribing NFTs on Bitcoin, BRC-20 meant issuing tokens on Bitcoin.

The technical principle was so simple it was almost unbelievable. Inscribe a snippet of JSON onto the Bitcoin blockchain. That JSON defines the token's name, total supply, and per-mint limit. Deploy, mint, transfer — all accomplished by inscribing different JSON payloads.

`{"p": "brc-20", "op": "deploy", "tick": "ordi", "max": "21000000", "lim": "1000"}`

No smart contracts. No virtual machine. No state management. Just writing text to the blockchain, then relying on off-chain indexers to read and keep the ledger. Ethereum's ERC-20 was a precision vending machine; BRC-20 was more like tacking a notice on a bulletin board: "I've issued a token called ORDI, total supply 21 million, max 1,000 per mint, first come first served."

Crude? Crude. But it worked.

What happened next — let the numbers speak.

Inscription count: around March 8, it crossed 100,000. April 8, one million — less than three months since launch. End of April, two million. End of May, ten million — over 80% related to BRC-20. August 4, twenty-one million. November, forty million. By late December, approaching fifty million. Early February 2024, sixty million.

If you had opened mempool.space on a certain day in May — Bitcoin's real-time mempool monitor — you would have seen a sight without precedent: the colored blocks representing pending transactions stacked from the bottom of the screen all the way to the top, like a tower of building blocks growing endlessly taller. Refresh every few seconds; the number only went up. Meanwhile, a coffee shop owner in El Salvador opened his wallet to pay a supplier and found the fee quote had gone from a few cents to more than ten dollars — more than the amount he was trying to send. He closed the wallet.

Bitcoin's mempool — the pool of transactions waiting to be confirmed — was jammed solid. On May 7, 2023, unconfirmed transactions exceeded 470,000. Daily transaction volume surged to 682,000 — 39% above the 2017 peak. Each block swelled from the normal ~2,000 transactions to over 4,300.

Fees took off with them. The average transaction fee for the entire month of May was $19.20, up 560% from the previous month. The peak on May 9 exceeded $30.91. On December 17 it reached $38.43 — the highest since April 2021.

Then something happened that hadn't happened since December 2017.

May 7–8, 2023. Around block 788,695, transaction fees surpassed the block subsidy for the first time since 2017. A single block's fee revenue reached 6.701 BTC — exceeding the 6.25 BTC block subsidy. Miners earned more in fees from one block than the mining reward for producing it.

It was the fifth time in history that the average block fee had exceeded the block subsidy. And the first time it had happened outside of a major bull market.

Picture the monitoring screen at a mining pool: a new block is mined, and the revenue column shows 6.701 BTC in fees plus 6.25 BTC in subsidy — nearly 13 BTC total, roughly the income of two normal blocks. Someone posted a screenshot in a miners' Telegram group with three words: "Look at the fees." The chat exploded.

Miners were smiling. For all of 2023, total transaction fee revenue reached $797 million. Roughly $80 million came directly from inscription activity. Since the block reward began halving in 2012, "can fees eventually replace the block subsidy?" had been the central open question of Bitcoin's economic model. Inscriptions provided a brief but powerful answer: yes.

But not everyone was smiling.

---

## A New War

Luke Dashjr had been writing code for Bitcoin since 2011. Twelve years.

He was a devout Catholic. His social media avatar was a cross, his personal website filled with passages about religious faith. His understanding of Bitcoin carried a kind of religious purity: Bitcoin is a peer-to-peer electronic cash system, block space is a scarce public resource, and it should be used for what it is "supposed" to be used for.

On August 25, 2023, he posted on Twitter in all caps:

**"REMINDER: ORDINALS ARE BOTH A SCAM AND AN ATTACK ON BITCOIN."**

On December 6, he posted a longer thread: inscriptions were "exploiting a vulnerability in Bitcoin Core to spam the blockchain." He pointed out that since 2013, Bitcoin Core had allowed users to set a limit on extra data size (-datacarriersize), and that inscriptions circumvented this limit by "disguising data as program code." He called it a bug. He patched it in Bitcoin Knots v25.1 and submitted a PR to Bitcoin Core demanding strict data size limits be broadly applied to all transactions.

This was not rhetoric. He actually wrote the patch (Ordisrespector). He actually implemented filtering in the OCEAN mining pool where he was involved. He intended to purge inscription transactions from the Bitcoin network.

The community erupted.

Those opposed to inscriptions argued: Bitcoin's block space is extremely limited — roughly 4 MB every ten minutes. Those 4 MB represent the only fully decentralized, censorship-resistant ledger space on the planet. Using a vault to store JPEG images was like keeping toilet paper in a safe. Worse still, surging fees were pricing out the people who actually needed Bitcoin for transfers — especially low-value users in developing countries.

Those in favor of inscriptions countered: Bitcoin is permissionless. Who gets to decide which transactions are "legitimate" and which are "spam"? As long as a transaction pays sufficient fees, miners have the economic incentive to include it — this is exactly the mechanism Satoshi designed. How is censoring inscription transactions any different from censoring specific transfer addresses? Filter inscriptions today, CoinJoin transactions tomorrow, addresses from sanctioned countries the day after — where does that road end?

Eric Wall wrote a pointed observation on Twitter: "Taproot adoption has been below 3% for its first 14 months. This week it suddenly hit 99.5%. Not a single Bitcoin maximalist celebrated. I don't understand you people. What do you actually want?"

Udi Wertheimer — a supporter of Taproot Wizards — defended inscriptions: "Real Bitcoiners are happy, fun-loving people. Hal Finney would have loved Bitcoin NFTs. Let's make Bitcoin fun again."

If this scene felt familiar, that's because it was.

The Scaling War of 2015 to 2017 had been fundamentally the same question: **who gets to decide how Bitcoin's block space should be used?** Back then the argument was over block size — how many megabytes. Both sides believed they understood Bitcoin's "true purpose"; both believed the other was destroying it. The inscription debate of 2023 was the sequel. The focus shifted from "how big should blocks be" to "what should go in them."

But there was one crucial difference.

The Scaling War required modifying the protocol — whether enlarging blocks or implementing SegWit, both demanded a network-wide consensus change. Inscriptions did not. Ordinals and BRC-20 used existing Bitcoin features already permitted by the consensus rules. They were legitimate Bitcoin transactions. To "ban" inscriptions, you would actually need to change the protocol.

In 2017, both sides fought over "should we change the rules?" In 2023, one side said "the rules allow me to do this," and the other said "the rules shouldn't allow you to do this."

The tables had turned.

In January 2024, Dashjr's PR to Bitcoin Core was closed. The person who closed it was Ava Chow, one of Bitcoin Core's maintainers. She wrote a single sentence: "It's clear that this PR is controversial and, in its current state, has no hope of reaching a resolution that everyone can accept."

The words sounded measured. The meaning was hard: no one has the authority to unilaterally decide which transactions are "legitimate." That power is distributed across tens of thousands of nodes around the world. You can run a node with a filtering patch, but you cannot force everyone else to do the same. As long as enough nodes and miners don't filter, inscriptions will continue to exist.

Same outcome as 2017. Users voted with their feet.

By the end of 2023, ORDI — the first BRC-20 token — listed on Binance on November 7 and surged 40.8% within 24 hours. In March 2024 it reached an all-time high of $96.17. A token issued via JSON bulletin-board notices briefly surpassed a $1 billion market cap.

---

## Halving Day

April 20, 2024. Bitcoin's fourth halving. The block reward dropped from 6.25 BTC to 3.125 BTC.

In the very block of the halving — block 840,000 — Casey Rodarmor launched his new protocol: Runes.

The timing was no coincidence. He had published the design on his blog on September 25, 2023. The halving block is a once-every-four-years ceremony for the entire network; by launching at that moment, Rodarmor was saying: I plan to be here a long time.

Runes was the evolution of BRC-20. If BRC-20 was tacking notices on a bulletin board, Runes was installing a structured message system on that board. It was based on the UTXO model — consistent with Bitcoin's native architecture — a single transaction could transfer multiple token types to multiple addresses, it was compatible with the Lightning Network, and it solved BRC-20's most criticized problem: UTXO bloat.

The Bitcoin network on halving day was a scene beyond belief.

The ViaBTC mining pool mined block 840,000. Total fees in that block: 37.67 BTC — approximately $2.4 million. Add the 3.125 BTC block subsidy, and the block's total value exceeded 40 BTC, roughly $2.6 million. It became the most expensive block in Bitcoin's history. The fee revenue miners had always dreamed of — on the very day the block reward was cut in half — came roaring back in a way no one had anticipated.

On April 20 itself, the average transaction fee surged to $127.97 — an all-time high, more than seven times the previous day's figure. The halving was supposed to slash miner revenue; the Runes frenzy made it rise instead.

The block reward was halved. But the value of block space multiplied dozens of times over.

---

A decentralized system has no boss. Satoshi wrote the rules, then vanished. What the rules permit is permitted. You may disapprove, but you cannot prevent it.

When Gregory Maxwell wrote the Taproot proposal in 2018, he was thinking about privacy and efficiency. When Pieter Wuille drafted the BIPs in 2019, he was thinking about technical elegance. Neither likely imagined that five years later, their code would be used by a former movie projectionist who'd once worked at Mr. Rags to etch a skull into the blockchain.

But that is the magic of open-source software. The tools you release into the world will be used for things you never imagined.

---

*Before creating Ordinals, Casey Rodarmor had tried to build another project on Bitcoin. It failed. He later said the failure taught him one thing: "Don't try to make Bitcoin do what it doesn't want to do. Ordinals worked because it didn't modify any of Bitcoin's rules — it just used what the rules already allowed." Inscription #0 — that pixel skull, black and white, Día de los Muertos style — was later traded by collectors for over $150,000. His comment at the time was two words: "probably nothing." In Bitcoin's history, the greatest changes have always begun with "probably nothing." The Times headline embedded in the Genesis Block — probably nothing. The two pizzas Laszlo bought for ten thousand bitcoins — probably nothing. Shaolinfry's UASF proposal posted on a forum — probably nothing. Then everything changed.*

---

<div align="center">
<a href="../">🏠 Home</a> |
<a href="https://twitter.com/bhbtc1337">🐦 Follow the Author</a> |
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 Join the Discussion</a>
</div>

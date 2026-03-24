# Genesis: The Cypherpunk Technical Puzzle

![Chapter Image](img/02.png)

> *"We cannot expect governments, corporations, or other large, faceless organizations to grant us privacy. We must defend our own privacy. We must build privacy with cryptography, anonymous remailers, digital signatures, and electronic money."*
> — Eric Hughes, *A Cypherpunk's Manifesto* (March 9, 1993)

Chaum's eCash was dead. But the lesson it left behind was worth more than the product itself: digital currency was technically feasible — you just couldn't entrust its fate to a single company.

In September 1992, three men living in the San Francisco Bay Area sat down for coffee — Eric Hughes, Timothy May, and John Gilmore. They decided to start a mailing list. They called it the Cypherpunk Mailing List.

The name sounded like an underground band. In reality, it was more like an underground weapons laboratory.

At its peak, the mailing list had over 700 subscribers. Julian Assange, who would go on to found WikiLeaks, was a regular lurker. Several technical concepts that later reshaped the internet — from anonymous communication to electronic cash — were first proposed in posts on this very list.

Before the mailing list even existed, Timothy May had already written *The Crypto Anarchist Manifesto*. Its core argument boils down to a single sentence: governments are acquiring unprecedented surveillance powers, and cryptography is the ordinary person's only weapon.

The conviction shared by this group was disarmingly simple: rather than hope governments will restrain themselves, build a system with code that requires no trust at all.

Over the next sixteen years, members of this mailing list — most of whom had never met in person, many hiding behind pseudonyms — each solved one of the technical puzzles that Bitcoin would eventually need. It was like a relay race with no coach. Each runner finished their leg and handed off the baton to the next, none of them knowing where the finish line was.

---

## First Leg: How to Ensure Fairness in a Game With No Referee

In 1997, British cryptographer Adam Back released a small program called Hashcash.

Its original purpose was mundane: fighting spam. The idea was to force anyone sending an email to first have their computer solve a mathematical puzzle — not a hard one, but one that took a few seconds of computation. A normal person sending a single email wouldn't mind waiting a few extra seconds. But a spammer trying to send a million emails, each requiring a few seconds of computation, would find it unbearable.

The idea sounded like a clever trick. But as Back stared at the results, he realized he had solved a problem far deeper than spam.

He had invented something called Proof of Work: using the cost of computational labor to create "expense" in the digital world. The physical world has natural scarcity — one apple cannot be eaten by two people at the same time. The digital world does not — copying a file costs nothing. But if you require every "digital object" to carry proof of real computational work, copying suddenly becomes expensive.

This is the core principle behind Bitcoin mining. Twelve years later, Satoshi Nakamoto would write it into Chapter 4 of the whitepaper. But the inventor was Adam Back, in 1997.

---

## Second Leg: What If Everyone Kept Their Own Ledger

In 1998, a Cypherpunk named Wei Dai posted a proposal to the mailing list: b-money.

The vision behind b-money read like science fiction in 1998. Dai described an electronic cash system with no banks, no government involvement whatsoever. How? By having every participant maintain their own ledger, recording how much money everyone had. If two ledgers disagreed, the one backed by the most Proof of Work would prevail.

How would money be created? Not printed by a central bank — anyone could "mine" new b-money by completing computational work. The more work you did, the more currency you earned.

Sound familiar?

Blockchain, mining, decentralized consensus — the very concepts that would later make Bitcoin famous worldwide, Wei Dai had thought of them all in 1998. What he lacked was the final step: making the system actually run in the real world. b-money remained on paper.

In the Bitcoin whitepaper's references, Satoshi Nakamoto cited Wei Dai's b-money as the very first entry. He was even more direct on the forums: "Bitcoin is an implementation of Wei Dai's b-money proposal."

---

## Third Leg: Digital Gold

That same year — 1998 — Nick Szabo designed Bit Gold.

Szabo was an enigmatic figure. Cryptographer, juris doctor, computer scientist — these three identities combined made him one of the rare few who understood both the technology and the institutions surrounding it.

His Bit Gold design bore a striking resemblance to Bitcoin: Proof of Work to generate digital assets, scarcity guaranteed by computational difficulty, transaction records stored across a distributed network. He even anticipated the need for a mechanism to adjust computational difficulty, ensuring the rate of production wouldn't spiral out of control as computers grew faster — the forerunner of Bitcoin's difficulty adjustment.

Szabo had an insight that preceded everyone else's: what the digital world needed was not "an electronic version of the dollar" but "an electronic version of gold" — an inherently scarce store of value that depended on no issuer.

Bit Gold was never implemented. But the concept of "digital gold" would become Bitcoin's most important identity label two decades later — from the Cyprus crisis to the $100,000 breakthrough, every time someone says "Bitcoin is digital gold," they are echoing an idea Nick Szabo had in 1998.

Because Bit Gold and Bitcoin were so alike, many suspected Szabo was Satoshi Nakamoto. He denied it. But his denial was like his designs — concise, composed, and giving you not one piece of information more than necessary.

---

## Fourth Leg: Making Proof of Work Transferable

In 2004, Hal Finney did something none of the others had managed.

Back had invented Proof of Work, but it was "use once and discard" — you computed it, it got verified once, and that was it. You couldn't hand it to someone else. Dai and Szabo had designed system frameworks, but both remained on paper. Finney bridged the two.

He developed a system called RPOW — Reusable Proof of Work. You used Hashcash to compute a Proof of Work, the system verified it was genuine, and then issued you a token. That token could be transferred to someone else. And they could pass it on to a third person.

For the first time, Proof of Work became "money" that could circulate.

RPOW still had one problem: it required a centralized server to verify and issue tokens. Finney used a "trusted hardware" approach to mitigate the trust issue, but at its core there was still a single point of failure — the same Achilles' heel as Chaum's DigiCash.

Yet RPOW proved something crucial: a Proof of Work-based digital currency was not a fantasy. It could actually run.

Four years later, Finney would become Bitcoin's first user. He posted three words on Twitter — "Running bitcoin" — becoming the first person after Satoshi Nakamoto to bring Bitcoin to life. From RPOW to Bitcoin, Finney didn't just run one leg of the relay. He ran nearly two.

---

## The Puzzle Complete

By 2008, all the pieces were there.

Proof of Work — solved by Back. Distributed ledger — solved by Wei Dai. Digital scarcity — solved by Szabo. Value transfer — solved by Finney. Add to that Ralph Merkle's data verification tree from 1979, Haber and Stornetta's timestamping technique from 1991, and the elliptic curve cryptography that matured through the 1980s — every piece of the puzzle had been polished and refined, scattered across mailing list posts and academic papers.

But no one had put them together.

Back solved the consensus problem but never thought of making a currency. Wei Dai envisioned the entire system but never wrote the code. Szabo's design came closest to completion but lacked the final implementation. Finney built a prototype but depended on a centralized server.

Each of them ran their leg. Each of them saw the direction of the finish line. But none of them crossed it.

Maybe they were too busy. Maybe they felt the timing wasn't right. Maybe they were waiting for the right person.

On October 31, 2008, that person appeared. An email arrived at the cryptography mailing list from an unknown address belonging to someone called "Satoshi Nakamoto." Attached was a nine-page whitepaper.

The final leg of the relay was picked up by someone nobody knew.

---

*Most participants on the Cypherpunk mailing list communicated under pseudonyms — a tradition that directly influenced Satoshi Nakamoto's culture of anonymity. Interestingly, Adam Back went on to found Blockstream, which became one of the most influential companies in the Bitcoin ecosystem. Wei Dai later showed little interest in Bitcoin, developing instead a deep fascination with AI safety. Nick Szabo continued to keep a low profile and remain mysterious. And Hal Finney — the one who came closest to Bitcoin among the four — passed away from ALS in 2014. The image of him writing code with an eye-tracking device in his final years may be the most powerful footnote to the Cypherpunk spirit.*

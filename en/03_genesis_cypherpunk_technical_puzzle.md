# Genesis: The Cypherpunk Technical Puzzle

<picture>
  <source srcset="img_webp/03.webp" type="image/webp">
  <img src="img/03.png" alt="The Cypherpunk Technical Puzzle" loading="lazy" width="800">
</picture>

![author](https://img.shields.io/badge/Author-beihaili-blue)
![date](https://img.shields.io/badge/Date-2025--09%20block%20863500-orange)

> 💡 Revealing the technical preparations before Bitcoin's birth. From the establishment of the Cypherpunk mailing list in 1992 to the gradual refinement of various key technologies, this group of tech geeks spent 20 years forging all the "weapons" needed to create Bitcoin. On the ruins of Chaum's failure, they chose a completely different path.
> 
> Follow me on Twitter: [@bhbtc1337](https://twitter.com/bhbtc1337)
> 
> Join our WeChat discussion group: [Form Link](https://forms.gle/QMBwL6LwZyQew1tX8)
> 
> Open source on GitHub: [Stories-about-Bitcoin](https://github.com/beihaili/Stories-about-Bitcoin)

> *"Privacy is necessary for an open society in the electronic age. Privacy is not secrecy. Privacy is the power to selectively reveal oneself to the world."*  
> ——Eric Hughes, "A Cypherpunk's Manifesto" (March 9, 1993)

While Chaum's ark was sinking, another group of people began to awaken.

They called themselves **Cypherpunks**.

This group shared common characteristics: they were all tech geeks, all believed in the power of cryptography, and all deeply despised government surveillance. More importantly, they didn't fight alone like Chaum, but formed a loose yet vibrant community.

**📅 September 1992, 17 years before Bitcoin's birth**

Three Bay Area programmers—Eric Hughes, Timothy C. May, and John Gilmore—created a mailing list at a gathering in California called the "Cypherpunk Mailing List." This seemingly simple mailing list later became the spiritual holy land of the entire digital currency world.

Timothy May wrote in "The Crypto Anarchist Manifesto":

> *"Computer technology is on the verge of providing the ability for individuals and groups to communicate and interact with each other in a totally anonymous manner. Two persons may exchange messages, conduct business, and negotiate electronic contracts without ever knowing the True Name, or legal identity, of the other."*

This mailing list hosted many figures who would later change the world. They each pioneered different technical fields, paving the way for Bitcoin.

Their belief was simple: **Rather than expecting government self-restraint, use code to build a system that doesn't require trust.**

---

**Proof of Work: "Fair Competition" in the Digital World**

**📅 March 1997, 12 years before Bitcoin's birth**

A British cryptographer named **Adam Back** released a seemingly insignificant small program—**Hashcash**.

At first glance, its purpose was simple: fighting spam email. Its working principle was this: want to send an email? Fine, first have your computer solve a math problem. The problem is simple—keep trying until you find a number that, when combined with your email content, produces a hash value with several leading zeros.

For regular users, sending an email and having the computer calculate for a few seconds was no big deal. But for spam creators wanting to send thousands of emails, this computational cost became unbearable.

Back called this **Proof of Work**. Sounds pretty ordinary, right?

But this seemingly simple "anti-spam tool" actually solved a fundamental problem in the digital world:

> **💡 How to achieve fair consensus without central authority?**

In the physical world, we have "scarcity"—the same apple cannot be owned by two people simultaneously. But in the digital world, copying costs almost nothing. How do you create digital scarcity? How do you prevent double-spending?

Adam Back's genius was using "computational work" to create digital scarcity. You want to obtain something? Sure, first prove you've done real computational work. This work cannot be forged or copied.

12 years later, Satoshi Nakamoto would write this mechanism into Chapter 4 of the Bitcoin whitepaper. Only then did people realize: Adam Back had already invented the core algorithm of Bitcoin mining in 1997!

When Satoshi Nakamoto published the Bitcoin whitepaper on the Cypherpunk mailing list, Adam Back was among the first to reply. He later recalled: "When I saw Satoshi cite my Hashcash paper, I immediately realized the potential of this system."

---

**Distributed Ledger: The Decentralized Accounting Revolution**

**📅 November 1998, 11 years before Bitcoin's birth**

Another Cypherpunk named **Wei Dai** posted an even crazier proposal to the mailing list—**b-money**.

The opening of this proposal was shocking enough:

> *"I am fascinated by Tim May's crypto-anarchy. Unlike the communities traditionally associated with the word 'anarchy,' in a crypto-anarchy the government is not temporarily destroyed but permanently forbidden and permanently unnecessary."*

Wei Dai envisioned a completely decentralized electronic cash system. In this system:

**1. Money Creation** — Anyone can create money by broadcasting the solution to a computational puzzle, with the amount of money created determined by the computational work value.

**2. Transfer Mechanism** — If Alice wants to transfer money to Bob, she simply broadcasts the message "I give Bob X amount," and everyone records this transaction in their ledger.

**3. Distributed Ledger** — Each participant maintains a ledger recording how much money everyone has. If ledgers disagree, the version with the most computational work prevails.

**4. Contract Execution** — The system can also execute smart contracts through collateral and arbitration mechanisms.

Sound familiar? Yes, this is the prototype of today's blockchain and smart contracts!

More importantly, Wei Dai explicitly proposed the concept of **"decentralized consensus."** He recognized that to escape centralized institutions, all participants must agree on the "truth." His proposed solution: **let the version with the most computational work become the truth**.

10 years later, when Satoshi Nakamoto explained Bitcoin on the Bitcointalk forum, he explicitly stated:

> *"Bitcoin is an implementation of Wei Dai's b-money proposal in the Cypherpunk community."*

Wei Dai had already imagined core concepts like decentralized ledgers, proof-of-work mining, and smart contracts in 1998. Satoshi later specifically acknowledged Wei Dai's b-money in the Bitcoin whitepaper's references.

---

**Reusable Proof of Work: The Missing Link**

**📅 August 2004, 5 years before Bitcoin's birth**

Another key figure was **Hal Finney**. This developer of PGP encryption software and veteran of the Cypherpunk movement developed the first **Reusable Proof of Work** (RPOW) system based on hashcash.

Finney solved a crucial problem: how to make proof of work "transferable"?

In Adam Back's Hashcash, each proof of work could only be used once—once you used it to send an email, it was consumed. But for currency, it must be transferable. Money that A spends to B should be spendable by B to C.

Finney's RPOW system introduced a "trusted hardware" server that could verify the validity of proof of work and issue corresponding tokens. These tokens could be transferred between users, generating new tokens with each transfer.

Although RPOW still relied on a centralized server, it proved that proof-of-work currency was achievable. More importantly, it became an important source of inspiration for Satoshi Nakamoto.

Finney later became a key figure in Bitcoin history—he was the first person to download Bitcoin software (besides Satoshi) and the first to receive a Bitcoin transfer. On January 12, 2009, Satoshi transferred 10 bitcoins to Finney, marking humanity's first peer-to-peer digital currency transaction.

---

**Smart Contracts: Code as Law**

**📅 1994, 15 years before Bitcoin's birth**

Another legendary figure was **Nick Szabo**. As early as 1994, he proposed a concept that sounded like science fiction: **Smart Contracts**.

Szabo asked a fundamental question: why must contracts be text on paper? Why can't contract terms be directly embedded in the digital world?

He gave an example: **vending machines**. You insert coins, the machine gives you goods and change—isn't this the simplest smart contract? The machine automatically executes the "pay money → get goods" protocol without any intermediaries, judges, or police.

Szabo further envisioned: what if cars also embedded smart contracts? You pay your car loan on time, the car operates normally; if overdue, the car automatically locks, and the keys return to the bank. Cheaper and more effective than hiring debt collectors.

He summarized four core objectives of smart contracts:

- **🔍 Observability** — All parties can observe contract execution
- **✅ Verifiability** — Ability to prove to arbitrators that contracts were fulfilled or breached
- **🔒 Privacy** — Unrelated third parties cannot peek at contract contents
- **⚡ Enforceability** — Automatic execution, minimizing dependence on external enforcement

This theory later became the theoretical foundation for smart contract platforms like Ethereum.

Interestingly, Szabo also designed his own digital currency scheme—**Bit Gold** (1998). Though never implemented, its design was remarkably similar to Bitcoin, leading some to suspect Nick Szabo was Satoshi Nakamoto himself (though this remains speculation).

---

**Other Pieces of the Cryptographic Puzzle**

The Cypherpunks contributed many other "puzzle pieces":

**🌳 Merkle Trees** (1979): Data structure invented by Ralph Merkle for efficiently verifying large amounts of data integrity. In Bitcoin, each block uses Merkle trees to organize transactions, allowing light nodes to verify transaction validity with minimal data downloads.

**✍️ Elliptic Curve Digital Signatures** (1985): Digital signature algorithms based on elliptic curve cryptography, more efficient than traditional RSA signatures. Bitcoin uses ECDSA to ensure only private key holders can spend bitcoins.

**⏰ Timestamping Services** (1991): Cryptographic technology for timestamping digital files proposed by Stuart Haber and Scott Stornetta. In Bitcoin, proof of work simultaneously serves as timestamps.

**🏛️ Byzantine Fault Tolerance** (1982): Distributed system consensus problems studied by Leslie Lamport and others. Bitcoin's proof-of-work mechanism can be seen as an ingenious solution to the Byzantine Generals Problem.

**📡 P2P Network Protocols**: From early Napster to BitTorrent, decentralized file-sharing networks provided important references for Bitcoin's network architecture.

---

**Code is Law**

These people shared a common belief: **Code is Law**.

They believed that rather than hoping governments would restrain themselves, it was better to use code to build a system that doesn't require trust. They wanted to use mathematics and cryptography to realize Hayek's ideal of free money.

Eric Hughes wrote in "A Cypherpunk's Manifesto":

> *"We cannot expect governments, corporations, or other large, faceless organizations to grant us privacy out of their beneficence. We must defend our own privacy if we expect to have any. We must come together and create systems which allow anonymous transactions to take place."*

This was the Cypherpunk philosophy: **Don't complain about darkness, light a candle, be your own beacon. Don't expect salvation from others, code it yourself.**

By **📅 2008**, almost all technical puzzle pieces were in place:

- ✅ **Proof of Work** → Solved fair consensus problem (Adam Back)
- ✅ **Digital Signatures** → Solved identity verification problem
- ✅ **Timestamping Services** → Solved sequencing problem (Haber & Stornetta)
- ✅ **Distributed Ledger** → Solved decentralized accounting problem (Wei Dai)
- ✅ **Smart Contracts** → Solved automatic execution problem (Nick Szabo)
- ✅ **Reusable Proof of Work** → Solved value transfer problem (Hal Finney)
- ✅ **P2P Networks** → Solved decentralized communication problem
- ✅ **Cryptographic Primitives** → Provided security foundation

These people were like martial arts masters in novels, scattered worldwide but all working toward the same goal. They knew why Chaum failed and knew what needed to be done to succeed.

All weapons had been forged, all technologies were mature. History's stage was set, the actors were in position.

All they needed was the right moment and a genius who could perfectly combine these puzzle pieces.

And that moment was about to arrive. That genius was about to take the stage.

---

*Cypherpunk mailing list members all used anonymous or pseudonymous communications, a tradition that directly influenced Satoshi's anonymous culture. The mailing list had over 700 subscribers at its peak, including future WikiLeaks founder Julian Assange, early Facebook developer Sean Parker, and others. Though Satoshi never posted to the mailing list, he was clearly deeply influenced by its technical philosophy and anonymous culture.*

---

<div align="center">
<a href="../">🏠 Return to Homepage</a> | 
<a href="https://twitter.com/bhbtc1337">🐦 Follow Author</a> | 
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 Join Discussion Group</a>
</div>
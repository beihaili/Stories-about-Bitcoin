# Undercurrents: The Scaling Debate Emerges

Bitcoin had a secret: each block could hold only 1MB of data. When Satoshi Nakamoto added this limit in 2010, nobody cared. Five years later, as the network ground to a halt, everyone started fighting — widen the road, or build an overpass? That fight nearly destroyed Bitcoin.

On July 15, 2010, Satoshi Nakamoto slipped an inconspicuous constraint into Bitcoin's code: a maximum block size of 1MB.

The rationale was straightforward — prevent attackers from creating enormous blocks to overwhelm the network. At the time, Bitcoin processed only a few hundred transactions a day. A 1MB cap was like posting a speed limit on a country lane that saw ten cars daily. Who would care?

Satoshi himself didn't think much of it. He wrote on the forum: "We can phase in a change later if we get closer to needing it."

He failed to anticipate two things. First, those words — "phase in a change later" — would become the most contentious sentence in Bitcoin's history. Second, he would not be around to do the phasing.

---

## Traffic Jam

In the spring of 2015, the bill came due.

Bitcoin's usage had multiplied several times over the previous year. Daily transactions grew from a few thousand to tens of thousands; average block sizes swelled from tens of kilobytes to hundreds. The 1MB ceiling hadn't been hit yet, but you could feel it pressing down.

Users were the first to feel the pain. A Bitcoin transfer that once confirmed in minutes now took ten, sometimes an hour. Fees were climbing too — if you wanted your transaction prioritized, you had to pay more. Like surge pricing on a ride-hailing app, except the surcharge was paid in real money.

BitPay started sweating. Their merchants accepted Bitcoin payments, and slower confirmations meant merchants waiting longer. Higher fees meant small purchases became absurd. A $2 fee on a $3 cup of coffee? That's not a payment — that's a donation.

Satoshi's promise to "phase in a change later if we get closer to needing it" — well, "needing it" had arrived.

The question was: who would execute the change? And how?

---

## The Heir's Proposal

Gavin Andresen thought the answer was simple.

He was Satoshi's chosen successor. In that April 2011 email — "I've moved on to other things" — Satoshi had named him as the person to carry the project forward. For four years, Gavin had served as the technical leader of Bitcoin's development community.

In May 2015, Gavin put forward BIP 101: raise the block size from 1MB straight to 8MB, then automatically double it every two years.

The logic was blunt: the road is jammed, so widen it. Go from two lanes to eight. Internet bandwidth and storage costs were dropping steadily — there was no reason to let the network be strangled by a parameter set half a decade ago.

Gavin wrote on his blog: "Bitcoin's goal is to become a global digital currency. If we artificially limit the network's capacity, we're limiting Bitcoin's potential."

Coinbase CEO Brian Armstrong backed him immediately. BitPay did too. Most companies with any stake in "Bitcoin payments" lined up in support — understandably, since network congestion hit their bottom line directly.

But.

---

## A Different Voice

The other core developers of Bitcoin Core disagreed.

Gregory Maxwell — cryptography expert, one of Bitcoin's most important developers — laid out his objections in detail on the forum: 8MB blocks would dramatically raise the cost of running a full node. Downloading blocks eight times larger, validating eight times more transactions, storing eight times more data — all of that demanded better hardware and faster connections. If only a handful of wealthy institutions could afford to run full nodes, Bitcoin's decentralization was finished.

Pieter Wuille offered an alternative: SegWit — Segregated Witness. It was an elegant technical optimization. Without changing the block size limit at all, it reorganized how transaction data was structured so that each block could fit more transactions. Roughly a 40% capacity increase. Not a radical fix, but a safe one.

And SegWit came with a bonus: it fixed a bug called "transaction malleability." Without that fix, the Lightning Network couldn't function properly. What was the Lightning Network? A payment system built on top of Bitcoin — an overpass, in effect — theoretically capable of handling near-unlimited transaction volume.

Widen the road versus build an overpass. That was the core of the entire debate.

Widening the road was direct, effective, and immediate. The downside: the wider the road, the higher the maintenance costs, and the fewer people who could afford to keep it running.

Building an overpass left the road itself untouched — existing security and decentralization stayed intact. The downside: the overpass existed only on paper. The Lightning Network whitepaper had just been published; a working product was nowhere close.

One side said, "Your overpass is a pipe dream." The other said, "Your wide road will kill decentralization."

Neither could convince the other.

---

## Bitcoin XT and Its Funeral

Gavin couldn't wait any longer. In August 2015, he and fellow developer Mike Hearn launched Bitcoin XT — a Bitcoin client with the 8MB block upgrade built in. If more than 75% of miners ran Bitcoin XT, the network would automatically upgrade.

This was the first time in Bitcoin's history that anyone had attempted to force a protocol change by forking the client software.

Gavin called it "giving the community a chance to choose." Opponents called it "an attack on consensus."

The argument spilled from technical forums onto Reddit. The moderators of r/Bitcoin began deleting posts that supported Bitcoin XT, on the grounds that XT counted as an "altcoin" and couldn't be discussed on a Bitcoin forum. Furious users who'd been censored founded a new subreddit: r/btc.

From that point on, the Bitcoin community had two Reddits: r/Bitcoin and r/btc, representing the small-block and big-block camps respectively. That rift persists to this day.

Bitcoin XT itself did not live long. By the end of 2015, fewer than 10% of nodes were running it — far below the 75% threshold. Most miners refused to risk splitting the network. Bitcoin Core's authority carried weight, too — most people still trusted the programmers who had been writing the code for years.

One evening in January 2016, Mike Hearn sat at his computer, fingers hovering above the keyboard. He stared at the title of the article he had just finished writing: "The Resolution of the Bitcoin Experiment."

He took a deep breath and clicked "Publish."

The article's conclusion boiled down to four words: Bitcoin has failed.

He wrote that Bitcoin was controlled by a small group of developers, that the community could not reach consensus, that the network could not scale. Then he opened an exchange and put every bitcoin he owned — every last one — up for sale.

The article was picked up by *The New York Times*. Bitcoin's price dropped over 10% that day. One of Bitcoin's earliest core developers had publicly declared defeat and sold his entire stake.

---

## The Calm Before the Storm

Mike Hearn was gone. Bitcoin XT was dead. But the problem remained unsolved.

The 1MB limit was still there. Blocks were getting fuller. Fees were getting higher. Transactions were getting slower.

Gavin Andresen's influence plummeted after the XT debacle. The man Satoshi himself had anointed as heir, having picked the wrong side in the Scaling War — or so it seemed at the time — was gradually pushed to the margins. Later, when he publicly endorsed Craig Wright as Satoshi Nakamoto, he lost the community's trust entirely. From Satoshi's spokesman to the community's outcast — that reversal was more brutal than any blockchain technology.

But the debate was far from over. After XT's failure, the big-block camp rolled out Bitcoin Classic (a 2MB proposal), then Bitcoin Unlimited (a proposal for blocks with no size limit). Each one failed, and each one deepened the fracture in the community.

The small-block camp pressed on with SegWit. Development proceeded steadily, but miners — especially Chinese miners led by Bitmain's Jihan Wu — refused to activate it. They had their reasons: SegWit would undermine one of Bitmain's patented technologies (AsicBoost), and bigger blocks aligned better with miners' commercial interests (more transactions meant more fees).

Every player on the board refused to budge. Developers insisted on SegWit. Miners refused to activate it. Entrepreneurs tried to mediate. Users hurled insults at each other on Reddit.

This stalemate would drag on until 2017. Then an anonymous developer — Shaolinfry — would propose an idea called UASF, users would don their hats and take to the streets (not literally, but spiritually), and a true war of independence would begin.

But that is a story for later.

---

*The single line of code Satoshi added in 2010 to impose the 1MB block limit is the most discussed line in Bitcoin's entire codebase. It consists of just a few characters, yet it ignited a global debate spanning years and involving billions of dollars. Sometimes, writing one line of code can change the world more than writing an entire book — but deleting that line turns out to be far harder than writing one, too.*

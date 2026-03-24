# Civil War and Independence: The Scaling War Intensifies

In the first half of 2017, Bitcoin was choking. A single transaction cost four dollars in fees — buying a cup of coffee meant paying nearly as much in fees as the coffee itself. By year's end that figure would hit fifty. The community's technical arguments had hardened into factional standoffs: Core developers versus miners, SegWit versus bigger blocks. The New York Agreement's compromise was rejected by both sides simultaneously. The war was escalating — and the solution, UASF, was brewing in the shadows.

In the spring of 2017, a programmer in New York wanted to buy a cup of coffee with Bitcoin. He opened his wallet and saw the recommended fee: four dollars. The coffee cost five. The fee was nearly as much as the coffee. He closed the wallet. By the end of the year, that same transaction would cost over fifty dollars.

XT had failed. Classic had failed. Unlimited was still floundering. Mike Hearn was gone. Gavin had been sidelined. But that one line of code — the 1MB limit — was still there. Blocks filled up one after another, like a highway gridlocked bumper to bumper.

By the first half of 2017, the situation had deteriorated beyond the point of procrastination. More than 200,000 transactions sat in the mempool every day, waiting in line. Confirmation times stretched from minutes to hours; some transactions waited for days. Coinbase's customer support fielded thousands of "why hasn't my transaction confirmed yet" complaints daily.

The very first line of the whitepaper reads: "A Peer-to-Peer Electronic Cash System." Now this "cash system" was too expensive to buy a cup of coffee.

---

## Two Camps

One evening in early 2017, Bitcoin Core developer Luke Dashjr opened Reddit and found his photograph Photoshopped onto a Nazi officer. The poster was a big-block supporter. He screenshot it and dropped it into a developer chat, without comment. The chat went silent for three seconds. Then someone replied with a single line: "At least the Photoshop isn't very convincing."

Nobody laughed. Two years earlier these people could argue about technical details until three in the morning and then head to the same bar for drinks. Now they were no longer colleagues. They were enemies.

The core of the dispute was, on the surface, not complicated. The Core camp wanted SegWit — leave the block size unchanged, optimize the data structure to boost capacity by roughly 40%, fix the transaction malleability bug along the way, and pave the road for the Lightning Network. Decentralization was the non-negotiable principle: if blocks got too big, ordinary people couldn't run full nodes, and Bitcoin would become just another banking system.

On the other side stood Jihan Wu. He controlled Bitmain — the world's largest mining hardware manufacturer — plus several major mining pools. His solution was blunt: make the blocks bigger. The network was clogged, users were furious. Bitcoin Unlimited even proposed blocks with no size cap at all.

On the technical merits, both sides had a point.

But Jihan Wu had a reason to oppose SegWit that he was less eager to discuss publicly: it would neutralize a patented technology called AsicBoost — an optimization that gave Bitmain's own miners a roughly 15% speed advantage over the competition. Once SegWit activated, that edge would vanish.

Core developers made this discovery public. Jihan Wu fired back, calling Core a "technical dictatorship."

The forums spiraled out of control. On BitcoinTalk, people sent death threats to developers in the opposing camp. r/Bitcoin deleted any post supporting bigger blocks, branding it "altcoin promotion." Over on r/btc, Core developers were drawn as cartoon villains. A community that was supposed to discuss cryptography had turned into a political movement.

This was no longer a debate. It was a war.

---

## The New York Agreement

In May 2017, a group of people attempted one last shot at peace.

Barry Silbert of Digital Currency Group convened Bitcoin's major industry players — exchanges, miners, wallet companies — for a closed-door meeting in New York. The goal was to find a compromise both sides could accept.

The result was the "New York Agreement," also known as SegWit2x: activate SegWit first (satisfying the Core supporters), then increase the block size from 1MB to 2MB three months later (satisfying the big-block camp).

The signatories represented over 80% of Bitcoin's global hashrate and the majority of its transaction volume. It looked like a perfect compromise.

But it had one fatal flaw: the Bitcoin Core development team was not in the room.

They hadn't been invited. Or rather, they had refused to attend. Core developers held that any protocol upgrade should be decided through an open technical discussion process — not voted on by corporate executives in a hotel conference room in New York.

"That's not how Bitcoin works," one Core developer wrote on the forum. "Bitcoin's rules aren't made by miners and CEOs behind closed doors. They're decided by the users who run nodes."

The New York Agreement was doomed from the day it was born. The big-block camp thought it wasn't bold enough — only 2MB? A drop in the bucket. The small-block camp saw it as a corporate cartel hijacking Bitcoin's governance. The moderates — if any still existed — discovered that neither side would accept their compromise.

---

## Bitcoin Unlimited's Self-Destruction

The big-block camp made a fatal error at the worst possible moment.

On the afternoon of March 15, 2017, an operations engineer at a mining facility in Shenzhen was staring at three monitors, the tea at his elbow long since gone cold.

The logs on his screen suddenly stopped. Not slowed down — stopped. Process exited. Connections dropped. All that remained in the terminal was a blinking cursor. Dozens of servers in the machine room still hummed with spinning fans, but the Bitcoin Unlimited nodes he managed were dead. Unnervingly silent. He restarted once — the logs scrolled a few lines, then stopped. He restarted again — same crash. He picked up his phone. The WeChat group had already exploded.

Across the globe, BU nodes went down in rapid succession at the same time. Someone had found a bug: an attacker only needed to send a single specially crafted packet, and any BU node would crash instantly. Within hours, the majority of BU nodes worldwide had been swept off the network.

For the big-block camp, this was devastating. You had been arguing that Core's code was too conservative, too restrictive of innovation — and your alternative couldn't even defend against a remote crash vulnerability? You wanted people to trust your code with a network worth tens of billions of dollars?

Mockery flooded the forums. Someone turned BU's bug report screenshots into memes. A Core developer posted a one-word tweet: "lol."

BU patched the bug. But you can't patch credibility. From that point on, support for Bitcoin Unlimited as a viable alternative noticeably faded.

---

## The Calm Before the Storm

By July 2017, every attempt at compromise had failed.

The New York Agreement's SegWit2x was still being pushed forward, but the battle lines between supporters and opponents were firmly drawn. Bitcoin Unlimited was critically wounded. Core developers' SegWit proposal had been ready since 2015, but miners had refused to activate it the entire time.

Network congestion was worsening. Fees were hitting new highs. Users' patience was running out.

And in the shadows, an anonymous developer called Shaolinfry had already posted the UASF proposal on the forums. The hats were being printed. The list of supporters was growing.

The Bitcoin community was about to face the most dramatic day in its history — August 1st.

But before that, there was a month of agony to endure. Everyone knew a split was inevitable, but nobody knew what form it would take, or who would win.

Someone posted a thread on the forum with a title that was a single sentence: "No matter what happens on August 1st, Bitcoin will never be the same."

He was right.

---

*The New York Agreement of May 2017 was signed by 58 companies representing 83% of global Bitcoin hashrate. The agreement was ultimately abandoned in November — the SegWit portion was successfully activated (under UASF pressure), but the 2x portion (doubling the block size to 2MB) was scrapped for lack of community consensus. Fifty-eight companies' joint signatures lost to a few thousand anonymous users wearing hats. It was perhaps the most powerful demonstration of "decentralized governance" in practice.*

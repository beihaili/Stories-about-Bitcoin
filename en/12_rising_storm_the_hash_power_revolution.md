# Rising Storm: The Hash Power Revolution

In the fall of 2010, Laszlo Hanyecz did something that changed Bitcoin history — again.

The first time, he bought two pizzas for ten thousand bitcoins. This time it was less conspicuous, but the impact may have been even greater.

He was sitting at home in Florida, staring at the mining program plodding along on his CPU — roughly ten million hash calculations per second. Then a thought struck him: mining is essentially running the same mathematical formula over and over until you stumble upon a result that meets the criteria. Each calculation is independent. None depends on the one before it.

Isn't that exactly what a graphics card was born to do?

The GPU — the graphics processing unit — was designed to render images: computing the color of thousands upon thousands of pixels simultaneously. To accomplish this, GPUs pack hundreds, sometimes thousands, of small processing cores. Each core is weaker than a CPU, but sheer numbers overwhelm it.

Laszlo spent a few sleepless nights writing GPU mining code.

When the test results came in, he may have frozen for a moment — just like when he saw those two boxes of pizza arrive.

CPU: 10 million hashes per second. GPU: 200 million hashes per second.

Twenty times faster.

---

## Graphics Cards Sell Out

Laszlo posted his code and benchmarks on the BitcoinTalk forum. The title was modest: "Mining with OpenCL is much faster than CPU."

The post was not modest. It detonated the forum.

Within days, every Bitcoin miner in the world — a few hundred people at the time — was scrambling to do the same thing: buy graphics cards. Not for gaming — for mining.

ATI (AMD) Radeon 5870 and 5970 cards became the miners' darlings, because ATI's architecture was better suited to the purely parallel computation that mining demands. NVIDIA cards held their own in gaming, but their mining efficiency lagged far behind ATI. A strange new phenomenon appeared in computer shops: buyers of high-end graphics cards stopped asking "what games can it run?" and started asking "what's the hash rate?"

AMD's GPU sales skyrocketed. Certain models sold out entirely. AMD itself was baffled at first — they assumed some blockbuster game had just launched. It wasn't until later that they realized: a peculiar tribe of people was using graphics cards to "mine" something called Bitcoin.

The forums filled with DIY mining rig posts. One person crammed four GPUs into a single case, cooling fans screaming like a helicopter lifting off. Another set up a mining rig on the balcony and used it for heating in winter (this was no joke — several high-end GPUs running at full load generate a remarkable amount of heat).

It was the golden age of home mining. Spend a few thousand dollars on graphics cards, and you could mine dozens of bitcoins a day from your living room. A single bitcoin was worth only a few cents to a few dollars at the time, but if you had saved those coins instead of selling them — never mind, the math only leads to heartbreak.

---

## The Lottery Problem

But GPU mining brought a new headache: income felt like playing the lottery.

The reward mechanism was winner-take-all — only the miner who actually discovered a new block received the 50-bitcoin reward. Everyone else? Zero. It was like a crowd of people all buying lottery tickets, with only one winner.

When a few dozen people were mining on CPUs, each person's odds were reasonable. But after GPUs entered the picture, total network hash power surged, and any individual miner's probability of winning plummeted. You might mine for a month straight and hit nothing, then strike gold one random day — or you might go three months with nothing at all. The electricity bill, however, didn't care whether you won. It arrived every month without fail.

Complaints began appearing on the forum: "Two months of mining, not a single block. Electricity bill paid for nothing."

A Czech programmer named Marek Palatinus — screen name "slush" — read those posts and thought of a simple solution: pool everyone's hash power together. When the pool finds a block, the reward is split in proportion to each person's contributed hash power.

Just like a group of coworkers buying lottery tickets together. Win, and everyone splits the pot by their share. Buy alone and you might never win in your lifetime; buy together and you collect a little every month.

On November 27, 2010, the world's first Bitcoin mining pool — Slush Pool — went live. Marek posted on the forum, his tone understated: "I built a mining pool. Feel free to try it."

Within months, Slush Pool's hash power accounted for over 10% of the entire network. Small miners finally had a steady income.

---

## The Paradox

But mining pools raised a question that made the cypherpunks frown.

Satoshi's whitepaper described "one-CPU-one-vote" — each participant votes with their own computer, votes proportional to hash power. The implicit assumption was that hash power would be distributed, with no single party controlling a majority.

GPUs broke the first layer of that assumption: not all "votes" were equal anymore. A person with a graphics card cast twenty votes for every one cast by a CPU miner.

Mining pools broke the second layer: hash power began to concentrate. A handful of large pools collectively controlled more than half the network's total hash power. Miners could freely join or leave any pool, but at any given moment, a small number of pool operators wielded enormous power.

If a single pool controlled more than 51% of hash power, it could theoretically tamper with transaction records — the so-called "51% attack."

The decentralized voting system Satoshi envisioned had begun drifting toward oligarchy in under two years.

This was nobody's conspiracy. It was economics. When mining is profitable, people seek the most efficient methods. GPUs are more efficient than CPUs, so people switch to GPUs. Cooperative mining is more efficient than going solo, so people form pools. Each decision is perfectly rational at the individual level, but in aggregate they produce a centralizing trend.

By late 2011, the first FPGA (field-programmable gate array) mining devices appeared — several times faster than GPUs, but also several times more expensive. This was merely a transitional phase. Everyone knew the ultimate weapon was the ASIC — a custom chip designed exclusively for mining. Once ASICs arrived, GPUs would be rendered obsolete just as CPUs had been before them.

From CPU to GPU to FPGA to ASIC, each upgrade raised the barrier to entry, demanded greater investment, and narrowed the field of participants. The egalitarian dream of "one person, one CPU, one vote" had, within two years, become the reality of "whoever can afford better hardware gets more votes."

This was the first time Bitcoin confronted a problem it may never fully solve: the direction of technological progress and the ideal of decentralization are sometimes at odds.

---

But let us look at it from another angle.

In 2010, the entire Bitcoin network's hash power was probably less than that of a single modern ASIC miner. A determined individual could rent a few servers and launch a 51% attack. The network's security was as fragile as paper.

By the end of 2012, total network hash power had increased several thousandfold. The cost of attacking the network went from tens of thousands of dollars to millions. The GPU miners and mining pools — whether driven by ideology or profit — had poured real money into electricity and hardware, building a wall around Bitcoin's security that was orders of magnitude thicker.

Satoshi's "one-CPU-one-vote" was a beautiful starting point. But what kept Bitcoin alive was not the beauty of the starting point — it was the thickness of the wall.

Beautiful ideals need hard reality to protect them. That was the first lesson the hash power revolution taught Bitcoin.

---

*Laszlo Hanyecz holds two records in Bitcoin history: the first person to buy a physical good with Bitcoin (two pizzas), and the first person to mine Bitcoin with a GPU. He later said discovering GPU mining excited him more than the pizza — "The pizza just proved Bitcoin could be spent. GPU mining proved Bitcoin could evolve." In 2018, he bought two more pizzas using the Lightning Network. The man and pizza, it seems, share some kind of special fate.*

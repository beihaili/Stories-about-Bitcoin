# Suit Revolution: Lightning Strikes

![配图](img/ch27.png)

![status](https://img.shields.io/badge/状态-已完成-success)
![author](https://img.shields.io/badge/作者-beihaili-blue)

> 💡 The scaling war raged for two years. One side wanted to widen the road; the other wanted to build a bridge above it. The road-wideners walked away. Those who stayed began building the bridge — three teams, three programming languages, hammering out a single set of blueprints in Milan. Six years later, a fishing village in Central America used that bridge to reinvent the act of spending money. Satoshi Nakamoto titled his white paper "A Peer-to-Peer Electronic Cash System" — the Lightning Network made those seven words true for the first time.
>
> Follow me on Twitter: [@bhbtc1337](https://twitter.com/bhbtc1337)
>
> Join our WeChat group: [Form link](https://forms.gle/QMBwL6LwZyQew1tX8)
>
> Open-sourced on GitHub: [Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3)

2014. San Francisco.

Two Bitcoin fanatics kept running into each other at the same kind of gatherings — the kind where pizza was the main course and protocol vulnerabilities were the main conversation. One was Joseph Poon, a Brooklyn native with dual master's degrees in computer science and electrical engineering from Georgia Tech, formerly a control engineer at Intel maintaining the kind of architecture systems complex enough to give you a headache. The other was Tadge Dryja, who held a computer engineering degree from Carnegie Mellon but had gone and gotten a photography MFA from the School of Visual Arts in New York — a man whose left brain and right brain were at war. Dryja had taught at Mie University in Japan, discovered Bitcoin there, then returned to San Francisco to become CTO of Mirror, a Bitcoin smart-contract startup.

Their conversations always circled back to the same problem: Bitcoin could process three to seven transactions per second. Visa did twenty-four thousand.

Seven.

That number was a wall. The scaling war was fought over this wall — the big-block camp wanted to tear it down and rebuild it bigger; the small-block camp wanted to build a bridge over it. Poon and Dryja were bridge-builders, but they didn't waste time arguing. On weekends, the two of them holed up in an informal co-working space in San Francisco, sketching diagrams on whiteboards, working through equations, writing code.

Six months later, they presented their work at SF Bitcoin Devs.

In February 2015, the initial draft was published. On January 14, 2016, the formal paper went online. The title was long, but every word earned its place: *The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments*.

The core idea can be explained with a single analogy.

Imagine you buy coffee from the shop downstairs every day. One latte, every morning. If every cup required a full bank transfer — fill out a form, review, clearing, settlement — both of you would lose your minds. In real life, you don't do that. You open a tab: deposit two hundred bucks at the start of the month, deduct one coffee per day, settle up at month's end.

The Lightning Network is that tab. Two people open a "payment channel" on the Bitcoin main chain, each locking some bitcoin into it. After that, all transactions are tallied inside the channel, off-chain. Only the final settlement gets written back to the main chain. A hundred transactions, just two on-chain operations: open the channel, close the channel.

The real elegance is in the routing. You have a channel with the coffee shop. The coffee shop has a channel with the bakery. You can pay the bakery through the coffee shop as a relay, even though you have no direct channel with the bakery. In theory, as long as there are enough channels and liquidity in the network, anyone can pay anyone. Instant settlement. Fees near zero. No seven-transactions-per-second bottleneck.

When the paper came out, the scaling debate was still in its early stages. The Lightning Network generated interest in technical circles, but in the broader Bitcoin world, it was just a theoretical concept that "might work someday."

That word — "might" — would take three years to remove. And removing it required one precondition.

---

## A Jammed Lock

The Lightning Network had a fatal dependency: SegWit.

The payment channel's security model relied on "pre-signed transactions" — when a channel opened, both parties signed settlement transactions in advance. These pre-signed transactions were linked to each other through Bitcoin's transaction ID (TXID). If the TXID was stable, everything worked fine.

But before SegWit, Bitcoin had a nasty design flaw: transaction malleability.

In plain English: you broadcast a Bitcoin transaction, and it gets a unique ID number — the TXID. But before a miner packages and confirms it, someone can quietly tweak certain bits in the signature. The transaction content doesn't change. The amount doesn't change. But the ID number does. For a normal transfer, no big deal — the money still arrives. But inside a Lightning channel, commitment transactions are chained together, each one referencing the previous one's TXID. If the first transaction's ID gets altered, every subsequent one is invalidated.

Think of it this way: you sign a lease with your landlord, stipulating that "the renewal clause in Contract No. A001 automatically takes effect in year three." Someone changes the original contract number from A001 to A002 — same content, different number. In year three, you show up with A001 to renew. The landlord says: I have no record of an A001.

SegWit's solution: separate the signature data from the transaction body, placing it in a standalone "witness" section. Signatures no longer participate in TXID calculation. No matter how the signature is altered, the TXID stays the same. The lock was fixed.

Without SegWit, there could be no secure Lightning Network.

This was one of the hidden storylines of the scaling war that most people missed. The people wearing UASF hats and cheering SegWit activation on the forums — many of them didn't fully understand what they were applauding. They thought they'd won a debate about block size. In reality, they had opened a door to an entirely new architecture.

On August 24, 2017, SegWit activated on the Bitcoin mainnet. The door was open.

---

## Three Teams, One Blueprint

Turning a paper into running code takes more than brains. It takes money, time, patience, and a mountain of engineering details — a single sentence in the paper like "this can be achieved via hash time-locked contracts" might translate into tens of thousands of lines of code.

Three teams began the work almost simultaneously.

The soul of the first team was Rusty Russell. Australian. A full-time free-software developer since the 1990s. If you've ever used Linux, chances are you've used something he wrote — he built iptables for the Linux kernel, the system that runs the firewall on virtually every Linux server in existence. He also rewrote Linux's module subsystem and was one of the earliest programmers paid to work on the kernel. Russell's wife encouraged him to take a break from kernel work, so he went and studied Bitcoin. In 2015 he joined Blockstream and began writing c-lightning full-time — in C, chasing bare-metal efficiency. A geek's geek.

Russell didn't just write code. He chaired the drafting of the BOLT specification — BOLT, standing for Basis of Lightning Technology, the universal protocol standard for the Lightning Network. Without BOLT, the three teams wouldn't have built one network; they'd have built three incompatible islands. In October 2016, after the Scaling Bitcoin conference in Milan, more than twelve developers from ACINQ, Blockstream, Lightning Labs, and other teams stayed behind, locked themselves in a room for two days, and hammered out BOLT's overall framework. Russell served as specification chair, grinding through message formats, routing algorithms, and error handling one clause at a time on mailing lists and GitHub issues. The process was neither romantic nor dramatic — just engineers doing engineer things. But without that blueprint, nothing that followed would exist.

The second team was Lightning Labs, founded in January 2016. Its founding members included the two white paper authors, Poon and Dryja (Dryja left in January 2017 to join the MIT Digital Currency Initiative as a research scientist), along with two key figures.

Elizabeth Stark. Brooklyn native. Harvard Law JD. She didn't write code. Earlier in her career, she had been a central figure in the anti-SOPA/PIPA internet freedom movement — mobilizing eighteen million people worldwide to sign petitions against internet censorship legislation. From anti-censorship to Bitcoin, the logic was clear: she had an instinctive revulsion toward centralized power controlling the flow of information. Stark channeled Silicon Valley's money and attention toward the Lightning Network, raising $82.5 million across three funding rounds, with Jack Dorsey leading the seed round. She became the Lightning Network's most recognizable public face. The one writing the code was Olaoluwa Osuntokun, known online as roasbeef — a BS and MS in computer science from UC Santa Barbara, lead developer of lnd, Forbes 30 Under 30 in 2019. If Stark was Lightning Labs' face, Osuntokun was its hands.

The third team was in Paris. ACINQ, founded by Fabrice Drouin and Pierre-Marie Padiou — one an Imperial College–trained distributed systems architect, the other an engineer who had worked in Société Générale's investment banking division. They wrote Eclair in Scala and launched the Phoenix wallet in 2019, which became one of the easiest Lightning wallets for ordinary users to pick up. The French don't make a fuss, but they get things done.

Three teams, three languages (C, Go, Scala), three technical philosophies. But they had to be interoperable.

December 6, 2017. The critical moment arrived.

Three implementations — Eclair, c-lightning, and lnd — completed the first cross-implementation interoperability test on the Bitcoin mainnet. An Eclair-based coffee shop application (called Starblocks) received a payment from an lnd mobile wallet user, routed through a c-lightning node. The nodes were distributed across Asia, Europe, South America, and North America.

One payment, three codebases, four continents.

The developers' joint statement was a single sentence, but it carried weight: "Interoperability makes a single Lightning Network possible — payments can be seamlessly routed between different implementations without being siloed or incompatible."

The blueprint had become a bridge.

---

## Stickers, Torches, and Pizza

On December 28, 2017, an engineer at Bitrefill named Alex Bosworth completed the first known mainnet commercial transaction on the Lightning Network — he topped up his phone. 0.00127 BTC, zero fees, instant. The amount was tiny, but it proved one thing: this was no longer a simulation on testnet.

Over the following weeks, the Lightning Network's first "merchants" appeared. On January 16, 2018, Blockstream opened an online store — the Blockstream Store — selling stickers and T-shirts printed with the Lightning logo. The only accepted payment method: Lightning Network. The stickers were worth next to nothing, but the act of buying them was a statement. During the scaling war, "the fee for a cup of coffee costs more than the coffee" had been one of the big-block camp's most devastating arguments against Bitcoin. Now, buying stickers on the Lightning Network cost less than a penny in fees.

Then a transaction with even greater symbolic weight took place.

February 25, 2018. Florida.

Remember Laszlo Hanyecz? The man who, eight years earlier, had paid 10,000 bitcoin for two Papa John's pizzas — pioneer of GPU mining, developer of Bitcoin's macOS client, creator of "Bitcoin Pizza Day." He was mentioned in the fun fact at the end of the value discovery chapter, buying pizza again eight years later. Now, let me unfold the details of that transaction.

The process had a distinctly geeky sense of ceremony: he opened a Lightning payment channel with a friend, the friend placed the order at Papa John's on his behalf, and the delivery driver was told that the pizzas could only be handed over if Hanyecz presented the first four and last four characters of the payment proof code. Hanyecz pulled out a notebook with the string of digits written on it. The delivery driver checked them, nodded, and handed over two cardboard boxes wafting the smell of cheese and peppers.

Two pizzas, 0.00649 BTC, roughly $67, fees of about six cents.

Laszlo's comment was characteristically understated: "I wanted to prove that you could still buy pizza with Lightning. If a $50 pizza costs $100 in fees, there's no point. The advantage of Lightning is that you get Bitcoin's security with instant transfers."

On January 19, 2019, a larger experiment began.

An anonymous Bitcoin enthusiast called Hodlonaut launched the "Lightning Torch." The rules were simple: he placed 100,000 satoshis (about $3.50) onto the Lightning Network and passed it to someone he trusted. That person added 10,000 satoshis and passed it to the next trusted person. And so on.

The torch traveled roughly 275 to 292 hops across more than sixty countries. Twitter founder Jack Dorsey carried the torch, then passed it to Elizabeth Stark. Litecoin creator Charlie Lee carried it. Binance CEO Changpeng Zhao carried it. Name after name strung together like a glowing chain — each hop a real Lightning transaction, each handoff a live test of the network's reliability.

In the end, the torch accumulated to 0.41 BTC and was donated to Bitcoin Venezuela — an organization promoting Bitcoin education and hardware development in a country whose economy had collapsed. A community game turned into a global stress test, and then into a charitable donation.

By the end of 2018, Lightning Network capacity exceeded 500 BTC, with roughly 2,100 active nodes and over 15,000 channels. By the end of 2021, capacity had grown to 3,233 BTC, nodes surpassed 19,000, and channels reached approximately 73,000. A six-fold increase in three years.

But numbers are just numbers. In 2018 and 2019, the Lightning Network was still a geek's toy. Opening a channel required technical know-how. Managing liquidity meant understanding routing. Wallet interfaces looked like command-line terminals. It was like the internet in the 1990s — it worked, but only techies used it.

To go from a geek's toy to an ordinary person's tool, it would take one person and one place.

---

## The Beach and the Tears

El Zonte. Pacific coast of El Salvador, La Libertad department, forty-two kilometers from the capital San Salvador. Population: 3,000. Dirt roads, a flawed drainage system, no bank branches. Most residents had no bank accounts. The waves were good.

Around 2004, an American named Mike Peterson arrived. San Diego native, economics degree, former financial planner — but he loved surfing. A surf trip brought him through El Zonte, and he "fell in love with the warm water, the beautiful waves, and especially the people" — then never left. He did community work in the village, founded the nonprofit Missionsake in 2015, funding scholarships and creating jobs. He discovered a cruel cycle: young people left the village to find work elsewhere, the children left behind had no one looking after them, and gangs stepped in to recruit them.

In early 2019, the tool to break the cycle fell from the sky.

An anonymous Californian discovered a forgotten USB drive. On it were bitcoins purchased years ago at a few cents apiece, now worth a staggering sum. Through a church connection, this person reached Peterson and proposed a multi-year, six-figure donation. But there was one condition: the money had to be distributed as bitcoin, not converted to dollars. The donor's reasoning was simple — "Actual use of Bitcoin is what will truly benefit people."

Peterson and community leaders used the funds to create the Bitcoin Beach Initiative. They distributed roughly $35 per month in bitcoin to hundreds of families in the village and created dozens of jobs. Then they began persuading merchants, one by one, to accept bitcoin.

The first to say yes was Mama Rosa — the village restaurant owner who sold pupusas, El Salvador's traditional corn cakes. Then the coffee stand, the electrician, the dentist. Around forty-five merchants in all. In October 2020, Galoy developed the Bitcoin Beach Wallet for El Zonte — later renamed Blink — an open-source Lightning wallet designed specifically for community daily payments. Fishermen sold fish for bitcoin, spent bitcoin at Mama Rosa's for pupusas, and Mama Rosa spent bitcoin on rent. Later, she used her bitcoin earnings to buy a truck and two cows.

The Lightning Network was the key that made this experiment possible. Daily spending in El Zonte was minuscule — a pupusa cost less than a dollar. If every transaction went through the main chain, fees would cost more than the food itself. The Lightning Network brought each payment under a penny, settlement under a second. Bitcoin Beach — that's what the outside world started calling El Zonte. Bloomberg sent reporters. CBS *60 Minutes* came to film a feature.

In early 2021, a twenty-seven-year-old from Chicago arrived.

Jack Mallers, born April 9, 1994. His grandfather, William J. Mallers Sr., was the youngest chairman in the history of the Chicago Board of Trade (CBOT) and is considered a key figure in the creation of the Chicago Board Options Exchange (CBOE). His father also served as CBOT chairman and co-founded one of Chicago's largest futures brokerage firms. Financial trading was dinner-table conversation in the Mallers household. But Jack didn't fit the Wall Street mold — he topped the U.S. Chess Federation's age-group ratings in kindergarten, won the state championship in third grade, then lost interest. He dropped out of college within a year and enrolled in a coding bootcamp. In 2013, his father introduced him to Bitcoin when it was trading below $100.

In 2017, he built the Zap Lightning wallet. In January 2020, he founded Strike — a cross-border payment app built on the Lightning Network. Its core function sounded almost too simple: you load dollars in the United States, and the recipient in another country receives local currency. The "carrier" in between is the Lightning Network. Seconds. Fees near zero. The user doesn't even need to know Bitcoin is involved.

He came to El Zonte looking for a proving ground. There, he witnessed the Lightning Network operating in real life — not a demo, not a simulation, but a real person at a real stall scanning a phone to buy a real lunch. Western Union took five days and skimmed 10% in fees. Strike settled in seconds, virtually free. This wasn't a comparison of technical specifications. It was the difference between a mother waiting or not waiting for money to feed her children.

Mallers' social media posts about El Zonte were spotted by Salvadoran president Bukele's brother. He reached out via Twitter DM. Mallers initially thought he was in trouble. But the topic the brother wanted to discuss was financial inclusion. Two days later, word came from the presidential office: they were planning to make Bitcoin legal tender.

June 5, 2021. Miami Beach. Bitcoin 2021 conference.

Several thousand Bitcoin supporters packed the venue. Onto the stage walked a young man in an ill-fitting suit, Chicago accent, hair a bit disheveled. Jack Mallers. He hadn't slept all night — Bukele's pre-recorded video had arrived only the day before. Once on stage, he realized all his notes were missing. He decided to wing it.

He began talking about his experience in El Salvador. About how fishermen in El Zonte received payments on their phones. About the face of a mother who waited five days for a Western Union remittance. About how central bank monetary expansion devours the purchasing power of ordinary people in emerging markets. About El Salvador — a country that lost its own currency to civil war, was forced to adopt the dollar, depended on overseas remittances for over twenty percent of GDP, and paid heartbreaking transfer fees.

As he spoke, his voice began to shake.

Then he cried.

Not performance. Not theatrics. It was a young man who had spent months crisscrossing Central America, who had seen the specific shape of poverty on El Zonte's dirt roads, and who suddenly realized that what he was building was changing real lives — and couldn't hold it together. The venue lights reflected off his wet face, the air thick with Miami's June humidity and the held breath of several thousand people.

The audience went quiet first. Then the applause began. Not the polite kind. The standing-up-from-your-chair kind.

Mallers wiped his eyes, took a deep breath. The screen behind him cut to a video — a young man in a backwards baseball cap appeared. Nayib Bukele, thirty-nine years old, president of El Salvador.

"I will be sending to Congress a bill that will make Bitcoin legal tender in El Salvador."

The venue erupted.

Mallers said a line that would be quoted countless times after: "One small step for Bitcoin, one giant leap for mankind."

Three days later, El Salvador's congress passed the Bitcoin Law, 62 votes to 19. The aftermath of this story — the Chivo wallet crashes, the street protests, IMF pressure, Bukele's Twitter trash-talking — belongs to the next chapter. This chapter only asks you to remember one thread:

From an anonymous donor's USB drive, to a fishing village pupusa stand, to a president's decision, to the tears of a young man on a Miami stage. That thread could be drawn because in between lay an invisible layer of infrastructure — the Lightning Network — making every sub-dollar payment possible.

Satoshi Nakamoto's nine-page white paper from 2008 was titled *Bitcoin: A Peer-to-Peer Electronic Cash System*. Peer-to-peer electronic cash. Not digital gold. Not a store of value — cash. Money you could spend.

Thirteen years later, those words came true for the first time in a fishing village on the Pacific coast.

---

*On February 25, 2018, Laszlo Hanyecz bought two Papa John's pizzas again. This time he paid 0.00649 BTC, roughly $67, with six cents in fees. The process was loaded with ceremony: he and a friend opened a Lightning Network payment channel, the friend placed the order, and the delivery driver was instructed to verify the first four and last four digits of the payment proof code — Laszlo read the string from a notebook before the pizzas were handed over. As the value discovery chapter noted, the 2010 pizzas cost 10,000 BTC, about $30. Eight years later, the same man, the same chain: 0.00649 BTC, $67. The first time proved Bitcoin "could be spent." The second time proved Bitcoin "was easy to spend." At early 2018 prices, those original 10,000 bitcoins were worth approximately eighty million dollars. This man seems destined to mark every Bitcoin technological milestone with pizza — and it's always Papa John's.*

---

<div align="center">
<a href="../">🏠 返回主页</a> |
<a href="https://twitter.com/bhbtc1337">🐦 关注作者</a> |
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 加入交流群</a>
</div>

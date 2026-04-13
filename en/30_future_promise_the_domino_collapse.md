# Future Promise: The Domino Collapse

![chapter image](img/ch30.png)

![status](https://img.shields.io/badge/状态-已完成-success)
![author](https://img.shields.io/badge/作者-beihaili-blue)

> 💡 In May 2022, a "stablecoin" backed by zero dollars lost its peg in 75 minutes, detonating the most catastrophic chain reaction in crypto history. Forty-five billion dollars evaporated. Three Arrows Capital, Celsius, and Voyager toppled one after another. Throughout the carnage, the Bitcoin network kept producing blocks — one every ten minutes, not one missed.
>
> Follow me on Twitter: [@bhbtc1337](https://twitter.com/bhbtc1337)
>
> Join our WeChat group: [Form link](https://forms.gle/QMBwL6LwZyQew1tX8)
>
> Open-sourced on GitHub: [Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3)

On April 17, 2022, Do Kwon posted a tweet.

His daughter had just been born. He named her Luna — the same name as the token he'd created. The caption read: "My dearest creation named after my greatest invention."

That day, LUNA was trading at $86. A month earlier it had hit an all-time high of $116. The entire Terra ecosystem commanded a market cap above $40 billion, making it the third-largest crypto system after Bitcoin and Ethereum. Do Kwon had a spot on Forbes Asia's 30 Under 30, a million Twitter followers, and nearly two hundred thousand devoted investors in South Korea — they called themselves "LUNAtics."

Three weeks later, Luna was trading at $0.0003.

That tweet about his daughter became the cruelest timestamp on the internet.

---

## The Alchemist

Kwon Do-hyung was born in Seoul on September 6, 1991. After graduating from Daewon Foreign Language High School, he left for the United States and earned a bachelor's degree in computer science from Stanford in 2015. His résumé listed brief stints at Microsoft and Apple, but he was clearly not the type to work for someone else.

In 2016, he founded Anyfi, a peer-to-peer network communications company, and secured roughly $600,000 in funding from the Korean government. That money was later flagged for conflicts of interest and alleged misuse. It was his first encounter with the problem of "other people's money." It would not be his last.

In January 2018, he and Korean e-commerce entrepreneur Daniel Shin co-founded Terraform Labs, registered in Singapore. The company's core product was an algorithmic stablecoin system — UST.

The concept of a stablecoin is straightforward: a cryptocurrency pegged 1:1 to the U.S. dollar. Existing solutions — USDT and USDC — relied on actual dollar reserves: you deposit one dollar, they issue one token. Do Kwon thought that approach was primitive. He would use an algorithm.

UST's pegging mechanism worked like this: it formed a mint-and-burn dual-token system with another token called LUNA. If UST fell to $0.98, arbitrageurs could buy UST, burn it on-chain to receive $1 worth of LUNA, then sell the LUNA and pocket the two-cent spread. This would continue until UST returned to $1. In reverse, if UST rose to $1.03, arbitrageurs could buy $1 of LUNA, burn it to mint one UST, and sell it at $1.03.

Elegant on paper. The problem was this: UST's "stability" depended entirely on LUNA's market cap. LUNA absorbed all the volatility; UST enjoyed all the calm. It was like a house built on springs — as long as the springs held, the house stood rock-solid. But if too many people rushed in at once, the springs would snap, the building would collapse, and you wouldn't even find the wreckage of the springs.

This was not a hypothetical. It was a precise prophecy.

Do Kwon, as it turned out, already knew the mechanism carried risk. In late 2020, he created a project called Basis Cash under the pseudonym "Rick Sanchez" — yes, the character from *Rick and Morty* who considers himself the smartest being in the universe. The token briefly surged to $155, then cratered and never re-pegged.

A reasonable person would have learned a lesson. The lesson Do Kwon learned was: next time, go bigger.

---

## The Twenty-Percent Bait

UST needed demand. Nobody was going to convert real money into a reserveless stablecoin just because "the algorithm is elegant." Do Kwon needed a reason for people to hand over their cash.

He found one: Anchor Protocol.

Anchor was a lending protocol on the Terra blockchain with a single selling point — roughly 20% annualized deposit yield. Park your UST in Anchor, do absolutely nothing, and collect nearly 120% of your principal in a year. In an era when traditional bank savings rates hovered near zero, that number worked like a giant magnet.

The results were immediate. From June 2021 to May 2022, UST deposits on Anchor grew 3,826%. By May 5, 2022, Anchor's total value locked (TVL) hit an all-time high of $17.15 billion. UST's total market cap stood at roughly $17.5 billion — three-quarters of it sitting in Anchor, collecting interest.

Three-quarters of a stablecoin's supply locked in a single protocol, earning yield. This was not a financial product. It was an ammunition depot waiting for a spark.

Where did the 20% come from? Subsidies. Borrowing demand fell far short of deposits; Anchor's revenue couldn't cover its payouts. The gap was plugged by a reserve fund — and that fund was draining fast. At its core, this was a Ponzi structure: interest from new deposits subsidized returns for old ones. As long as growth continued, the music kept playing.

Do Kwon was not worried. He was busy picking fights on Twitter.

In July 2021, British economist Frances Coppola criticized UST's algorithmic mechanism. Do Kwon replied: "I don't debate the poor on Twitter, and sorry I don't have any change on me for her at the moment."

On March 23, 2022, he tweeted that UST would destroy MakerDAO's decentralized stablecoin DAI: "By my hand $DAI will die."

A week before the collapse, someone asked him about the sustainability of the crypto industry. He laughed: "95% are going to die, but there's also entertainment in watching companies die too."

He was right about that. What he didn't expect was that he'd be the one providing the entertainment.

Meanwhile, to add a safety cushion for UST, Do Kwon established the Luna Foundation Guard (LFG) and began aggressively buying bitcoin as reserves. Through a $1 billion OTC trade via Genesis Global Trading, a $500 million bitcoin purchase from Three Arrows Capital, and subsequent additional buys, LFG amassed 80,394 BTC.

Eighty thousand, three hundred and ninety-four bitcoins. His last line of defense.

---

## Seventy-Five Minutes

Saturday, May 7, 2022.

Before 3 p.m. GMT, UST was still firmly pegged at one dollar. LUNAtics around the world were calculating their Anchor interest. Do Kwon was probably enjoying his weekend.

Then everything fell apart in 75 minutes.

Post-mortem on-chain analysis reconstructed the fatal window. At 21:44 GMT, Terraform Labs itself withdrew 150 million UST from a Curve liquidity pool — ostensibly to prepare for a new pool launch. Thirteen minutes later, at 21:57, an address tagged "Wallet A" executed an 85-million-UST swap on Curve — the single largest trade in the pool's history. Between 22:32 and 22:38, "Wallet B" made three consecutive swaps totaling 75 million UST. At 22:52, Terraform Labs pulled another 100 million UST from the pool. At 22:59, a final 25-million-UST sell hit.

Seventy-five minutes. Over half a billion dollars of selling pressure. The liquidity pool was drained dry.

UST depegged by more than 200 basis points on Curve and over 100 basis points on Binance. It closed the day 60 basis points below the peg.

The next day, Sunday. Anchor Protocol saw roughly $2.5 billion in withdrawals overnight. LFG emergency-lent $1.5 billion to defend the peg. UST barely held within 100 basis points. The whales were already running — holders with positions above $1 million pulled out 40%; those between $100,000 and $1 million pulled out 30%. And holders with less than $10,000? They were buying more.

Retail caught the falling knife. Four words that have repeated themselves countless times in financial history.

May 9, Monday. The crypto market crashed across the board. Bitcoin plunged to $31,000 by 6:30 p.m. UST lost its peg in earnest, dropping to $0.65. LUNA was trading at around $62.

Do Kwon tweeted that day: "Anon, you could listen to CT influensooors about UST depegging for the 69th time. Or you could remember they're all now poor, and go for a run instead."

When he posted those words, UST had already lost 35% of its value.

On May 10, UST briefly rebounded to $0.90, then fell again to $0.67. On May 11, it cratered below $0.23. The LUNA blockchain minted roughly one billion new tokens in a single day — the death spiral had engaged. UST holders frantically converted their UST into LUNA, causing LUNA's supply to explode, its price to accelerate downward, and the collapsing price of LUNA to further destroy UST's peg mechanism. The springs had snapped, the building was caving in, and every person trying to flee was accelerating the collapse.

On May 12, 200 billion LUNA were minted on-chain. On May 13, minting reached 6 trillion within hours. LUNA's total supply ballooned from 1 billion to 6 trillion — a 6,000-fold increase. The price fell from its all-time high of $116 to $0.0003.

In 2011, Bitcoin had experienced a comparable plunge: from $32 to $2, a 94% drop. But after Bitcoin's crash, the network kept running, blocks kept appearing, miners kept mining. After LUNA's crash, its creator pulled the plug himself.

Terraform Labs halted the Terra blockchain that day. A blockchain shut down by its own creator — Chaum's eCash, Mt. Gox's exchange, Do Kwon's blockchain. Centralized systems always end the same way.

What about LFG's 80,394 bitcoins? Starting May 8, LFG dumped them in a frenzy. 52,189 BTC were transferred to counterparties in exchange for UST; 33,206 BTC were sold outright. The total haul: roughly 2.68 billion UST.

It wasn't enough. UST kept falling.

When the smoke cleared, LFG's bitcoin reserves had gone from 80,394 to 313.

Three hundred and thirteen. The moat had evaporated by 99.6%. And the castle it was supposed to protect no longer existed.

Within one week, approximately $45 billion in market value across the Terra ecosystem vanished into thin air. An estimated one million people became victims.

In Seoul, an investor who had lost $2.3 million broke into Do Kwon's residence in Seongdong District, demanding he take full responsibility for the collapse and the suicides it had caused. Do Kwon's wife filed for an emergency restraining order.

Elsewhere in South Korea, a 36-year-old father called his daughter's school to say he was taking his 35-year-old wife and 10-year-old daughter, Cho Yu-na, on a trip to Jeju Island. They never reached Jeju. The family drove to Wando instead. On June 30, police recovered their car and three bodies from the waters off Wando. The father's search history contained "LUNA," "sleeping pills," and a Korean euphemism for suicide.

A ten-year-old girl.

Some numbers are statistics. Some numbers are lives.

---

## The Dominoes

Terra did not fall alone. When it went down, it crushed everyone standing too close behind it.

The first domino to topple was Three Arrows Capital.

Su Zhu and Kyle Davies met at Phillips Academy Andover, then both went on to Columbia University, and from there into Credit Suisse's Hong Kong trading desk. In 2012, the pair founded Three Arrows Capital (3AC) in Singapore, initially trading emerging-market FX derivatives arbitrage. After banks stopped dealing with them in 2017, they pivoted to crypto.

By 2021, Three Arrows Capital claimed a net asset value of $18 billion. On podcasts, Su Zhu promoted his "supercycle" thesis — the argument that the crypto market would grow indefinitely without major corrections, and that if Bitcoin captured gold's market cap, it could reach $2.5 million per coin.

Their strategy looked clever: become the largest institutional holder of the Grayscale Bitcoin Trust (GBTC), accumulating nearly 39 million GBTC shares by late 2020. The playbook was simple — borrow bitcoin, convert it into GBTC shares, wait out the six-month lockup, and sell at a premium. As long as GBTC traded at a premium, this was a money-printing machine.

But starting in 2021, GBTC's premium flipped to a discount. Leverage amplified gains on the way up and losses on the way down. 3AC was trapped in a depreciating GBTC position, like a swimmer who only discovers they're naked when the tide goes out.

Then they poured roughly $200 million into LUNA.

The May collapse wiped that investment to near zero. On June 16, margin calls went unanswered. On June 27, a British Virgin Islands court ordered the liquidation of Three Arrows Capital. Total creditor claims: $3.5 billion, involving more than twenty companies.

Before they ran — or rather, while they still thought they could — they placed an order for a yacht.

Its name was "Much Wow" — a nod to the Dogecoin meme. Built by Italian manufacturer Sanlorenzo, 171 feet, 52 meters long, reportedly the largest Sanlorenzo ever sold in Asia. Price tag: $50 million. Registered under a Cayman Islands company with the same name, "Much Wow Limited." Paid for with clients' money.

The yacht sat in the port of La Spezia, Italy, final payment outstanding. The two founders never set foot on it. It just sat there, unclaimed — a $50 million monument to a fantasy built with other people's money.

On September 29, 2023, Su Zhu was arrested at Singapore's Changi Airport while attempting to leave the country. The charge: contempt of court for refusing to cooperate with the liquidation investigation. He was sentenced to four months.

Kyle Davies? His whereabouts remain unknown to this day. He was spotted painting in Bali, giving interviews remotely from Dubai, and was rumored to be hiding in Portugal. He has publicly stated he has no regrets and plans to avoid prison. In a March 2024 podcast interview, he sat smiling, without a trace of remorse.

Three and a half billion dollars in debt. One handcuffed at the airport, the other painting in Bali.

---

Three Arrows Capital's collapse knocked over the next card: Celsius Network.

One Friday evening in May 2022, Alex Mashinsky sat in front of his camera as usual, launching his weekly YouTube livestream "Ask Mashinsky Anything." He wore his signature black T-shirt — the one that read "Banks are not your friends." The chat was filled with panic: Terra had just gone to zero, the market was cratering, were Celsius deposits safe? Mashinsky smiled, his tone like a patient father: "Celsius is fine. Your funds are safe."

The man had genuine accomplishments. Born October 1965 in Soviet Ukraine, he emigrated to Israel with his Jewish family in the 1970s and came to the United States in 1988. In the 1990s he founded VoiceSmart, one of the earliest VOIP phone services; later he created Arbinet, a marketplace for telecom companies to trade call minutes; he even helped build the wireless network for the New York City subway. He once stormed into a Chase Bank branch to stage a performance-art protest against the way traditional banks exploited ordinary people.

But in crypto, he became a different character.

In 2017, he founded Celsius Network. The slogan: "Unbank Yourself." Beyond the T-shirt, he sold HODL T-shirts, HODL polo shirts, HODL skateboards, even "Unbank Yourself" baby onesies. He packaged himself as a grassroots hero, the people's champion against the banks.

Celsius's business model was a mirror image of Anchor's: customers deposited crypto assets, Celsius promised to deploy those assets for investment returns, offering annualized yields as high as 18.6%. It called itself "the safest place for your crypto."

Celsius never turned a profit.

To fill the hole, Mashinsky gambled his customers' money on increasingly dangerous bets. He staked clients' ETH through Lido for stETH, deposited the stETH into Aave as collateral to borrow more ETH, then staked that on Lido again — layer upon layer of leverage, like Russian nesting dolls, each one smaller and more fragile than the last. In June 2021, ETH staked through Stakehound went wrong — Stakehound lost the private keys, and at least 35,000 ETH (over $50 million) vanished permanently. Celsius never told its customers.

By the time the shockwaves from Terra's collapse and Three Arrows Capital's blowup reached Celsius, the tower of leverage was already swaying.

On June 12, 2022, Celsius tweeted: all withdrawals, swaps, and transfers between accounts were suspended. The reason cited was "extreme market conditions."

Approximately $12 billion in user assets were frozen.

The irony: the day before the freeze, Mashinsky was still on Twitter reassuring users that Celsius had "minimal exposure" to Luna and UST, dismissing contrary claims as "rumors."

The deeper irony: two to three weeks before the freeze — in mid-to-late May 2022 — Mashinsky himself withdrew more than $10 million. Celsius executives collectively withdrew roughly $17 million.

The man wearing the "Banks are not your friends" T-shirt moved his own money out before locking the doors.

Then came Voyager Digital. The Toronto-based crypto trading platform had lent Three Arrows Capital 15,250 BTC and 350 million USDC — approximately $650 to $670 million in total. After 3AC defaulted, Voyager filed for bankruptcy on July 6, 2022. More than 100,000 creditors; eventual recovery rate: roughly 35.7% — thirty-five cents on the dollar.

FTX briefly won the bid to acquire Voyager at a $1.4 billion valuation, and users hoped to recover 72%. But five months later, FTX itself blew up — that story belongs to the next chapter. The white knight rode halfway to the rescue, and then the horse died too.

That was the summer of 2022. Terra fell and crushed 3AC. 3AC fell and crushed Celsius and Voyager. Celsius and Voyager's collapse deepened the market panic, sending Bitcoin from $46,206 at the start of the year all the way down to roughly $17,600 on June 18 — its lowest point since December 2020.

Every falling domino screamed the same thing: I am centralized, I am controlled by a handful of people, and those people screwed up.

---

## The One That Didn't Fall

On June 8, 2022, the Bitcoin network's hash rate quietly set a new all-time high: 292 EH/s.

The timing was almost absurd. Bitcoin's price had tumbled from $46,206 at the start of the year to below twenty thousand. Terra's wreckage was still smoldering. Celsius had just frozen withdrawals. Three Arrows Capital's margin calls were being ignored. The market's fear index was off the charts. And at the very moment when everyone was fleeing crypto, more computing power was plugging into the Bitcoin network. Mining investment is a long-term commitment — those machines reflected deployment plans made months earlier — but the chain didn't care about any of that. It only knew one thing: the force protecting it was stronger than it had ever been.

Throughout 2022, the Bitcoin network maintained 100% uptime. One block every ten minutes on average, uninterrupted all year. On September 12, it hit 5,000 consecutive days online.

That same year: Do Kwon pressed Terra's kill switch. Mashinsky froze Celsius withdrawals. Su Zhu and Kyle Davies simply disappeared. One man, a group of executives, two business partners — behind every collapse was a specific person who made a specific decision. Bitcoin had no such person. Not because it was lucky, but because Satoshi Nakamoto had deleted that role from the system thirteen years earlier.

The price bottomed at $15,768 in November 2022 — hammered down by FTX's final blow. But every block on the chain arrived on schedule, every transaction was faithfully recorded. No one could freeze it. Not because no one wanted to, but because no one could.

The lesson left behind by this catastrophe fits in a single sentence: "Not your keys, not your Bitcoin." Mt. Gox had taught it once, at a cost of $470 million. This round — Terra, 3AC, Celsius — taught it again, and the tuition climbed to tens of billions. But the bill wasn't finished yet. Five months later, a curly-haired young man in shorts and a T-shirt who testified before Congress would push the number to new heights.

But that is a story for the next chapter.

---

*On March 23, 2023, Do Kwon was arrested at the airport in Podgorica, the capital of Montenegro. He was about to board a private jet to Dubai, carrying a forged Costa Rican passport and Belgian travel documents. He claimed he'd believed they were legitimate "golden passport" fast-track citizenship papers. On December 31, 2024, he was extradited to the United States. He pleaded guilty in August 2025. On December 11, Judge Paul Engelmayer sentenced him to 15 years in federal prison. The judge said: "This was a fraud on an epic, generational scale." He added: "Real people lost 40 billion dollars in real money, not some paper loss." Mashinsky fared no better — on May 8, 2025, he was sentenced to 12 years in federal prison and ordered to forfeit $48 million. The man who said "I don't debate the poor" and the man who preached "Unbank Yourself" ended up in the same federal prison system.*

---

<div align="center">
<a href="../">🏠 Home</a> |
<a href="https://twitter.com/bhbtc1337">🐦 Follow the Author</a> |
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 Join the Community</a>
</div>

# Breaking Waves: Bitcoin Independence Day

<picture>
  <source srcset="../img_webp/23.webp" type="image/webp">
  <img src="../img/23.png" alt="Breaking Waves: Bitcoin Independence Day" loading="lazy" width="800">
</picture>

On August 1, 2017, at 3:12 PM Beijing time, the Bitcoin network produced its 478,559th block. From a technical perspective, this block wasn't particularly special—it contained approximately 2,000 transactions, was close to the 1MB limit in size, and had the same mining difficulty as the previous block. But from a historical perspective, this seemingly ordinary block marked one of the most important watersheds in Bitcoin's history.

At the moment this block was confirmed, the Bitcoin network achieved SegWit (Segregated Witness) activation, while a new fork coin called Bitcoin Cash was officially born. The scaling debate that had raged for over two years was finally resolved in a dramatic way: not through compromise, but through division.

At Bitcoin meetups around the world, supporters raised their glasses to celebrate this "Bitcoin Independence Day." But this celebration was complex—containing both the joy of victory and the pain of separation.

## Seeds of Grassroots Uprising

The story begins with an anonymous developer. On GitHub, his username was Shaolinfry, and no one knew his real identity. But in the spring of 2017, it was this mysterious figure who proposed an idea that would change Bitcoin's history: User Activated Soft Fork (UASF).

In February 2017, while entrepreneurs discussed the SegWit2x agreement in luxury hotels in New York, Shaolinfry published an article titled "User Activated Soft Fork" on a technical forum. The core idea was simple: users shouldn't passively wait for miners or developers to decide, but should actively activate the protocol upgrades they want.

"Bitcoin's true power belongs to users," Shaolinfry wrote, "If enough users run software supporting a specific protocol upgrade, miners must follow, or their mined blocks will be rejected."

This idea seemed radical at the time, even dangerous. Traditional soft forks required support from a majority of miners to activate, while UASF attempted to bypass miners and push upgrades directly through users.

But Shaolinfry's idea struck a nerve with many users. After two years of arguing, they were tired of waiting, tired of passively watching the games between entrepreneurs and miners. They wanted to regain control over Bitcoin's future.

## The Technical Revolution of BIP 148

Shaolinfry's philosophy quickly transformed into a concrete technical proposal: BIP 148. This proposal required all Bitcoin nodes to reject any blocks that didn't signal support for SegWit after August 1, 2017.

From a technical perspective, BIP 148 was an ingenious design. It leveraged the characteristics of soft forks—tightening rules rather than loosening them. Nodes supporting BIP 148 would reject blocks that didn't support SegWit, but older nodes would still accept blocks supporting SegWit.

"This is an application of economic game theory," an anonymous technical analyst explained on the forum. "Miners' income comes from block rewards and transaction fees. If most exchanges, wallets, and merchants run BIP 148, then blocks not supporting SegWit have no economic value."

But BIP 148 also carried enormous risks. Without sufficient support, it could cause the Bitcoin network to split into two chains. Worse still, if the BIP 148-supporting chain received too little hash power, there might be long periods without block generation.

## The Symbolic War of Hats and Flags

Despite technical risks and expert skepticism, the UASF movement quickly gained widespread grassroots support. This support was evident not only in technical forum discussions but also in real-world symbolic actions.

The most representative was the popularity of UASF hats. These hats printed with "UASF" and "User Activated Soft Fork" became identity markers for supporters. At Bitcoin meetups around the world, people wearing UASF hats gathered together, discussing technical details and sharing reasons for support.

Erik Voorhees, CEO of ShapeShift, although concerned about UASF's technical risks, appeared at the Miami Bitcoin Conference wearing a UASF hat. "I don't necessarily support BIP 148's specific implementation," he told reporters, "but I support the principle of user sovereignty."

Social media became the main mobilization platform for the UASF movement. The #UASF hashtag was frequently used on Twitter, with supporters sharing technical articles, creating promotional graphics, and organizing offline meetups.

More importantly, the UASF movement attracted many technically-minded supporters. They not only understood BIP 148's technical principles but also actively participated in code development and testing work.

## The Critical Choice of Economic Nodes

The key to UASF's success lay in gaining support from enough "economic nodes." In Bitcoin's context, economic nodes refer to participants who provide economic value to the network: exchanges, payment processors, wallet service providers, large merchants, etc.

The first major economic node to express support was Bitfinex. This then-world's largest Bitcoin exchange announced it would support the BIP 148-activated chain on August 1st. "We believe users should have the right to choose their preferred version of Bitcoin," Bitfinex's statement read.

Kraken quickly followed suit, announcing support for UASF. Several other smaller exchanges and service providers also successively expressed support. However, some large platforms remained cautious, worried that supporting UASF might bring technical risks and legal liability.

More crucial was the attitude of wallet service providers. If major wallet software didn't support BIP 148, ordinary users would find it difficult to participate in UASF. Fortunately, Bitcoin Core wallet would follow BIP 148 rules by default, providing an important user base for UASF.

## The Historical Watershed Moment

On August 1, 2017, at 12:37 PM UTC, one of the most dramatic days in Bitcoin's history began. On this day, three important events occurred almost simultaneously: BIP 148 activation, SegWit lock-in, and Bitcoin Cash fork.

From a technical timeline perspective, the events of this day occurred in a carefully designed sequence. First, BIP 148 activated at UTC 0:00, beginning to mandate all blocks signal support for SegWit. Then, enough miners began signaling support for SegWit, triggering SegWit's formal activation process. Finally, Bitcoin ABC created the first Bitcoin Cash block at block height 478,558.

This precise timing arrangement wasn't coincidental but the result of various parties' game theory. UASF pressure forced miners to switch to supporting SegWit at the last moment, while Bitcoin Cash's fork provided an exit for those still insisting on the big block route.

At Bitcoin meetups worldwide, supporters nervously stared at block explorers, watching each new block's generation. When the first block mandatorily supporting SegWit was confirmed, venues erupted in warm applause and cheers.

## The Technical Significance of SegWit Activation

SegWit's activation wasn't just the resolution of the scaling debate but an important milestone in Bitcoin's technical development. This upgrade solved multiple long-standing technical problems and laid the foundation for Bitcoin's future development.

Most importantly was the fix for transaction malleability. Before SegWit, transaction IDs could change before transactions were confirmed, making it difficult to construct complex multi-layer transactions. SegWit completely solved this problem by separating signature data from the transaction body.

This fix paved the way for Layer 2 solutions like the Lightning Network. Lightning Network relies on complex multi-signature transactions and timelock mechanisms, all of which require predictable transaction IDs.

SegWit also provided effective capacity increases. While the block size limit remained 1MB, separating signature data allowed blocks to contain more transactions. In practical use, SegWit could increase network capacity by approximately 40%.

## Bitcoin Cash's Fork Experiment

Just as the Bitcoin community celebrated SegWit activation, a new cryptocurrency was born: Bitcoin Cash. This fork coin embodied the big block faction's different vision for Bitcoin's future.

Bitcoin Cash increased the block size limit from 1MB to 8MB, removed SegWit, and simplified the difficulty adjustment algorithm. These changes reflected the big block faction's core philosophy: Bitcoin should prioritize being a payment system rather than a store of value or settlement layer.

The forking process was smoother than many expected. Although there were some technical issues and network instability, the Bitcoin Cash network successfully launched and began producing blocks. This proved the resilience and forkability of the Bitcoin protocol.

But Bitcoin Cash also faced enormous challenges. First was the hash power allocation problem. Since both networks shared the same mining algorithm, miners could freely switch between them. This led to unstable hash power allocation, with both networks experiencing significant block time fluctuations.

More important was the market acceptance issue. Although Bitcoin Cash was technically similar to Bitcoin, it needed to build its own ecosystem: exchange support, wallet integration, merchant acceptance, etc.

## Establishment of User Sovereignty Principle

UASF's success not only resolved technical disputes but more importantly established the principle of user sovereignty in Bitcoin governance. This event proved that in decentralized systems, users hold ultimate decision-making power.

Traditionally, Bitcoin's technical upgrades required miner support to activate. This gave miners enormous veto power, allowing them to block upgrades users wanted. UASF overturned this power relationship, proving users could bypass miner obstruction and directly activate protocol upgrades.

This successful case established an important precedent for Bitcoin governance. It showed that in the power game between miners, developers, and users, users hold ultimate decision-making power. This power comes from creating economic value: if users refuse to use a certain version of Bitcoin, that version loses value.

## The Far-reaching Significance of Long-term Impact

Looking back in history, the impact of August 1, 2017, far exceeded people's expectations at the time. This day not only resolved the scaling debate but also laid the foundation for Bitcoin's long-term development.

SegWit's activation opened a new chapter of Bitcoin technical innovation. Lightning Network, Taproot upgrade, sidechain technology, and other subsequent developments all built on SegWit's foundation. Without the breakthrough of August 1st, none of these innovations would have been possible.

Bitcoin Cash's fork also produced unexpected positive impacts. It provided an experimental platform for big block philosophy, allowing the market to test different technical routes. Although Bitcoin Cash ultimately didn't surpass Bitcoin, the experiment itself was valuable.

More importantly, the user sovereignty principle established on August 1st influenced the entire cryptocurrency industry. Many subsequent protocol upgrades borrowed from UASF experience, implementing changes through user activation rather than miner activation.

UASF's success also proved the feasibility of decentralized governance. It showed that even without central authority, distributed participants could coordinate consistently to push system upgrades.

When historians review Bitcoin's development, they'll find August 1, 2017, was a crucial turning point. Before this day, Bitcoin was still an experimental technical project facing technical bottlenecks and governance crises. After this day, Bitcoin became mature financial infrastructure with the capability for continued development.

Those who celebrated wearing UASF hats on August 1st might not have realized they were witnessing a historical turning point. Their grassroots actions not only changed Bitcoin but also set an example for the development of the entire decentralized system.

This is the true meaning of Bitcoin Independence Day: it wasn't just a victory of technology, but a victory of free will.

---

*August 1st is forever remembered by the Bitcoin community as "Independence Day," that day proved users hold ultimate decision-making power in decentralized systems, and UASF became a classic case in blockchain governance history.*
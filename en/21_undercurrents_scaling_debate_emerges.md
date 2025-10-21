# Undercurrents: The Scaling Debate Emerges

<picture>
  <source srcset="../img_webp/21.webp" type="image/webp">
  <img src="../img/21.png" alt="Undercurrents: The Scaling Debate Emerges" loading="lazy" width="800">
</picture>

In the spring of 2015, the Bitcoin network was experiencing a seemingly minor but actually significant change. In Princeton University's Computer Science Department, graduate students noticed that Bitcoin transaction confirmation times were beginning to significantly lengthen. What used to take minutes now took over ten minutes, sometimes even an hour. Transaction fees were also quietly rising, making small transactions increasingly uneconomical.

Behind these seemingly superficial technical issues lay a deeper contradiction: Bitcoin was experiencing the backlash of its own success. The growth in network usage was exceeding the system's processing capacity, and the root of this problem could be traced back to a seemingly temporary technical decision made by Satoshi Nakamoto in 2010—limiting block size to 1MB.

No one anticipated at the time that this simple number would trigger the most intense technical and philosophical controversy in Bitcoin's history, nearly tearing the entire community apart.

## The Historical Legacy of 1MB

To understand the origins of the scaling debate, we must return to July 15, 2010. On that day, Satoshi Nakamoto added a simple limitation to the Bitcoin code: each block could not exceed 1MB in size. The purpose of this limitation was simple—to prevent malicious attackers from clogging the network by creating enormous blocks.

At the time, this limitation seemed very generous. The Bitcoin network in 2010 had only a few hundred transactions per day, with average block sizes under 1KB. A 1MB limit was like building a ten-lane highway for a small town with only a dozen people—it seemed more than sufficient.

When Satoshi explained this decision on the BitcoinTalk forum, he wrote: "We can phase in a change later if we get closer to needing it. This is a problem that can be solved later through soft fork or hard fork." He clearly considered this only a temporary measure that could be easily adjusted when needed.

But history proved that seemingly simple technical decisions often produce unexpected complex consequences.

## The Problem Emerges

By the end of 2014, Bitcoin network usage began to grow rapidly. Daily transaction volume grew from thousands to tens of thousands, and average block size grew from dozens of KB to hundreds of KB. Although there was still room before hitting the 1MB limit, the trend was clear: without action, the network would soon encounter capacity bottlenecks.

The first obvious symptoms appeared in the spring of 2015. Users began complaining about extended transaction confirmation times, especially for transactions using lower fees. Some Bitcoin wallets began automatically adjusting fee algorithms, suggesting users pay higher fees to ensure transactions could be confirmed promptly.

Coinbase engineers noticed this change. They found that without timely adjustment of fee strategies, users' withdrawal requests might wait in the mempool for hours before being confirmed. "This is not the user experience we want," wrote a Coinbase engineer in an internal email.

More serious was merchant feedback. BitPay reported that some small payment transactions they processed had fees approaching the transaction amount itself. "This completely violates Bitcoin's original purpose as a payment system," BitPay CEO Stephen Pair said in an interview.

Although these problems hadn't reached crisis levels yet, they sent a clear warning to the technical community: Bitcoin's scaling problem was no longer theoretical discussion but a real challenge.

## Gavin's Radical Proposal

Facing increasingly severe scaling pressure, Gavin Andresen decided to take action. As Satoshi's chosen successor and chief developer of the Bitcoin Core project, he felt responsible for solving this critical problem.

In May 2015, Gavin proposed BIP 101, suggesting to increase the block size limit from 1MB to 8MB, with automatic doubling every two years until reaching 8GB in 2036. The logic of this proposal was simple: since network capacity was insufficient, directly increase capacity.

"Bitcoin's goal is to become a global digital currency," Gavin wrote in his blog. "If we artificially limit network capacity, we're limiting Bitcoin's development potential. Moore's Law tells us that computing power and storage capacity will continue to grow, and we should trust technological progress."

Gavin's proposal received support from some large enterprises. Coinbase CEO Brian Armstrong publicly expressed support for BIP 101, considering it the most direct method to solve the scaling problem.

But this seemingly reasonable proposal triggered fierce controversy in the technical community.

## Technical Conservatives' Concerns

Other members of the Bitcoin Core development team expressed strong concerns about BIP 101. Their opposition wasn't based on personal grudges but on deep consideration of Bitcoin's long-term security and decentralization characteristics.

Core developer Gregory Maxwell detailed the reasons for opposition on technical forums: "8MB block size would significantly increase the cost of running full nodes. If only a few wealthy entities could run full nodes, Bitcoin would lose its decentralized characteristics."

The deeper divergence lay in different understandings of Bitcoin's essence. Large block supporters believed Bitcoin should first be a payment system, so user experience and transaction costs were the most important considerations. Small block supporters believed Bitcoin should first be a decentralized value storage system, so security and censorship resistance were the most important considerations.

This divergence reflected a fundamental contradiction within the Bitcoin community: the conflict between technological idealism and practical pragmatism.

## Bitcoin XT's Fork Attempt

Facing opposition from the Bitcoin Core development team, Gavin decided to take more radical action. In August 2015, he teamed up with Mike Hearn to launch Bitcoin XT, a fork version of Bitcoin software with BIP 101's block size increase mechanism built-in.

Bitcoin XT's release was technically significant because it was the first attempt to push protocol changes through client forks. If more than 75% of miners ran Bitcoin XT, the network would automatically upgrade to 8MB blocks.

"This is not an attempt to split the community, but to give the community a choice," Gavin wrote when announcing Bitcoin XT. "If most users and miners believe 8MB blocks are the right path, they can express support by running Bitcoin XT."

Bitcoin XT's release immediately triggered fierce controversy. Supporters believed this embodied democratic decision-making, letting users rather than developers decide Bitcoin's future direction. Opponents believed this was a dangerous challenge to the consensus mechanism that could lead to network splits.

More seriously, controversy began shifting from technical levels to personal attacks. Some extreme opponents launched cyber attacks against Gavin and Mike Hearn, including DDoS attacks on their websites and servers. Reddit's Bitcoin forum began censoring posts supporting Bitcoin XT, claiming these contents violated "altcoin" rules.

## Community Division

Bitcoin XT's launch completely divided the Bitcoin community into two camps. Supporters were called "big blockers," opponents were called "small blockers," and both sides engaged in fierce debates on various platforms.

Big blockers' arguments were relatively straightforward: Bitcoin needed scaling to meet growing demand, 8MB blocks were technically feasible, and delaying scaling would harm Bitcoin's competitiveness.

Small blockers' arguments were more complex but equally powerful: large blocks would threaten decentralization, increase systemic network risks, and scaling could be achieved through Layer 2 solutions like the Lightning Network.

The intensity of controversy exceeded everyone's expectations. On the BitcoinTalk forum, originally harmonious technical discussions became fierce debates. On Reddit, users supporting different viewpoints began downvoting and reporting each other. On Twitter, disagreements among some prominent figures became public, further exacerbating community division.

Worse still, controversy began affecting Bitcoin's market performance. Investors worried that community division would lead to network forks, and Bitcoin prices showed a clear downward trend in the second half of 2015.

## Bitcoin XT's Failure

Despite Gavin and Mike Hearn's vigorous promotion, Bitcoin XT ultimately failed to gain sufficient support. By the end of 2015, less than 10% of nodes were running Bitcoin XT, far below the 75% threshold needed to trigger an upgrade.

Bitcoin XT's failure had multiple causes. First, the Bitcoin Core development team's authority played an important role. Although Bitcoin was theoretically decentralized, most users and miners still relied on Core developers' technical judgment.

Second, the SegWit proposal provided a seemingly more conservative alternative. SegWit could increase network capacity without changing block size limits while fixing other technical issues.

Third, the technical complexity of forks confused and worried many users. Hard forks required coordination and upgrades from all network participants, and any mistake could lead to fund losses.

In January 2016, Mike Hearn announced his withdrawal from Bitcoin development and published an article titled "The Resolution of the Bitcoin Experiment," declaring Bitcoin a "failure." Although this article sparked controversy, it also marked the official end of the first scaling attempt.

## Deep Governance Crisis

Bitcoin XT's failure exposed deep-seated problems in Bitcoin's governance mechanisms. Although Bitcoin was designed as a decentralized system, in actual operation, power remained concentrated in the hands of a few key participants.

Developers had enormous influence because they controlled code modifications. Miners theoretically had final decision-making power, but their decisions were often driven by economic interests rather than technical considerations. The user base seemed to have "voting with their feet" power, but most users lacked the ability and motivation to participate in technical decisions.

This governance dilemma not only affected the resolution of scaling controversies but also laid the groundwork for subsequent more intense controversies.

## Laying the Groundwork for Future Controversies

The 2015-2016 scaling controversy, though temporarily ended with Bitcoin XT's failure, laid the groundwork for future more intense controversies. The factional positions formed in the controversy, institutionalized opposition, and unresolved fundamental problems would all re-erupt in the 2017 scaling war.

More importantly, the controversy established a precedent for pushing protocol changes through forks. Although Bitcoin XT failed, it proved that forking was a viable technical means. This precedent would inspire subsequent fork attempts, ultimately leading to the birth of Bitcoin Cash.

When the last day of 2016 arrived, the Bitcoin network still maintained a 1MB block size limit, and the scaling problem remained fundamentally unresolved. But the controversy had changed everything: Bitcoin was no longer a purely technical project but a social system involving complex interest relationships and value choices.

In Princeton University's laboratory, graduate students continued observing Bitcoin network performance metrics. Transaction confirmation times were still lengthening, fees were still rising, and block sizes were approaching the 1MB limit. All technical indicators pointed to the same conclusion: the Bitcoin network was heading toward a critical turning point.

History would prove that the 2015-2016 scaling controversy emergence was not an isolated technical problem but the inevitable growing pains Bitcoin experienced in its transition from experiment to maturity. This pain, though it tore the community apart, also drove technological innovation and governance mechanism development.

From the moment Satoshi set the 1MB limit, this controversy was inevitable. The only questions were when it would arrive and how it would be resolved.

---

*The 1MB block size limit still exists in the Bitcoin protocol today, and that scaling controversy that began in 2015 ultimately gave birth to the flourishing development of Layer 2 solutions like the Lightning Network.*

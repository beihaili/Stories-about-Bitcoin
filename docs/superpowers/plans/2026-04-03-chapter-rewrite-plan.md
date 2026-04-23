# 四章重写实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重写全书质量最低的4章（Ch11、Ch35、Ch36、Ch37），消除章节间内容重叠，补充一手史料，加强人物塑造，让全书终段达到与前段同等水准。

**Architecture:** 每章独立重写，但Ch35-37作为一组协调设计以消除重叠。每章遵循"备份→整理素材→写作→质量检查"流程。写作风格严格遵循《写作圣经》。

**Tech Stack:** Markdown写作、WebSearch/WebFetch补充资料、资料/目录JSON参考

---

## 关键约束

1. **重写前必须备份原版到`正文/历史版本/`目录**（用户硬性要求）
2. **改哪就改哪，不擅自扩大修改范围**（用户反馈）
3. **遵循《写作圣经》的风格DNA**：先铺事实后给观点、人物驱动、每章至少一个灵魂时刻
4. **一手史料优先**：论坛原帖、邮件原文、当事人引言
5. **重叠消除表**必须严格执行（见下方）

## 重叠消除对照表

| 内容 | Ch35 十万 | Ch36 缺席 | Ch37 光 |
|------|-----------|-----------|---------|
| Larry Fink "I was wrong" | 删除 | 不出现 | 不出现 |
| ETF/500亿规模 | 一句带过 | 不出现 | 不出现 |
| 特朗普/大选 | 一句带过 | 不出现 | 不出现 |
| 芬尼ALS/去世 | 不出现 | **主场** | 仅Running Bitcoin Challenge |
| 中本聪100万枚/一聪没动 | 不出现 | **主场** | 不出现 |
| 哈耶克3000册/预言 | 不出现 | **主场** | 不出现 |
| Patoshi Pattern | 不出现 | **主场** | 不出现 |
| 创世区块铭文 | 不出现 | 不出现 | **主场** |
| 全球使用场景 | 不出现 | 不出现 | **主场** |
| 苹果市值对比 | **主场** | 不出现 | 不出现 |
| 全节点/网络数据 | 不出现 | 不出现 | **主场** |

---

## Task 1: Ch11 第一次泡沫 — 重写

**目标**：从"事件概述"转为"人物群像" — 4个真实人物讲述同一场泡沫的不同命运

**Files:**
- Backup: `正文/历史版本/11_风起云涌_第一次泡沫_backup_20260403.md`
- Modify: `正文/11_风起云涌：第一次泡沫.md`
- Reference: `资料/market_and_exchanges.json`, `资料/bitcoin_security_incidents_comprehensive.json`, `资料/early_bitcoin_community_history.json`

### 新结构（5节，约3500字）

**第1节：从1到32**（约500字）
- Gawker文章和Mt.Gox被黑**只各用一句话带过**（"如第九章所述"/"如第十章所述"），不再重复叙述
- 聚焦价格曲线本身和FOMO情绪
- 引用Felix Salmon的媒体-价格正反馈循环分析："The value of bitcoins, it turns out, is highly sensitive to media coverage."
- 引用Vitalik Buterin（当时17岁）的一周年回顾文："The sudden climb brought great hope to the Bitcoin community... and the decline brought no less despair."

**第2节：被盗的25,000枚**（约700字）
- **主角：Allinvain** — Bitcoin Express创始人
- 2011年6月13日，25,033 BTC被盗（当时$500,000）
- 原帖引用："I am totally devastated today. I just woke up to see a very large chunk of my bitcoin balance gone..."
- 技术细节：未加密的wallet.dat、没有二次验证的Slush Pool
- NPR Planet Money报道标题："Someone Just Stole $500,000 In Bitcoins"
- 社区反应：质疑vs同情
- 意义：比特币史上第一起重大盗窃，"Not Your Keys"教训的最早版本

**第3节：0.01美元的赌注**（约800字）
- **主角：Kevin (toasty)** — Mt.Gox闪崩中的投机者
- 原帖引用（BitcoinTalk topic #20207）："I had just purchased over 250,000 bitcoins for $2,613. At the trading price immediately before this large sell order happened, that number would have been worth nearly $5 million."
- 交易记录："06/19/11 17:51 Bought BTC 259684.77 for 0.0101"
- Mt.Gox回滚交易的决定
- 社区大辩论："不可篡改性 vs 实用主义"——这是比特币社区第一次面对这个根本问题
- Kevin实际提走643 BTC

**第4节：六篇讣告**（约700字）
- 具体列出2011年的6篇"比特币已死"文章（Forbes/Gizmodo/Wired等），给出标题、日期、当时价格
- EFF停止接受比特币（2011年6月20日），引用EFF官方声明的理由
- **Bruce Wagner的MyBitcoin丑闻**：The Bitcoin Show主持人、首届比特币大会组织者，在MyBitcoin存了25,000 BTC，MyBitcoin跑路后154,406 BTC被盗
- Wired的"The Rise and Fall of Bitcoin"是最重量级的一篇讣告

**第5节：赌一万美元的人**（约800字）
- **主角：Roger Ver** — 在所有人说比特币已死时逆行
- 2011年初以~$1/BTC大量买入
- MemoryDealers成为全球首个接受比特币的成熟企业（2011.4.26）
- 在硅谷竖起世界首个比特币广告牌
- 公开下注$10,000赌比特币两年内跑赢黄金、白银、美股100倍
- 赌注结果：两年两个月后比特币涨了15,000%+，Ver将1,000 BTC捐给Foundation for Economic Education
- 收束：周期律——"每一次循环结束后，底部都比上一次的顶部高"
- 结尾冷知识：苹果市值对比（保留原版，从Ch35移到这里更合适——1454倍→不到2倍）

### Steps

- [ ] **Step 1: 备份原版**
```bash
cp "正文/11_风起云涌：第一次泡沫.md" "正文/历史版本/11_风起云涌_第一次泡沫_backup_20260403.md"
```

- [ ] **Step 2: 整理素材文件**
从资料/中提取相关内容，结合上方搜集的一手史料（Allinvain、Kevin、Roger Ver、Bruce Wagner），整理为写作参考要点

- [ ] **Step 3: 写作新版Ch11**
按上述5节结构重写，约3500字。严格遵循写作圣经风格。确保与Ch09/Ch10零重叠。

- [ ] **Step 4: 质量检查**
对照写作圣经检查：
- 至少有1个灵魂时刻？
- 至少3个一手引用？
- 至少2个有名有姓的人物？
- 与Ch09/Ch10零内容重叠？
- 结尾冷知识与本章内容相关？

- [ ] **Step 5: 提交用户审阅**

---

## Task 2: Ch35 十万美元突破 — 重写

**目标**：聚焦"十万美元"的市场机制和历史意义，不碰人物致敬（Ch36）和哲学反思（Ch37）

**Files:**
- Backup: `正文/历史版本/35_未来可期_十万美元突破_backup_20260403.md`
- Modify: `正文/35_未来可期：十万美元突破.md`
- Reference: `资料/price_milestones_detailed.json`, `资料/bitcoin_etf_history_detailed.json`, `资料/bitcoin_latest_developments_2024_2025.json`

### 新结构（4节，约2800字）

**第1节：六位数**（约600字）
- 保留2024年12月5日的具体时刻和出租车司机场景（好素材）
- **删除**ETF详述和大选详述——只用一句话："ETF获批（第33章）和大选变天（第34章）推倒了最后两块多米诺骨牌，一个月内涨幅超过50%。"
- **删除**Larry Fink "I was wrong"（已在Ch33详述）

**第2节：买家换了**（约800字）
- 本章独有核心：三次高点的买家结构对比
- 2011年：极客和赌徒（呼应新Ch11）
- 2017年：散户和投机者，出租车司机推荐买币 = 泡沫见顶
- 2024年：养老基金、保险公司、主权财富基金，三到五年配置计划
- Saylor 400亿持仓（一句话，不展开——Ch25已详述）
- 链上数据：70%一年不动、交易所余额降30%、第四次减半（450/天）
- "想买的人在排队，想卖的人不动"

**第3节：473次讣告**（约600字）
- 比特币"已死"的完整统计：从2011年到2024年累计473次
- 价格每次被宣布死亡后的表现
- "这大概是人类历史上被宣布死亡次数最多的东西"
- 苹果市值对比移至Ch11，这里不再重复

**第4节：路标**（约400字）
- 简洁收束：十万美元是路标不是终点
- **不再提芬尼/中本聪/哈耶克**——全部留给Ch36
- 过渡悬念："但在这条路上，有些人永远不会到达终点。"
- 结尾冷知识：Patoshi Pattern地址监控——如果任何地址活动，市场将地震。（注：原来在Ch35结尾的冷知识移到Ch36更合适，这里换一个与市场机制相关的冷知识，如减半周期或供应量统计）

### Steps

- [ ] **Step 1: 备份原版**
```bash
cp "正文/35_未来可期：十万美元突破.md" "正文/历史版本/35_未来可期_十万美元突破_backup_20260403.md"
```

- [ ] **Step 2: 写作新版Ch35**
按上述4节结构重写，约2800字。严格执行重叠消除表。

- [ ] **Step 3: 质量检查**
- 与Ch33（ETF）、Ch34（大选）零内容重叠？
- 与Ch36（缺席的人）零内容重叠？
- 芬尼/中本聪/哈耶克是否完全不出现？
- 有独属于"十万美元"的叙事角度？

- [ ] **Step 4: 提交用户审阅**

---

## Task 3: Ch36 缺席的人 — 重写

**目标**：全书情感高潮 — 用一手材料写透每个"缺席的人"，引入3个从未出现的新人物

**Files:**
- Backup: `正文/历史版本/36_未来可期_缺席的人_backup_20260403.md`
- Modify: `正文/36_未来可期：缺席的人.md`
- Reference: `资料/key_figures.json`, `资料/early_bitcoin_developers_comprehensive.json`

### 新结构（5节，约4000字）

**第1节：预言者**（约500字）
- 哈耶克段落精简保留
- **补充**1984年Cato Institute采访英文原文：
  > "I don't believe we shall ever have a good money again before we take the thing out of the hands of government, that is, we can't take it violently out of the hands of government, all we can do is by some sly roundabout way introduce something that they cannot stop."
- 收束于1992年去世——"他的3000册书最终卖出了几十万册，但他本人永远不知道有人真的造出了'政府无法阻止的东西'。"

**第2节：第一个信徒**（约1000字）— 大幅扩写
- 核心素材：Hal Finney的"Bitcoin and me"原帖（BitcoinTalk, 2013年3月19日）
- 关键引文（直接引用英文原文+中文翻译）：
  - "When Satoshi announced Bitcoin on the cryptography mailing list, he got a skeptical reception at best. Cryptographers have seen too many grand schemes by clueless noobs."
  - "I was more positive. I had long been interested in cryptographic payment schemes."
  - "I thought I was dealing with a young man of Japanese ancestry who was very smart and sincere."
  - 为什么停止挖矿："It made my computer run hot, and the fan noise bothered me."（最朴素的理由）
  - ALS诊断后："I am essentially paralyzed... I operate the computer using a commercial eyetracker system."
  - "I'm pretty lucky overall. Even with the ALS, my life is very satisfying."
  - "Easy come, easy go."
  - "My bitcoins are stored in our safe deposit box, and my son and daughter are tech savvy. I think they're safe enough. I'm comfortable with my legacy."
- Running Bitcoin推文与ETF批准的巧合：2009年1月10日 vs 2024年1月11日
- 收束于Alcor人体冷冻保存（第128号病人）

**第3节：沉默的创造者**（约800字）
- 中本聪最后通信的**完整叙述**
- **补充**致Gavin的最后邮件（2011年4月26日）：
  > "I wish you wouldn't keep talking about me as a mysterious shadowy figure, the press just turns that into a pirate currency angle. Maybe instead make it about the open-source project and give more credit to your dev contributors."
- Gavin回复说接受了CIA演讲邀请——中本聪从此沉默
- Patoshi Pattern：100万枚，一聪未动，十六年
- "一个人创造了一种价值千亿美元的资产，然后转身走进了永恒的沉默。"

**第4节：墓碑与代码**（约900字）— 全新段落
- **Len Sassaman**（1980-2011）：密码朋克，Mixmaster维护者，与Chaum合作过，31岁去世。Dan Kaminsky在区块138725为他刻下ASCII艺术悼词——区块链上的第一座墓碑，也是第一幅ASCII艺术作品。
- **Dan Kaminsky**（1979-2021）：互联网安全救世主（DNS漏洞发现者），为朋友在区块链上刻碑的人自己也走了，42岁。2021年入选互联网名人堂。
- **Timothy May**（1951-2018）：密码朋克运动创始人，《加密无政府主义者宣言》作者，Intel前高级科学家35岁退休。去世前对加密行业失望——认为已偏离初衷。
- 暗线：创造者们一个个离去，但代码还在运行。区块链上的墓碑永远不会风化。

**第5节：去中心化**（约400字）
- 保留金句："去中心化不是口号。去中心化是：创造者可以消失，系统继续运转。"
- 现在这句话的分量完全不同——读者已经见证了6个以上的缺席者
- 结尾冷知识：Fran Finney每年举办"Running Bitcoin Challenge"跑步挑战为ALS研究筹款。"Running bitcoin——这三个字的主人不再跑步了，但以他名字命名的跑步每年都在继续。"

### Steps

- [ ] **Step 1: 备份原版**
```bash
cp "正文/36_未来可期：缺席的人.md" "正文/历史版本/36_未来可期_缺席的人_backup_20260403.md"
```

- [ ] **Step 2: 搜索验证一手材料**
通过WebFetch访问以下URL验证关键引文：
- Hal Finney "Bitcoin and me": nakamotoinstitute.org/library/bitcoin-and-me/
- Len Sassaman区块链墓碑: cirosantilli.com/cool-data-embedded-in-the-bitcoin-blockchain/len-sassaman-tribute
- Cato Institute哈耶克采访原文

- [ ] **Step 3: 写作新版Ch36**
按上述5节结构重写，约4000字。这应该是全书最长的章节之一。

- [ ] **Step 4: 质量检查**
- "Bitcoin and me"引文是否准确？
- 与Ch35零内容重叠？
- 新增三个人物（Sassaman/Kaminsky/May）是否有足够细节？
- 是否达到"全书情感高潮"的定位？

- [ ] **Step 5: 提交用户审阅**

---

## Task 4: Ch37 光未熄灭（终章）— 重写

**目标**：从抽象的散文变成具体的"光在哪里亮着" — 用真实数据和真实人物证明"光未熄灭"，作为全书的有力收束

**Files:**
- Backup: `正文/历史版本/37_未来可期_光未熄灭_backup_20260403.md`
- Modify: `正文/37_未来可期：光未熄灭.md`
- Reference: `资料/bitcoin_latest_developments_2024_2025.json`

### 新结构（5节，约3500字）

**第1节：地下室**（约600字）
- 保留现有开场场景（好素材：嗡嗡声、凉掉的咖啡）
- **补充硬数据**：
  - 99.98%正常运行率
  - 17年仅宕机14小时47分钟（2次：2010年整数溢出8h27m + 2013年共识bug 6h20m）
  - 2013年至今100%不间断，超过13年
  - 算力达到1 ZH/s（10^21 hash/s）
  - 181个国家有节点（全球197国中的92%）
  - 约71,000+个节点（含不可达节点）
- "十七年里只'宕机'过两次，加起来不到十五个小时。这个记录比全球任何银行系统、任何科技巨头的服务器都要好。"

**第2节：最后一公里**（约800字）— 全新段落
- **委内瑞拉**：通胀229%，街头摊贩用USDT标价。Carlos的引文："I use USDT for everything—buying food, paying rent. It is much more reliable than the bolivar."
- **刚果Goma**：2021年Nyiragongo火山爆发后，Juvin Kombi的Jikofood餐厅用闪电网络帮助流离失所的家庭
- **叙利亚难民Tey Elrjula**：没有身份证无法开银行账户，比特币成了替代方案。"Bitcoin changed my life."
- **约旦**：联合国WFP的Building Blocks项目用区块链+虹膜扫描为10万名叙利亚难民提供援助
- 这些才是"理想照进现实"最真实的样子

**第3节：从太空到地面**（约500字）— 全新段落
- **Blockstream卫星**（2017年起）：从太空广播比特币区块链，覆盖五大洲。任何有卫星天线和廉价USB接收器的人都能接收——即使断网。
- **Locha Mesh**（Bitcoin Venezuela项目）：开源硬件网状网络，在无互联网甚至无电网环境下传输比特币交易
- "光未熄灭"的最极端证明：哪怕断网断电，比特币也能传播。从太空到地面，从卫星到网状网络。

**第4节：那束光**（约600字）
- 创世区块收束（保留，这是Ch37的"主场"）
- "49年前的预言。16年前的代码。此刻你手中的这本书。"
- 但现在这段话有了全新的重量——前面有委内瑞拉的摊贩、刚果的餐厅、叙利亚的难民、太空中的卫星做铺垫

**第5节：Running Bitcoin**（约500字）— 全新结尾
- Fran Finney每年举办"Running Bitcoin Challenge"跑步挑战，为ALS研究筹款
- 2025年2月的最近一次挑战
- 芬尼不再跑步了，但以他名字命名的跑步每年都有人在跑
- 回扣Ch04开头的"Running bitcoin"三个字——形成全书首尾闭环
- **全书最后一句**："Running bitcoin。这三个字的主人走了。但跑步还在继续。光未熄灭。"
- 结尾冷知识：blockchain.com/btc/block/0（保留——邀请读者亲自去看创世区块）

### Steps

- [ ] **Step 1: 备份原版**
```bash
cp "正文/37_未来可期：光未熄灭.md" "正文/历史版本/37_未来可期_光未熄灭_backup_20260403.md"
```

- [ ] **Step 2: 搜索验证全球使用数据**
通过WebSearch/WebFetch验证：
- 比特币网络运行时间统计（bitbo.io/uptime）
- 委内瑞拉/刚果/叙利亚案例的具体引文
- Blockstream Satellite覆盖范围
- Fran Finney Running Bitcoin Challenge最新信息

- [ ] **Step 3: 写作新版Ch37**
按上述5节结构重写，约3500字（从原来的1100字扩展3倍+）。

- [ ] **Step 4: 质量检查**
- 字数是否达到3000+？
- 与Ch36零内容重叠？
- 全球使用场景是否有具体人名和引文？
- 全书最后一句是否有力？
- 是否与Ch04（Running bitcoin开头）形成首尾闭环？

- [ ] **Step 5: 提交用户审阅**

---

## 执行顺序

建议按以下顺序执行：

1. **Ch11**（独立章节，不依赖其他章节改动）
2. **Ch35**（必须在Ch36之前，因为Ch35的"不碰"内容由Ch36承接）
3. **Ch36**（必须在Ch37之前，因为Finney段落在Ch36是主场，Ch37只用Running Bitcoin Challenge）
4. **Ch37**（最后写，需要确认Ch36的内容后才能确定边界）

每章完成后提交用户审阅，确认后再进入下一章。

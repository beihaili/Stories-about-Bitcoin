# 学习指南：暗潮汹涌——Mt.Gox的覆灭

> 对应章节：`正文/17_暗潮汹涌：Mt.Gox的覆灭.md`

## 本章关键概念

1. **Mt.Gox** — 2010-2014年全球最大的比特币交易所，巅峰期处理全球约80%的比特币交易，因管理混乱最终丢失约85万枚比特币后破产
2. **交易延展性攻击（Transaction Malleability）** — 比特币交易在被区块确认前，其交易ID可被恶意篡改，导致交易所误判提现状态而重复打款；Mt.Gox以此为借口暂停提现，但根本原因是其代码将交易ID作为唯一标识符
3. **"Not your keys, not your Bitcoin"** — Mt.Gox崩塌后诞生的社区核心准则：如果私钥不在你手里，你持有的只是交易所的IOU（欠条），而非真正的比特币
4. **冷钱包与热钱包** — 冷钱包离线存储私钥，安全性高但操作不便；热钱包在线运行便于交易但易受攻击。Mt.Gox破产后在冷钱包中意外找回约20万枚比特币
5. **交易所对手方风险** — 将资产托管给中心化第三方所面临的风险，包括黑客攻击、内部管理失当和资金挪用，Mt.Gox事件是这一风险的经典案例

## 思考题

1. Mt.Gox事件与更早的eCash倒闭有何相似之处？中心化托管的"原罪"是否可以通过更好的监管来解决，还是只有自托管才是根本出路？
2. "Not your keys, not your Bitcoin"的道理人人都懂，但大多数人仍然把比特币存在交易所或通过ETF持有。便利性与安全性之间的矛盾，你认为未来会如何演化？
3. Mt.Gox崩塌后比特币价格暴跌，但网络本身从未中断。这说明了去中心化系统的什么特性？"交易所倒了"和"比特币死了"之间的区别为何常被混淆？

## 延伸阅读

- [Mt.Gox 破产始末（Wikipedia）](https://en.wikipedia.org/wiki/Mt._Gox) — 完整的Mt.Gox历史时间线、破产程序与债权人赔偿进展
- [Bitcoin Transaction Malleability（Bitcoin Wiki）](https://en.bitcoin.it/wiki/Transaction_malleability) — 交易延展性漏洞的技术原理，以及后来SegWit如何从根本上修复了这个问题
- [The Mt. Gox Hack Explained（Chainalysis Blog）](https://www.chainalysis.com/blog/mt-gox-repayment/) — 链上数据分析视角回顾Mt.Gox资金流向与赔偿方案

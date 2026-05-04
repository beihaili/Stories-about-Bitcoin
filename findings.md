# 《我给中本聪送外卖》通宵写作 Findings

## 已知项目状态

- 当前本地提交：`5a22f42 feat: 补齐外卖故事前30章`。
- `我给中本聪送外卖/正文/` 已有 01-30 连续章节。
- 发布脚本：`python3 scripts/export_fanqie_delivery.py --clean`。
- 当前故事结构表规划 31-37 为终局段，重点从历史知识转向李觉“决定怎么活”。

## 写作要求摘要

- 核心闭环：现实刺点 -> 历史照面 -> 认知改写 -> 现实动作。
- 李觉不是发财逆袭；结尾要回到“身份未变，认知变了”。
- 赵晴不是女主，是现实校准器；陈浩是清醒同谋者；母亲线负责稳定焦虑。
- 中本聪账号不解释机制，结尾只揭到半句，力度控制在读者能拼但作者不说破。

## 待补事实锚点

- 31 FTX：FTX/Alameda 崩塌、提款停止、破产、普通人托管信任再破碎。
- 32 铭文：Ordinals/Inscriptions、开放系统的噪音与规则治理。
- 33 ETF：美国现货比特币 ETF 批准和上市，胜利与收编并存。
- 34 大选与战略储备：政治/国家叙事、美国战略比特币储备政策。
- 35 十万美元突破：价格爽点必须被现实讽刺压住。
- 36 缺席的人：物件清点，回收 01、02 物件线。
- 37 光未熄灭：终局主动姿态，中本聪账号回到 `btc block 0`。

## 已核对来源与写作边界

- FTX / SBF：美国司法部 SDNY 2024-03-28 新闻稿确认 SBF 被判 25 年，涉及 FTX 客户资金挪用、投资者和贷款方欺诈，金额级别为数十亿美元。写作中可压缩为“FTX 信任崩塌”，但不能写成比特币协议失败。
  - 来源：https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison
- 现货比特币 ETP/ETF：SEC 主席声明确认 2024-01-10 批准一批现货比特币 ETP 份额上市交易，同时声明不等于认可比特币本身。写作中重点应放在“入口合法化”与“自托管理想的妥协”。
  - 来源：https://www.sec.gov/newsroom/speeches-statements/gensler-statement-spot-bitcoin-011023
- 战略比特币储备：白宫 2025-03-06 fact sheet 确认行政令建立 Strategic Bitcoin Reserve 和 U.S. Digital Asset Stockpile，储备以刑事/民事没收的比特币资本化，并授权预算中性增持策略。写作中必须标明这是 2025 年事实，不要误写成 2024 年大选当天已落地。
  - 来源：https://www.whitehouse.gov/fact-sheets/2025/03/fact-sheet-president-donald-j-trump-establishes-the-strategic-bitcoin-reserve-and-u-s-digital-asset-stockpile/
- Taproot：区块 709,632 于 2021-11-14 激活 Taproot。铭文章可把 Taproot 作为“规则打开的门”，但要说明铭文没有修改共识规则。
  - 来源：https://www.blockchain.com/explorer/blocks/btc/709632
- Ordinals / Inscriptions：Galaxy 研究说明 Casey Rodarmor 在 2022-12 发布 ORD，铭文把任意数据编码进比特币交易并绑定到聪；理论上可接近 4MB。写作中把争议重点放在“规则允许的噪音”。
  - 来源：https://www.galaxy.com/insights/research/bitcoin-ordinals-inscriptions-5-billion-nft-market
- 十万美元突破：Axios/AP 均报道比特币在 2024-12-05 前后首次突破 100,000 美元，并与大选后行情、友好监管预期、ETF 和减半周期相关。写作中不能让价格成为胜利终点，必须压回现实讽刺。
  - 来源：https://www.axios.com/2024/12/05/bitcoin-100000-crypto-all-time-high
  - 来源：https://apnews.com/article/stock-markets-fed-rates-bitcoin-88d737ab0669b10c06ab39386ed30a74

## 决策

- 采用路线 A：先补完整本初稿，再做评分和改写。
- 31-37 每章均新增合同、beats、审稿；评分可集中到 `设定/结构/章节评分/31-37章评分报告.md`。
- 历史锚点 31-35 必补；36-37 如果是现实/尾声为主，可建“叙事锚点”型历史文件或在审稿中注明无新增硬史实。
- 36 章负责物件回收：01、02 不强行在 05-12 回收，改为尾声铁盒回收，并在物件档更新“实际回收章节：36”。
- 37 章不写破中本聪身份。采用“独居女程序员 / 普通客户的半句暗示”与 `btc block 0` 回环，读者能拼，正文不点破。

## 2026-05-04 读者视角复盘

- 全书主线成立：普通外卖员被中本聪订单拖入比特币历史，最终从“寻找答案/暴富机会”转向“自己承担判断和生活行动”。
- 当前版本更接近“精品历史现实主义 + 设定型小说”，题材、立意和历史质感强；番茄平台向还需要增强开篇留存、章节钩子、冲突密度和中后段沉浸场景。
- 最强结构点：13-16 章“违规问未来 -> 账号沉默 -> 回到现实行动”，证明本书不是历史旅游，而是主角被迫成长。
- 最强情绪点：24 章陈浩失业、31 章 FTX 信任破碎、34 章母亲稳定焦虑、37 章普通订单结尾。
- 主要改写优先级：先处理 01-03 章开篇阅读节奏，再考虑 26-37 章中偏短章节的场景加厚。

## 2026-05-04 DeepSeek 重写工作流决策

- 不直接使用聊天里出现的 API key，避免密钥进入命令历史、补丁、日志或提交。
- 新增 `.env.deepseek` 本地文件承载真实密钥；该文件被 `.gitignore` 的 `.env.*` 规则忽略。
- 默认 DeepSeek 配置：
  - `DEEPSEEK_BASE_URL=https://key.bigsong.site/v1`
  - `DEEPSEEK_MODEL=deepseek-v4-pro`
- 第一步只生成第1章开篇样章，不覆盖正文。样章用于比较节奏、钩子、现实压力和 AI 味控制。

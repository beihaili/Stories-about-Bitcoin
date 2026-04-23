# 番茄发布工作流：《我给中本聪送外卖》

## 当前结论

截至 2026-04-21，未发现番茄小说官方提供作者后台发布 API 或官方 MCP。

当前采用更简单的方案：本地导出纯文本 + 本地一键复制页面 + 作者后台人工粘贴发布。不接浏览器自动化，不碰真实后台。

## 已有脚本

```bash
python3 scripts/export_fanqie_delivery.py --clean
```

默认输入：

```text
我给中本聪送外卖/正文/
```

默认输出：

```text
发布/番茄/我给中本聪送外卖/
```

输出目录已加入 `.gitignore`，因为它是正文的发布副本，不作为源文件维护。

## 输出内容

- `chapters/第001章_标题.txt`：一章一文件，第一行为 `第001章 标题`
- `all_chapters.txt`：整本合并纯文本
- `copy.html`：本地一键复制页面，可复制单章或整本
- `manifest.json`：章节清单、字数、风险词、AI 辅助标记
- `README.md`：发布暂存包说明、人工复核词、发布前检查

## 当前门槛

脚本本地设置了 `20000` 字符的初始投稿准备线：

```bash
python3 scripts/export_fanqie_delivery.py --target-initial-chars 20000
```

这不是自动发布条件，只是本地提醒。真正能否投稿、签约、推荐，以番茄作者后台和合同为准。

## 安全边界

- 不逆向番茄私有接口。
- 不绕过登录、验证码、风控或审核流程。
- 不自动选择最终发布，除非人工明确确认。
- 后台如询问是否使用 AI，应按实际创作流程如实选择。
- 比特币题材需人工复核是否被误判为投资建议、交易引导、私下交易、平台漏洞等。

## 复制发布路线

1. 手动创建作品，确认书名、分类、简介、封面、合同和 AI/版权条款。
2. 运行 `python3 scripts/export_fanqie_delivery.py --clean`。
3. 打开 `发布/番茄/我给中本聪送外卖/copy.html`。
4. 点击“复制本章”或“复制全部”。
5. 粘贴到番茄作者后台，人工确认 AI/版权选项、定时发布时间和正文格式后发布。

## 参考来源

- 番茄作家专区：<https://fanqienovel.com/writer/zone/>
- 番茄帮助中心：<https://fanqienovel.com/writer/zone/help>
- 番茄内容发布规范：<https://fanqienovel.com/writer/zone/article/7237084151751376957>
- 番茄定时发布说明：<https://fanqienovel.com/writer/zone/article/7482607861307015230>
- 第三方 Fanqie MCP（读/查为主）：<https://github.com/lemnt-ai/fanqie-mcp-server>
- 第三方 fanqie-publisher-skill（Playwright 发布思路）：<https://github.com/amm10090/fanqie-publisher-skill>

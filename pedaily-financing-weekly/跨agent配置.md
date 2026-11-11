# 跨 Agent 配置方法

## 推荐：共享 Codex skills 目录

将整个 `pedaily-financing-weekly` 文件夹复制到所有 Agent 共用的 `$CODEX_HOME/skills`（未设置时通常为 `~/.codex/skills`）：

```bash
cp -R pedaily-financing-weekly "${CODEX_HOME:-$HOME/.codex}/skills/"
```

复制后，新建 Agent 或下一轮会自动发现技能。显式调用：

```text
使用 $pedaily-financing-weekly，整理 2026-11-01 至 2026-11-11 的具身智能、商业航天和低空经济融资事件，输出带来源的 Excel。
```

## 多 Agent 任务分工

主 Agent 负责日期区间、赛道口径、去重和最终 Excel；子 Agent 可分别负责：

- 周列表候选抓取：运行 `scripts/pedaily_weekly.py`；
- 单篇原文核验：补齐金额、轮次、领投方、全部投资方；
- 企业主体核验：确认中国大陆注册地和业务赛道；
- 质量复核：检查日期、重复事件、来源链接和是否误纳入二级市场事项。

子 Agent 调用时应传入技能绝对路径，避免依赖其当前工作目录：

```text
请使用 /绝对路径/pedaily-financing-weekly/SKILL.md 的规则，完成投资界融资周报的单篇事件核验；只返回结构化字段和来源链接。
```

## 当前环境安装位置

本项目副本位于：

`/Users/liwenxu/Desktop/yzc/中信建投/skills/pedaily-financing-weekly`

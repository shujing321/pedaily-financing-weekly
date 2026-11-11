# pedaily-financing-weekly

按日期区间抓取投资界（pedaily.cn）融资周报，核验单篇原文并整理一级市场融资事件。适用于具身智能、航空航天、低空经济、汽车及汽车零部件等赛道的融资清单。

## 一键安装

macOS/Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/shujing321/pedaily-financing-weekly/main/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://raw.githubusercontent.com/shujing321/pedaily-financing-weekly/main/install.ps1 | iex
```

## 本地安装

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R pedaily-financing-weekly "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后重启 Codex，并使用：

```text
使用 $pedaily-financing-weekly，整理指定日期区间的投资界融资事件并输出 Excel。
```

## 数据口径

主数据源仅为投资界融资周报及投资界单篇原文；不使用其他网站补充主表。脚本只抓取公开周报候选链接，金额、轮次和投资方需由 Agent 回到投资界原文核验。

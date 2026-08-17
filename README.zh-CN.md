# NovelGame

> **再也不用每次重新描述你的故事设定。** 一个面向 AI 代理的自包含互动小说引擎——世界观、角色、规则只需打包一次，AI 每次会话自动加载，进度跨上下文不丢失。

**阅读语言：** [English](README.md) · [中文](README.zh-CN.md) · [日本語](README.ja.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Agent Plugins](https://img.shields.io/badge/Agent%20Plugins-1.0.0-blue.svg)](https://agent-plugins.org)
[![Output Languages](https://img.shields.io/badge/Output-EN%20%7C%20%E4%B8%AD%E6%96%87%20%7C%20%E6%97%A5%E6%9C%AC%E8%AA%9E-blue.svg)](README.md)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-Yes-brightgreen.svg)](skills/novel-game/scripts/state.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)

基于 [Agent Plugins](https://agent-plugins.org) 1.0.0 规范构建（Working Draft）。

## 为什么选择 NovelGame？

| 痛点 | 普通 AI 对话 | 使用 NovelGame |
|------|--------------|----------------|
| **重复设定** | 每次会话都要重新口述世界观、角色、规则（"半天设定半天，太麻烦"） | 设定即文件——写一次，永久自动加载 |
| **进度丢失** | 上下文被压缩或新开对话时，故事状态全部蒸发 | 状态持久化到磁盘 JSON 存档；章节快照 + 动态上下文注入可恢复——恢复不是重开 |
| **AI 味写作** | 千篇一律的套路化、模板化文风 | 反套路引擎：套话黑名单、感官优先写作规则、非典型剧情库、叙事质量自评 |

## 功能特性

- **设定即文件** — 世界观写一次，每次会话自动加载。
- **状态即脚本** — 所有进度、好感度、背包、flag、分支历史通过 `state.py` 持久化为 JSON 存档；状态跨上下文丢失和新会话依然存活。
- **分层记忆** — 短期（近期事件）、中期（章节摘要）、长期（玩家偏好反思）三层记忆，长故事不丢上下文。
- **章节快照 + 动态上下文注入** — 上下文压缩或新会话后无缝恢复，恢复不是重开。
- **ToT 分支规划** — 内部评估 3–5 个剧情方向，只保留最强的 2–4 个选项。
- **叙事质量评分** — 对每段输出自评 OOC、设定一致性、连贯性、反套路强度、选项质量。
- **反套路引擎** — 套话黑名单、感官优先写作规则、非典型剧情库，避免 AI 味文风。
- **英文优先、多语言输出** — 引擎规则和命令用英文保证精确；剧情正文可切换**英文、中文、日文**。

## 语言支持

| 语言 | 代码 | 剧情输出 |
|------|------|----------|
| 英语（默认） | `en` | 支持 |
| 中文 | `zh` | 支持 |
| 日语 | `ja` | 支持 |

- 引擎规则、命令、脚本内部输出固定为英文，保证指令理解无歧义。
- 在设定文件中设置默认语言（`## Language: en|zh|ja`），或随时在对话中说 "switch to Chinese"、"用中文"、"日本語に切り替えて" 切换。
- 设定文件支持中/英/日三种语言编写，初始状态解析器三种语言都能识别。

## 快速开始

```bash
# 1. 复制设定模板并填写
cp skills/novel-game/references/SETTINGS.md my_story.md

# 2. 从设定初始化存档
python3 skills/novel-game/scripts/new_story.py --settings my_story.md --title "My Story" --dir ./saves

# 3. 开始游玩——引擎每回合读取状态
python3 skills/novel-game/scripts/state.py summary --dir ./saves
```

或直接使用内置示例：

```bash
python3 skills/novel-game/scripts/new_story.py \
  --settings skills/novel-game/references/EXAMPLE.md \
  --title "The Fogbound Detective" --dir ./saves
```

## 演示

内置示例《雾都缉凶》中的一回合（中文输出）：

> **你**（对法医 Erin）："我要看港口仓库火灾的案卷。"
>
> **NovelGame** — *Erin 眯起眼睛，把牛皮纸文件夹推过桌面，指尖在边缘停留。"那场火不是意外。有人想让那些记录消失。"*（好感度 +5）
>
> 1. 问她从灰烬里发现了什么。
> 2. 拿起文件夹，一言不发地离开。
> 3. 告诉她你信任她的判断——并且是认真的。

引擎已记录你对 Erin 的好感度、更新背包、写入事件日志——全部持久化到 JSON 存档，下次会话直接续玩。

## 仓库结构

```
novel-game/
├── LICENSE                     # Apache License 2.0
├── README.md                   # 英文 README
├── README.zh-CN.md             # 中文 README
├── README.ja.md                # 日文 README
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── plugin.json                 # Agent Plugins manifest
└── skills/
    └── novel-game/
        ├── SKILL.md            # 引擎指令（英文）
        ├── scripts/
        │   ├── state.py        # 状态管理 CLI（JSON 存档）
        │   └── new_story.py    # 从设定文件初始化存档
        └── references/
            ├── SETTINGS.md     # 故事设定模板
            ├── RULES.md        # 引擎强制规则
            ├── ANTI_TROPE.md   # 反套路清单与剧情库
            └── EXAMPLE.md      # 可直接游玩的示例故事
```

## 状态命令参考

```
python3 scripts/state.py init --title <title> [--settings <file>] [--dir <dir>]   # 创建存档
python3 scripts/state.py get [--story <id>] [--dir <dir>]                        # 读取完整状态
python3 scripts/state.py summary [--story <id>] [--dir <dir>]                    # 紧凑状态摘要
python3 scripts/state.py set --key <flag> --value <value> [--dir <dir>]          # 设置 flag
python3 scripts/state.py add-stat --key <stat> --delta <delta> [--dir <dir>]     # 调整数值
python3 scripts/state.py add-item --item <item> [--dir <dir>]                    # 加入背包
python3 scripts/state.py remove-item --item <item> [--dir <dir>]                 # 移出背包
python3 scripts/state.py set-node --node <node> [--dir <dir>]                    # 设置当前节点
python3 scripts/state.py log --event <event> [--dir <dir>]                       # 记录事件
python3 scripts/state.py remember --tier <short|mid|long> --content <content> [--dir <dir>]
python3 scripts/state.py recall --tier <short|mid|long> [--keyword <word>] [--limit N] [--dir <dir>]
python3 scripts/state.py reflect --content <reflection> [--dir <dir>]            # 写入玩家偏好反思
python3 scripts/state.py snapshot --scene <scene> --characters <chars> --goal <goal> --threads <threads> [--dir <dir>]
python3 scripts/state.py restore [--dir <dir>]                                    # 从最新快照恢复
python3 scripts/state.py context [--dir <dir>]                                    # 恢复用完整上下文块
python3 scripts/state.py list [--dir <dir>]                                      # 列出存档
```

存档目录优先级：`--dir` 参数 > `$NOVEL_DATA_DIR` > `./saves`。

## 环境要求

- Python 3.10+（仅标准库，无第三方依赖）

## 支持本项目

如果 NovelGame 让你少了一次"重新设定"的麻烦，请考虑：

- **给仓库点个 Star** — 这是帮助更多人发现它的最好方式。
- **分享**给喜欢用 AI 玩/写互动小说的朋友。
- 在 Issues 中**反馈问题**或**提需求**。
- **参与贡献** — 参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 协议

[Apache License 2.0](LICENSE)

# 小六壬速断

![小六壬速断封面](docs/cover.png)

`xiaoliu-ren-quick-read` 是一个“选字＋实际起课时间”的中文 Skill。它按固定笔画数据计算字宫、时宫与落宫，再结合字义，给出一句克制直接的娱乐性速断和一个现实行动。

低风险日常问题可以回答“课面偏有、偏无或更像什么”，但不承诺必中，不给精确应期，也不替代事实核验或专业意见。

## 当前版本

- Skill ID：`xiaoliu-ren-quick-read`
- 版本：`v1.0.1`
- RedSkill 与 GitHub Release 共用文件：`xiaoliu-ren-quick-read-v1.0.1-redskill.zip`
- ZIP SHA-256：`550D495100420E98F144370A4BE56FD7854D4FC3055E575B3D6C09ABBB118E50`

## 兼容性

采用通用 Agent Skills（`SKILL.md`）结构，可在 GPT/Codex、Claude Code（CC）、WorkBuddy、CodeBuddy 等主流 Agent 工具中安装使用。

## 特点

- **输入简单**：一个汉字，加上如实填写的实际起课时间。
- **三宫可复算**：固定数据与公式生成字宫、时宫和落宫。
- **直断但不绝对**：可以说“课面偏有/偏无”“更像”，不说“注定、必中、一定”。
- **时间不随选**：使用提出问题并准备起课时的真实当地时间，不挑“吉时”，不换时间刷结果。
- **安全边界明确**：高风险结果不出课面，不提供恐吓、改运、法事或付费化解建议。
- **默认显式调用**：`allow_implicit_invocation: false`。

## 使用示例

```text
请调用 xiaoliu-ren-quick-read（小六壬速断）Skill。
这篇论文能不能顺利接收？
选字：春
实际起课时间：上午九点
```

示例输出：

> 一句速断：若问能否“顺利直收”，课面偏否；若问最终是否仍有接收机会，偏有。更像先等待，经过返修或反复沟通后再推进。“春”取生长之意，转机在修改完善，而非原稿不动。

> 这是传统意象框架上的娱乐性自省，不替代事实核验或专业意见。

## 安装

从本仓库的 `v1.0.1` Release 下载版本化 ZIP，按照所用 Agent 工具的 Skill 导入方式安装；支持从 GitHub 安装的工具也可直接使用本仓库地址。

如需手动安装，请将 ZIP 中的 Skill 文件解压到个人 Skill 目录中的 `xiaoliu-ren-quick-read` 文件夹。Codex 的 Windows 用户目录通常为：

```text
%USERPROFILE%\.codex\skills\xiaoliu-ren-quick-read
```

安装后，在对话中明确点名“小六壬速断”或 `xiaoliu-ren-quick-read` 即可；在 Codex 中可直接写出 `$xiaoliu-ren-quick-read`。

## 文件结构

```text
SKILL.md
agents/
  openai.yaml
assets/
  UNICODE-LICENSE.txt
  unihan-total-strokes.txt
references/
  method.md
  palaces.md
scripts/
  cast.py
```

GitHub 仓库额外包含 `README.md` 和 `docs/cover.png`；这两个文件不进入 RedSkill ZIP。

## 数据来源

笔画索引来自 Unicode 17.0.0 Unihan `kTotalStrokes`，用于保证相同输入可重复计算。Unicode 数据的许可文本见 `assets/UNICODE-LICENSE.txt`。

可复算性只表示计算一致，不代表现实预测经过科学验证。

## 使用边界

- 论文、考试、求职、普通合作等低风险日常主题可以给出课面倾向，但不作现实保证。
- 不预测医疗、人身安全、诉讼、犯罪、投资、借贷、保险或赌博等高风险结果。
- 不判断第三人的秘密、忠诚、健康、行踪或真实动机。
- 不提供符咒、法事、祭祀、改运或付费化解建议。
- 同一问题 24 小时内不通过换字或更改起课时间重复起课。

## 版本一致性

本仓库中的七个 Skill 文件应与 RedSkill `v1.0.1` ZIP 逐字节一致。发布 GitHub Release 时直接上传已核验的 RedSkill ZIP，不重新压缩。

## 权利说明

本仓库未附加通用开源许可证。除 Unicode 数据按其随附许可使用外，其他原创内容保留所有权利。

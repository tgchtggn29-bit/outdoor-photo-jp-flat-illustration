# outdoor-photo-jp-flat-illustration

把用户提供的徒步、露营、登山、滑雪、骑行或旅行人物照片，转为温和、简洁、日式扁平卡通素材插画提示词。

## 包含内容

- `skills/outdoor-photo-jp-flat-illustration/SKILL.md` — 技能主文件（工作流 + 提示词结构）
- `skills/outdoor-photo-jp-flat-illustration/references/` — 风格锁定与画质参考文档
- `skills/outdoor-photo-jp-flat-illustration/scripts/build_prompt.py` — 提示词生成脚本
- `skills/outdoor-photo-jp-flat-illustration/templates/` — 提示词模板

## 本地安装

插件已注册到个人 marketplace（`~/.agents/plugins/marketplace.json`）。在 Codex 应用中打开插件列表即可安装，安装后新开会话即可使用 skill。

## 发布到 GitHub

1. 在 GitHub 创建仓库（例如 `outdoor-photo-jp-flat-illustration`），把本目录内容上传。
2. 在仓库根目录放置 `.agents/plugins/marketplace.json`（把 `plugins` 数组里的 `source.path` 保持为 `./plugins/outdoor-photo-jp-flat-illustration`，并确保插件位于仓库的 `plugins/` 目录下）。
3. 使用者通过 `codex plugin marketplace add <仓库地址>` 添加该 marketplace，即可安装插件。

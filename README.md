# outdoor-photo-jp-flat-illustration

把用户提供的徒步、露营、登山、滑雪、骑行或旅行人物照片，转为温和、简洁、日式扁平卡通素材插画提示词的 Codex 插件。

## 安装

在 Codex 中运行：

```bash
codex plugin marketplace add https://github.com/tgchtggn29-bit/outdoor-photo-jp-flat-illustration
```

添加后打开插件列表，安装 `outdoor-photo-jp-flat-illustration` 插件，新开任务即可使用对应 skill。

## 仓库结构

```text
.
├── .agents/plugins/marketplace.json   # marketplace 清单
├── plugins/outdoor-photo-jp-flat-illustration/
│   ├── .codex-plugin/plugin.json      # 插件清单
│   ├── README.md
│   └── skills/outdoor-photo-jp-flat-illustration/
│       ├── SKILL.md
│       ├── references/
│       ├── scripts/
│       └── templates/
```

## 使用

把一张户外照片发给 Codex，并说明“用 outdoor-photo-jp-flat-illustration 转成日式扁平插画”，即可生成对应风格的插画提示词。

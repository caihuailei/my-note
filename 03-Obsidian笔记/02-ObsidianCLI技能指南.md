# Obsidian CLI 技能完全指南

## 🚀 快速入门
```bash
# 安装 Obsidian CLI
npm install -g obsidian-cli

# 初始化工作空间
obsidian-cli init F:/biji/笔记
```

## 📋 核心命令
### 笔记操作
```bash
obsidian-cli create "新笔记.md" --content "开始写作..."
obsidian-cli search "AI"
obsidian-cli link "旧笔记.md" "新笔记.md"
```

### 自动化流程
```yaml
# cron.yaml - 每日18:00执行
tasks:
  - name: 整理重复笔记
    command: obsidian-cli deduplicate -p .
## 目录

- ## 为什么需要“第二大脑” [原片 @ 00:42](https://www.bilibili.com/video/BV1cGXVBTEz4?t=42)*
- ## 持久化上下文 [原片 @ 00:46](https://www.bilibili.com/video/BV1cGXVBTEz4?t=46)*
- ## 双向记忆与更新 [原片 @ 02:26](https://www.bilibili.com/video/BV1cGXVBTEz4?t=146)*
- ## 技能构建的优化 [原片 @ 03:10](https://www.bilibili.com/video/BV1cGXVBTEz4?t=190)*
- ## 跨AI平台兼容性 [原片 @ 05:29](https://www.bilibili.com/video/BV1cGXVBTEz4?t=329)*
- ## 团队协作与扩展 [原片 @ 06:24](https://www.bilibili.com/video/BV1cGXVBTEz4?t=384)*
- ## Obsidian 的工作原理 [原片 @ 07:02](https://www.bilibili.com/video/BV1cGXVBTEz4?t=422)*
- ## claude.md 文件的作用 [原片 @ 07:55](https://www.bilibili.com/video/BV1cGXVBTEz4?t=475)*
- ## 与 Claude 内置记忆的区别 [原片 @ 09:16](https://www.bilibili.com/video/BV1cGXVBTEz4?t=556)*
- ## Obsidian 的优势 [原片 @ 09:41](https://www.bilibili.com/video/BV1cGXVBTEz4?t=581)*
- ## 系统架构与长期价值 [原片 @ 10:42](https://www.bilibili.com/video/BV1cGXVBTEz4?t=642)*
- ## 文件结构建议 [原片 @ 13:19](https://www.bilibili.com/video/BV1cGXVBTEz4?t=799)*
- ## 设置步骤详解 [原片 @ 17:02](https://www.bilibili.com/video/BV1cGXVBTEz4?t=1022)*
- ## 插件辅助设置 [原片 @ 17:40](https://www.bilibili.com/video/BV1cGXVBTEz4?t=1060)*
- ## AI 总结

---

## 为什么需要“第二大脑” [原片 @ 00:42](https://www.bilibili.com/video/BV1cGXVBTEz4?t=42)*

当前大多数AI代理在使用时，每次对话都从零开始，缺乏对用户背景、项目和工作流程的理解。这种模式限制了AI成为真正自主工作的核心接口。

为了解决这一问题，视频提出构建一个“第二大脑”系统——即一个持久化的知识库，使AI能够持续访问并理解用户的上下文信息。

该系统的核心目标是：
- 提供**持久化上下文**（Persistent Context）
- 实现**双向记忆**（Two-Way Memory）
- 支持**跨AI平台兼容性**
- 具备**团队可扩展性**

通过这个系统，AI不再只是工具，而是成为能够理解业务、学习决策、自动执行任务的智能助手。

---

## 持久化上下文 [原片 @ 00:46](https://www.bilibili.com/video/BV1cGXVBTEz4?t=46)*

### 传统AI的局限性
- 每次对话独立进行，无法保留历史信息。
- 用户必须重复解释自己的情况、项目、策略等。
- 缺乏对个人或组织整体背景的理解。

### 第二大脑如何解决？
- 将所有关键信息存储在Obsidian中，形成一个中央知识库。
- 包括但不限于：
  - 企业战略
  - 项目进度
  - 品牌定位
  - 工作流程
  - 团队成员角色
  - 会议记录
  - 客户画像（ICP）

### 实际应用示例
- 在Claude Code中提问：”我今天应该专注于什么？”
- AI会自动读取Obsidian中的上下文文件，如每日计划、优先级列表、待办事项等。
- 返回答案：应关注”落地页文案修改”、”录制Obsidian视频”、”安排西班牙线下活动”。

---

## 双向记忆与更新 [原片 @ 02:26](https://www.bilibili.com/video/BV1cGXVBTEz4?t=146)*

除了读取上下文，第二大脑还支持**双向交互**——AI不仅可以获取信息，还能将新产生的知识写回知识库。

### 关键机制
- 当用户在AI聊天中做出决策或设定规则时，可以明确指令：“记住这一点在我的第二大脑中。”
- AI会将这些内容保存到对应的Markdown文件中，例如写作偏好文档。

### 示例场景
- 用户发现AI生成的内容使用了M-dash（—），但自己不喜欢这种方式。
- 指令：“不要在为我撰写内容时使用M-dashes。”
- AI将其作为一条规则添加到`writing_preferences.md`文件中。
- 此后所有相关技能（如LinkedIn发帖、newsletter撰写）都会继承此规则。

### 复合效应
随着时间推移，每一次互动都在强化AI的认知能力：
- 决策被记录 → 规则被建立 → 流程被优化 → 效率提升
- 这种**复合增长**使得AI越用越聪明。



---

## 技能构建的优化 [原片 @ 03:10](https://www.bilibili.com/video/BV1cGXVBTEz4?t=190)*

在Claude平台上，“技能”（Skills）是预设的任务流程模板，用于自动化特定操作，如撰写LinkedIn帖子。

### 传统方式的问题
- 每个技能都需要包含大量参考文件（如品牌指南、语气模板、客户画像等）。
- 需要重复配置相同的信息，导致维护成本高。
- 更新一处需手动同步到多个技能中。

### 新方法：指向第二大脑
- 不再将参考文件嵌入技能本身，而是让技能**引用**Obsidian中的对应文件。
- 例如：
  - `linkedin_instant.skill`仅包含流程说明。
  - 所有上下文（如ICP、语气风格）由`claude.md`指引至Obsidian中的相应文档。

### 优势
- **统一管理**：只需修改一次文件，所有依赖该文件的技能自动更新。
- **快速迭代**：新建技能时只需定义流程，无需重复输入上下文。
- **减少冗余**：避免重复存储相同数据。


---

## 跨AI平台兼容性 [原片 @ 05:29](https://www.bilibili.com/video/BV1cGXVBTEz4?t=329)*

第二大脑的本质是一个本地的Markdown文件夹，因此它可以被任何支持文件读写的AI代理访问。

### 支持的平台包括：
- **Claude Code**
- **Claude Cowork**
- **Codex**
- **Entiregravity**
- 其他任意AI代理服务

### 实践演示
- 给不同AI提供相同的Obsidian文件夹路径（如`BenAIS`）。
- 同一个问题：“我今天应该专注什么？”
  - Claude Code回答：落地页文案、Obsidian视频、西班牙线下活动。
  - Codex回答：落地页文案、YouTube制作、西班牙线下活动。
- 结果一致，说明上下文共享成功。

### 核心逻辑
- 所有AI都读取同一个知识源。
- 不受平台限制，实现真正的**跨系统一致性**。


---

## 团队协作与扩展 [原片 @ 06:24](https://www.bilibili.com/video/BV1cGXVBTEz4?t=384)*

该系统不仅适用于个人，还可扩展至整个团队，打造企业级AI操作系统。

### 团队共享的优势
- 所有成员的AI代理共享同一套知识库。
- 包含：
  - 公司战略
  - ICP文档
  - 品牌声音
  - 公司目标
  - SOP流程
- 团队成员无论使用哪个AI平台，都能获得一致的知识支持。

### 应用场景
- 工程师可基于品牌声音撰写LinkedIn文章。
- 销售人员可根据最新客户洞察调整话术。
- 新员工可通过知识库快速上手。

### 协同机制
- 使用Obsidian的同步功能，确保团队成员之间的上下文实时更新。
- 任何人在任一设备上的更改都会反映在整个系统中。


---

## Obsidian 的工作原理 [原片 @ 07:02](https://www.bilibili.com/video/BV1cGXVBTEz4?t=422)*

Obsidian并不是一个复杂的数据库，而是一个**可视化文件管理器**。

### 核心概念
- **Vault**：Obsidian中的“知识库”，实际上就是电脑上的一个文件夹。
- **文件格式**：全部为Markdown（`.md`）文件。
- **链接系统**：通过内部链接（`[[文件名]]`）建立文档间的关联。

### 与AI集成的方式
- 将Obsidian的Vault路径提供给AI代理（如Claude Cowork、Claude Code）。
- AI可以直接读取和写入这些文件。
- 无需API、云同步或中间层，完全本地运行。

### 为何选择Obsidian？
- **免费且开源**
- **强大的图谱视图**：展示文档间的关系网络。
- **灵活的标签与属性系统**：便于分类与检索。
- **命令行支持**（CLI）：适合自动化脚本调用。


---

## claude.md 文件的作用 [原片 @ 07:55](https://www.bilibili.com/video/BV1cGXVBTEz4?t=475)*

`claude.md` 是整个系统的”导航地图”或”系统提示”（system prompt），告诉AI如何查找和更新信息。

### 功能描述
- 类似于一个全局指令文件，定义了：
  - 文件夹结构
  - 如何定位特定信息
  - 数据写入规则
  - 上下文加载顺序

### 示例内容
```markdown
# Folder Instructions
Use this to give Claude instructions for working in this folder.

## Organization Assistant
You are an organization AI assistant. Your identity, behavior, and output style are defined by this system.

## Session Startup
At the START of every conversation:
1. context/operator.md — who the operator is (name, role, responsibilities)
2. The most recent file in 'Daily/' — what happened last session
```

### 工作流程
1. 用户提问 → AI判断需要更多信息。
2. AI读取`claude.md`以确定去哪里找。
3. AI读取指定文件（如会议记录）。
4. AI整合信息并返回答案。
5. 若有新信息，AI根据`claude.md`规则写回正确位置。

---

## 与 Claude 内置记忆的区别 [原片 @ 09:16](https://www.bilibili.com/video/BV1cGXVBTEz4?t=556)*

虽然Claude自身具备一定的记忆功能，但其局限性明显：

| 对比维度 | Claude 内置记忆 | Obsidian 第二大脑 |
|--------|------------------|--------------------|
| 存储形式 | 单一文档 | 多文件结构 |
| 内容范围 | 基础事实 | 完整上下文（策略、项目、关系） |
| 更新方式 | 手动设置 | 自动双向同步 |
| 可视化 | 无 | 图谱视图清晰展示关系 |
| 团队共享 | 有限 | 支持多人协作 |

### 关键差异
- **规模**：内置记忆通常只存储少量关键点；Obsidian可容纳数千个文档。
- **灵活性**：Obsidian允许复杂结构与层级关系；内置记忆较扁平。
- **可扩展性**：Obsidian可连接外部工具、插件、自动化流程。


---

## Obsidian 的优势 [原片 @ 09:41](https://www.bilibili.com/video/BV1cGXVBTEz4?t=581)*

尽管你可以在普通文件夹中实现类似功能，但Obsidian提供了显著优势：

### 主要优点
- **可视化图谱**：自动识别文档间链接，形成知识网络。
  - 示例：品牌文档链接到ICP文档，AI可据此推理。
- **搜索与过滤**：支持标签、属性、全文搜索。
- **版本控制**：支持Git集成，追踪变更历史。
- **跨平台同步**：通过Obsidian Sync或第三方工具实现多设备同步。
- **插件生态**：丰富插件增强功能（如日历、任务管理、代码块）。

### 使用建议
- 初期不必追求完美结构，先建立基础框架。
- 随着使用自然生长，AI会帮你生成更多内容。
- 重点在于**持续积累**而非一次性设计。



---

## 系统架构与长期价值 [原片 @ 10:42](https://www.bilibili.com/video/BV1cGXVBTEz4?t=642)*

该系统不仅仅是提高效率的工具，更是一种**未来工作模式的雏形**。

### 核心趋势
1. **AI推理能力增强**：AI越来越擅长逻辑推理和软件操作。
2. **技能与插件成熟**：可自动化复杂任务（如邮件跟进、报告生成）。
3. **上下文缺失**：此前阻碍AI自主性的最大瓶颈。

### 解决方案
- 通过第二大脑补足上下文，使AI能够：
  - 理解业务全貌
  - 做出符合策略的决策
  - 自主执行端到端流程

### 长期复利效应
- 每一次决策都被记录 → 形成知识资产
- 每一次修正都被保存 → 提升AI准确性
- 每一项技能都被优化 → 构建智能闭环

> “六个月后的AI比第一天强得多，因为它的‘大脑’已经积累了大量智慧。”



---

## 文件结构建议 [原片 @ 13:19](https://www.bilibili.com/video/BV1cGXVBTEz4?t=799)*

推荐两种初始文件结构：**企业版** 和 **个人版**。

### 企业版（团队适用）
```
├── context/
│   ├── team.md
│   ├── strategy.md
│   ├── brand.md
│   └── icp.md
├── daily/
│   └── 2024-03-25.md
├── departments/
│   ├── community/
│   │   └── youtube_to_community_sop.md
│   └── engineering/
├── intelligence/
│   ├── meeting_transcripts/
│   └── competitor_research.md
├── onboarding/
│   └── new_team_member_guide.md
├── projects/
│   └── obsidian_video_project.md
├── resources/
│   └── prompt_templates.md
├── skills/
│   └── linkedin_post_generator.md
├── tasks/
│   └── todo_list.md
└── teams/
    └── ben_ai.md
```

### 个人版（独行者适用）
- 移除`departments`、`teams`、`onboarding`等模块。
- 保留核心结构：context、daily、projects、skills、tasks。

### 设计原则
- **简单开始**：从5个文件起步。
- **自然演化**：随着使用逐步扩展。
- **可重用性**：将通用资源集中存放。

---

## 设置步骤详解 [原片 @ 17:02](https://www.bilibili.com/video/BV1cGXVBTEz4?t=1022)*

### 第一步：安装Obsidian
- 访问官网下载并安装。
- 创建新Vault（如命名为`BenAI_test`）。
- 选择一个本地文件夹作为存储位置。

### 第二步：配置AI代理
- 在Claude Cowork或Claude Code中，授予AI访问该文件夹的权限。
- 确保路径正确，AI可读写。

### 第三步：创建`claude.md`
- 在根目录创建`claude.md`文件。
- 输入基本导航指令，如：
  ```markdown
  # Folder Instructions
  At the start of each session, load:
  - context/operator.md
  - daily/latest.md
  ```

### 第四步：填充初始上下文
- 通过AI提问引导生成内容，例如：
  - “帮我写下我的品牌定位。”
  - “总结一下我们上周的会议要点。”

---

## 插件辅助设置 [原片 @ 17:40](https://www.bilibili.com/video/BV1cGXVBTEz4?t=1060)*

为了简化设置过程，作者开发了一个名为 **BenAI CDM Plugin** 的插件。

### 功能特点
- 自动生成推荐文件结构。
- 引导用户填写关键上下文信息。
- 快速部署`claude.md`指令。
- 支持个人与企业两种模式。

### 安装方式
1. 进入Claude Code → Customize → Add Marketplace。
2. 添加AI加速器提供的插件链接。
3. 在插件市场中找到“BenAI CDM Plugin”并安装。
4. 运行插件，选择“solopreneur”或“business”模式。
5. 回答几个问题即可完成初始化。

### 使用效果
- 几分钟内搭建完整知识库。
- 自动创建必要的文件和链接。
- 降低入门门槛，适合非技术用户。


---

## AI 总结

本视频展示了如何利用Obsidian构建一个”第二大脑”系统，使其与Claude AI（如Claude Cowork、Claude Code）深度集成，赋予AI持久记忆、双向学习和跨平台协作能力。通过将所有上下文信息存储在本地Markdown文件中，并借助`claude.md`文件进行导航，AI能够理解用户的业务、策略和偏好，从而实现高度个性化的自动化工作流。该系统不仅提升了个人效率，还可扩展至团队，推动企业向AI驱动的工作模式转型。核心理念是：**上下文才是未来的竞争力**，越早开始积累，AI就越强大。

## 我的总结

这是一个卖自己知识产品的博主，但是他的视频内容还是可以的
<p align="center"><img src="logo.png" width="180" alt="活人感 logo"></p>

# 活人感 · astrbot_plugin_humanlike

给 AstrBot 加一层「像人」的东西：学群里怎么说话、记得住人、偶尔自己上网找梗、学会自己收表情包。

并不是人格插件，人格还是用你自己写的那份。它只负责把**语气、习惯、记忆**喂给模型。

## 它做什么

| 模块 | 作用 |
|---|---|
| 风格学习 | 每个会话攒够消息就让模型提炼「这个群怎么说话」，注入系统提示 |
| 自我复盘 | 拿自己的回复和群风格对比，产出修正建议（可关） |
| 跨会话记忆 | 同一个人在不同群/私聊说过的话，它会记住。 |
| 用户档案 | 按 QQ 号建档案：称呼、喜好、不喜欢什么、最近在忙什么 |
| 群成员小本本 | 注入最近活跃的人，帮她分清谁是谁 |
| 网感 | 定时从B站热门评论里提炼当下的网络语气 |
| 表情包 | 自动收藏群里的图，按概率回图 |
| 翻旧账 | 读 AstrBot 历史消息库，补档案；提供关键词搜索工具 |
| 联网 | 内置 `web_search` / `web_read`，不需要额外 API key |
| 插件推荐 | 扫插件市场，把没装的高星插件私信推给管理员 |

## 安装

把本仓库放进 AstrBot 的插件目录：

```
<AstrBot>/data/plugins/astrbot_plugin_humanlike
```

重启 AstrBot，在 WebUI 的插件管理里启用并配置。

依赖：`aiohttp`（AstrBot 自带，`requirements.txt` 里仍显式声明）。

## 命令

| 命令 | 作用 |
|---|---|
| `/活人感状态` | 看当前会话学到了什么、存了几张图 |
| `/活人感学习` | 立刻学一轮 |
| `/活人感用户` | 看自己的档案 |
| `/活人感记住 <内容>` | 手动往档案里记一条 |
| `/活人感翻旧账` | 重新扫一遍历史消息 |
| `/活人感上网` | 立刻抓一轮网感 |
| `/活人感推荐` | 立刻扫一次插件市场 |
| `/活人感不用` | 十天不再推插件 |

## 配置

所有配置都能在 WebUI 里改。下表是完整清单。

<!-- CONFIG_TABLE:START -->
| 键 | 说明 | 默认 |
|---|---|---|
| `enabled` | 启用活人感插件 | `True` |
| `style_enabled` | 学习群友说话方式（需要调用一次 LLM，按条数触发） | `True` |
| `style_learn_every` | 每积累多少条新消息学习一轮（太小会费 token） | `25` |
| `style_max_samples` | 每个群最多保留多少条样本 | `120` |
| `style_max_chars` | 注入提示词的风格片段最大字数 | `600` |
| `style_inject` | 把学到的风格注入系统提示词 | `True` |
| `style_self_review` | 自我复盘：定期拿自己的回复和群风格对比，产出修正建议 | `True` |
| `style_global` | 跨会话：把每个会话学到的风格汇总成全局风格，在别的对话里也能用 | `True` |
| `style_global_chars` | 全局风格注入的最大字数 | `220` |
| `user_memory_enabled` | 按 QQ 号认人：给每个人建长期档案，跨群跨私聊共用 | `True` |
| `user_learn_every` | 同一个人每积累多少条发言更新一次档案 | `30` |
| `user_max_chars` | 单人档案注入的最大字数 | `300` |
| `cross_memory_enabled` | 跨会话内容记忆：把这个人在别的群/私聊说过的话带一段过来 | `True` |
| `cross_max_msgs` | 每次带几条最近的消息 | `8` |
| `cross_max_chars` | 跨会话片段的最大字数 | `320` |
| `backfill_enabled` | 允许翻 AstrBot 的历史消息库补档案（只读） | `True` |
| `backfill_on_start` | 启动 90 秒后自动翻一次历史 | `True` |
| `backfill_limit` | 每次最多翻多少条历史消息 | `300` |
| `web_search_enabled` | 允许她联网搜索（Bing/搜狗，不需要 API key） | `True` |
| `tidy_linebreaks` | 把回复里的换行并成逗号，避免 QQ 里出现生硬分行 | `True` |
| `web_enabled` | 从网上公开语料里学「网感」（B 站热门高赞评论） | `True` |
| `web_interval_hours` | 每多少小时上网学一次（0=只手动） | `12` |
| `web_video_count` | 每次抓几个热门视频的评论 | `6` |
| `web_max_comments` | 每次最多用多少条评论作为语料 | `60` |
| `web_inject` | 把网感注入提示词（建议开，但限得很短） | `True` |
| `web_max_chars` | 网感片段注入的最大字数 | `260` |
| `reply_short` | 限制回复长度与条数 | `True` |
| `group_reply_max_chars` | 群聊单条回复的字数上限 | `40` |
| `private_reply_max_chars` | 私聊每条回复的字数上限 | `100` |
| `private_max_messages` | 私聊最多分几条发（1=不分） | `2` |
| `knowledge_max_chars` | 被问正经问题时的字数上限（会放宽） | `260` |
| `knowledge_max_messages` | 被问正经问题时群里最多分几条 | `2` |
| `persona_reminder_enabled` | 每轮在末尾重申一次人设，防止她忘了自己是谁 | `True` |
| `persona_reminder_chars` | 人设重申的最大字数 | `240` |
| `roster_enabled` | 注入群成员花名册，帮她分清不同的人 | `True` |
| `roster_max_chars` | 花名册注入的最大字数 | `260` |
| `meme_enabled` | 自动收藏群里的图片/表情包 | `True` |
| `meme_max_kb` | 单张图最大体积（KB），超过就不收 | `2048` |
| `meme_groups` | 只在这些群收图（留空=所有群） | `[]` |
| `meme_send_enabled` | 用收藏的表情包回图 | `True` |
| `meme_reply_probability` | 普通回复时附一张图的概率 | `0.12` |
| `meme_reply_on_image_probability` | 对方发图时回图的概率 | `0.6` |
| `meme_send_cooldown` | 同一会话两张图之间最小间隔（秒） | `300` |
| `recommend_enabled` | 启用插件推荐 | `True` |
| `recommend_admin_qq` | 推荐私信发给哪个 QQ（只填号码） | `` |
| `recommend_min_stars` | 只推荐 Star 数不低于这个值的插件 | `30` |
| `recommend_top_n` | 每次最多推荐几个 | `3` |
| `recommend_auto_hours` | 每隔多少小时自动推荐一次（0=关闭自动，只手动） | `0` |
| `debug` | 输出调试日志 | `False` |
<!-- CONFIG_TABLE:END -->

## 数据存在哪

```
data/plugin_data/astrbot_plugin_humanlike/
├── state.json      # 所有学习结果（档案、风格、表情索引）
└── memes/          # 收藏的图，按 sha1 前两位分目录
```

`state.json` 是纯JSON，可以直接看、直接改、直接备份。删掉等于清空记忆。

## 关于 token

这个插件会主动调模型：

- 风格学习：每 `style_learn_every` 条消息一次
- 用户档案：每 `user_learn_every` 条一次
- 网感：每 `web_interval_hours` 小时一次
- 自我复盘：默认关

每轮对话还会往提示词里注入几百字（风格、档案、网感、花名册）。嫌贵就把 `style_max_chars`、`web_max_chars`、`user_max_chars` 调小，或者直接关掉对应模块。

## 隐私说明

- 会读取AstrBot自己的 `data_v4.db`（`platform_message_history` 表），只读，用来补历史档案。
- 会把群友的发言片段发给当前配置的模型，用于提炼风格和档案。
- 联网搜索会把关键词发给B 站/Bing。
- 收藏的图片只存在本地，不会上传。
- 小本本会带QQ号，介意的话把 `roster_enabled` 关掉。

## 兼容性

- 只在aiocqhttp（NapCat / onebot v11）下完整可用。
- 合并转发解析依赖 AstrBot 与平台适配器，开启后会把转发内容展平成文本。
- 表情回图依赖平台支持图片消息。
- AstrBot >= 4.24.0。

## 许可

MIT，见 [LICENSE](LICENSE)。

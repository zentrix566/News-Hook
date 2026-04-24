# News-Hook

每日新闻推送，通过 GitHub Actions 定时抓取并分分类推送到飞书群组。

## 功能

- 分多次推送，每个分类单独一条消息
- **AI 资讯**：中文 + 英文
- **运维/DevOps**：中文 + 英文
- **国际新闻**：英文
- **国内新闻**：中文
- 通过 GitHub Actions 定时执行（每天一次）
- 自动推送到飞书群组通过 Webhook

## 配置说明

### 环境变量

在 GitHub Secrets 中配置以下环境变量：

- `FEISHU_INFORMATION_WEBHOOK` - 飞书机器人 Webhook 地址

### 本地开发

1. 克隆项目
```bash
git clone https://github.com/yourusername/News-Hook.git
cd News-Hook
```

2. 创建环境变量文件
```bash
cp .env.example .env
# 编辑 .env 填入你的飞书 Webhook 地址
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行
```bash
python main.py
```

## 自定义新闻源

编辑 `config.py` 中的 `RSS_FEEDS` 配置添加或修改新闻源。

## 定时任务

GitHub Actions 默认每天北京时间 9 点执行一次，可以在 `.github/workflows/send-news.yml` 中修改 cron 表达式。

## License

MIT © [zentrix566]()

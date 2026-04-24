# News-Hook

🤖 AI 新闻和运维资讯每日推送，通过 GitHub Actions 定时抓取并发送到飞书群组。

## 功能

- 每日自动抓取 AI 领域最新新闻
- 每日自动抓取 DevOps/运维领域相关资讯
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

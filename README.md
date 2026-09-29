# EnterpriseAIDocumentPlatform

## Project documents

- [Project specification](enterprise-ai-project-spec.md)
- [Learning tasks and acceptance record](LEARNING_TASKS.md)


## Local setup

```sh
git clone https://github.com/ZhiouZhu2001/EnterpriseAIDocumentPlatform.git
cd EnterpriseAIDocumentPlatform
cp .env.example .env
docker compose up -d
cd backend
uv sync --locked
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 39800
```

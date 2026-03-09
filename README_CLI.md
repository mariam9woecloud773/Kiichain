# KiiChain CLI

Терминальное приложение (CMD) по описанию проекта KiiChain. Оформление — **Rich**.

## Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python main.py
```

## Меню

| Код | Действие |
|-----|----------|
| 1 | **Install Dependencies** — инструкции по установке Go 1.24.11+ и проверка версии |
| 2 | **Settings** — аппаратные требования (RAM, SSD, ядра) |
| 3 | **About** — о проекте и содержимое папки `about/` с хэштегами |
| 4 | **Quick Links** — Oro Testnet, Explorer, Faucet (с возможностью открыть в браузере) |
| 5 | **Documentation & Resources** — документация, Developer Hub, Whitepaper, Blog |
| 6 | **Hardware Requirements** — минимум и рекомендации по железу |
| 7 | **Operating System** — поддерживаемые ОС (Linux, Arch, Ubuntu) |
| 0 | Выход |

## Папка `about/`

Файлы с описанием проекта и хэштегами по README:

- `project.md` — о KiiChain, фичи, #Kiichain #blockchain #EVM #CometBFT #stablecoins #RWA #DeFi #Solidity #crypto
- `testnet.md` — Oro Testnet, #OroTestnet #testnet #validator #faucet #explorer #Kiichain
- `resources.md` — документация и ресурсы, #Documentation #Whitepaper #DeveloperHub #Kiichain #builders
- `tech.md` — Go, ОС, железо, #Go #golang #Linux #hardware #Kiichain #node #validator

## Зависимости

- Python 3.8+
- [Rich](https://github.com/Textualize/rich) — оформление в терминале

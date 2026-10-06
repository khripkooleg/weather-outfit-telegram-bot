# Weather Outfit Telegram Bot

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Framework](https://img.shields.io/badge/framework-aiogram_v3-blue.svg)
![Infrastructure](https://img.shields.io/badge/IaC-Terraform-purple.svg)
![Configuration](https://img.shields.io/badge/CM-Ansible-red.svg)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

**Weather Outfit Telegram Bot** - це повністю автоматизований, AI-powered Телеграм-Бот, створений на базі `aiogram`. Цей бот аналізує поточний прогноз погоди (поки що тільки для Вінниці) та надає щоденні персоналізовані поради щодо вибору одягу з урахуванням температурного режиму за допомогою **Google Gemini API**.

---

## Основні можливості
* **Прогноз погоди та стилістика**: Генерує поради щодо вибору вбрання відповідно до температури та погодних умов за допомогою OpenMeteo та Google Gemini AI.
* **Контейнеризація**: Запуск програми у середовищі Docker.
* **Автоматизований деплой**: Повне автоматтичне розгортання на віддалений AWS EC2 сервер та оновлення через GitHub Actions Pipeline.

---

## Тех. стек
* **Language/Framework**: Python 3.11+, `aiogram 3.x`.
* **AI Engine**: Google Gemini API.
* **Cloud Infrastructure**: AWS ( ECR, EC2 ) розгорнуті через Terraform та налаштовані Ansible.
* **CI/CD Pipeline**: Github Actions ( збірка, публікація в AWS ECR, деплой через ssh ).
* **Containerization**: Dockerfile, Docker Compose.

---

## Структура проєкту

```
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD Pipeline (Build, Push to ECR, Deploy to EC2)
├── ansible/
│   ├── aws-infra/
│   │   ├── tasks/
│   │   │   ├── install.yml       # Встановлення Docker, AWS CLI, залежностей
│   │   │   ├── main.yml          # Точка входу виконання задач
│   │   │   └── verify.yml        # Перевірка Docker та аутентифікація в ECR
│   │   └── inventory.ini
│   ├── group_vars/
│   │   └── all.yml               # Глобальні змінні Ansible (aws_region, ecr_repo_url)
│   ├── inventory/
│   │   └── hosts.yml             # Опис хостів для Ansible
│   ├── ansible.cfg               # Конфігурація Ansible
│   └── playbook.yml              # Головний Playbook для налаштування сервера
├── terraform/                    # HCL конфігурації для інфраструктури AWS (VPC, EC2, ECR)
├── bot/                          # Вихідний код Telegram-бота
├── docker-compose.yml            # Специфікація для запуску боту на EC2
├── Dockerfile                    # Інструкція збірки Docker-образу
├── requirements.txt              # Залежності Python
└── README.md
```

---

## Локальний запуск та розробка
1. Клонування репозиторію шляхом `git clone https://github.com/khripkooleg/weather-outfit-telegram-bot`.
2. Створення файлу середовища `.env` у корінній директорії та задання наступних значень: `BOT_TOKEN` - API ключ Телеграм-Бота, `AI_KEY` - API ключ Gemini AI.
3. Запуск через Docker Compose: `docker compose up -d --build`.

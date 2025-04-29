
# FinanceLog — Personal Finance Tracker Bot 📈

A Telegram bot designed for personal finance management.  
Track your income and expenses directly through Telegram, store transactions securely in a local database, and review your financial history anytime.

Built with Python, aiogram, and SQLite.

---

## 🧩 Features

- Add income and expenses via simple Telegram commands
- Track your current balance
- View complete transaction history
- Secure data storage using SQLite
- Modular and scalable code structure
- Environment variables for secure configuration

---

## 🧱 Technologies Used

- Python 3.10+
- [aiogram](https://docs.aiogram.dev/en/latest/) — Telegram Bot Framework
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment configuration
- SQLite — Local database (built-in with Python)

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/tikoarm/python-finance-log.git
cd FinanceLog
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```dotenv
TG_TOKEN=your-telegram-bot-token
```

4. Run the bot:

```bash
python3 main.py
```

---

## 🛠 Project Structure

```plaintext
FinanceLog/
│
├── modules/
│   ├── base_utils.py        # Utility functions
│   ├── functions.py         # Business logic (add income/expense, balance)
│   ├── tg_bot.py            # Telegram bot handlers
│   ├── SqlCode.py           # SQL queries
│   └── settings.py          # Environment configuration
│
├── database.db              # SQLite database
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (not included in GitHub)
├── main.py                  # Project entry point
└── README.md
```

---

## 📄 License & Attribution

This project is provided for educational and non-commercial use.  
If you use or modify this project, please give proper credit.

---

## 👨‍💻 Author

Developed by **Tigran Kocharov**  
📧 tiko.nue@icloud.com

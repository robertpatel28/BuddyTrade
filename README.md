# 📊 BuddyTrade – Stock Portfolio Dashboard (Python + PyQt6)

**BuddyTrade** is a desktop stock analysis and portfolio management system developed using Python and PyQt6. Designed with a scalable MVC architecture and a command-driven state engine, the system enables users to manage their portfolios, perform technical stock analysis, and explore market insights through a user-friendly GUI.

---

## 🚀 Key Features

- 📈 Dynamic portfolio viewer with entry price, shares, current price, gain/loss, and recommendations
- 📊 Technical indicator analyzer (EMA, SMA, RSI, ADX, Volume SMA, etc.)
- 📋 Personalized watchlist panel
- 📰 Market summary and insights frame
- 🖥️ PyQt6 GUI auto-generated from Qt Designer `.ui` files
- 🧠 MVC + Command pattern for maintainable architecture
- 🗄️ Azure SQL Database integration for persistent storage
- 🔒 Login/logout view state management with `CommandValue` enums

---

## 🔧 Technologies Used

- `Python 3.11+`
- `PyQt6`
- `Azure SQL Database`
- `ODBC Driver 17+`
- `Object-Oriented Programming`
- `MVC Design Pattern`
- `Command Pattern`
- `Qt Designer`

---

## 📁 Core Classes & Structure

| Class / File                      | Description                                                                 |
|-----------------------------------|-----------------------------------------------------------------------------|
| `main.py`                         | Entry point of the application                                              |
| `dashboard_controller.py`         | Loads the main dashboard, portfolio, watchlist, and charts                 |
| `portfolio_controller.py`         | Manages portfolio-related data flow and updates                            |
| `user_controller.py`              | Handles login, logout, and user session state                              |
| `analysis_controller.py`          | Loads and responds to technical analysis interactions                      |
| `db_service.py`                   | Azure SQL data access layer; handles portfolio, user, and analysis queries |
| `auth_service.py`                 | Provides user authentication functions                                     |
| `app_state.py`                    | Controls global state transitions using commands                           |
| `command.py`                      | Defines `Command` and `CommandValue` enums for state control               |
| `state_machine.py`                | Core finite state engine logic                                             |
| `dashboard.py`                    | `Ui_dashboard` view generated from `dashboard.ui`                          |
| `login.py`                        | `Ui_login` view from `login.ui`                                            |
| `home_logged_in.py`              | `Ui_home_logged_in` view from `home_logged_in.ui`                          |
| `home_logged_out.py`             | `Ui_home_logged_out` view from `home_logged_out.ui`                        |
| `analysis.py`                     | `Ui_analysis` view from `analysis.ui`                                      |
| `user.py`                         | User model (id, email, password, etc.)                                     |
| `portfolio.py`                    | Portfolio model (ticker, shares, price, gain/loss, etc.)                   |
| `holding.py`                      | Represents a single stock position                                         |
| `orchestrator_agent.py`          | Agent pipeline orchestrator (future AI integration)                        |
| `search_agent.py`                 | Stub for semantic search integration                                       |
| `portfolio_agent.py`              | Stub for portfolio analytics agent                                         |
| `news_sentiment_agent.py`         | Stub for news sentiment analysis                                           |
| `alert_agent.py`                  | Stub for alert/trigger generation                                          |
| `api_service.py`                  | Connects to external APIs (for market data, etc.)                          |
| `file_service.py`                 | Handles file uploads/downloads if used                                     |

---

## 🧠 Concepts Demonstrated

- MVC structure for GUI and logic separation
- GUI Controller for every `.ui` view
- Command pattern with `CommandValue` enum for view state routing
- Persistent storage using Azure SQL + `pyodbc`
- Modular service layers for authentication, data access, and state control
- Qt Designer `.ui` files compiled and linked dynamically via PyQt6
- Responsive architecture for scaling with future AI integrations

---

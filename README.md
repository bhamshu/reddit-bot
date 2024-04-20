# Reddit Bot

A Reddit bot for automating tasks on Reddit. Follow these steps to set up and initialize the database.

## Quick Setup

1. **Environment Setup**

   - Ensure Python 3.6+ is installed.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configuration**

   - Create a `.env` from `.env.example` and update it with your database settings:
     ```bash
     cp .env.example .env
     ```

3. **Database Initialization**
   - Run `db.init_db.py` to set up your database:
     ```bash
     python -m db.init_db
     ```

Now your environment is ready, and the database is initialized.

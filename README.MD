# TWIXIT

![Twixit Banner](/twixit/assets/Banner.png)

![Stars](https://img.shields.io/github/stars/DevBrianMatthews/twixit?style=for-the-badge&logo=github&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/DevBrianMatthews/twixit?style=for-the-badge&logo=github&logoColor=white&color=orange)
![License](https://img.shields.io/github/license/DevBrianMatthews/twixit?style=for-the-badge&color=000000)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.x-black?style=for-the-badge&logo=playwright&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=for-the-badge&color=blue)

Twixit is a command-line tool that automatically deletes Tweets and Retweets on X. You can delete everything in order, by time periods, or by specific dates.

---

## 📋 Requirements

- Python 3.10+
- Your `tweets.js` file — request it from X

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/DevBrianMatthews/twixit.git
cd twixit
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate        # Mac/Linux
env\Scripts\activate           # Windows
```

3. Install dependencies:

```bash
pip install python-dotenv playwright pyfiglet click
playwright install chromium
```

4. Create a `.env` file in the root folder with your credentials:

```
X_USERNAME=your-username
X_PASSWORD="your-password"
```

5. Download your Twitter archive from X:
   `Settings → Your Account → Download an archive of your data`

    Place the `tweets.js` file (found inside the `data/` folder of the archive) in the root directory of this project.

---

## 🚀 Usage

### Adding credentials

When you run the command for the first time, **Twixit** will ask for your `x.com` credentials and save them locally. After that you can run any command.

```
> python twixit.py

 ______                            __
/\__  _\            __          __/\ \__
\/_/\ \/ __  __  __/\_\   __  _/\_\ \ ,_\
   \ \ \/\ \/\ \/\ \/\ \ /\ \/'\/\ \ \ \/
    \ \ \ \ \_/ \_/ \ \ \\/>  </\ \ \ \ \_
     \ \_\ \___x___/'\ \_\/\_/\_\\ \_\ \__\
      \/_/\/__//__/   \/_/\//\/_/ \/_/\/__/

> Enter your username:
> Enter your password:
> Repeat for confirmation:

✓ Credentials saved. Run 'python twixit.py --help' to see available options.
```

---

### `twixit.py --limit [int]`

Deletes the specified number of tweets, from the most recent to the oldest.

```bash
python twixit.py --limit 10

# This example deletes only the 10 most recent tweets
```

---

### `twixit.py --after [yyyy-mm-dd]`

Deletes all tweets posted after the given date.

```bash
python twixit.py --after 2022-01-15

# This example deletes all tweets after January 15, 2022
```

---

### `twixit.py --before [yyyy-mm-dd]`

Deletes all tweets posted before the given date.

```bash
python twixit.py --before 2022-01-15

# This example deletes all tweets before January 15, 2022
```

---

### `twixit.py --between [yyyy-mm-dd] [yyyy-mm-dd]`

Deletes all tweets posted between the two given dates.

```bash
python twixit.py --between 2022-01-15 2023-01-15

# This example deletes all tweets between January 15, 2022 and January 15, 2023
```

---

### `twixit.py --setup`

Updates your stored credentials.

```bash
python twixit.py --setup
```

---

### `twixit.py --help`

Displays all available commands with their descriptions.

```bash
python twixit.py --help
```

---

## 🔁 Delete Retweets

Use the `--retweet` flag to delete retweets. By default it deletes all of them from the most recent to the oldest. You can also combine it with the filtering options:

```bash
python twixit.py --retweet
python twixit.py --retweet --limit 15
python twixit.py --retweet --after 2022-01-15
python twixit.py --retweet --before 2022-01-15
python twixit.py --retweet --between 2022-01-15 2023-01-15
```

---

## ⚠️ Known Limitations

- **X Archive:** Tweet IDs are sourced exclusively from the local `tweets.js` file. To get it, request your data from X at `Settings → Your Account → Download an archive of your data`. X can take up to 24 hours to deliver it.
- **Rate limiting:** X may block activity after a while. If this happens, simply restart the process to continue deleting tweets. The browser may also slow down over time due to memory usage.
- **External cache:** Deleting tweets from your account does not remove them from Google's cache or third-party services that may have indexed them.

---

## 📦 Dependencies

| Library         | Purpose                                |
| --------------- | -------------------------------------- |
| `python-dotenv` | Load credentials from `.env`           |
| `playwright`    | Simulates user behavior in the browser |
| `datetime`      | Handles timezone conversion            |
| `click`         | Builds the CLI commands                |
| `pyfiglet`      | Generates the Twixit ASCII art         |

---

## 📄 License

MIT License — feel free to use and modify this project.

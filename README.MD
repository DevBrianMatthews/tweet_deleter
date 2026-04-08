# 🐦 Tweet Deleter

A Python script that deletes all your tweets from X (formerly Twitter) using your Twitter Archive and the X API v2.

---

## 📋 Requirements

- Python 3.10+
- A [X Developer account](https://developer.x.com) with an app configured with **Read and Write** permissions
- Your Twitter Archive (`tweets.js` file)

---

## ⚙️ Installation

1. Clone the repository:

```bash
   git clone https://github.com/your-username/tweet_deleter.git
   cd tweet_deleter
```

2. Create and activate a virtual environment:

```bash
   python -m venv env
   source env/bin/activate        # Mac/Linux
   env\Scripts\activate           # Windows
```

3. Install dependencies:

```bash
   pip install tweepy python-dotenv
```

4. Create a `.env` file in the root folder with your credentials:

```
API_KEY=your_consumer_key
API_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

5. Download your Twitter Archive from X:
   `Settings → Your Account → Download an archive of your data`

    Place the `tweets.js` file (found inside the `data/` folder of the archive) in the root of this project.

---

## 🚀 Usage

```bash
python main.py
```

The script will print each deleted tweet ID in real time:

```
Tweet con el ID: 1234567890 eliminado
Tweet con el ID: 9876543210 eliminado
```

---

## ⚠️ Known Limitations

- **Rate limit:** The X API Free tier allows 17 DELETE requests every 15 minutes. The script pauses 53 seconds between each request — deleting 915 tweets takes approximately 13 hours.
- **Archive only:** The Free tier does not support fetching tweets via API (`GET /2/users/:id/tweets` requires a paid plan). Tweet IDs are sourced exclusively from the local `tweets.js` file.
- **External cache:** Deleting tweets from your account does not remove them from Google cache or third-party services that may have indexed them.

---

## 📦 Dependencies

| Library         | Purpose                      |
| --------------- | ---------------------------- |
| `tweepy`        | X API v2 wrapper             |
| `python-dotenv` | Load credentials from `.env` |

---

## 📄 License

MIT License — feel free to use and modify this project.

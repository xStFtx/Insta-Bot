# Instagram Bot

A simple bot to automate various interactions on Instagram such as liking posts based on hashtags, unfollowing non-followers, and posting comments.

## Features:

- **Like Posts**: The bot can like posts based on provided hashtags.
  
- **Auto Comment**: After liking, the bot can post a comment selected from a predefined list.
  
- **Follow Users**: Follow users based on certain engagement metrics.
  
- **Unfollow Non-Followers**: Unfollows users who aren't following back after a week.
  
- **Logging**: Maintains a log for actions and errors during the bot's operations.

- **SQLite Database**: Keeps a record of the posts the bot has already liked to prevent duplication.

## Installation:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment (recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venvScriptsactivate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration:

1. Create a `config.ini` file in the root directory with the following structure:
   ```ini
   [INSTAGRAM]
   USERNAME = your_instagram_username
   PASSWORD = your_instagram_password

   [SETTINGS]
   DELAY_BETWEEN_LIKES = 15
   DELAY_BETWEEN_COMMENTS = 30
   UNFOLLOW_AFTER_DAYS = 7
   COMMENTS_LIST = Great post!,Amazing shot!,Love this.,This is fantastic!

   ```

2. Edit `bot.py` if you want to modify the default comments or add new features.

## Usage:

1. Run the script:
   ```bash
   python bot.py
   ```

2. The bot will prompt you for hashtags and the number of posts you want to interact with.

3. Watch as the bot automates your Instagram interactions!

## Contributing:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:

MIT

---

*Note: Use this bot responsibly and ensure you're not violating Instagram's terms of use.*

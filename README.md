# Mentis

This repository contains a Telegram bot written in Python that uses the Groq API to create a chatbot. The bot offers multiple features and supports two languages.

## Features

- Responds to a wide range of questions and assists with various tasks, providing innovative ideas.
- Understands and processes audio messages
- Handles a list of allowed users
- Creates custom greetings for users and remembers their names
- Maintains conversation history with the option to refresh (delete) it
- Offers three different Language Models (LLMs) for users to choose from
- Supports two languages: Russian and English
  - Automatically detects the user's Telegram interface language at the start of the chat
  - Allows users to change the language manually
  - Displays all commands and bot responses in the chosen language

## Configuration
All sensitive data is store in the `.env` file, which is not included in the repository. The file contains the following:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   BOT_TOKEN=your_bot_token_here
   USERS=user1,user2,user3
   USERNAMES=User1,User2,User3
   ADMINS=admin1,admin2
   MESSAGES=Message 1 to user 1;Message 2 to user 1|Message 1 to user 2
   ```
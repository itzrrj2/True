import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Replace with your bot token from BotFather
TOKEN = "7482868409:AAEnZDq8GddbtQmXIPMD-K7Swkv3aNxj3DY"

# Required channel usernames (without @)
REQUIRED_CHANNELS = ["Xstream_links1", "Sr_Robots"]

# API Endpoint
API_URL = "https://turecaller.pikaapis0.workers.dev/?number={}"

def check_subscription(user_id: int, bot) -> bool:
    """Check if the user has joined both required channels."""
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = bot.get_chat_member(f"@{channel}", user_id)
            if chat_member.status in ["left", "kicked"]:
                return False  # User is not subscribed
        except Exception as e:
            return False  # If any error occurs, assume not subscribed
    return True  # User is subscribed to both channels

def fetch_caller_details(phone_number: str) -> str:
    """Fetch caller details from the API and return a formatted response."""
    response = requests.get(API_URL.format(phone_number))
    
    if response.status_code == 200:
        data = response.json()
        
        truecaller_name = data.get("Truecaller", "Not Found")
        unknown_name = data.get("Unknown", "Not Found")
        carrier = data.get("carrier", "Unknown Carrier")
        local_format = data.get("local_format", "Unknown Format")
        location = data.get("location", "Unknown Location")

        formatted_response = (
            f"📞 *Caller Details:*\n"
            f"📝 *Truecaller Name:* {truecaller_name}\n"
            f"❓ *Truecaller2 Name:* {unknown_name}\n"
            f"📡 *Carrier:* {carrier}\n"
            f"📟 *Local Format:* {local_format}\n"
            f"📍 *Location:* {location}"
        )
        
        return formatted_response
    else:
        return "⚠️ Error fetching details. Please try again later."

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user messages and fetch details if a valid phone number is sent."""
    user_message = update.message.text.strip()
    user_id = update.message.from_user.id

    # Check if user is subscribed
    if not check_subscription(user_id, context.bot):
        channels_list = "\n".join([f"👉 [Join @{ch}](https://t.me/{ch})" for ch in REQUIRED_CHANNELS])
        update.message.reply_text(
            f"⚠️ *You must join the following channels to use this bot:*\n\n{channels_list}",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    # If user is subscribed, proceed with fetching caller details
    if user_message.startswith("+") and user_message[1:].isdigit():
        result = fetch_caller_details(user_message)
        update.message.reply_text(result, parse_mode="Markdown")
    else:
        update.message.reply_text("⚠️ Please send a valid phone number in international format (e.g., +918317394605).")

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text("Welcome! Send a phone number to get caller details.")

def main():
    """Main function to run the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.command, start))  # Handles /start

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

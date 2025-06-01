import asyncio
import nest_asyncio
nest_asyncio.apply()


from telegram import Update # type: ignore
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes # type: ignore

# Dictionary to hold users' to-do lists
user_todos = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to your To-Do Bot!\nUse /add <task> to add tasks.\nUse /list to see your tasks.\nUse /done <number> to remove.")

# /add command
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = ' '.join(context.args)
    if not task:
        await update.message.reply_text("Please provide a task after /add.")
        return
    user_todos.setdefault(user_id, []).append(task)
    await update.message.reply_text(f"✅ Added: {task}")

# /list command
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = user_todos.get(user_id, [])
    if not tasks:
        await update.message.reply_text("Your to-do list is empty.")
    else:
        msg = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
        await update.message.reply_text(f"📋 Your tasks:\n{msg}")

# /done command
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = user_todos.get(user_id, [])
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use /done <task number> to remove a task.")
        return
    index = int(context.args[0]) - 1
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        await update.message.reply_text(f"❌ Removed: {removed}")
    else:
        await update.message.reply_text("Invalid task number.")

# Run the bot
async def main():
    # import os

    # TOKEN = os.getenv("BOT_TOKEN")
    # app = ApplicationBuilder().token(TOKEN).build()

    app = ApplicationBuilder().token("7876341862:AAGjBpWcR_tjqkwVj2q0KE6unpC37VCdgeo").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())



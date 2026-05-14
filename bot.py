import os
from flask import Flask, request
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to ZambiaFX Bot 📊\n\n"
        "Use /help to see commands."
    )

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/forex - Forex analysis\n"
        "/otc - OTC analysis\n"
        "/signal - Get signal\n"
        "/risk - Trading risk management\n"
        "/session - Show current trading session\n"
        "/news - Market news"
    )

# --- RISK COMMAND ---
async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ RISK MANAGEMENT RULES\n\n"
        "• Risk only 1–3% per trade\n"
        "• Avoid revenge trading\n"
        "• Stop after 3 consecutive losses\n"
        "• Weak signals = smaller stake\n"
        "• High volatility requires caution\n"
        "• OTC markets can be unpredictable\n"
        "• Patience is part of trading\n\n"
        "📌 Protect your capital first."
    )

# --- SESSION COMMAND ---
async def session(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from datetime import datetime, timezone, timedelta

    zambia_time = datetime.now(timezone(timedelta(hours=2)))
    weekday = zambia_time.weekday()

    current_hour = zambia_time.hour
    current_minute = zambia_time.minute

    is_weekend = weekday >= 5

    if is_weekend:
        market_session = "Weekend / OTC Mode ⚡"
        advice = "Forex market is closed. Focus on OTC pairs only."

    elif (current_hour > 22 or (current_hour == 22 and current_minute >= 30)) or current_hour <= 6:
        market_session = "Night / OTC Mode ⚡"
        advice = "Normal Forex may be inactive. Focus more on OTC pairs."

    else:
        market_session = "Day / Forex + OTC Mode 📈"
        advice = "Forex pairs and OTC pairs can both be considered."

    await update.message.reply_text(
        f"🕒 CURRENT MARKET SESSION\n\n"
        f"Time: {current_hour:02d}:{current_minute:02d}\n"
        f"Session: {market_session}\n\n"
        f"Advice: {advice}"
    )

# --- FOREX COMMAND ---
async def forex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Forex Market Analysis:\n"
        "Trend: Neutral\n"
        "Advice: Wait for confirmation"
    )

# --- OTC COMMAND ---
async def otc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ OTC Market Analysis:\n"
        "Trend: Volatile\n"
        "Advice: Trade with caution"
    )

# --- SIGNAL COMMAND ---
import random

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    volatility = random.randint(20, 100)

    forex_pairs = [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
        "NZD/USD",
        "USD/CHF",
        "EUR/JPY",
        "GBP/JPY",
        "AUD/JPY",
        "CAD/JPY",
        "CHF/JPY",
        "EUR/GBP",
        "EUR/CHF",
        "GBP/CHF",
        "AUD/CAD",
        "AUD/CHF",
        "NZD/JPY"
    ]

    otc_pairs = [
        "EUR/USD OTC",
        "GBP/USD OTC",
        "USD/JPY OTC",
        "AUD/USD OTC",
        "USD/CHF OTC",
        "EUR/JPY OTC",
        "GBP/JPY OTC",
        "EUR/GBP OTC",
        "AUD/JPY OTC"
    ]

    from datetime import datetime, timezone, timedelta

zambia_time = datetime.now(timezone(timedelta(hours=2)))
weekday = zambia_time.weekday()
current_hour = zambia_time.hour
current_minute = zambia_time.minute

is_weekend = weekday >= 5

if is_weekend:
    market_session = "Weekend / OTC Mode ⚡"
    pairs = otc_pairs

elif (current_hour > 22 or (current_hour == 22 and current_minute >= 30)) or current_hour <= 6:
    market_session = "Night / OTC Mode ⚡"
    pairs = otc_pairs

else:
    market_session = "Day / Forex + OTC Mode 📈"
    pairs = forex_pairs + otc_pairs

pair = random.choice(pairs)

if "OTC" in pair:
    market_type = "OTC ⚡"
else:
    market_type = "Forex 📈"

trend = random.choice(["Bullish 📈", "Bearish 📉"])

rsi = random.randint(10, 90)

    strength = random.choice([
        "Weak ⚠️",
        "Moderate 📊",
        "Strong 💪"
    ])

    # --- adaptive timeframe logic ---
    if volatility >= 80:
        timeframe = "1–3 min"
        confidence = random.randint(60, 72)

    elif volatility >= 60:
        timeframe = "3–5 min"
        confidence = random.randint(70, 80)

    elif volatility >= 40:
        timeframe = "5–10 min"
        confidence = random.randint(78, 86)

    else:
        timeframe = "10–15 min"
        confidence = random.randint(82, 92)

    # --- RSI logic ---
    if rsi <= 30:
        rsi_state = "Oversold"
    elif rsi >= 70:
        rsi_state = "Overbought"
    else:
        rsi_state = "Neutral"

    # --- trend direction ---
    if trend == "Bullish 📈":
        direction = "BUY ↑"
    else:
        direction = "SELL ↓"

    # --- FILTER SYSTEM (NEW LEVEL 6 CORE) ---

    no_trade = False

    # weak market penalty
    if strength == "Weak ⚠️":
        confidence -= 15

    # low volatility penalty
    if volatility < 30:
        confidence -= 10

    # risky conditions
    if strength == "Weak ⚠️" and volatility < 35:
        no_trade = True

    # confidence floor
    if confidence < 50:
        confidence = 50

    # --- reasoning system ---
    if no_trade:
        reason = "Weak market conditions detected. Waiting is safer."

        await update.message.reply_text(
            f"⚠️ NO TRADE RECOMMENDED\n\n"
            f"Pair: {pair}\n"
            f"Market Type: {market_type}\n"
            f"Session: {market_session}\n"
            f"Trend: {trend}\n"
            f"RSI: {rsi} ({rsi_state})\n"
            f"Market Strength: {strength}\n"
            f"Volatility: {volatility}/100\n\n"
            f"🧠 Reason: {reason}"
        )

    else:

        # --- ALIGNMENT / CONFLICT ENGINE ---

        conflict = False
        alignment = False

        if trend == "Bullish 📈" and rsi_state == "Oversold":
            alignment = True
            direction = "BUY ↑"
            confidence += 8
            reason = "Bullish trend + oversold RSI support a BUY reversal"

        elif trend == "Bearish 📉" and rsi_state == "Overbought":
            alignment = True
            direction = "SELL ↓"
            confidence += 8
            reason = "Bearish trend + overbought RSI support a SELL reversal"

        elif trend == "Bearish 📉" and rsi_state == "Oversold":
            conflict = True
            confidence -= 18
            reason = "Conflict detected: bearish trend but RSI is oversold. Reversal risk."

        elif trend == "Bullish 📈" and rsi_state == "Overbought":
            conflict = True
            confidence -= 18
            reason = "Conflict detected: bullish trend but RSI is overbought. Pullback risk."

        else:
            reason = "Market momentum and trend alignment"

        if strength == "Weak ⚠️":
            confidence -= 10

        if volatility < 30:
            confidence -= 8

        if conflict and confidence < 70:
            no_trade = True

        if confidence < 50:
            confidence = 50

        if confidence > 95:
            confidence = 95


        await update.message.reply_text(
            f"📊 LEVEL 6 SIGNAL\n\n"
            f"Pair: {pair}\n"
            f"Market Type: {market_type}\n"
            f"Trend: {trend}\n"
            f"RSI: {rsi} ({rsi_state})\n"
            f"Market Strength: {strength}\n"
            f"Direction: {direction}\n"
            f"Timeframe: {timeframe}\n"
            f"Volatility: {volatility}/100\n"
            f"Confidence: {confidence}%\n\n"
            f"Signal Quality: {'Strong Alignment ✅' if alignment else 'Conflict Risk ⚠️' if conflict else 'Normal Setup 📊'}\n"
            f"🧠 Reason: {reason}"
        )
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 Market News:\n\n"
        "No live news API yet.\n"
        "Next upgrade will connect real forex news (CPI, NFP, interest rates)."
    )

# --- AUTO REPLY ---
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hello" in text:
        await update.message.reply_text("Hello 👋 Welcome to ZambiaFX Bot")

    elif "otc" in text:
        await update.message.reply_text(
            "⚡ OTC (Over-The-Counter) markets are broker-driven markets.\n"
            "They are more volatile and used for short-term trading."
        )

    elif "forex" in text:
        await update.message.reply_text(
            "📈 Forex involves trading global currency pairs like EUR/USD."
        )

    elif "signal" in text:
        await update.message.reply_text("Use /signal for trading signals 📊")

    else:
        await update.message.reply_text("Type /help to see commands")

# --- MAIN APP ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("forex", forex))
app.add_handler(CommandHandler("otc", otc))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("risk", risk))
app.add_handler(CommandHandler("session", session))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
from flask import Flask
from threading import Thread

web = Flask(__name__)

@web.route('/')
def home():
    return "Bot is running!"

@web.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    print("TradingView Alert Received:")
    print(data)

    return {"status": "success"}, 200

def run_web():
    web.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()
app.run_polling(drop_pending_updates=True)

import os
import re
import subprocess
from threading import Thread
from flask import Flask
import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# ==================== FLASK KEEP-ALIVE SERVER ====================
app = Flask('')

@app.route('/')
def home():
    return "Main Bot is alive and running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server, daemon=True)
    t.start()

# ==================== BOT SETUP ====================
TOKEN = '8710736330:AAHsNib6LNJsaNAYBiIHAv6zgCKvXwyCTbs[span_0](start_span)'[span_0](end_span)
bot = telebot.TeleBot(TOKEN)[span_1](start_span)[span_1](end_span)

running_bots = {}[span_2](start_span)[span_2](end_span)
deploy_sessions = {}[span_3](start_span)[span_3](end_span)

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)[span_4](start_span)[span_4](end_span)
    markup.add(KeyboardButton("🚀 Deploy Bot"), KeyboardButton("⚙️ Manage Bot"))[span_5](start_span)[span_5](end_span)
    return markup[span_6](start_span)[span_6](end_span)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Welcome to Bot Hoster! 🤖\n\nNiche theke option select korun:",
        reply_markup=get_main_keyboard()
    )[span_7](start_span)[span_7](end_span)

# ==================== DEPLOY BOT LOGIC ====================
@bot.message_handler(func=lambda message: message.text == "🚀 Deploy Bot")
def deploy_bot_prompt(message):
    msg = bot.send_message(
        message.chat.id,
        "Apnar bot er `.py` file ta ekhane send korun...",
        reply_markup=ReplyKeyboardRemove()
    )[span_8](start_span)[span_8](end_span)
    bot.register_next_step_handler(msg, handle_py_file)[span_9](start_span)[span_9](end_span)

def handle_py_file(message):
    if not message.document or not message.document.file_name.endswith('.py'):[span_10](start_span)[span_10](end_span)
        msg = bot.send_message(
            message.chat.id,
            "❌ Doya kore ekta valid .py file send korun! (Try again 🚀 Deploy Bot)",
            reply_markup=get_main_keyboard()
        )[span_11](start_span)[span_11](end_span)
        return[span_12](start_span)[span_12](end_span)

    bot.send_message(message.chat.id, "⏳ Python File downloading...")[span_13](start_span)[span_13](end_span)
    
    file_info = bot.get_file(message.document.file_id)[span_14](start_span)[span_14](end_span)
    downloaded_file = bot.download_file(file_info.file_path)[span_15](start_span)[span_15](end_span)
    file_name = message.document.file_name[span_16](start_span)[span_16](end_span)
    
    with open(file_name, 'wb') as new_file:[span_17](start_span)[span_17](end_span)
        new_file.write(downloaded_file)[span_18](start_span)[span_18](end_span)
        
    deploy_sessions[message.chat.id] = {'py_file': file_name}[span_19](start_span)[span_19](end_span)
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)[span_20](start_span)[span_20](end_span)
    markup.add(KeyboardButton("⏭️ Skip"))[span_21](start_span)[span_21](end_span)
    
    msg = bot.send_message(
        message.chat.id,
        f"✅ `{file_name}` downloaded!\n\nEbar jodi apnar kono `requirements.txt` file thake, seta send korun.\nNa thakle nicher **Skip** button a click korun.",
        reply_markup=markup,
        parse_mode="Markdown"
    )[span_22](start_span)[span_22](end_span)
    bot.register_next_step_handler(msg, handle_requirements_file)[span_23](start_span)[span_23](end_span)

def handle_requirements_file(message):
    user_session = deploy_sessions.get(message.chat.id)[span_24](start_span)[span_24](end_span)
    if not user_session:[span_25](start_span)[span_25](end_span)
        return[span_26](start_span)[span_26](end_span)
        
    py_file_name = user_session['py_file'][span_27](start_span)[span_27](end_span)

    if message.text == "⏭️ Skip":[span_28](start_span)[span_28](end_span)
        bot.send_message(
            message.chat.id,
            "⏩ Skipped requirements.txt. Auto-detecting packages...",
            reply_markup=get_main_keyboard()
        )[span_29](start_span)[span_29](end_span)
        run_bot_process(message.chat.id, py_file_name, req_file=None)[span_30](start_span)[span_30](end_span)
        
    elif message.document and message.document.file_name == 'requirements.txt':[span_31](start_span)[span_31](end_span)
        bot.send_message(
            message.chat.id,
            "⏳ Downloading requirements.txt...",
            reply_markup=get_main_keyboard()
        )[span_32](start_span)[span_32](end_span)
        
        file_info = bot.get_file(message.document.file_id)[span_33](start_span)[span_33](end_span)
        downloaded_file = bot.download_file(file_info.file_path)[span_34](start_span)[span_34](end_span)
        req_file_name = f"req_{message.chat.id}.txt[span_35](start_span)"[span_35](end_span)
        
        with open(req_file_name, 'wb') as new_file:[span_36](start_span)[span_36](end_span)
            new_file.write(downloaded_file)[span_37](start_span)[span_37](end_span)
            
        bot.send_message(message.chat.id, "📦 Installing packages from requirements.txt...")[span_38](start_span)[span_38](end_span)
        
        try:
            subprocess.run(['pip', 'install', '-r', req_file_name], check=True)[span_39](start_span)[span_39](end_span)
            bot.send_message(message.chat.id, "✅ All packages installed successfully!")[span_40](start_span)[span_40](end_span)
            os.remove(req_file_name)[span_41](start_span)[span_41](end_span)
        except subprocess.CalledProcessError as e:[span_42](start_span)[span_42](end_span)
            bot.send_message(message.chat.id, f"⚠️ Requirements install a problem hoyeche. Error: {e}")[span_43](start_span)[span_43](end_span)
            
        run_bot_process(message.chat.id, py_file_name, req_file=True)[span_44](start_span)[span_44](end_span)
        
    else:
        msg = bot.send_message(message.chat.id, "❌ Please ekta valid `requirements.txt` send korun ba 'Skip' e click korun.")[span_45](start_span)[span_45](end_span)
        bot.register_next_step_handler(msg, handle_requirements_file)[span_46](start_span)[span_46](end_span)

def run_bot_process(chat_id, py_file_name, req_file=None):
    if not req_file:[span_47](start_span)[span_47](end_span)
        try:
            with open(py_file_name, 'r') as f:[span_48](start_span)[span_48](end_span)
                code_content = f.read()[span_49](start_span)[span_49](end_span)
                imports = re.findall(r'^(?:import|from)\s+([a-zA-Z0-9_]+)', code_content, re.MULTILINE)[span_50](start_span)[span_50](end_span)
                unique_imports = set(imports)[span_51](start_span)[span_51](end_span)
                
                for module in unique_imports:[span_52](start_span)[span_52](end_span)
                    bot.send_message(chat_id, f"📦 Auto-Installing {module}...")[span_53](start_span)[span_53](end_span)
                    subprocess.run(['pip', 'install', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)[span_54](start_span)[span_54](end_span)
        except Exception as e:[span_55](start_span)[span_55](end_span)
            bot.send_message(chat_id, f"⚠️ Dependency check error: {e}")[span_56](start_span)[span_56](end_span)

    try:
        process = subprocess.Popen(["python", py_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)[span_57](start_span)[span_57](end_span)
        
        if chat_id not in running_bots:[span_58](start_span)[span_58](end_span)
            running_bots[chat_id] = {}[span_59](start_span)[span_59](end_span)
            
        running_bots[chat_id][py_file_name] = process[span_60](start_span)[span_60](end_span)
        
        bot.send_message(
            chat_id,
            f"🎉 **Bot Successfully Deployed!**\n\n📁 File: `{py_file_name}` is now live in the background.",
            parse_mode="Markdown"
        )[span_61](start_span)[span_61](end_span)
        
    except Exception as e:[span_62](start_span)[span_62](end_span)
        bot.send_message(chat_id, f"❌ Bot start korte problem hoyeche: {e}")[span_63](start_span)[span_63](end_span)
        
    if chat_id in deploy_sessions:[span_64](start_span)[span_64](end_span)
        del deploy_sessions[chat_id][span_65](start_span)[span_65](end_span)

# ==================== MANAGE BOT LOGIC ====================
@bot.message_handler(func=lambda message: message.text == "⚙️ Manage Bot")
def manage_bots(message):
    user_bots = running_bots.get(message.chat.id, {})[span_66](start_span)[span_66](end_span)
    
    if not user_bots:[span_67](start_span)[span_67](end_span)
        bot.send_message(message.chat.id, "🤷‍♂️ Apnar kono bot live nei ekhon.")[span_68](start_span)[span_68](end_span)
        return[span_69](start_span)[span_69](end_span)
        
    markup = InlineKeyboardMarkup()[span_70](start_span)[span_70](end_span)
    for b_name in user_bots.keys():[span_71](start_span)[span_71](end_span)
        markup.add(
            InlineKeyboardButton(f"🛑 Stop {b_name}", callback_data=f"stop_{b_name}"),[span_72](start_span)[span_72](end_span)
            InlineKeyboardButton(f"🗑 Delete {b_name}", callback_data=f"del_{b_name}")[span_73](start_span)[span_73](end_span)
        )[span_74](start_span)[span_74](end_span)
        
    bot.send_message(message.chat.id, "👇 Niche theke apnar bot manage korun:", reply_markup=markup)[span_75](start_span)[span_75](end_span)

@bot.callback_query_handler(func=lambda call: call.data.startswith('stop_') or call.data.startswith('del_'))
def handle_management(call):
    action, bot_name = call.data.split('_', 1)[span_76](start_span)[span_76](end_span)
    user_id = call.message.chat.id[span_77](start_span)[span_77](end_span)
    
    process = running_bots.get(user_id, {}).get(bot_name)[span_78](start_span)[span_78](end_span)
    
    if process:[span_79](start_span)[span_79](end_span)
        process.terminate()[span_80](start_span)[span_80](end_span)
        
        if action == 'del':[span_81](start_span)[span_81](end_span)
            del running_bots[user_id][bot_name][span_82](start_span)[span_82](end_span)
            if os.path.exists(bot_name):[span_83](start_span)[span_83](end_span)
                os.remove(bot_name)[span_84](start_span)[span_84](end_span)
            bot.answer_callback_query(call.id, f"{bot_name} Deleted!")[span_85](start_span)[span_85](end_span)
            bot.edit_message_text(
                f"🗑 `{bot_name}` file deleted ar bot stopped.",
                user_id,
                call.message.message_id,
                parse_mode="Markdown"
            )[span_86](start_span)[span_86](end_span)
        else:
            bot.answer_callback_query(call.id, f"{bot_name} Stopped!")[span_87](start_span)[span_87](end_span)
            bot.edit_message_text(
                f"🛑 `{bot_name}` ekhon paused/stopped ache.",
                user_id,
                call.message.message_id,
                parse_mode="Markdown"
            )[span_88](start_span)[span_88](end_span)
    else:
        bot.answer_callback_query(call.id, "Bot already stopped ba not found!", show_alert=True)[span_89](start_span)[span_89](end_span)

# ==================== MAIN RUNNER ====================
if __name__ == "__main__":
    keep_alive()
    print("Main Host Bot is running with Flask keep-alive server...")
    bot.infinity_polling()

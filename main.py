# -*- coding: utf-8 -*-
import os
import random
from flask import Flask
from threading import Thread
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

app = Flask(__name__)
@app.route('/')
def home(): return "OK"
@app.route('/health')
def health(): return "OK", 200

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "7145036494"))
FORCE_CHANNEL = "pkwbiwjwbekeekkw"
FORCE_LINK = "https://t.me/pkwbiwjwbekeekkw"

bot = telebot.TeleBot(TOKEN, threaded=False)
os.makedirs("database", exist_ok=True)
os.makedirs("temp", exist_ok=True)

def get_points(uid):
    try:
        with open(f"database/{uid}.txt","r",encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except: return 0

def add_points(uid, n):
    try:
        with open(f"database/{uid}.txt","w",encoding="utf-8") as f:
            f.write(str(get_points(uid)+n))
    except: pass

def is_sub(uid):
    try:
        s = bot.get_chat_member(f"@{FORCE_CHANNEL}", uid).status
        return s in ['member','administrator','creator']
    except: return True

def sub_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("اشترك", url=FORCE_LINK))
    kb.add(types.InlineKeyboardButton("تحققت", callback_data="check"))
    return kb

def make_img(text):
    try:
        img = Image.new("RGB", (1080, 1350), (0,0,0))
        draw = ImageDraw.Draw(img)
        y=40
        for line in text.split("\n")[:20]:
            draw.text((30, y), line[:50], fill=(255,255,255))
            y+=60
        path = f"temp/{random.randint(10000,99999)}.jpg"
        img.save(path)
        return path
    except:
        path = f"temp/{random.randint(10000,99999)}.jpg"
        Image.new("RGB", (500,500), (0,0,0)).save(path)
        return path

PRICES = {
"design":5,"filter":5,"textpic":5,"hd":5,"logo":10,"card":10,"banner":10,"poster":10,"qr":5,"cv":10,
"fake":5,"active":5,"code":5,"temp10":5,"perm":15,"secure":10,
"charge":5,"track":5,"coupon":5,"invoice":5,
"daman_s":5,"daman_a":5,"daman_n":5,"daman_e":5,"daman_sh":5,"daman_f":5,
"follow":15,"like":15,"view":15,"member":15,
"unban_all":15,"num":15,"usnum":25,"whats":15,
"ad_post":20,"ad_pin":30,"ad_spon":50,"ad_all":100
}

@bot.message_handler(commands=['start'])
def start(m):
    try:
        uid=m.from_user.id
        if not is_sub(uid):
            bot.send_message(uid, f"اشترك اولا\n{FORCE_LINK}", reply_markup=sub_kb())
            return
        pts=get_points(uid)
        kb=types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton("القناة", url=FORCE_LINK))
        kb.add(types.InlineKeyboardButton("--- ضمان 6 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("متجر 5", callback_data="daman_s"), types.InlineKeyboardButton("حساب 5", callback_data="daman_a"))
        kb.add(types.InlineKeyboardButton("ارقام 5", callback_data="daman_n"), types.InlineKeyboardButton("ايميل 5", callback_data="daman_e"))
        kb.add(types.InlineKeyboardButton("شحن 5", callback_data="daman_sh"), types.InlineKeyboardButton("متابعين 5", callback_data="daman_f"))
        kb.add(types.InlineKeyboardButton("--- ايميل 6 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("وهمي 5", callback_data="fake"), types.InlineKeyboardButton("تفعيل 5", callback_data="active"))
        kb.add(types.InlineKeyboardButton("كود 5", callback_data="code"), types.InlineKeyboardButton("10د 5", callback_data="temp10"))
        kb.add(types.InlineKeyboardButton("دائم 15", callback_data="perm"), types.InlineKeyboardButton("مشفر 10", callback_data="secure"))
        kb.add(types.InlineKeyboardButton("--- شحن 4 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("شحن 5", callback_data="charge"), types.InlineKeyboardButton("تتبع 5", callback_data="track"))
        kb.add(types.InlineKeyboardButton("خصم 5", callback_data="coupon"), types.InlineKeyboardButton("فاتورة 5", callback_data="invoice"))
        kb.add(types.InlineKeyboardButton("--- زياده 4 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("متابعين 15", callback_data="follow"), types.InlineKeyboardButton("لايكات 15", callback_data="like"))
        kb.add(types.InlineKeyboardButton("مشاهدات 15", callback_data="view"), types.InlineKeyboardButton("اعضاء 15", callback_data="member"))
        kb.add(types.InlineKeyboardButton("--- فك حظر شامل ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("فك حظر شامل 15", callback_data="unban_all"), types.InlineKeyboardButton("رقم وهمي 15", callback_data="num"))
        kb.add(types.InlineKeyboardButton("امريكي 25", callback_data="usnum"), types.InlineKeyboardButton("واتس شامل 15", callback_data="whats"))
        kb.add(types.InlineKeyboardButton("--- تصميم 10 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("تصميم 5", callback_data="design"), types.InlineKeyboardButton("فلتر 5", callback_data="filter"))
        kb.add(types.InlineKeyboardButton("كتابة 5", callback_data="textpic"), types.InlineKeyboardButton("جودة 5", callback_data="hd"))
        kb.add(types.InlineKeyboardButton("لوجو 10", callback_data="logo"), types.InlineKeyboardButton("بطاقة 10", callback_data="card"))
        kb.add(types.InlineKeyboardButton("بانر 10", callback_data="banner"), types.InlineKeyboardButton("بوستر 10", callback_data="poster"))
        kb.add(types.InlineKeyboardButton("سيفي 10", callback_data="cv"), types.InlineKeyboardButton("QR 5", callback_data="qr"))
        kb.add(types.InlineKeyboardButton("--- اعلان 4 ---", callback_data="no"))
        kb.add(types.InlineKeyboardButton("نشر 20", callback_data="ad_post"), types.InlineKeyboardButton("تثبيت 30", callback_data="ad_pin"))
        kb.add(types.InlineKeyboardButton("ممول 50", callback_data="ad_spon"), types.InlineKeyboardButton("بث 100", callback_data="ad_all"))
        kb.add(types.InlineKeyboardButton(f"رصيدك {pts}", callback_data="bal"))
        kb.add(types.InlineKeyboardButton("شراء نقاط", callback_data="buy"))
        bot.send_message(uid, f"متجر زيده - 40 زر شغال\nرصيدك {pts}\nفك الحظر الشامل موجود\n{FORCE_LINK}", reply_markup=kb)
    except Exception as e:
        print(f"start error {e}")

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    try:
        uid=c.from_user.id
        chat=c.message.chat.id
        d=c.data
        if d=="check":
            if is_sub(uid):
                bot.answer_callback_query(c.id,"تم")
                try: bot.delete_message(chat,c.message.message_id)
                except: pass
                start(c.message)
            else:
                bot.answer_callback_query(c.id,"اشترك اولا",show_alert=True)
            return
        if d=="no":
            bot.answer_callback_query(c.id)
            return
        bot.answer_callback_query(c.id)
        if not is_sub(uid):
            bot.send_message(chat,f"اشترك\n{FORCE_LINK}",reply_markup=sub_kb())
            return
        if d=="buy":
            bot.send_message(chat,f"شراء نقاط\n5=1000 يمني\n15=2500\n30=5000\n100=15000\nالكريمي جعار\nايدك {uid}")
            return
        if d=="bal":
            bot.send_message(chat,f"رصيدك {get_points(uid)}")
            return
        price=PRICES.get(d,5)
        if get_points(uid)<price:
            bot.send_message(chat,f"تحتاج {price} رصيدك {get_points(uid)}")
            return
        if d in ["unban_all","whats"]:
            bot.send_message(chat,f"ارسل الرقم المحظور مع رمز البلد\nمثال +9677xxxxxxx\nالسعر {price}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_unban(m, price))
            return
        if d in ["filter","hd","textpic"]:
            bot.send_message(chat,f"ارسل الصورة - {d}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_photo(m,d,price))
            return
        if d in ["design","logo","card","banner","poster","cv"]:
            bot.send_message(chat,f"ارسل النص - {d}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_text(m,d,price))
            return
        if d.startswith("daman_"):
            bot.send_message(chat,f"ارسل اسم المتجر - {d}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_daman(m,d,price))
            return
        add_points(uid,-price)
        msgs={
            "fake":f"ايميل {random.randint(1000,9999)}@tempmail.com\nباس {random.randint(100000,999999)}",
            "active":f"تفعيل user{random.randint(100,999)}@gmail.com كود {random.randint(100000,999999)}",
            "code":f"كودك {random.randint(100000,999999)}",
            "temp10":f"ايميل {random.randint(1000,9999)}@10min.com",
            "perm":f"دائم store{random.randint(100,999)}@gmail.com",
            "secure":f"مشفر {random.randint(1000,9999)}@proton.com",
            "charge":"تم شحن 10$",
            "track":f"تتبع TRK{random.randint(10000000,99999999)}",
            "coupon":f"خصم ZAYDA{random.randint(10,99)} 20%",
            "invoice":f"فاتورة INV{random.randint(1000,9999)}",
            "follow":"تم 1000 متابع",
            "like":"تم 500 لايك",
            "view":"تم 1000 مشاهده",
            "member":"تم 200 عضو",
            "num":f"رقم +1{random.randint(1000000000,9999999999)} كود {random.randint(100000,999999)}",
            "usnum":f"امريكي +1{random.randint(1000000000,9999999999)}",
            "qr":f"QR {FORCE_LINK}",
            "ad_post":f"تم نشر {FORCE_LINK}",
            "ad_pin":f"تم تثبيت {FORCE_LINK}",
            "ad_spon":"تم الممول",
            "ad_all":"تم البث للكل"
        }
        bot.send_message(chat,f"{msgs.get(d,f'تم {d}')}\nخصم {price} رصيدك {get_points(uid)}\n/start")
    except Exception as e:
        print(f"callback error {e}")
        try: bot.send_message(c.message.chat.id,"خطا جرب /start")
        except: pass

def do_unban(m, price):
    try:
        num=m.text.strip()
        uid=m.from_user.id
        txt=f"🔓 فك حظر شامل للرقم\n{num}\n\n✅ تم:\n- واتس عادي: طلب\n- واتس بزنس: طلب\n- واتس عمر: فك\n- تليجرام: فك\n- ايمو: فك\n- فايبر: فك\n- سيجنال: فك\n- بوتيم: فك\n\n1- احذف التطبيق\n2- ثبت الرسمي\n3- انتظر 12 ساعه\n4- سجل من جديد\n\n{FORCE_LINK}\nنجاح 95%"
        add_points(uid,-price)
        bot.send_message(m.chat.id,f"{txt}\n\nخصم {price} رصيدك {get_points(uid)}\n/start")
    except Exception as e:
        bot.send_message(m.chat.id,f"خطا {e}")

def do_photo(m, typ, price):
    try:
        if m.content_type!='photo':
            bot.send_message(m.chat.id,"ارسل صورة")
            return
        f=bot.get_file(m.photo[-1].file_id)
        data=bot.download_file(f.file_path)
        p1=f"temp/{m.from_user.id}_1.jpg"
        open(p1,"wb").write(data)
        img=Image.open(p1).convert("RGB")
        if typ=="filter":
            img=img.filter(ImageFilter.DETAIL)
            img=ImageEnhance.Color(img).enhance(1.8)
        elif typ=="hd":
            img=ImageEnhance.Sharpness(img).enhance(2.0)
        p2=f"temp/{m.from_user.id}_2.jpg"
        img.save(p2)
        add_points(m.from_user.id,-price)
        bot.send_photo(m.chat.id, open(p2,"rb"), caption=f"تم {typ} رصيدك {get_points(m.from_user.id)}")
    except Exception as e:
        bot.send_message(m.chat.id,f"خطا {e}")

def do_daman(m, typ, price):
    try:
        out=make_img(f"ضمان {typ}\n{m.text}\n7 ايام ذهبي\n{FORCE_LINK}")
        add_points(m.from_user.id,-price)
        bot.send_photo(m.chat.id, open(out,"rb"), caption=f"تم {typ} رصيدك {get_points(m.from_user.id)}")
    except Exception as e:
        bot.send_message(m.chat.id,f"خطا {e}")

def do_text(m, typ, price):
    try:
        out=make_img(f"{typ}\n{m.text}\n{FORCE_LINK}")
        add_points(m.from_user.id,-price)
        bot.send_photo(m.chat.id, open(out,"rb"), caption=f"تم {typ} رصيدك {get_points(m.from_user.id)}")
    except Exception as e:
        bot.send_message(m.chat.id,f"خطا {e}")

@bot.message_handler(commands=['add'])
def add_cmd(m):
    if m.from_user.id!=ADMIN_ID: return
    try:
        _, uid, pts = m.text.split()
        add_points(int(uid), int(pts))
        bot.send_message(int(uid), f"تم شحن {pts} رصيدك {get_points(int(uid))}")
        bot.send_message(m.chat.id,"تم")
    except:
        bot.send_message(m.chat.id,"/add id points")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    try:
        if m.text.startswith('/'): return
        bot.send_message(m.chat.id,"اضغط /start")
    except: pass

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"polling {e}")

if __name__=="__main__":
    Thread(target=run_bot, daemon=True).start()
    port=int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, threaded=True)
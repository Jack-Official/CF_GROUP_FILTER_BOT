class script(object):   
    SUPPORT_TXT = """<b><u>⦁ ᴄʜᴀɴɴᴇʟꜱ & ɢʀᴏᴜᴩ ⦁</u>

🎬 ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇsᴛɪɴɢ ɢʀᴏᴜᴩ.
📣 ᴍᴏᴠɪᴇ ᴜᴩᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ.
🚦 ʙᴏᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ.</b>"""

    ABOUT_TXT = """<b><u>⚠️ ᴀʙᴏᴜᴛ ᴍᴇ</u></b>

<b>⦁ ᴍʏ ɴᴀᴍᴇ: {}</b>
<b>⦁ ᴍʏ ᴏᴡɴᴇʀ: <a href=https://t.me/TG_x_filter>🇮🇳❍ 𝖒𝖆𝖓𝖙𝖎𝖘 ❍™◢ ◤</b></a>
<b>⦁ ᴄʀᴇᴀᴛᴏʀ: <a href=tg://settings>ᴛʜɪꜱ ᴩᴇʀꜱᴏɴ</b></a>
<b>⦁ ʟɪʙʀᴀʀʏ: <a href=https://docs.pyrogram.org/>ᴩʏʀᴏɢʀᴀᴍ</b></a>
<b>⦁ ʟᴀɴɢᴜᴀɢᴇ: <a href=https://www.python.org/>ᴩʏᴛʜᴏɴ3</b></a>
<b>⦁ ᴅᴛᴀᴛʙᴀꜱᴇ: <a href=https://www.mongodb.com/>ᴍᴏɴɢᴏDB</b></a>
<b>⦁ ʙᴏᴛ ꜱᴇʀᴠᴇʀ: <a href=https://railway.app/>ʀᴀɪʟᴡᴀʏ</b></a>
<b>⦁ ꜱᴜᴩᴩᴏʀᴛ: <a href=https://t.me/+iEbhY7mM4oE1OTVl>ᴊᴏɪɴ ʜᴇʀᴇ</b></a>
<b>⦁ ʙᴜɪʟᴅ ꜱᴛᴀᴛᴜꜱ: [ ꜱᴛᴀʙʟᴇ ]</b>"""

    STATUS_TXT = """<u><b>📊 ꜱᴛᴀᴛᴜꜱ </b></u>

<b>╔═══[ ꜱᴛᴀᴛᴜꜱ ʙᴏᴀʀᴅ ]═══╗</b>
<b>📁 ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ :<code>{}</code></b>
<b>👥 ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ :<code>{}</code></b>
<b>💬 ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ : <code>{}</code></b>
<b>🗃 ᴜꜱᴇᴅ ꜱᴛᴏʀᴀɢᴇ : <code>{}</code> MB</b>
<b>╚═══[ ꜱᴛᴀᴛᴜꜱ ʙᴏᴀʀᴅ ]═══╝</b>"""
    
    LOG_TEXT_G = """#AddNewGroup
    
<b>⪼ 👥 𝖦𝗋𝗈𝗎𝗉 : {a}</b>
<b>⪼ 🆔 𝖦𝗋𝗈𝗎𝗉 𝖨𝖣 : <code>{b}</code></b>
<b>⪼ 🧲 𝖦𝗋𝗈𝗎𝗉 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 : @{c}</b>
<b>⪼ 🕵️‍♂️ 𝖳𝗈𝗍𝖺𝗅 𝖬𝖾𝗆𝖻𝖾𝗋𝗌 : {d}</b>
<b>⪼ 👨‍💻 𝖠𝖽𝖽𝖾𝖽 𝖡𝗒 :{e}</b>

<b>⪼🍃 𝖡𝗈𝗍 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 : {f}</b>
"""
    LOG_TEXT_P = """#StartNewUser
    
<b>⪼ 🆔 𝖨𝖣 : <code>{}</code></b>
<b>⪼ 😎 𝖭𝖺𝗆𝖾 : {}</b>
<b>⪼ ♻️ 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 : @{}</b>

<b>⪼ 🍃 𝖡𝗈𝗍 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 : @{}</b> """   

    CUSTOM_FILE_CAPTION = """<b>🎟️ ʀᴇϙᴜᴇsᴛᴇᴅ ʙʏ  {mention}</b>
    
    <b>🗃 ғɪʟᴇ ɴᴀᴍᴇ :</b><b><code>{file_name}</code></b>"""

    REQBEST = """♻️ ᴀsᴋ ᴍᴏᴠɪᴇs ᴄᴏʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ\n\n♻️ ᴅᴏɴᴛ ᴀsᴋ ᴍᴏᴠɪᴇs ᴛʜᴏsᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ɪɴ ᴏᴛᴛ ᴛʜᴇᴀᴛʀᴇ ϙᴜᴀʟɪᴛʏ ᴀᴠᴀɪʟᴀʙʟᴇ 🥹\n\n♻️ ғᴏʀ ʙᴇᴛᴛᴇʀ ʀᴇsᴜʟᴛ\n\n- ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ʏᴇᴀʀ\n\n- ᴇɴɢ : ʟᴇᴏ 2023"""

    REQTIPS = """🎬 MOVIE REQUEST FORMAT 🎬\n\n➲ ɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ\n➲ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ᴏʀ sᴇʀɪᴇs ɴᴀᴍᴇ\n➲ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ\n➲ ᴘᴀsᴛᴇ ᴛʜɪs ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ :"""

    REQINFO = """⚠️ INFORMATION ⚠️\n\nᴀғᴛᴇʀ 1 ᴅᴀʏs ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡᴇʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ\n\nɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ ʀᴇϙᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ ᴏʀ sᴇʀɪᴇs ғɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ"""

    NEOSUB = """അഥവാ ഗ്രൂപ്പ്‌ കോപ്പിറൈറ് കിട്ടി പോയാൽ.. പുതിയ ഗ്രൂപ്പ്‌ തുടങ്ങുമ്പോൾ ഇപ്പോൾ ജോയിൻ ആകുന്ന ചാനൽ വഴി ആയിരിക്കും അറിയിക്കുന്നത് 🤥"""

    HOWTOUES_TXT = """<b>‼️ <u>Instructions</u> ‼️</b>

<b>How to add me in your group?</b>

• Copy my username or Click on add Group » Go to your Group administrator settings » Click Add admin » Give all permissions » Click tick mark » Done
• Then use /connect command in your group
• Connected Successfully I Will Provide Films In Your Group

<b>‼️ <u>നിർദ്ദേശങ്ങൾ</u> ‼️</b>

<b>നിങ്ങളുടെ ഗ്രൂപ്പിൽ എന്നെ എങ്ങനെ ചേർക്കാം?</b>

• എന്റെ ഉപയോക്തൃനാമം പകർത്തുക അല്ലെങ്കിൽ ആഡ് ഗ്രൂപ്പ് ക്ലിക്ക് ചെയ്യുക » നിങ്ങളുടെ ഗ്രൂപ്പ് അഡ്മിനിസ്ട്രേറ്റർ ക്രമീകരണങ്ങളിലേക്ക് പോകുക » അഡ്മിനെ ചേർക്കുക ക്ലിക്ക് ചെയ്യുക » എല്ലാ അനുമതികളും നൽകുക » ടിക്ക് മാർക്ക് ക്ലിക്ക് ചെയ്യുക » പൂർത്തിയായി
• തുടർന്ന് നിങ്ങളുടെ ഗ്രൂപ്പിൽ /connect കമാൻഡ് ഉപയോഗിക്കുക
• വിജയകരം നിങ്ങളുടെ ഗ്രൂപ്പ് അംഗങ്ങൾക്കായി ഞാൻ സിനിമകൾ നൽകുന്നതാണ്"""
    
   
   

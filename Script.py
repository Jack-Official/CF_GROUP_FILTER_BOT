class script(object):   
    SUPPORT_TXT = """<b><u>⦁ Channels & Groups ⦁</u>

🎬 <i>Movie Requesting Groups</i>
📣 <i>Movie Updates Channel</i></b>"""

    ABOUT_TXT = """<b>━━━❰ {} ❱━━━➣</b>
    
<b>○ <i>Owner Name : <a href=https://t.me/TG_x_filter>🇮🇳 𝗛𝗘𝗗𝗗𝗬 ◢ ◤</b></a></i>

<b>○ <i>Creator : <a href=tg://settings>My Friend</b></a></i>

<b>○ <i>Library : Pyrogram</b></i>

<b>○ <i>Language : Python3</b></i>

<b>○ <i>Data Base : MongoDB</b></i>

<b>○ <i>Build Status : v5.2 [Stable]</b></i> """

    STATUS_TXT = """
<b>╔═══[<u>📊 Status Board 📊</u>]═══╗</b>
<b>📁 <i>Total Files</i>: <code>{}</code></b>
<b>👥 <i>Total Members</i>: <code>{}</code></b>
<b>💬 <i>Total Chats</i>: <code>{}</code></b>
<b>🗃 <i>Used Storage</i>: <code>{}</code></b>
<b>╚═══════════════════╝</b>"""
    
    LOG_TEXT_G = """#AddNewGroup
    
<b>• 👥 ɢʀᴏᴜᴩ : {a}</b>
<b>• 🆔 ɢʀᴏᴜᴩ ɪᴅ : <code>{b}</code></b>
<b>• 🧲 ɢʀᴏᴜᴩ ᴜꜱᴇʀɴᴀᴍᴇ : @{c}</b>
<b>• 🕵️‍♂️ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ : {d}</b>
<b>• 👨‍💻 ᴀᴅᴅᴇᴅ ʙʏ : {e}</b>

<b>• 🤖 ʙᴏᴛ ɴᴀᴍᴇ : {f}</b>
"""
    LOG_TEXT_P = """#StartNewUser
    
<b>• 🆔 ɪᴅ : <code>{}</code></b>
<b>• 😎 ɴᴀᴍᴇ : {}</b>
<b>• ♻️ ᴜꜱᴇʀɴᴀᴍᴇ : @{}</b>

<b>• 🤖 ʙᴏᴛ ᴜꜱᴇʀɴᴀᴍᴇ : @{}</b> """   

    CUSTOM_FILE_CAPTION = """<b>🎟️ Hello 👋 {mention} 💕</b>
    
<b>📁 File Name :</b><b><code>{file_name}</code></b>

<b>☟ ʝσιи • ѕнαяє • ѕυρρσят ☟
╭────── • ◆ • ──────╮
▢ Join : [OTT Updates](https://t.me/cinema_flix_updates)
╰────── • ◆ • ──────╯
☟ ʝσιи • ѕнαяє • ѕυρρσят ☟</b>"""

    REQBEST = """♻️ ᴀsᴋ ᴍᴏᴠɪᴇs ᴄᴏʀʀᴇᴄᴛ sᴘᴇʟʟɪɴɢ\n\n♻️ ᴅᴏɴᴛ ᴀsᴋ ᴍᴏᴠɪᴇs ᴛʜᴏsᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ɪɴ ᴏᴛᴛ ᴛʜᴇᴀᴛʀᴇ ϙᴜᴀʟɪᴛʏ ᴀᴠᴀɪʟᴀʙʟᴇ 🥹\n\n♻️ ғᴏʀ ʙᴇᴛᴛᴇʀ ʀᴇsᴜʟᴛ\n\n- ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ʏᴇᴀʀ\n\n- ᴇɴɢ : ʟᴇᴏ 2023"""

    REQTIPS = """🎬 MOVIE REQUEST FORMAT 🎬\n\n➲ ɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ\n➲ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ᴏʀ sᴇʀɪᴇs ɴᴀᴍᴇ\n➲ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ\n➲ ᴘᴀsᴛᴇ ᴛʜɪs ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ :"""

    REQINFO = """⚠️ INFORMATION ⚠️\n\nᴀғᴛᴇʀ 1 ᴅᴀʏs ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡᴇʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ\n\nɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ ʀᴇϙᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ ᴏʀ sᴇʀɪᴇs ғɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ"""

    NEOSUB = """അഥവാ ഗ്രൂപ്പ്‌ കോപ്പിറൈറ് കിട്ടി പോയാൽ.. പുതിയ ഗ്രൂപ്പ്‌ തുടങ്ങുമ്പോൾ ഇപ്പോൾ ജോയിൻ ആകുന്ന ചാനൽ വഴി ആയിരിക്കും അറിയിക്കുന്നത് 🤥"""

    MY_OWNER_TXT = """<b><b>╭──── •❰<u>🤴Owner Details🤴</u>❱• ──
┣ ○ <b><i>Full Name : 🇮🇳 𝗛𝗘𝗗𝗗𝗬 ◢ ◤</b></i>
┣ ○ <b><i>Username : @TG_x_filter</b></i>
╰──────────────────────</b></b>"""
    IMDB_TEMPLATE_TXT = """<b>🎬 Name : <a href={url}>{title}</a> \n📅 Year : {year} \n🎙 Language : {language} \n🌟 Rating : {rating}/ 10 \n🎭 Genre : {genres}</b>"""
    
   
   

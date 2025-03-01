import asyncio, re, ast, math, logging
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, SINGLE_BUTTON, PROTECT_CONTENT, \
    SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, NO_RESULTS_MSG, START_MESSAGE, PMFILTER, G_FILTER, BUTTON_LOCK, BUTTON_LOCK_TEXT, NOR_IMG, SPELL_IMG

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import del_all, find_filter, get_filters
from database.gfilters_mdb import find_gfilter, get_gfilters
from plugins.helper.admin_check import admin_fliter



logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
FILTER_MODE = {}
G_MODE = {}
NON_IMG ="""<b><i>👋Hello <a href=tg://settings >My Friend</a></i></b>\n\n<b>❝ <i>Use the Button Below to Search on Google or IMDB And Copy the Correct Movie Name And Paste.</i></b>\n\n<b>❝ <i>Don't Ask Movies that Are Not Released in OTT Platform.</i></b>\n\n<b>❝ <i>Try to Ask in [ Movie name, Year ] This Fromat.</i></b>\n\n<i><b><u>⚠️ Don't Use: ➲ [+:;'*!-&.. etc</i></b></u>"""

@Client.on_message(filters.command('autofilter') & filters.group & admin_fliter)
async def fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**Incomplete Command...**")
      
      m = await message.reply("**Setting.../**")

      if args in mode_on:
          FILTER_MODE[str(message.chat.id)] = "True" 
          await m.edit("**Auto-Filter Enabled**")
      
      elif args in mode_of:
          FILTER_MODE[str(message.chat.id)] = "False"
          await m.edit("**Auto-Filter Disabled**")
      else:
          await m.edit("Use :- /autofilter on 𝙾𝚁 /autofilter off")


@Client.on_message(filters.command('g_filter') & filters.group & admin_fliter)
async def g_fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**Incomplete Command...**")
      
      m = await message.reply("**Setting.../**")

      if args in mode_on:
          G_MODE[str(message.chat.id)] = "True" 
          await m.edit("**Global Enabled**")
      
      elif args in mode_of:
          G_MODE[str(message.chat.id)] = "False"
          await m.edit("**Global Disabled**")
      else:
          await m.edit("Use :- /g_filter on 𝙾𝚁 /g_filter off")


@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.incoming & filters.group)
async def give_filter(client, message):
    if G_FILTER:
        if G_MODE.get(str(message.chat.id)) == "False":
            return 
        else:
            kd = await global_filters(client, message)
        if kd == False:          
            k = await manual_filters(client, message)
            if k == False:
                if FILTER_MODE.get(str(message.chat.id)) == "False":
                    return
                else:
                    await auto_filter(client, message)   
    else:
        k = await manual_filters(client, message)
        if k == False:
            if FILTER_MODE.get(str(message.chat.id)) == "False":
                return
            else:
                await auto_filter(client, message)   


@Client.on_message(filters.private & filters.text & filters.chat(AUTH_USERS) if AUTH_USERS else filters.text & filters.private)
async def pm_filter(client, message):
    if PMFILTER:
        if G_FILTER:
            kd = await global_filters(client, message)
            if kd == False:
                await pm_AutoFilter(client, message)
        else:
            await pm_AutoFilter(client, message)
    else:
        return


@Client.on_message(filters.private & filters.text & filters.incoming)
async def pv_filter(client, message):
    kd = await global_filters(client, message)
    if kd == False:
        await auto_filter(client, message)
        

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    nxreq  = query.from_user.id if query.from_user else 0
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f" [{get_size(file.file_size)}]  {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f" {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f" {get_size(file.file_size)}",
                    callback_data=f'files#{nxreq}#{file.file_id}',
                ),
            ]
            for file in files
        ]  

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("☜ 𝗕𝗮𝗰𝗸", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f" {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} ",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton("❏ 𝗣𝗮𝗴𝗲", callback_data="pages"), 
             InlineKeyboardButton(f" {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} ", callback_data="pages"),
             InlineKeyboardButton("𝗡𝗲𝘅𝘁 ☞", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("☜ 𝗕𝗮𝗰𝗸", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f" {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} ", callback_data="pages"),
                InlineKeyboardButton("𝗡𝗲𝘅𝘁 ☞", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            one_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔍 Search in Google 🔎", url="https://www.google.com")]])
            k = await query.message.edit('<b>👋Hey {message.from_user.mention}</b>\n\nHere is movie request format👇\n\n• Go to Google\n\n• Type the movie name you want\n\n• Copy the movie name with correct spelling\n\n• Then paste the movie name here in this group\n\n<b>🚫 Dont Spam 🚫</b>', reply_markup = one_button)
            await asyncio.sleep(99)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('𝖯𝗅𝖾𝖺𝖾𝖾 𝖲𝗁𝖺𝗋𝖾 𝖠𝗇𝖽 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.💞')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return
        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Buddy Don't Touch Others Property 😁", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "𝙲𝙾𝙽𝙽𝙴𝙲𝚃"
            cb = "connectcb"
        else:
            stat = "𝙳𝙸𝚂𝙲𝙾𝙽𝙽𝙴𝙲𝚃"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("🗑️Delete", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("⭅ Back", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"𝙶𝚁𝙾𝚄𝙿 𝙽𝙰𝙼𝙴 :- **{title}**\n𝙶𝚁𝙾𝚄𝙿 𝙸𝙳 :- `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('𝖲𝗁𝖺𝗋𝖾 𝖠𝗇𝖽 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.💞')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))
        
        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('𝖲𝗁𝖺𝗋𝖾 𝖠𝗇𝖽 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.💞')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('𝖲𝗁𝖺𝗋𝖾 𝖠𝗇𝖽 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.💞')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('𝖲𝗁𝖺𝗋𝖾 𝖠𝗇𝖽 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.💞')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)

    if query.data.startswith("pmfile"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)                                                                                                      
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return            
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "pmfilep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [[                          
                          InlineKeyboardButton('🗑️ Delete / Close 🗑️', callback_data='close_data')
                        ]]
                    )
                )                       
        except Exception as e:
            await query.answer(f"⚠️ Error {e}", show_alert=True)
        
    if query.data.startswith("file"):        
        ident, req, file_id = query.data.split("#")
        if BUTTON_LOCK:
            if int(req) not in [query.from_user.id, 0]:
                return await query.answer(BUTTON_LOCK_TEXT.format(query=query.from_user.first_name), show_alert=True)             
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)                               
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [[                          
                          InlineKeyboardButton('🗑️ Delete / Close 🗑️', callback_data='close_data')
                        ]]
                    )
                )
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart Okay", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
               f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)  
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
            reply_markup=InlineKeyboardMarkup(
                [[                          
                  InlineKeyboardButton('🗑️ Delete / Close 🗑️', callback_data='close_data')
                ]]
            )
        )
    elif query.data == "pages":
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ..👀", show_alert=True)
    elif query.data == "reqtips":
        await query.answer(text=script.REQTIPS, show_alert=True)
    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)
    elif query.data == "reqbest":
        await query.answer(text=script.REQBEST, show_alert=True)
    elif query.data == "nomg":
        await query.answer("ഇവിടെ നോക്കണ്ട സാധനം കൊടുക്കുന്നില്ല..🤧", show_alert=True)
    elif query.data =="neosub":
        await query.answer(text=script.NEOSUB, show_alert=True)
    elif query.data == "closeme":
        buttons = [[
            InlineKeyboardButton('✨ Click Here For More Buttons ✨', callback_data='start')
        ]]   
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )        
    elif query.data == "start":   
        buttons = [[
            InlineKeyboardButton('✗ Click To Close This Buttons ✗', callback_data='closeme')
            ],[
            InlineKeyboardButton('🤴 Owner', callback_data='my_owner'),
            InlineKeyboardButton('Support 💬', callback_data='support')
            ],[
            InlineKeyboardButton('⚠️ About', callback_data='about'),
            InlineKeyboardButton('Close ✗', callback_data='close_data')    
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )        
    elif query.data == "support":
        buttons = [[
            InlineKeyboardButton('• Main Update Channel •', url="https://t.me/cinema_flix_updates")
            ],[
            InlineKeyboardButton('• Group 1 •', url="https://t.me/Mallu_Movie_Hub_Group"),
            InlineKeyboardButton('• Group 2 •', url="https://t.me/+iEbhY7mM4oE1OTVl")
            ],[
            InlineKeyboardButton('⭅ Back To Home ⇛', callback_data='start')
        ]] 
        reply_markup = InlineKeyboardMarkup(buttons)             
        await query.message.edit_text(                     
            text=script.SUPPORT_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('⭅ Back', callback_data='start'),
            InlineKeyboardButton('Status 📊', callback_data='stats'),
            InlineKeyboardButton('Close ✗', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons) 
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "my_owner":
        buttons = [[
            InlineKeyboardButton('⭅ Back', callback_data='start'),
            InlineKeyboardButton('Contact 📞', url="https://t.me/TG_x_filter")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MY_OWNER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⭅ Back ', callback_data='about'),
            InlineKeyboardButton('Refresh ⏳', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⭅ Back ', callback_data='about'),
            InlineKeyboardButton('Refresh ⏳', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⭅ Back ', callback_data='about'),
            InlineKeyboardButton('Refresh ⏳', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⭅ Back ', callback_data='about'),
            InlineKeyboardButton('Refresh ⏳', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
      )
        
    elif query.data == "predvd":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'predvd',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('PreDVD File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} PʀᴇDVD Fɪʟᴇs.</b>")

    elif query.data == "camrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'camrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('CamRip File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} CᴀᴍRɪᴘ Fɪʟᴇs.</b>")

    elif query.data == "predvdrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'Predvdrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('PreDVDRip File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} PʀᴇDVDRɪᴘ Fɪʟᴇs.</b>")

    elif query.data == "hdcam":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HDCam',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('HDCams File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HDCᴀᴍ Fɪʟᴇs.</b>")

    elif query.data == "hdcams":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HD-Cam',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('HD-Cams File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HD-Cᴀᴍ Fɪʟᴇs.</b>")

    elif query.data == "sprint":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'S-print',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('S-Print File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} S-Pʀɪɴᴛ Fɪʟᴇs.</b>")

    elif query.data == "hdts":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HDTS',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('HDTS File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HDTS Fɪʟᴇs.</b>")

    elif query.data == "hdtss":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HD-TS',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('HD-TS File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HD-TS Fɪʟᴇs.</b>")
        
    elif query.data == "predvd":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Deleting PreDVDs... Please wait...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'predvd',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('PreDVD File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Successfully deleted {deleted} PreDVD files.</b>")

    elif query.data == "camrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Deleting CamRips... Please wait...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'camrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('CamRip File Found ! Successfully deleted from database.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Successfully deleted {deleted} CamRip files.</b>")
        
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return 

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('▪️Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('𝐒𝐢𝐧𝐠𝐥𝐞' if settings["button"] else '𝐃𝐨𝐮𝐛𝐥𝐞',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('🤖Bᴏᴛ Pᴍ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✓ 𝖸ᴇꜱ' if settings["botpm"] else '✕ Nᴏ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('📁Fɪʟᴇ Sᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✓ 𝖸ᴇꜱ' if settings["file_secure"] else '✕ Nᴏ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('🌄Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✓ 𝖸ᴇꜱ' if settings["imdb"] else '✕ Nᴏ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('🔎Sᴩᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✓ 𝖸ᴇꜱ' if settings["spell_check"] else '✕ Nᴏ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('🫂Wᴇʟᴄᴏᴍᴇ Mɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✓ 𝖸ᴇꜱ' if settings["welcome"] else '✕ Nᴏ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    req = message.from_user.id if message.from_user else 0
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f" [{get_size(file.file_size)}]  {file.file_name}", callback_data=f'{pre}#{req}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f" {file.file_name}",
                    callback_data=f'{pre}#{req}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f" {get_size(file.file_size)}",
                    callback_data=f'{pre}#{req}#{file.file_id}',
                ),
            ]
            for file in files
        ]   
        
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton("❏ 𝗣𝗮𝗴𝗲𝘀", callback_data="pages"), 
             InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / 6)}", callback_data="pages"),
             InlineKeyboardButton(text="𝗡𝗲𝘅𝘁 ☞", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="💢..𝗡𝗼 𝗠𝗼𝗿𝗲 𝗡𝗲𝘅𝘁 𝗣𝗮𝗴𝗲𝘀..💢", callback_data="pages")]
        )                   
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            group = message.chat.title,
            requested = message.from_user.mention,
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>⚬ The Results For : {search}</b>\n\n<b>⚬ Request By : {message.from_user.mention}</b>\n\n<b>⚬ Total Files : {str(total_results)}</b>\n\n<b>⚬ Powered By : {message.chat.title}</b>"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await fmsg.delete()            
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))           
            await asyncio.sleep(IMDB_DELET_TIME)
            await fmsg.delete()            
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await fek.delete()
    else:
        fuk = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(IMDB_DELET_TIME)
        await fuk.delete()        
    if pmspoll:
        await msg.message.delete()


async def advantage_spell_chok(msg):
    mv_rqst = msg.text
    search = msg.text.replace(" ", "+")
    btn = [[
        InlineKeyboardButton(
            text="🔎 Google 🔍",
            url=f"https://google.com/search?q={search}"
        ),
        InlineKeyboardButton(
            text="🔮 IMDB 🔮",
            url=f"https://imdb.com/find?q={search}")

    ]]
    spl = await msg.reply_photo(
            photo="https://envs.sh/RCE.jpg", 
            caption=NON_IMG.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(btn)
    )
    await asyncio.sleep(99)
    await spl.delete()
    await msg.delete()
    return

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True, reply_to_message_id=reply_id)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False


async def global_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            knd3 = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(IMDB_DELET_TIME)
                            await knd3.delete()
                            await message.delete()

                        else:
                            button = eval(btn)
                            knd2 = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(IMDB_DELET_TIME)
                            await knd2.delete()
                            await message.delete()

                    elif btn == "[]":
                        knd1 = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(IMDB_DELET_TIME)
                        await knd1.delete()
                        await message.delete()

                    else:
                        button = eval(btn)
                        knd = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(IMDB_DELET_TIME)
                        await knd.delete()
                        await message.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

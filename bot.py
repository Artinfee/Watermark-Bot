# (c) @artin_fe

# This is Telegram Video Watermark Adder Bot's Source Code.

# I Hardly Made This. So Don't Forget to Give Me Credits.

# Done this Huge Task for Free. If you guys not support me,

# I will stop making such things!

# Edit anything at your own risk!

# Don't forget to help me if I done any mistake in the codes.

# Support Group: @artin_fe 

# Bots Channel: @hector_tm

import os

import time

import json

import random

import asyncio

import aiohttp

from hachoir.metadata import extractMetadata

from hachoir.parser import createParser

from PIL import Image

from core.ffmpeg import vidmark

from core.clean import delete_all, delete_trash

from pyrogram import Client, filters

from configs import Config

from core.handlers.main_db_handler import db

from core.display_progress import progress_for_pyrogram, humanbytes

from core.handlers.force_sub_handler import handle_force_subscribe

from core.handlers.upload_video_handler import send_video_handler

from core.handlers.broadcast_handlers import broadcast_handler

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram.errors.exceptions.flood_420 import FloodWait

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MessageNotModified

AHBot = Client(Config.BOT_USERNAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)

@AHBot.on_message(filters.command(["start", "help"]) & filters.private)

async def HelpWatermark(bot, cmd):

	if not await db.is_user_exist(cmd.from_user.id):		await db.add_user(cmd.from_user.id)

		await bot.send_message(

			Config.LOG_CHANNEL,

			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"

		)

	if Config.UPDATES_CHANNEL:

		fsub = await handle_force_subscribe(bot, cmd)

		if fsub == 400:

			return

	await cmd.reply_text(

		text=Config.USAGE_WATERMARK_ADDER,

		parse_mode="Markdown",

		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/artin_fe"), InlineKeyboardButton("Support Group", url="https://t.me/artin_fe")], [InlineKeyboardButton("Bots Channel", url="https://t.me/hector_tm")], [InlineKeyboardButton("Source Code", url="https://github.com/artin_fe/Watermark-Bot")]]),

		disable_web_page_preview=True

	)

@AHBot.on_message(filters.command(["reset"]) & filters.private)

async def reset(bot, update):

        await db.delete_user(update.from_user.id)

        await db.add_user(update.from_user.id)

        await update.reply_text("تنظیمات با موفقیت بازنشانی شد")

@AHBot.on_message(filters.command("settings") & filters.private)

async def SettingsBot(bot, cmd):

	if not await db.is_user_exist(cmd.from_user.id):

		await db.add_user(cmd.from_user.id)

		await bot.send_message(

			Config.LOG_CHANNEL,

			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"

		)

	if Config.UPDATES_CHANNEL:

		fsub = await handle_force_subscribe(bot, cmd)

		if fsub == 400:

			return

	## --- Checks --- ##

	position_tag = None

	watermark_position = await db.get_position(cmd.from_user.id)

	if watermark_position == "5:main_h-overlay_h":

		position_tag = "Bottom Left"

	elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":

		position_tag = "Bottom Right"

	elif watermark_position == "main_w-overlay_w-5:5":

		position_tag = "Top Right"

	elif watermark_position == "5:5":

		position_tag = "Top Left"

	watermark_size = await db.get_size(cmd.from_user.id)

	if int(watermark_size) == 5:

		size_tag = "5%"

	elif int(watermark_size) == 7:

		size_tag = "7%"

	elif int(watermark_size) == 10:

		size_tag = "10%"

	elif int(watermark_size) == 15:

		size_tag = "15%"

	elif int(watermark_size) == 20:

		size_tag = "20%"

	elif int(watermark_size) == 25:

		size_tag = "25%"

	elif int(watermark_size) == 30:

		size_tag = "30%"

	elif int(watermark_size) == 35:

		size_tag = "35%"

	elif int(watermark_size) == 40:

		size_tag = "40%"

	elif int(watermark_size) == 45:

		size_tag = "45%"

	else:

		size_tag = "7%"

	## --- Next --- ##

	await cmd.reply_text(

		text="در اینجا می توانید تنظیمات واترمارک خود را تنظیم کنید:",

		disable_web_page_preview=True,

		parse_mode="Markdown",

		reply_markup=InlineKeyboardMarkup(

			[

				[InlineKeyboardButton(f"موقعیت واترمارک - {position_tag}", callback_data="lol")],

				[InlineKeyboardButton("بالا سمت چپ ", callback_data=f"position_5:5"), InlineKeyboardButton("بالا سمت راست", callback_data=f"position_main_w-overlay_w-5:5")],

				[InlineKeyboardButton("Setپایین سمت چپ", callback_data=f"position_5:main_h-overlay_h"), InlineKeyboardButton("پایین سمت راست", callback_data=f"position_main_w-overlay_w-5:main_h-overlay_h-5")],

				[InlineKeyboardButton(f"سایز واترمارک - {size_tag}", callback_data="lel")],

				[InlineKeyboardButton("5%", callback_data=f"size_5"), InlineKeyboardButton("7%", callback_data=f"size_7"), InlineKeyboardButton("10%", callback_data=f"size_10"), InlineKeyboardButton("15%", callback_data=f"size_15"), InlineKeyboardButton("20%", callback_data=f"size_20")],

				[InlineKeyboardButton("25%", callback_data=f"size_25"), InlineKeyboardButton("30%", callback_data=f"size_30"), InlineKeyboardButton("35%", callback_data=f"size_30"), InlineKeyboardButton("40%", callback_data=f"size_40"), InlineKeyboardButton("45%", callback_data=f"size_45")],

				[InlineKeyboardButton(f"تنظیمات را به حالت پیش فرض بازنشانی کنید", callback_data="reset")]

			]

		)

	)

@AHBot.on_message(filters.document | filters.video | filters.photo & filters.private)

async def VidWatermarkAdder(bot, cmd):

	if not await db.is_user_exist(cmd.from_user.id):

		await db.add_user(cmd.from_user.id)

		await bot.send_message(

			Config.LOG_CHANNEL,

			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"

		)

	if Config.UPDATES_CHANNEL:

		fsub = await handle_force_subscribe(bot, cmd)

		if fsub == 400:

			return

	## --- Noobie Process --- ##

	if cmd.photo or (cmd.document and cmd.document.mime_type.startswith("image/")):

		editable = await cmd.reply_text("دانلود عکس ...")

		watermark_path = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/thumb.jpg"

		await asyncio.sleep(5)

		c_time = time.time()

		await bot.download_media(

			message=cmd,

			file_name=watermark_path,

		)

		await editable.delete()

		await cmd.reply_text("این به عنوان واترمارک ویدیوی بعدی ذخیره شد!

اکنون هر ویدیویی را ارسال کنید تا شروع به اضافه کردن واترمارک به ویدیو کنید!")

		return

	else:

		pass

	working_dir = Config.DOWN_PATH + "/WatermarkAdder/"

	if not os.path.exists(working_dir):

		os.makedirs(working_dir)

	watermark_path = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/thumb.jpg"

	if not os.path.exists(watermark_path):

		await cmd.reply_text("شما هیچ واترمارکی تنظیم نکردید!\n\nتصویر JPG یا PNG ارسال کنید")

		return

	file_type = cmd.video or cmd.document

	if not file_type.mime_type.startswith("video/"):

		await cmd.reply_text("این یک ویدیو نیست!")

		return

	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"

	if os.path.exists(status):

		await cmd.reply_text("متأسفیم، در حال حاضر من مشغول کار دیگری هستم!\n\nپس از مدتی دوباره امتحان کنید!")

		return

	preset = Config.PRESET

	editable = await cmd.reply_text("دانلود ویدیو...", parse_mode="Markdown")

	with open(status, "w") as f:

		statusMsg = {

			'chat_id': cmd.from_user.id,

			'message': editable.message_id

		}

		json.dump(statusMsg, f, indent=2)

	dl_loc = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/"

	if not os.path.isdir(dl_loc):

		os.makedirs(dl_loc)

	the_media = None

	user_info = f"**UserID:** #id{cmd.from_user.id}\n**Name:** [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})"

	## --- Done --- ##

	try:

		forwarded_video = await cmd.forward(Config.LOG_CHANNEL)

		logs_msg = await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"استارت دانلود!\n\n{user_info}", reply_to_message_id=forwarded_video.message_id, disable_web_page_preview=True, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{cmd.from_user.id}")]]))

		await asyncio.sleep(5)

		c_time = time.time()

		the_media = await bot.download_media(

			message=cmd,

			file_name=dl_loc,

			progress=progress_for_pyrogram,

			progress_args=(

				"Downloading Sir ...",

				editable,

				logs_msg,

				c_time

			)

		)

		if the_media is None:

			await delete_trash(status)

			await delete_trash(the_media)

			print(f"Download Failed")

			await editable.edit("Unable to Download The Video!")

			return

	except Exception as err:

		await delete_trash(status)

		await delete_trash(the_media)

		print(f"Download Failed: {err}")

		await editable.edit("Unable to Download The Video!")

		return

	watermark_position = await db.get_position(cmd.from_user.id)

	if watermark_position == "5:main_h-overlay_h":

		position_tag = "Bottom Left"

	elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":

		position_tag = "Bottom Right"

	elif watermark_position == "main_w-overlay_w-5:5":

		position_tag = "Top Right"

	elif watermark_position == "5:5":

		position_tag = "Top Left"

	else:

		position_tag = "Top Left"

		watermark_position = "5:5"

	watermark_size = await db.get_size(cmd.from_user.id)

	await editable.edit(f"Trying to Add Watermark to the Video at {position_tag} Corner ...\n\nPlease Wait!")

	duration = 0

	metadata = extractMetadata(createParser(the_media))

	if metadata.has("duration"):

		duration = metadata.get('duration').seconds

	the_media_file_name = os.path.basename(the_media)

	main_file_name = os.path.splitext(the_media_file_name)[0]

	output_vid = main_file_name + "_[" + str(cmd.from_user.id) + "]_[" + str(time.time()) + "]_[@artin_fe]" + ".mp4"

	progress = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/progress.txt"

	try:

		output_vid = await vidmark(the_media, editable, progress, watermark_path, output_vid, duration, logs_msg, status, preset, watermark_position, watermark_size)

	except Exception as err:

		print(f"امکان افزودن واترمارک وجود ندارد: {err}")

		await editable.edit("امکان افزودن واترمارک وجود ندارد!")

		await logs_msg.edit(f"#ERROR: امکان افزودن واترمارک وجود ندارد!\n\n**Error:** `{err}`")

		await delete_all()

		return

	if output_vid is None:

		await editable.edit("Something went wrong!")

		await logs_msg.edit("#ERROR: Something went wrong!")

		await delete_all()

		return

	await editable.edit("واترمارک با موفقیت اضافه شد!\در\در تلاش برای آپلود...")

	await logs_msg.edit("واترمارک با موفقیت اضافه شد!\در\در تلاش برای آپلود...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{cmd.from_user.id}")]]))

	width = 100

	height = 100

	duration = 0

	metadata = extractMetadata(createParser(output_vid))

	if metadata.has("duration"):

		duration = metadata.get('duration').seconds

	if metadata.has("width"):

		width = metadata.get("width")

	if metadata.has("height"):

		height = metadata.get("height")

	video_thumbnail = None

	try:

		video_thumbnail = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/" + str(time.time()) + ".jpg"

		ttl = random.randint(0, int(duration) - 1)

		file_genertor_command = [

			"ffmpeg",

			"-ss",

			str(ttl),

			"-i",

			output_vid,

			"-vframes",

			"1",

			video_thumbnail

		]

		process = await asyncio.create_subprocess_exec(

			*file_genertor_command,

			stdout=asyncio.subprocess.PIPE,

			stderr=asyncio.subprocess.PIPE,

		)

		stdout, stderr = await process.communicate()

		e_response = stderr.decode().strip()

		t_response = stdout.decode().strip()

		print(e_response)

		print(t_response)

		Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)

		img = Image.open(video_thumbnail)

		img.resize((width, height))

		img.save(video_thumbnail, "JPEG")

	except Exception as err:

		print(f"Error: {err}")

	# --- Upload --- #

	file_size = os.path.getsize(output_vid)

	if (int(file_size) > 2097152000) and (Config.ALLOW_UPLOAD_TO_STREAMTAPE is True) and (Config.STREAMTAPE_API_USERNAME != "NoNeed") and (Config.STREAMTAPE_API_PASS != "NoNeed"):

		await editable.edit(f"Sorry Sir,\n\nFile Size Become {humanbytes(file_size)} !!\nI can't Upload to Telegram!\n\nSo Now Uploading to Streamtape ...")

		try:

			async with aiohttp.ClientSession() as session:

				Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"

				hit_api = await session.get(Main_API.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS))

				json_data = await hit_api.json()

				temp_api = json_data["result"]["url"]

				files = {'file1': open(output_vid, 'rb')}

				response = await session.post(temp_api, data=files)

				data_f = await response.json(content_type=None)

				download_link = data_f["result"]["url"]

				filename = output_vid.split("/")[-1].replace("_"," ")

				text_edit = f"File Uploaded to Streamtape!\n\n**File Name:** `{filename}`\n**Size:** `{humanbytes(file_size)}`\n**Link:** `{download_link}`"

				await editable.edit(text_edit, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=download_link)]]))

				await logs_msg.edit("Successfullyفایل در Streamtape آپلود شد!\n\nمن اکنون آزاد هستم!", parse_mode="Markdown", disable_web_page_preview=True)

		except Exception as e:

			print(f"Error: {e}")

			await editable.edit("متأسفیم، مشکلی پیش آمد!\n\nدر Streamtape آپلود نمی‌شود.  می توانید گزارش دهید [Support Group](https://t.me/artin_fe).")

			await logs_msg.edit(f"هنگام آپلود در Streamtape خطایی دریافت کردم!\n\nخطا: {e}")

		await delete_all()

		return

	await asyncio.sleep(5)

	try:

		sent_vid = await send_video_handler(bot, cmd, output_vid, video_thumbnail, duration, width, height, editable, logs_msg, file_size)

	except FloodWait as e:

		print(f"Got FloodWait of {e.x}s ...")

		await asyncio.sleep(e.x)

		await asyncio.sleep(5)

		sent_vid = await send_video_handler(bot, cmd, output_vid, video_thumbnail, duration, width, height, editable, logs_msg, file_size)

	except Exception as err:

		print(f"Unable to Upload Video: {err}")

		await logs_msg.edit(f"#ERROR: Unable to Upload Video!\n\n**Error:** `{err}`")

		await delete_all()

		return

	await delete_all()

	await editable.delete()

	forward_vid = await sent_vid.forward(Config.LOG_CHANNEL)

	await logs_msg.delete()

	await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"#WATERMARK_ADDED: Video Uploaded!\n\n{user_info}", reply_to_message_id=forward_vid.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{cmd.from_user.id}")]]))

@AHBot.on_message(filters.command("cancel") & filters.private)

async def CancelWatermarkAdder(bot, cmd):

	if not await db.is_user_exist(cmd.from_user.id):

		await db.add_user(cmd.from_user.id)

		await bot.send_message(

			Config.LOG_CHANNEL,

			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"

		)

	if not int(cmd.from_user.id) == Config.OWNER_ID:

		await cmd.reply_text("شما نمی توانید از آن دستور استفاده کنید!")

		return

	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"

	with open(status, 'r+') as f:

		statusMsg = json.load(f)

		if 'pid' in statusMsg.keys():

			try:

				os.kill(statusMsg["pid"], 9)

				await delete_trash(status)

			except Exception as err:

				print(err)

		await delete_all()

		await bot.send_message(chat_id=Config.LOG_CHANNEL, text="#WATERMARK_ADDER: Stopped!")

		await cmd.reply_text("فرآیند افزودن واترمارک متوقف شد!")

		try:

			await bot.edit_message_text(chat_id=int(statusMsg["chat_id"]), message_id=int(statusMsg["message"]), text="🚦🚦 Last Process Stopped 🚦🚦")

		except:

			pass

@AHBot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)

async def open_broadcast_handler(bot, message):

	await broadcast_handler(c=bot, m=message)

@AHBot.on_message(filters.private & filters.command("status"))

async def sts(_, m):

	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"

	if os.path.exists(status):

		msg_text = "متأسفیم، در حال حاضر من مشغول کار دیگری هستم!\nدر حال حاضر نمی توانم واترمارک اضافه کنم."

	else:

		msg_text = "من اکنون رایگان هستم!\nهر ویدیویی را برای اضافه کردن واترمارک برای من ارسال کنید"

	if int(m.from_user.id) == Config.OWNER_ID:

		total_users = await db.total_users_count()

		msg_text += f"\n\n**Total Users in DB:** `{total_users}`"

	await m.reply_text(text=msg_text, parse_mode="Markdown", quote=True)

@AHBot.on_callback_query()

async def button(bot, cmd: CallbackQuery):

	cb_data = cmd.data

	if "refreshmeh" in cb_data:

		if Config.UPDATES_CHANNEL:

			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))

			try:

				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.message.chat.id)

				if user.status == "kicked":

					await cmd.message.edit(

						text="مشکلی پیش آمد.  با من تماس بگیرید",

						parse_mode="markdown",

						disable_web_page_preview=True

					)

					return

			except UserNotParticipant:

				await cmd.message.edit(

					text="**شما هنوز عضو نشده اید ☹️، لطفا برای استفاده از این ربات به کانال به روز رسانی های من بپیوندید!**\n\nبه دلیل بارگذاری بیش از حد، فقط مشترکین کانال می توانند از ربات استفاده کنند.!",

					reply_markup=InlineKeyboardMarkup(

						[

							[

								InlineKeyboardButton("🤖 عضویت در کانال📌", url=invite_link.invite_link)

							],

							[

								InlineKeyboardButton("🔄 تایید عضویت 🔄", callback_data="refreshmeh")

							]

						]

					),

					parse_mode="markdown"

				)

				return

			except Exception:

				await cmd.message.edit(

					text="مشکلی پیش آمد.  با من تماس بگیرید",

					parse_mode="markdown",

					disable_web_page_preview=True

				)

				return

		await cmd.message.edit(

			text=Config.USAGE_WATERMARK_ADDER,

			parse_mode="Markdown",

			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/artin_fe"), InlineKeyboardButton("Support Group", url="https://t.me/artin_fe")], [InlineKeyboardButton("Bots Channel", url="https://t.me/hector_tm")]]),

			disable_web_page_preview=True

		)

	elif "lol" in cb_data:

		await cmd.answer("آقا، این دکمه کار نمی کند XD\n\nدکمه های پایین را فشار دهید تا موقعیت واترمارک را تنظیم کنید!", show_alert=True)

	elif "lel" in cb_data:

		await cmd.answer("آقا، این دکمه کار نمی کند XD\n\nدکمه های پایین را فشار دهید تا اندازه واترمارک تنظیم شود", show_alert=True)

	elif cb_data.startswith("position_") or cb_data.startswith("size_"):

		if Config.UPDATES_CHANNEL:

			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))

			try:

				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.message.chat.id)

				if user.status == "kicked":

					await cmd.message.edit(

						text="مشکلی پیش آمد.  با من تماس بگیرید.",

						parse_mode="markdown",

						disable_web_page_preview=True

					)

					return

			except UserNotParticipant:

				await cmd.message.edit(

					text="**شما هنوز عضو نشده اید ☹️، لطفا برای استفاده از این ربات به کانال به روز رسانی های من بپیوندید!**\n\nبه دلیل بارگذاری بیش از حد، فقط مشترکین کانال می توانند از ربات استفاده کنند.!",

					reply_markup=InlineKeyboardMarkup(

						[

							[

								InlineKeyboardButton("🤖 عضویت در کانال📌", url=invite_link.invite_link)

							],

							[

								InlineKeyboardButton("🔄 تایید عضویت 🔄", callback_data="refreshmeh")

							]

						]

					),

					parse_mode="markdown"

				)

				return

			except Exception:

				await cmd.message.edit(

					text="مشکلی پیش آمد.  با من تماس بگیرید [Support Group](https://t.me/artin_fe).",

					parse_mode="markdown",

					disable_web_page_preview=True

				)

				return

		await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"#SETTINGS_SET: [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) Changed Settings!\n\n**User ID:** #id{cmd.from_user.id}\n**Data:** `{cb_data}`", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{cmd.from_user.id}")]]))

		new_position = cb_data.split("_", 1)[1]

		if cb_data.startswith("position_"):

			await db.set_position(cmd.from_user.id, new_position)

		elif cb_data.startswith("size_"):

			await db.set_size(cmd.from_user.id, new_position)

		watermark_position = await db.get_position(cmd.from_user.id)

		if watermark_position == "5:main_h-overlay_h":

			position_tag = "Bottom Left"

		elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":

			position_tag = "Bottom Right"

		elif watermark_position == "main_w-overlay_w-5:5":

			position_tag = "Top Right"

		elif watermark_position == "5:5":

			position_tag = "Top Left"

		else:

			position_tag = "Top Left"

		watermark_size = await db.get_size(cmd.from_user.id)

		if int(watermark_size) == 5:

			size_tag = "5%"

		elif int(watermark_size) == 7:

			size_tag = "7%"

		elif int(watermark_size) == 10:

			size_tag = "10%"

		elif int(watermark_size) == 15:

			size_tag = "15%"

		elif int(watermark_size) == 20:

			size_tag = "20%"

		elif int(watermark_size) == 25:

			size_tag = "25%"

		elif int(watermark_size) == 30:

			size_tag = "30%"

		elif int(watermark_size) == 35:

			size_tag = "35%"

		elif int(watermark_size) == 40:

			size_tag = "40%"

		elif int(watermark_size) == 45:

			size_tag = "45%"

		else:

			size_tag = "7%"

		try:

			await cmd.message.edit(

				text="در اینجا می توانید تنظیمات واترمارک خود را تنظیم کنید:",

				disable_web_page_preview=True,

				parse_mode="Markdown",

				reply_markup=InlineKeyboardMarkup(

					[

						[InlineKeyboardButton(f"موقعیت واترمارک - {position_tag}", callback_data="lol")],

						[InlineKeyboardButton("بالا سمت چپ ", callback_data=f"position_5:5"), InlineKeyboardButton("بالا سمت راست", callback_data=f"position_main_w-overlay_w-5:5")],

						[InlineKeyboardButton("Setپایین سمت چپ", callback_data=f"position_5:main_h-overlay_h"), InlineKeyboardButton("پایین سمت راست", callback_data=f"position_main_w-overlay_w-5:main_h-overlay_h-5")],

						[InlineKeyboardButton(f"پایین سمت راست - {size_tag}", callback_data="lel")],

						[InlineKeyboardButton("5%", callback_data=f"size_5"), InlineKeyboardButton("7%", callback_data=f"size_7"), InlineKeyboardButton("10%", callback_data=f"size_10"), InlineKeyboardButton("15%", callback_data=f"size_15"), InlineKeyboardButton("20%", callback_data=f"size_20")],

						[InlineKeyboardButton("25%", callback_data=f"size_25"), InlineKeyboardButton("30%", callback_data=f"size_30"), InlineKeyboardButton("35%", callback_data=f"size_30"), InlineKeyboardButton("40%", callback_data=f"size_40"), InlineKeyboardButton("45%", callback_data=f"size_45")],

				                [InlineKeyboardButton(f"تنظیمات را به حالت پیش فرض بازنشانی کنید", callback_data="reset")]

					]

				)

			)

		except MessageNotModified:

			pass

	elif cb_data.startswith("ban_"):

		if Config.UPDATES_CHANNEL is None:

			await cmd.answer("متاسفم قربان، شما هیچ کانال به روز رسانی تنظیم نکردیدl!", show_alert=True)

			return

		try:

			user_id = cb_data.split("_", 1)[1]

			await bot.kick_chat_member(chat_id=Config.UPDATES_CHANNEL, user_id=int(user_id))

			await cmd.answer("کاربر از کانال به‌روزرسانی‌ها ممنوع شد!", show_alert=True)

		except Exception as e:

			await cmd.answer(f"Can't Ban Him!\n\nError: {e}", show_alert=True)

	elif "reset" in cb_data:

		await db.delete_user(cmd.from_user.id)

		await db.add_user(cmd.from_user.id)

		await cmd.answer("تنظیمات با موفقیت بازنشانی شد!", show_alert=True)

AHBot.run()

# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "23737035"))
API_HASH = getenv("API_HASH", "5381b94dbcb2f25b313ea7b29583805c")
BOT_TOKEN = getenv("BOT_TOKEN", "7206156037:AAEd1yPYMn1vP4tWWX82QxFaMcQ6yOJ7BNY")
OWNER_ID = int(getenv("OWNER_ID", "6955269919"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://ggn:ggn@ggn.upuljx5.mongodb.net/?retryWrites=true&w=majority&appName=ggn")
LOG_GROUP = int(getenv("LOG_GROUP", "-1002155139704"))
SESSION = getenv("PYROGRAM_V2_SESSION", "BQFqMssAjC6yR9FLCkVnjTDcJk6UpJWWdVfgHPEUpDtYfVU6mDTTfiL-vRdJZzkpx-1FEACihnaJjMvly-tuzJQWW0mFC4hdWI8QC6tDjw0GNxlb1vQH64rNFdY1FZdVy98icWNHohkJUaj2j_Md3mfLIeUbBFrmMI3VERr-L8jpg0FaDlx4keblxCjS6QKdT7q53tMVMvu-js6luyBzVj6sdtIFlzFtF_PrYnjLBhvCqBHGdcENKdadHDPbPFFtld0xGFse99XUxvf55s3XXE9gH0aoxd3QK7I0M5RbSI5aKRfen_CFnBkujWdRragOhg2vLiaPQkl0xn-VTsu-GIYQTb1sewAAAABy2dl8AA")
FORCESUB = getenv("FORCESUB", "SmexyStore")

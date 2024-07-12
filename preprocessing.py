import subprocess

# Install nltk using pip
subprocess.call(['pip', 'install', 'nltk'])

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.isri import ISRIStemmer
import string

df = pd.read_csv('/home/combined_data.csv')
# print(df.head(10))

df = df[['Comment']]

# Print the first 10 rows of the modified DataFrame
# print(df.head(10))
# print(df.duplicated().sum())

# print("Before removing duplicates: ", df.shape)

# Remove duplicates
df = df.drop_duplicates()
df = df.dropna()

# Check the shape after removing duplicates
# print("After removing duplicates: ", df.shape)

df = df.dropna(subset=['Comment'])

# print("After removing nan: ", df.shape)

mentions = []
for Comment in df['Comment']:
    if Comment is not None:
        mentions.extend(re.findall(r'@\w+', Comment))

# Remove all mentions from the dataset
df['Comment'] = df['Comment'].apply(lambda Comment: re.sub(r'@\w+', '', Comment) if Comment is not None else Comment)
# print(mentions)
df.head(10)

def is_english(text):
    if text and re.match('^[A-Za-z0-9 .,!?\-\'"]*$', text):
        return None  # Return None for English text
    return text  # Keep the original text for non-English

df['Comment'] = df['Comment'].apply(is_english)


#remove English
english = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
          "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
for eng in english:
    df['Comment'] = df['Comment'].str.replace(eng, ' ')

# print(df.head(10))

# Regular expression pattern for identifying most URLs
url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Replace URLs with an empty string in the specific column
df['Comment'] = df['Comment'].str.replace(url_pattern, '', regex=True)
df.head(10)


#check emails

def check_emails_in_reviews(df):
    # Regular expression pattern for detecting email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # List to store rows where email addresses are found
    rows_with_emails = []

    # Iterate over each Comment in the DataFrame
    for index, Comment in df['Comment'].items():
        # Check if the Comment is a string and contains an email
        if isinstance(Comment, str) and re.search(email_pattern, Comment):
            rows_with_emails.append(index)

    return rows_with_emails

rows_with_emails = check_emails_in_reviews(df)
# print(rows_with_emails)

def check_links(dataframe):
    # Regular expression pattern for identifying a link
    link_pattern = r'https?://\S+A'
    rows_with_link= []

    # Function to apply to each comment to check for a link
    for index, Comment in df['Comment'].items():
      # Check if the Comment is a string and contains an email
      if isinstance(Comment, str) and re.search(link_pattern, Comment):
        rows_with_link.append(index)

    return rows_with_link

rows_with_link = check_links(df)
# print(rows_with_link)


# Regular expression pattern for identifying most URLs
url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Replace URLs with an empty string in the specific column
df['Comment'] = df['Comment'].str.replace(url_pattern, '', regex=True)


def normalize(sentence):

    sentence = re.sub("[إأآا]", "ا", sentence)
    sentence = re.sub("ى", "ي", sentence)
    sentence = re.sub("ؤ", "ء", sentence)
    sentence = re.sub("ئ", "ء", sentence)
    sentence = re.sub("ة", "ه", sentence)
    sentence = re.sub("گ", "ك", sentence)
    return sentence

def normalize_reviews(df, column_name):
    df[column_name ] = df[column_name].apply(lambda x: normalize(x) if isinstance(x, str) else x)
    return df


df = normalize_reviews(df, 'Comment')
df.head(10)

spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–", "؟","\"\"","\"",'""']
for char in spec_chars:
    df['Comment'] = df['Comment'].str.replace(char, ' ')

df.head(10)

# Remove punctuations
df['Comment'] = df['Comment'].astype(str)
df['Comment'] = df['Comment'].apply(lambda x: re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~ \"|#|$|%|&|\'|\*|\+|,|-|\.|\/|:||;|<|=|>|[|\\|]|^|_|`|{||}~"""), ' ', x))
df['Comment'] = df['Comment'].apply(lambda x: re.sub(r'([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', '', x))

pattern = r'(.)\1+'
df['Comment'] = df['Comment'].replace(pattern, r'\1', regex=True)
df.head(10)

#Remove arkam w stop words
def remove_numbers(text):
    return re.sub(r'\d+', '', str(text))


# Apply the remove_numbers function to the Comment column
df['Comment'] = df['Comment'].apply(remove_numbers)

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('arabic')

def remove_stop_words(text):
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)

# Apply the remove_stop_words function to the "Comment" column
df['Comment'] = df['Comment'].apply(remove_stop_words)

df = df.dropna()


def remove_duplicate_words(text):
    # Check for None values
    if text is None:
        return None

    # Split the text into words
    words = text.split()

    # Remove duplicates while preserving the order
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    # Reconstruct the sentence with unique words
    cleaned_text = ' '.join(unique_words)

    return cleaned_text

# Remove rows with 'None' values in the 'Comment' column
df = df[df['Comment'].notna()]

# Apply the function to the 'Comment' column in your DataFrame
df['Comment'] = df['Comment'].apply(remove_duplicate_words)
# print(df.head(10))


# Remove ExtraChar like "الللللللللللللللله" to "الله"
df['Comment'] = df['Comment'].apply(lambda x: x[0:2] + ''.join([x[i] for i in range(2, len(x)) if x[i]!=x[i-1] or x[i]!=x[i-2]]))
df.Comment=df.Comment.apply(lambda x:x.replace('؛',"", ))
df.head(10)

#replace emojis with words

emojis = {
    "🙂":" يبتسم ",
    "😂":" يضحك ",
    "💔":" قلب حزين ",
    "🙂":" يبتسم ",
    "❤️":" حب ",
    "❤":" حب ",
    "😍":" حب ",
    "😭":" يبكي ",
    "😢":" حزن ",
    "😔":" حزن ",
    "♥":" حب ",
    "💜":" حب ",
    "😅":" يضحك ",
    "🙁":" حزين ",
    "💕":" حب ",
    "💙":" حب ",
    "😞":" حزين ",
    "😊":" سعادة ",
    "👏":" يصفق ",
    "👌":" احسنت ",
    "😴":" ينام ",
    "😀":" يضحك ",
    "😌":" حزين ",
    "🌹":" وردة ",
    "🙈":" حب ",
    "😄":" يضحك ",
    "😐":" محايد ",
    "✌":" منتصر ",
    "✨":" نجمه ",
    "🤔":" تفكير ",
    "😏":" يستهزء ",
    "😒":" يستهزء ",
    "🙄":" ملل ",
    "😕":" عصبية ",
    "😃":" يضحك ",
    "🌸":" وردة ",
    "😓":" حزن ",
    "💞":" حب ",
    "💗":" حب ",
    "😑":" منزعج ",
    "💭":" تفكير ",
    "😎":" ثقة ",
    "💛":" حب ",
    "😩":" حزين ",
    "💪":" عضلات ",
    "👍":" موافق ",
    "🙏🏻":" رجاء طلب ",
    "😳":" مصدوم ",
    "👏🏼":" تصفيق ",
    "🎶":" موسيقي ",
    "🌚":" صمت ",
    "💚":" حب ",
    "🙏":" رجاء طلب ",
    "💘":" حب ",
    "🍃":" سلام ",
    "☺":" يضحك ",
    "🐸":" ضفدع ",
    "😶":" مصدوم ",
    "✌️":" مرح ",
    "✋🏻":" توقف ",
    "😉":" غمزة ",
    "🌷":" حب ",
    "🙃":" مبتسم ",
    "😫":" حزين ",
    "😨":" مصدوم ",
    "🎼 ":" موسيقي ",
    "🍁":" مرح ",
    "🍂":" مرح ",
    "💟":" حب ",
    "😪":" حزن ",
    "😆":" يضحك ",
    "😣":" استياء ",
    "☺️":" حب ",
    "😱":" كارثة ",
    "😁":" يضحك ",
    "😖":" استياء  ",
    "🏃🏼":" يجري ",
    "😡":" غضب ",
    "🚶":" يسير ",
    "🤕":" مرض ",
    "‼️":" تعجب ",
    "🕊":" طائر ",
    "👌🏻":" احسنت ",
    "❣":" حب ",
    "🙊":" مصدوم ",
    "💃":" سعادة مرح ",
    "💃🏼":" سعادة مرح ",
    "😜":" مرح ",
    "👊":" ضربة ",
    "😟":" استياء ",
    "💖":" حب ",
    "😥":" حزن ",
    "🎻":" موسيقي ",
    "✒":" يكتب ",
    "🚶🏻":" يسير ",
    "💎":" الماظ ",
    "😷":" وباء مرض ",
    "☝":" واحد ",
    "🚬":" تدخين ",
    "💐" : " ورد ",
    "🌞" : " شمس ",
    "👆" : " الاول ",
    "⚠️" :" تحذير ",
    "🤗" : " احتواء ",
    "✖️": " غلط ",
    "📍"  : " مكان ",
    "👸" : " ملكه ",
    "👑" : " تاج ",
    "✔️" : " صح ",
    "💌": " قلب ",
    "😲" : " مندهش ",
    "💦": " ماء ",
    "🚫" : " خطا ",
    "👏🏻" : " برافو ",
    "🏊" :" يسبح ",
    "👍🏻": " تمام ",
    "⭕️" :" دائره كبيره ",
    "🎷" : " ساكسفون ",
    "👋": " تلويح باليد ",
    "✌🏼": " علامه النصر ",
    "🌝":" مبتسم ",
    "➿"  : " عقده مزدوجه ",
    "💪🏼" : " قوي ",
    "📩":  " تواصل معي ",
    "☕️": " قهوه ",
    "😧" : " قلق و صدمة ",
    "🗨": " رسالة ",
    "❗️" :" تعجب ",
    "🙆🏻": " اشاره موافقه ",
    "👯" :" اخوات ",
    "©" :  " رمز ",
    "👵🏽" :" سيده عجوزه ",
    "🐣": " كتكوت ",
    "🙌": " تشجيع ",
    "🙇": " شخص ينحني ",
    "👐🏽":" ايدي مفتوحه ",
    "👌🏽": " بالظبط ",
    "⁉️" : " استنكار ",
    "⚽️": " كوره ",
    "🕶" :" حب ",
    "🎈" :" بالون ",
    "🎀":    " ورده ",
    "💵":  " فلوس ",
    "😋":  " جائع ",
    "😛":  " يغيظ ",
    "😠":  " غاضب ",
    "✍🏻":  " يكتب ",
    "🌾":  " ارز ",
    "👣":  " اثر قدمين ",
    "❌":" رفض ",
    "🍟":" طعام ",
    "👬":" صداقة ",
    "🐰":" ارنب ",
    "☂":" مطر ",
    "⚜":" مملكة فرنسا ",
    "🐑":" خروف ",
    "🗣":" صوت مرتفع ",
    "👌🏼":" احسنت ",
    "☘":" مرح ",
    "😮":" صدمة ",
    "😦":" قلق ",
    "⭕":" الحق ",
    "✏️":" قلم " ,
    "ℹ":" معلومات ",
    "🙍🏻":" رفض ",
    "⚪️":" نضارة نقاء ",
    "🐤":" حزن ",
    "💫":" مرح ",
    "💝":" حب ",
    "🍔":" طعام ",
    "❤︎":" حب ",
    "✈️":" سفر ",
    "🏃🏻‍♀️":" يسير ",
    "🍳":" ذكر ",
    "🎤":" مايك غناء ",
    "🎾":" كره ",
    "🐔":" دجاجة ",
    "🙋":" سؤال ",
    "📮":" بحر ",
    "💉":" دواء ",
    "🙏🏼":" رجاء طلب ",
    "💂🏿 ":" حارس ",
    "🎬":" سينما ",
    "♦️":" مرح ",
    "💡":" قكرة ",
    "‼":" تعجب ",
    "👼":" طفل ",
    "🔑":" مفتاح ",
    "♥️":" حب ",
    "🕋":" كعبة ",
    "🐓":" دجاجة ",
    "💩":" معترض ",
    "👽":" فضائي ",
    "☔️":" مطر ",
    "🍷":" عصير ",
    "🌟":" نجمة ",
    "☁️":" سحب ",
    "👃":" معترض ",
    "🌺":" مرح ",
    "🔪":" سكينة ",
    "♨":" سخونية ",
    "👊🏼":" ضرب ",
    "✏":" قلم ",
    "🚶🏾‍♀️":" يسير ",
    "👊":" ضربة ",
    "◾️":" وقف ",
    "😚":" حب ",
    "🔸":" مرح ",
    "👎🏻":" لا يعجبني ",
    "👊🏽":" ضربة ",
    "😙":" حب ",
    "🎥":" تصوير ",
    "👉":" جذب انتباه ",
    "👏🏽":" يصفق ",
    "💪🏻":" عضلات ",
    "🏴":" اسود ",
    "🔥":" حريق ",
    "😬":" عدم الراحة ",
    "👊🏿":" يضرب ",
    "🌿":" ورقه شجره ",
    "✋🏼":" كف ايد ",
    "👐":" ايدي مفتوحه ",
    "☠️":" وجه مرعب ",
    "🎉":" يهنئ ",
    "🔕" :" صامت ",
    "😿":" وجه حزين ",
    "☹️":" وجه يائس ",
    "😘" :" حب ",
    "😰" :" خوف و حزن ",
    "🌼":" ورده ",
    "💋":  " بوسه ",
    "👇":" لاسفل  ",
    "❣️":" حب ",
    "🎧":" سماعات ",
    "📝":" يكتب ",
    "😇":" دايخ ",
    "😈":" رعب ",
    "🏃":" يجري ",
    "✌🏻":" علامه النصر ",
    "🔫":" يضرب ",

    "❗️":" تعجب ",
    "👎":" غير موافق ",
    "🔐":" قفل ",
    "👈":" لليمين ",
    "™":" رمز ",
    "🚶🏽":" يتمشي ",
    "😯":" متفاجأ ",
    "✊":" يد مغلقه ",
    "😻":" اعجاب ",
    "🙉" :" قرد ",
    "👧":" طفله صغيره ",
    "🔴":" دائره حمراء ",
    "💪🏽":" قوه ",
    "💤":" ينام ",
    "👀":" ينظر ",
    "✍🏻":" يكتب ",
    "❄️":" تلج ",
    "💀":" رعب ",
    "😤":" وجه عابس ",
    "🖋":" قلم ",
    "🎩":" كاب ",
    "☕️":" قهوه ",
    "😹":" ضحك ",
    "💓":" حب  ",
    "☄️ ":" نار ",
    "👻":" رعب ",
    "❎":" خطء ",
    "🤮":" حزن ",
    '🏻':" احمر ",
    "💧":"دمعة",
    "🌳":"شجره",
    "🖤" : "قلب اسود",
    "🌂" :"شمسيه",
    "🥺⃢" : " كيوت",
    "❄" : " تلج",
    "🎃" : "يقطينة",
    "🤪": "مجنون",
    "✅ ": "علامة صح",
    "👰" : "عروس",
    "😗" : "وجه يقبل",
    "🎁" : "هدية" ,
    "🤝" : "مصافحة",
    "💯" : "مئة في المئة",
    "🤯" :"ذهول" ,
    "🦛" : "فرس النهر",
    "🦄 ": "حصان الوحيد القرن",
    "🦓 ":"حمار وحشي",
    "🐴" :"حصان",
    "🥰 ":"وجه بعيون القلب",
    "👅" : "لسان",
    "👄" : "شفاه",
    "🤴" : "أمير",
    "🚮 ": "سلة مهملات",
    "🤩 ":"وجه بعيون نجمية",
    "🛑 ": "إشارة توقف",
    "✋ ":"يد مرفوعة",
}

emoticons_to_emoji = {
    ":)" : "🙂",
    ":(" : "🙁",
    "xD" : "😆",
    ":=(": "😭",
    ":'(": "😢",
    ":'‑(": "😢",
    "XD" : "😂",
    ":D" : "🙂",
    "♬" : "موسيقي",
    "♡" : "❤",
    "☻"  : "🙂",
}
def replace_emojis_emoticons(text):
    # Check if text is None
    if text is None:
        return text  # or return '' if you prefer to replace None with an empty string

    # Replace emoticons with emojis
    for emoticon, emoji in emoticons_to_emoji.items():
        text = text.replace(emoticon, emoji)

    # Replace emojis with words
    for emoji, word in emojis.items():
        text = text.replace(emoji, word)

    return text

df['Comment'] = df['Comment'].apply(replace_emojis_emoticons)
df.head(5)
df = df.dropna()
df = df.replace('', pd.NA)
df = df.dropna()
# print(df.head(10))
df.to_csv('comments.csv', index=False, encoding='utf-8-sig')
print("*******************************************************")
print("!!!!!!!!!!!!!! Done!!!!!!!!!!!!!!!!!")
print("*******************************************************")

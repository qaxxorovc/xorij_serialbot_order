import sqlite3 as sq
import asyncio
from datetime import datetime
import random
import os
import pandas as pd

async def connect_db():
    conn = sq.connect('database.db')
    cur = conn.cursor()
    return conn, cur



async def create_admins_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Admins 
        (
            adminid INTEGER NOT NULL
        )        
    """)
    conn.commit()
    conn.close()

async def getinfo():
    # Foydalanuvchilarni va kanallarni olish
    conn, cur = await connect_db()
    
    # Foydalanuvchilar sonini olish
    cur.execute("SELECT COUNT(*) FROM Users")
    users_count = cur.fetchone()[0]
    
    # Majburiy obuna kanallari sonini olish
    cur.execute("SELECT COUNT(*) FROM Channels")
    channels_count = cur.fetchone()[0]
    
    conn.close()

    # Tayyor matnni yaratish
    info_text = f"""
    📊 Bot ma'lumotlari:
    
    👤 Foydalanuvchilar soni: {users_count}
    📢 Majburiy obuna kanallari soni: {channels_count}
    """
    
    return info_text



async def get_admins_ids():
    conn, cur = await connect_db()
    cur.execute("SELECT adminid FROM Admins")
    admins = cur.fetchall()  # barcha adminlarni olish
    conn.close()

    return [admin[0] for admin in admins]  # faqat admin ID'larini ro'yxatga olish


async def fake_link():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fake_link 
        (
            link_id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_title,
            link
        )        
    """)
    conn.commit()
    conn.close()

async def add_link(title: str, link: str):
    conn, cur = await connect_db()
    cur.execute("INSERT INTO fake_link (link_title, link) VALUES (?, ?)", (title, link))
    conn.commit()
    conn.close()

# Barcha linklarni olish
async def get_all_links():
    conn, cur = await connect_db()
    cur.execute("SELECT * FROM fake_link")
    rows = cur.fetchall()
    conn.close()
    return rows

# ID bo‘yicha linkni o‘chirish
async def remove_link_by_id(link_id: int):
    conn, cur = await connect_db()
    cur.execute("DELETE FROM fake_link WHERE link_id = ?", (link_id,))
    conn.commit()
    conn.close()

async def movie_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies 
        (
            MovieID,
            MovieCaption,
            MovieCode
        )        
    """)
    conn.commit()
    conn.close()


async def Serial_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Serials 
        (
            SerialID,
            SerialCaption,
            SerialNumber INTEGER,
            SerialPart INTEGER
        )        
    """)
    conn.commit()
    conn.close()



async def get_serial(serialnumber, serialpart):
    """Serialni olish uchun funksiyaning asynxron varianti"""
    conn, cur = await connect_db()
    try:
        cur.execute("""
            SELECT SerialID, SerialCaption
            FROM Serials 
            WHERE SerialNumber = ? AND SerialPart = ?
        """, (serialnumber, serialpart))
        serial = cur.fetchone()
        
        if serial:
            serial_id, serial_caption = serial
            return serial_id, serial_caption
        else:
            return None
    except Exception as e:
        print(f"Xato: {e}")
        return None
    finally:
        conn.close()




async def add_serial_to_db(serial_id: int, caption: str, serial_number: int, serial_part: int):
    """Serial ma'lumotlarini bazaga qo'shish"""
    conn, cur = await connect_db()
    cur.execute("""
        INSERT INTO Serials (SerialID, SerialCaption, SerialNumber, SerialPart) 
        VALUES (?, ?, ?, ?)
    """, (serial_id, caption, serial_number, serial_part))
    conn.commit()
    conn.close()



async def count_unique_serials():
    conn, cur = await connect_db()
    cur.execute("""
        SELECT COUNT(DISTINCT SerialNumber) FROM Serials
    """)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0



async def get_serial(serial_number, serial_part):
    conn, cur = await connect_db()
    cur.execute("""
        SELECT SerialID, SerialCaption FROM Serials 
        WHERE SerialNumber = ? AND SerialPart = ?
    """, (serial_number, serial_part))
    result = cur.fetchone()
    conn.close()
    return result if result else (None, None)



async def add_serial(serial_id: str, caption: str, part: int):
    conn, cur = await connect_db()
    cur.execute("""
        INSERT INTO Serials (SerialID, SerialCaption, SerialPart)
        VALUES (?, ?, ?)
    """, (serial_id, caption, part))
    conn.commit()
    conn.close()



async def channels_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Channels 
        (
            ChannelName VARCHAR(255),
            Channelusername VARCHAR(255) NOT NULL,
            Channelid VARCHAR(255) NOT NULL
        )        
    """)
    
    conn.commit()
    conn.close()      


async def users_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users 
        (
            name VARCHAR(255),
            username VARCHAR(255),
            userid VARCHAR(255) NOT NULL
        )        
    """)
    
    conn.commit()
    conn.close()  


async def adduser(name, username, userid):
    conn, cur = await connect_db()

    cur.execute("SELECT COUNT(*) FROM Users WHERE userid = ?", (userid,))
    result = cur.fetchone()

    if result[0] == 0:
        cur.execute("""
            INSERT INTO Users (name, username, userid)
            VALUES (?, ?, ?)
        """, (name, username, userid))
        conn.commit()
        conn.close()
    else:
        conn.close()


async def find_channel_usernames():
    conn, cur = await connect_db()
    cur.execute("SELECT ChannelName, Channelusername FROM Channels")
    usernames = cur.fetchall()
    conn.close()

    if usernames:
        return [f"{channel[0]} - {channel[1]}" for channel in usernames]
    return []

async def find_channel_ids():
    conn, cur = await connect_db()
    cur.execute("SELECT Channelid FROM Channels")
    channel_ids = cur.fetchall()
    
    return [channel_id[0] for channel_id in channel_ids]
async def addchannelcheck(ChannelName, Channelusername, Channelid):
    
    conn, cur = await connect_db()
    cur.execute("""
            INSERT INTO Channels VALUES (?,?,?)""",(ChannelName,Channelusername,Channelid))
    conn.commit()
    conn.close()

async def deletechannelcheck(channelid):
    conn, cur = await connect_db()
    cur.execute("DELETE FROM Channels WHERE Channelid = ?", (channelid,))
    
    conn.commit()
    
    conn.close()

async def generate_unique_movie_code():
    conn, cur = await connect_db()
    
    while True:
        random_code = random.randint(10000, 99999)
        
        cur.execute("SELECT 1 FROM Movies WHERE MovieCode = ?", (random_code,))
        result = cur.fetchone()
        
        if not result: 
            conn.close()
            return random_code    
        
async def addmoviebot(MovieID, MovieCaption, MovieCode):
    conn, cur = await connect_db()
    cur.execute("""
            INSERT INTO Movies (MovieID, MovieCaption, MovieCode)
            VALUES (?, ?, ?)
        """, (MovieID, MovieCaption, MovieCode))
    conn.commit()
    conn.close()

async def deletemoviebot(MovieCode):
    conn, cur = await connect_db()
    cur.execute("""DELETE FROM Movies WHERE MovieCode = ?""", (MovieCode,))
    conn.commit()
    conn.close()

async def useridlist():
    conn, cur = await connect_db()

    cur.execute("SELECT userid FROM Users")
    userids = cur.fetchall()

    userids_list = [userid[0] for userid in userids]

    conn.close()
    return userids_list 

async def save_each_table_to_excel():
    conn, cur = await connect_db()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    folder = "exels"
    os.makedirs(folder, exist_ok=True)

    saved_files = []

    for table in tables:
        table_name = table[0]
        cur.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=columns)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = os.path.join(folder, f"{current_time}_{table_name}.xlsx")

        with pd.ExcelWriter(file_name) as writer:
            df.to_excel(writer, sheet_name=table_name)

        saved_files.append(file_name)

    conn.close()
    print(f"Saved tables: {', '.join(saved_files)}")
    return saved_files

async def findmovie(MovieCode):
    conn, cur = await connect_db()
    cur.execute("SELECT MovieID, MovieCaption FROM Movies WHERE MovieCode = ?", (MovieCode,))
    movie = cur.fetchone()
    conn.close()
    
    if movie:
        return [movie[0], movie[1]]
    else:
        return None  
    

async def get_admin_ids():
    conn, cur = await connect_db()
    cur.execute("SELECT adminid FROM Admins")
    admin_ids = cur.fetchall()

    return admin_ids    

async def add_admin(admin_id):
    conn, cur = await connect_db()
    try:
        cur.execute("SELECT * FROM Admins WHERE adminid = ?", (admin_id,))
        if cur.fetchone():
            print(f"⚠️ Admin {admin_id} allaqachon ro'yxatda mavjud.")
            return False
        
        cur.execute("INSERT INTO Admins (adminid) VALUES (?)", (admin_id,))
        conn.commit()
        print(f"✅ Admin {admin_id} muvaffaqiyatli qo'shildi!")
        return True
    except Exception as e:
        print(f"❌ Admin qo'shishda xato: {e}")
        return False
    finally:
        conn.close()

async def remove_admin(admin_id):
    conn, cur = await connect_db()
    cur.execute("DELETE FROM Admins WHERE adminid = ?", (admin_id,))
    conn.commit()
    conn.close()        

import sqlite3

def cacheFile(filename, data):
    filename = filename.replace('.', '/.')
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data BLOB)')
    c.execute('SELECT filename FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    if len(list(c)) != 0:
        c.execute('UPDATE cachedfiles_string SET data=\'?\' WHERE filename=\'?\'', (data, filename))
    else:
        c.execute('INSERT INTO cachedfiles_string VALUES (?,?)', ("'" + filename + "'", "'" + data + "'"))
    conn.commit()
    conn.close()

def getCachedFile(filename):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data BLOB)')
    c.execute('SELECT data FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    try:
        row = list(c)[0]
    except:
        row = [""]
    conn.commit()
    conn.close()
    return row[0]

def cacheFileS(filename, data):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data TEXT)')
    c.execute('SELECT filename FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    if len(list(c)) != 0:
        c.execute('UPDATE cachedfiles_string SET data=? WHERE filename=?', (data, filename))
    else:
        c.execute('INSERT INTO cachedfiles_string VALUES (?,?)', (filename, data))
    conn.commit()
    conn.close()

def getCachedFileS(filename):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data TEXT)')
    c.execute('SELECT data FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    try:
        row = list(c)[0]
    except:
        print("[DB    ] Could not find file {} in string file cache.".format(filename))
        row = [""]
    conn.commit()
    conn.close()
    return row[0]

#====================================
# Prefix Stuff
#====================================

def setPrefix(serverid, prefix):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS prefixes (serverid INTEGER, prefix TEXT)')
    c.execute('SELECT prefix FROM prefixes WHERE serverid=' + serverid)
    if len(list(c)) != 0:
        c.execute('UPDATE prefixes SET prefix=? WHERE serverid=?', (prefix, serverid))
    else:
        c.execute('INSERT INTO prefixes VALUES (?,?)', (serverid, prefix))
    conn.commit()
    conn.close()

def getPrefix(serverid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS prefixes (serverid INTEGER, prefix TEXT)')
    c.execute('SELECT prefix FROM prefixes WHERE serverid=' + serverid)
    try:
        row = list(c)[0]
    except:
        row = ["!"]
    conn.commit()
    conn.close()
    return row[0]

#====================================
# Logging Stuff
#====================================

def logUserMessage(message):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_messages (userid INTEGER, username TEXT, message TEXT, serverid INTEGER, servername TEXT)')
    c.execute('INSERT INTO user_messages VALUES (?,?,?,?,?)',
              (message.author.id, message.author.name, message.content, message.server.id, message.server.name))
    conn.commit()
    conn.close()

#====================================
# Server Owner Stuffs
#====================================

def isOwner(uid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    cur = c.execute('SELECT userid FROM owners')
    for row in list(cur):
        if str(row[0]) == str(uid):
            conn.commit()
            conn.close()
            return True
    conn.commit()
    conn.close()
    return False

def getOwners():
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    cur = c.execute('SELECT userid FROM owners')
    owners = []
    for row in list(cur):
        owners.append(row[0])
    conn.commit()
    conn.close()
    return owners

def addOwner(uid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    c.execute('INSERT INTO owners VALUES (' + uid + ')')
    conn.commit()
    conn.close()
#    Copyright 2017 Starbot Discord Project
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Manage message log size.

from api import database
from api.database.table import Table, TableTypes


def message_count_set(id_server, count):
    '''Set the current message count.'''
    database.init()
    table_message_count = Table('messagecounts', TableTypes.pGlobal)
    try:
        entry_message_count = Table.search(table_message_count, 'serverid', '{}'.format(id_server))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_message_count = None

    if entry_message_count:
        entry_message_count.edit(dict(serverid=id_server, count=count))
    else:
        Table.insert(table_message_count, dict(serverid=id_server, count=count))


def message_count_get(id_server):
    '''Get the current message count.'''
    database.init()
    table_message_count = Table('messagecounts', TableTypes.pGlobal)
    try:
        msg_count = Table.search(table_message_count, 'serverid', '{}'.format(id_server)).data[1]
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        msg_count = '0'

    return int(msg_count)

# Log messages to database.

def message_log(msg):
    '''Log a message into the database.'''
    database.init()
    table_log = Table('user_messages', TableTypes.pGlobal)
    Table.insert(table_log, dict(userid=msg.author.id, username=msg.author.name, message=msg.content,
                                 serverid=msg.server.id, servername=msg.server.name))

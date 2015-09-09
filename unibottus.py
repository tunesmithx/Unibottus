#!/usr/bin/env python
# coding: utf-8

from jabberbot import JabberBot, botcmd

import logging
logging.basicConfig()

username = 'tunesmith_x'
domain = 'goonfleet.com'
fulllogin = username + '@' + domain
nickname = 'Tutroid'
chatroom = 'big_bees@conference.goonfleet.com' 
server = 'brobuck.goonfleet.com'

passwordFile = open('password.txt', 'r')
password = passwordFile.read()
passwordFile.close()

importantMembers = []

class Unibottus(JabberBot):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        
        super(Unibottus, self).__init__(*args, **kwargs)
        
    def callback_presence(self, conn, presence):
        toJid, fromJid, presenceType, affiliation = presence.getTo(), presence.getFrom(), presence.getType(), presence.getAffiliation()
        
        if self.jid.bareMatch(toJid) and fromJid is not None and fromJid.bareMatch(chatroom):
            # Should be a MUC presence message if we get here.
            nick = fromJid.getResource()
            
            # We care about nicknames, not JIDs, since nicknames cause attention.
            if presenceType == 'unavailable': # Person left room
                importantMembers.remove(nick)
            elif affiliation == 'owner': # Owner (flag) entered (says 'admin' for stars)
                importantMembers.append(nick)
        
        return super(Unibottus, self).callback_presence(conn, presence)
    
    @botcmd
    def ayy(self, mess, args):
        """Don't do this"""
        self.send_simple_reply(mess, 'lmao')
        
    @botcmd
    def ping(self, mess, args):
        """Gets you some attention from the bosses"""
        reply = ' '.join(importantMembers)
        
        self.send_simple_reply(mess, reply)

if __name__ == '__main__':
    mucbot = Unibottus(fulllogin, password, debug=True, acceptownmsgs=True, server=server, command_prefix='!')
    mucbot.connect()
    mucbot.muc_join_room(chatroom, nickname)
    mucbot.serve_forever()
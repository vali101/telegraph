from .client import Client
from .message import Message
from .config import path

import time
import shelve
from pathlib import Path
import logging
import pandas as pd
import numpy as np
import ast

import telethon.sync
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel as Telethon_Channel


class Channel:
    def __init__(self, username, num_messages, ranker):
        """
        The Channel class download num_messages from the given channel and saves them in a csv file. If the messages
        have been downloaded previously it loads them from disk.

        :param username: name of channel
        :type username: str
        :param num_messages: amount of messages that will be scraped (None --> all)
        :type num_messages: int
        :param ranker: Ranker object
        :type ranker: Ranker
        """
        self.client = Client.getClient()
        self.username = username
        self.num_messages = num_messages
        self.comment_channel = None

        self.participants_count, chats = self.__get_channel_meta()
        logging.debug("participants: %s, chats: %s" % (self.participants_count, chats))

        for chat in chats:
            if chat.username is not None and chat.username.lower() != username:
                self.comment_channel = chat.username.lower()

        if self.comment_channel is not None:
            ranker.set_priority(self.comment_channel.lower())

        self.messages = self.__getMessagesNew(username)
        self.__write_csv()

    def __write_csv(self):
        df = pd.DataFrame(self.messages)
        df.to_csv('%s/csv_data/%s.csv' % (path, self.username), index=False)

    # Load messages if already scraped
    def __getMessagesNew(self, username):
        channel_path = '%s/csv_data/%s.csv' % (path, self.username)
        channel_file = Path(channel_path)
        if channel_file.is_file():
            messages_formatted = pd.read_csv(channel_path).replace({np.nan: None}).to_dict(orient="records")
            # Interpret strings of lists as lists
            for index, message in enumerate(messages_formatted):
                if messages_formatted[index]["mentions"] is not None:
                    messages_formatted[index]["mentions"] = ast.literal_eval(str(message["mentions"]))
                if messages_formatted[index]['mentioned_in_link'] is not None:
                    messages_formatted[index]['mentioned_in_link'] = ast.literal_eval(str(message["mentioned_in_link"]))

            # Get messages newer
            last_message_id = max(x["id"] for x in messages_formatted)
            messages_formatted_new = self.__get_messages_formatted(username, min_id=last_message_id)
            logging.info("List was updated with %s messages" % len(messages_formatted_new))
            messages_formatted.extend(messages_formatted_new)
            time.sleep(1)

        else:
            # print("Loaded messages online")
            messages_formatted = self.__get_messages_formatted(username)
            time.sleep(10)
        return messages_formatted

    def __get_messages_formatted(self, username, min_id=0):
        try:
            messages = list(self.client.get_messages(self.username, limit=self.num_messages, min_id=min_id))
        except telethon.errors.FloodWaitError as e:
            logging.info("FloodWaitError: Sleep for " + str(e.seconds))
            if e.seconds < 2000:
                time.sleep(e.seconds + 50)
            else:
                time.sleep(e.seconds)
            # When block gone retry
            return self.__get_messages_formatted()

        return [Message(message, self.participants_count).__dict__ for message in messages]

    # "get_entity" as well as "GetFullChannelRequest" are very expensive API queries if they are used frequently
    # you can get blocked therefore this function tries to cache them locally
    def __get_channel_meta(self):
        with shelve.open('channel_meta') as channel_meta:
            if self.username in channel_meta.keys():
                return channel_meta[self.username][0], channel_meta[self.username][1]
        try:
            channel_entity = self.client.get_entity(self.username)
        except telethon.errors.FloodWaitError as e:
            logging.info("FloodWaitError: Sleep for " + str(e.seconds))
            if e.seconds < 2000:
                time.sleep(e.seconds + 200)
            else:
                time.sleep(e.seconds)
            # When block gone retry
            return self.__get_channel_meta(self.client)

        if not isinstance(channel_entity, Telethon_Channel):
            raise TypeError("Username ist not a channel")

        full_channel_entity = self.client(GetFullChannelRequest(channel=channel_entity))
        participants_count = full_channel_entity.full_chat.participants_count

        chats = full_channel_entity.chats

        with shelve.open('channel_meta') as channel_meta:
            channel_meta[self.username] = (participants_count, chats)

        return participants_count, chats

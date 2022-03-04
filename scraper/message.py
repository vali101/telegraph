from .utils import find_mentions, find_links, extract_channels_from_links
from telethon.tl.types import MessageEntityTextUrl
import re


class Message:

    def __init__(self, message, participants_count):
        """
        This class maps the telethon entity message (telethon.tl.custom.message.Message) in a custom data object
        which will be processed into a row in a csv later on.

        :param message:
        :type message:
        :param participants_count:
        :type participants_count:
        """
        self.channel_name = message.chat.username.lower()
        self.channel_id = message.chat.id
        self.title = message.chat.title
        self.datetime = str(message.date)
        self.participants_count = participants_count
        self.raw_text = "" if message.raw_text is None else message.raw_text.replace("\'", "\"")
        self.views = message.views
        self.id = message.id
        self.sender = message.sender_id
        self.post_author = message.post_author
        self.is_reply = message.is_reply

        self.links = []

        self.reply_to_message_id = None
        self.group_type = None
        self.member_count = None
        self.forward_from = None
        self.forward_from_channel_id = None
        self.forward_from_post_id = None
        self.mentions = None
        self.sender = None
        self.sender_id = None

        try:
            self.reply_to_message_id = message.reply_to_msg_id
        except AttributeError:
            pass

        try:
            self.member_count = message.chat.participants_count
        except AttributeError:
            pass

        try:
            self.sender = message.sender.username
            self.sender_id = message.sender.id
        except AttributeError:
            pass

        try:
            self.forward_from = None if message.forward.chat.username is None else message.forward.chat.username.lower()
            self.forward_from_channel_id = message.forward.channel_id
            self.forward_from_post_id = message.forward.channel_post
        except AttributeError:
            pass

        if message.is_group is True:
            self.group_type = "group"
        else:
            self.group_type = "channel"

        links_message_entity = [] if message.entities is None else [entity.url for entity in message.entities if type(
            entity) == MessageEntityTextUrl]

        if self.raw_text is not None:
            self.mentions = find_mentions(self.raw_text)
            self.links.extend(find_links(self.raw_text))

        self.links.extend(links_message_entity)
        self.mentioned_in_link = extract_channels_from_links(self.links)

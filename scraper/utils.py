import re


# Extracte mentions from raw text like "@word"
def find_mentions(raw_text):
    mentions = re.findall('@(\w+)', raw_text)
    return None if not mentions else [mention.lower() for mention in mentions]


# Extract Links from message
def find_links(raw_text):
    return None if raw_text is None else re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),'
                                                    ']|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_text)


def extract_channels_from_links(links):
    usernames = []
    for link in links:
        match = re.match('https:\/\/t.me\/s\/(\w+)', link)
        if match:
            usernames.append(match.group(1))
    return usernames


def extract_channels_from_links_website(links):
    usernames = []
    for link in links:
        match = re.match('https:\/\/t.me\/(\w+)', link)
        if match:
            usernames.append(match.group(1))
    return usernames

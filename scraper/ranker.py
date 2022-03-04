from .config import path

import logging
import shelve
import json
from datetime import datetime


class Ranker:
    def __init__(self, step_size):
        """
        Creates the ranker object which determines which channels need to be scraped next. If the scraper was
        executed before the old ranking is loaded.

        :param step_size: Numbers of channels per iteration
        :type step_size: int
        :rtype: object
        """
        self.step_size = step_size
        self.start_time = str(datetime.now().strftime("%d-%b-%Y (%H-%M-%S.%f)"))
        with shelve.open('cache') as cache:
            # Init cache dicts if not existing
            if not {'scraped', 'ranking', 'channel_queue', 'iteration'}.issubset(set(list(cache.keys()))):
                self.iteration = 0
                self.ranking = {}
                self.channel_queue = {}
                self.scraped = {}
                self.removed_from_ranking = []
                self.priority_channels = []
            else:
                self.iteration = cache["iteration"]
                self.ranking = cache["ranking"]
                self.scraped = cache["scraped"]
                self.channel_queue = cache["channel_queue"]
                self.removed_from_ranking = cache["removed_from_ranking"]
                self.priority_channels = cache["priority_channels"]

    def get_next_candidate(self):
        """
        Returns the next Candidate that needs to be scraped.

        :return: Candidate (channel) name
        :rtype: str
        """
        if len(self.channel_queue) == 0:
            self.__fill_queue()
            self.iteration += 1
        return max(self.channel_queue, key=self.channel_queue.get)

    def set_candidate_scraped(self, channel_name):
        """
        Mark a Channel as scraped for Consistency when a channel is fully persisted

        :param channel_name: name of a channel (lowercase)
        :type channel_name: str
        """
        if self.iteration not in list(self.scraped.keys()):
            self.scraped[self.iteration] = {}
        try:
            self.scraped[self.iteration][channel_name] = self.channel_queue[channel_name]
        except KeyError as e:
            logging.info("Error: " + str(e))
            logging.info(self.channel_queue)

        self.__write_iterations()

    def updateRanking(self, channel, curr_channel):
        """
        Gets a channel object and looks for mentions, forwards and telegram links to update ranking.

        :param channel: Name of the channel which should be evaluated.
        :type channel: str
        :param curr_channel: Name of channel that is currently scraped.
        :type curr_channel: str
        """
        for message in channel.messages:
            # Update ranking via forwards
            forward_from = message["forward_from"]
            if forward_from is not None:
                self.__update_ranking_per_mention(curr_channel, forward_from)

            # Update ranking vie mentions
            mentions = []
            if message["mentions"] is not None:
                mentions = message["mentions"]

            for mention in mentions:
                self.__update_ranking_per_mention(curr_channel, mention)

            # Update ranking via Links
            for mention_link in message['mentioned_in_link']:
                self.__update_ranking_per_mention(curr_channel, mention_link)

    def set_seed_to_queue(self, channels):
        """
        In the beginning all the seed channels need to be added to the ranker.

        :param channels: List of channels which should be evaluated first.
        :type channels: listOfObjects: [str]
        """
        for channel in channels:
            channel_lower = channel.lower()
            self.channel_queue[channel_lower] = -1
            self.removed_from_ranking.append(channel_lower)

    def get_iteration(self):
        """
        Return the current iteration.

        :return: iterations
        :rtype: int
        """
        return self.iteration

    def set_priority(self, channel_name):
        """
        Set high priority for supergroups which belong to channels for comments

        :param channel_name: Channel with priority
        :type channel_name: str
        """
        if channel_name not in self.removed_from_ranking:
            self.priority_channels.append(channel_name)

    def drop_channel(self, channel_name):
        """
        Delete channel from queue after transaction is done.

        :param channel_name: Channel to be dropped
        :type channel_name: str
        """

        self.channel_queue.pop(channel_name, None)
        self.removed_from_ranking.append(channel_name)
        self.__cache_ranking()

    def __write_iterations(self):
        with open('%s/iterations/%s.json' % (path, self.start_time), 'w',
                  encoding='utf8') as outfile:
            json.dump(self.scraped, outfile, ensure_ascii=False)

    def __cache_ranking(self):
        with shelve.open('cache') as cache:
            cache["ranking"] = self.ranking
            cache["channel_queue"] = self.channel_queue
            cache["scraped"] = self.scraped
            cache["iteration"] = self.iteration
            cache["removed_from_ranking"] = self.removed_from_ranking
            cache["priority_channels"] = self.priority_channels

    def __fill_queue(self):
        for i in range(self.step_size):
            if self.priority_channels:
                candidate = self.priority_channels.pop()
                ranking_queue = 1000000
            else:
                # Calcualate count aggregation to easier find max values.
                ranking_evaluated = {k: {"count": v["count"], "unique_channels_count": len(v["unique_channels"])}
                                     for (k, v) in self.ranking.items()}
                # Get all candidates with max unique channels mentions.
                candidate_with_best_ranking = max(ranking_evaluated, key=lambda v: ranking_evaluated[v][
                    "unique_channels_count"])
                ranking_of_best_candidate = ranking_evaluated[candidate_with_best_ranking]["unique_channels_count"]
                unique_channels_candidates = {k: v for k, v in ranking_evaluated.items() if
                                              v["unique_channels_count"] ==
                                              ranking_of_best_candidate}
                # Within these candidate get the one with the most absolute mentions first.
                candidate = max(unique_channels_candidates, key=lambda v: unique_channels_candidates[v]["count"])

                logging.debug(f'best ranking unique: {ranking_of_best_candidate}, candidate: {candidate}')

                ranking_queue = ranking_evaluated[candidate_with_best_ranking]["count"]

            self.channel_queue[candidate] = ranking_queue
            # Remove Candidate from Ranking
            self.ranking.pop(candidate, None)
            # Add to done list
            self.removed_from_ranking.append(candidate)

    def __update_ranking_per_mention(self, curr_channel, mention):
        curr_channel = curr_channel.lower()
        mention = mention.lower()
        if mention not in self.removed_from_ranking and mention != curr_channel:
            if mention in self.ranking:
                self.ranking[mention]["count"] += 1
                if curr_channel not in self.ranking[mention]["unique_channels"]:
                    self.ranking[mention]["unique_channels"].add(curr_channel)
            else:
                self.ranking[mention] = {}
                self.ranking[mention]["count"] = 0
                self.ranking[mention]["unique_channels"] = {curr_channel}

                logging.debug(f'ranking {mention}: ' + str(self.ranking[mention]["unique_channels"]))

from .ranker import Ranker
from .channel import Channel
from .config import path

import logging
from telethon.errors.rpcerrorlist import ChannelPrivateError
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError, UsernameInvalidError


class Scraper:
    def __init__(self, num_messages, step_size, maximum_iterations):
        """
        The Scraper finds channels from a given list of seed channels, via discriminative snowball sampling.

        :param num_messages: How many messages should be scraped.
        :type num_messages: int
        :param step_size: How big should each iteration be.
        :type step_size: int
        """
        self.ranker = Ranker(step_size)
        self.maximum_iterations = maximum_iterations
        self.num_messages = num_messages
        self.step_size = step_size
        self.iteration = 0

    def scrape(self, seed_channels):
        """
        Starts the scraper with a list of seed channels.

        :param seed_channels: List of seed channels to start sampling
        :type seed_channels: listOfObjects: [str]
        """
        if self.ranker.get_iteration() == 0:
            self.ranker.set_seed_to_queue(seed_channels)

        # Scrape as long as max iterations are not reached
        while True:
            if self.ranker.get_iteration() > self.maximum_iterations:
                print("Maximum Iterations reached")
                break
            channel_name = self.ranker.get_next_candidate()
            self.__scrape_channel(channel_name)

    def __scrape_channel(self, channel_name):
        """
        Scrapes a single channel

        :param channel_name: Name of the channel
        :type channel_name: str
        """
        channel_name = channel_name.lower()
        logging.info('Scraping messages from: %s' % channel_name)
        try:
            channel = Channel(channel_name, self.num_messages, self.ranker)
            self.ranker.updateRanking(channel, channel_name)
            self.ranker.set_candidate_scraped(channel_name)
        except TypeError as e:
            logging.info("TypeError, err msg: %s" % (str(e)))
        except ChannelPrivateError as e:
            logging.info("ChannelPrivateError: err msg: %s" % (str(e)))
        except ValueError as e:
            logging.info("ValueError: err msg: %s" % (str(e)))
        except UsernameNotOccupiedError as e:
            logging.info("UsernameNotOccupiedError:  err msg: %s" % (str(e)))
        except UsernameInvalidError as e:
            logging.info("UsernameInvalidError: err msg: %s" % (str(e)))
        finally:
            self.ranker.drop_channel(channel_name)

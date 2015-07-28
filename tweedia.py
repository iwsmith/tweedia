#!/usr/bin/env python
from __future__ import print_function
import tweepy
import os
import time

def post_photo(api, status, photo_path):
    return api.update_with_media(photo_path, status)

def poll_dir(directory, action, sleep_duration=5, filter_fn = None):
    #Existing files at startup should be ignored
    cache = set(os.listdir(directory))
    while True:
        new_files = filter(lambda x: x not in cache, os.listdir(directory))
        if filter_fn:
            new_files = filter(filter_fn, new_files)
        for f in new_files:
            fpath = os.path.join(directory, f)
            action(fpath)
            cache.add(f)
    time.sleep(sleep_duration)

if __name__ == "__main__":
    import argparse
    import functools
    import ConfigParser
    parser = argparse.ArgumentParser("Automatically upload media to twitter")
    parser.add_argument("--directory", help="Directory to watch media for", default=os.getcwd())
    parser.add_argument("--config", "-c", help="Configuration file to use", default=os.path.join(os.getenv("HOME"), ".tweedia"))
    parser.add_argument("--status", "-s", help="Status to include in tweets")
    parser.add_argument("-d", "--dryrun", help="Dry Run. Prints the name of new files", action="store_true")

    args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    if os.path.isfile(args.config):
        config.read(args.config)
        auth = tweepy.OAuthHandler(config.get("auth","consumer_key"), config.get("auth", "consumer_secret"))
        auth.set_access_token(config.get("auth","access_key"), config.get("auth", "access_secret"))
    else:
        print("Please enter access key (https://apps.twitter.com/): ")
        consumer_key = raw_input("Consumer key: ")
        consumer_secret = raw_input("Consumer secret: ")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        print("Please grant permission to tweedia: " + auth.get_authorization_url())
        verifier = raw_input("Verifier: ")
        auth.get_access_token(verifier)
        config.add_section("auth")
        config.set("auth", "consumer_key", consumer_key)
        config.set("auth", "consumer_secret", consumer_secret)
        config.set("auth", "access_key", auth.access_token)
        config.set("auth", "access_secret", auth.access_token_secret)
        with open(args.config, "w") as fp:
            config.write(fp)

    api = tweepy.API(auth, wait_on_rate_limit=True, compression=True)

    if args.dryrun:
        poll_dir(args.directory, print)
    else:
        poll_dir(args.directory, functools.partial(post_photo, api, args.status))

#!/usr/bin/env python
from __future__ import print_function
import tweepy
import os
import time

CONSUMER_TOKEN="p9VZFZSkFS7vC4DCWwFTIRQir"
CONF_FILE = os.path.join(os.getenv("HOME"), ".tweedia")

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
    import pickle
    parser = argparse.ArgumentParser("Automatically upload media to twitter")
    parser.add_argument("--directory", help="Directory to watch media for", default=os.getcwd())
    parser.add_argument("--status", "-s", help="Status to include in tweets")
    parser.add_argument("consumer_secret", help="Consumer Secret")
    parser.add_argument("-d", "--dryrun", help="Dry Run. Prints the name of new files", action="store_true")

    args = parser.parse_args()

    config = dict()
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, args.consumer_secret)
    if os.path.isfile(CONF_FILE):
        print("sd")
        config = pickle.load(open(CONF_FILE, "r"))
        auth.set_access_token(config["access_token"], config["access_secret"])
    else:
        print("Please grant permission to tweedia: " + auth.get_authorization_url())
        verifier = raw_input("Verifier: ")
        auth.get_access_token(verifier)
        config["access_token"] = auth.access_token
        config["access_secret"] = auth.access_token_secret
        pickle.dump(config, open(CONF_FILE, "w"), protocol = pickle.HIGHEST_PROTOCOL)

    api = tweepy.API(auth, wait_on_rate_limit=True, compression=True)

    if args.dryrun:
        poll_dir(args.directory, print)
    else:
        poll_dir(args.directory, functools.partial(post_photo, api, args.status))

# Tweedia: Automatically upload media to twitter
This script will upload any new files to a twitter account. Really quite simple.

## Configuration
A configuration file is used to store the the various OAuth credentials to access token.
By default this will be in ``~/.tweedia``.

If the file does not exist on the first run you will be asked for:
1. A consumer token
2. A consumer secret
3. Verifier code

You can also manually set the values in the configuration file.
``
[auth]
consumer_key = SOME_KEY
consumer_secret = SOME_SECRET
access_key = ACCESS_KEY
access_secret = ACCESS_SECRET
``

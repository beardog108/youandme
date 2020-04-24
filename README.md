# youandme 🧑‍🤝‍🧑

[![Build Status](https://travis-ci.org/beardog108/youandme.svg?branch=master)](https://travis-ci.org/beardog108/youandme)

Only you and the person you're talking to should know the details of the converation.

This is a Python library to share data anonymously and securely* with limited traffic metadata. It is designed for generic byte streaming, but a script 'yam' is included to enable basic CLI instant messaging.

\* The ID one connects to a host with must be shared via a secure (private, authenticated) channel.

`$ pip install youandme`

You also need a recent Tor daemon in executable path. 0.4 Tor is what is tested. https://www.torproject.org/download/tor/

# why

In normal socket connections, Eve can see when Alex and Bob communicate and the size of their communications.

This library sends continuous streams of data (null bytes) even when no information is being communicated, in order to increase unobservability of transmission times and packet sizes.

Anonymity and encryption is provided via Tor onion services, though this library could easily be adapted to use plaintext (and encryption by an application) or another relay like I2P.


# security

As stated above, this library does no authentication. However, if the ID is shared privately and safely, the tunnel will have roughly the security of a Tor v3 onion service, with increased metadata unobservability.


## What an attacker sees in a normal Tor connection

![](no-dummy.png)


## What an attacker sees in a youandme connection


![](dummy.png)

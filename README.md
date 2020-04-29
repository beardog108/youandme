![](logo.png)


[![Build Status](https://travis-ci.org/beardog108/youandme.svg?branch=master)](https://travis-ci.org/beardog108/youandme) ![](https://img.shields.io/pypi/wheel/youandme) ![](https://img.shields.io/github/languages/top/beardog108/youandme) ![](https://img.shields.io/badge/metadata%20surveillance-LIMITED-blue) ![](https://img.shields.io/github/languages/code-size/beardog108/youandme)

Only you and the person you're talking to should know the details of the conversation. This includes metadata.

This is a Python library to share data anonymously and securely* with limited traffic metadata. It is designed for generic byte streaming over a private tunnel, using Tor onion services..


This library is meant to be used by other libraries or applications, however a script 'yam' is included to enable basic CLI instant messaging.


\* The ID one connects to a host with must be shared via a secure (private, authenticated) channel.

# install 📥

`$ pip install youandme`

You also need a recent Tor daemon in executable path. 0.4 Tor is what is tested. https://www.torproject.org/download/tor/

## basic chat usage 💬

`$ yam.py host`

This will start a bare-bones CLI-based chat and output an address to be given to a friend.

The friend connects:

`$ yam.py conn --address <address>`

# purpose 🧑‍🤝‍🧑

In normal socket connections, Eve can see when Alex and Bob communicate and the size of their communications.

This library sends continuous streams of data (null bytes) even when no information is being communicated, in order to increase unobservability of transmission times and packet sizes.

Anonymity and encryption is provided via Tor onion services, though this library could easily be adapted to use plaintext (and encryption by an application) or another relay like I2P.


# security 🔒

As stated above, this library does no authentication. However, if the ID is shared privately and safely, the tunnel will have roughly the security of a Tor v3 onion service, with increased metadata unobservability.

That said, one should not rely on any software when the stakes are too high.


## what an attacker sees in a normal Tor connection

![](no-dummy.png)


## what an attacker sees in a youandme connection


![](dummy.png)


# Limitations + Road map

This project will forever follow the KISS principle, but these two three will be addressed.

* Multi-byte character support (full utf-8 support)
* Tor bridge support
* Support non-anonymous hidden services. Mainly useful for certain development needs

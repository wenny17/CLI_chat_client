# CLI chat client

Client for chat from CLI. Allow reading/writing to chat

## How to install

Python 3.6 has to be installed. Use pip3 to install dependencies:

```
pip3 install -r requirements.txt
```
Put all necessary parameters to .env file. This is default parameters for utility and you can change them by CLI arguments
```
HOST=minechat.dvmn.org
PORT_READ=5000
PORT_WRITE=5050
```

## Quickstart

Run `python3 listen_minechat.py` to read incoming messages or `python3 writer_minechat.py -message 'YOUR_MESSAGE'` to send message to chat.

```
python3 listen_minechat.py --help
usage: listen-minechat.py [-h] [-host HOST] [-port PORT] [-history HISTORY]

python3 writer_minechat.py -message
usage: writer-minechat.py [-h] [-token TOKEN]
                          [-message [MESSAGE [MESSAGE ...]]] [-host HOST]
                          [-port PORT] [-login LOGIN]


```


## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

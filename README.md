Ggama -- Github-facing Llama-index wrapper
------------------------------------------

Ggama is a Python-based local interface to ChatGPT with additional context
provided in vector form based on files in a github repository, allowing you
to ask it questions about that repository in detail.


Requirements
------------

- OpenAI access token,
- GitHub access token,
- GitHub repository,
- Python 3.7 or higher,
- eel package (for web api),
- llama-index and llama-index-readers-github,


Use
---

1- Install requirements,
2- Copy ggama.user.toml-template to ggama.user.toml and edit your own values in,
3- Run app.py which will launch a very simple eel-based chat interface using the
   specified GitHub repository as a source of data and OpenAI's ChatGPT as an
   inference engine,

e.g

```sh
# prep
$ python -m venv venv
$ . ./venv/bin/activate
# . ./venv/scripts/activate.ps1 for powershell on win/lin/mac
$ pip install -r requirements.txt

# config
$ cp config.user.toml-template config.user.toml
$ $EDITOR config.user.toml   # <- edit settings

# run
$ python app.py
```

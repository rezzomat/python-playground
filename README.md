# python-playground

## Dependencies

### Requirements
Python 3.6+ is required. Installing package dependencies via:

`pip install -r requirements.txt`

### Extras
Extra dependencies:

 - Discord.py [rewrite]: `pip install git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]`
 - flask-bootstrap (Bootstrap 4.3): `pip install git+ssh://git@github.com/naiii/flask-bootstrap.git`
 
## Config
`config.ini` file required in the root directory with following fields:

```ini
[Discord]
token=<discord-token>
client_id=<client-id>
client_secret=<client-secret>

[GitHub]
token=<token>
owner=<github repo owner>
repo=<github repo name>

```
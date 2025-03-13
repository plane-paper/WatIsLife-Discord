# WatIsLife-Discord

## About
A much easier render on Discord of the ongoing project [WatIsLife](https://github.com/plane-paper/WatIsLife). Requires some rights.

Counts how many time you've said you want to KYS.

## Commands and Usage

The only phrase that triggers a counter increment right now is "kill myself", in that exact fashion. I might add more keywords very soon.

The bot has three commands:
1. !depressionlevel - returns the count of the current user
2. !curedepression - resets the count of the current user
3. !watchlist - returns all users that have a count > 0, from highest count to lowest.

## Deployment

### My iteration
Use [this link](https://discord.com/oauth2/authorize?client_id=1349295351538126858&permissions=8&integration_type=0&scope=bot) to invite the bot to your server. It will ask for administrator rights, which is an overkill... but I'm too lazy to configure it right now. I *might* change it later. Who knows.

If the link expires or has other problems, please let me know by opening an issue on GitHub.

### Your iteration
If you want to deploy your own bot, do this:
1. Download or clone the repository, all you really need is main.py.
2. Install Python and then run `pip install discord` in your terminal (if this fails, use `python -m pip install discord` or `py -m pip install discord`)
3. Go to Discord developer portal, select start new app, go to "bot", configure it, and click reset token. Copy the token and **save it somewhere temporarily, as Discord won't give it to you again**. You can come back and configure any other further details anytime.
4. Create a env.py file in the same directory as main.py. Paste this in:
    ```python
    def token():
        return "Your_Token"
    ```
    Obviously, replace `Your_Token` with your actual token. You can delete the previously saved token now if you wish.
5. Go back to discord developer portal and select "OAuth2", scroll to the URL generator, configure as needed, and copy the URL to your browser, then just select the server you want to invite the bot to.
6. Launch main.py on your local computer. Note your computer **must be connected to the internet**.
7. Done! Notice, for the bot to be online and responding, main.py must be running on some internet-connected computer. Alternatively, run the prorgram on a microcomputer like a [RaspPi](https://www.raspberrypi.com/documentation/computers/os.html).

## Cloning and Additional Development
I really struggle to believe that this thing can be used in other projects, but if you wish, clone away.

If you aren't against me stealing your precious intellectual work, please consider opening a pull request (Please I'm begging on my knees I need people to fix my terrible program).

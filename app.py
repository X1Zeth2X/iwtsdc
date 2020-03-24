from bot import Bot
from yaml import load, dump, YAMLError, FullLoader

""" Goals:
* Automatically enter classes based on schedule.

* Send "Good morning" greetings after 5 mins.
* Send "Interesting" mid class.
* Send "Thanks! bye." 1 minute before class ends.

* Record the session
* Save recorded session.
"""

# Entry point.
if __name__ == '__main__':
    # Load YAML data
    with open("iwtsdc.yaml", "r") as stream:
        try:
            print("Loading data...")
            data = load(stream, Loader=FullLoader)

        # Print any errors
        except YAMLError as e: print(e)

    try:
        print("Initializing bot...\n")
        bot = Bot(data)
        bot.run()

    except Exception as e:
        print('Something went wrong!')
        print(e)

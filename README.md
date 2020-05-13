# ReBel
ReBel is a client-server-based multiuser ringing software, use it to ring with others across the internet. The bells each person can ring and the keys used to ring them are all completely customisable, as is the total number of bells.

Executables for Windows and macOS have been provided and can be found here. ReBel is written in Python 3 and so it can also be run directly from the source code. To do this change into the 'src' directory and run 'rebel.py'.

## Usage
Open ReBel, enter in your name, the IP of the server (given to you by the person running the server), and the server port. Click 'Connect to Server' and then click 'Start Ringing'. This will take you to the ringing screen and from there you can start ringing.

![](img/ReBel_MenuScreen.png?raw=true|width="50")

By default you can ring bells 1 and 2 using the 'j' and 'f' keys though once you are in the ringing screen you can click on the 'Options' menu and change which bells you can ring and which keys you use to ring them. You're not limited to ringing only two bells and can instead set it to as many, or as few, as you want.

![](img/ReBel_RingingScreen.png?raw=true|width="50")

The total number of bells is set centrally through the server so that everyone sees and hears the same number of bells.

## Requirements to Run the Python Source Code
To run the Python source code you need to have Python 3 installed, as well as the 'pygame' and 'pydub' Python modules which can be installed via pip.

## Notes on Running a ReBel Server
It's easiest to keep the default values used for the local server IP and server port (just hit the 'Enter' key when the server prompts for these). ReBel attempts to determine the public IP address and print it to the server terminal, though it's not guaranteed to successfully determine it 100% of the time as it depends on an external 3rd party website. The public IP address is used by other people to access the server and so this is what needs to be passed on to them, as well as the server port if it's default value is changed.

For computers outside of your home network to see your ReBel server you'll need to portforward the server port to the computer hosting the server, usually done through your router settings.

## Server Commands
- help - Lists the available commands and their descriptions.
- quit - Shuts the server down.
- exit - Shuts the server down.
- ip - Displays the server IP information.
- ls - Lists the clients connected to the server.
- numberOfBells - Gives the total number of bells.
- setNumberOfBells x - Sets the total number of bells to x, where x is a positive integer.
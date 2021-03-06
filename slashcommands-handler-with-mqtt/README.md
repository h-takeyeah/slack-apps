# Slash Commands Handler with MQTT

*Devices* does not have any global IP but information which is calculated by these *devices* is needed to respond to your Slash Commands.

Using Pub/Sub model is good choice.

## Interaction flow

Slash Commands are handled through the process below.

> - A user in Slack types in the message box with the command, and submits it.
> - A payload is sent via an HTTP POST request to your app.
> - Your app responds in some way. <- This repository's role
> (Enabling interactivity with Slash Commands)

`main.py` is responsible for the part that returns the message. This script will be placed at *"Devices"*(right bottom corner of the figure below).

![slashcommand-with-mqtt](https://user-images.githubusercontent.com/61489178/152280378-325a3336-e9d3-4a0a-9443-748c71c86b86.jpg)


## References

- [Enabling interactivity with Slash Commands | Slack](https://api.slack.com/interactivity/slash-commands)

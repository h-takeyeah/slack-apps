# Slash Commands Handler with MQTT

*Computer A* does not have any global IP but information which is calculated at this computer is needed to respond to your Slash Commands.

Using Pub/Sub is good choice  when your Slash Commands cannot respond until

> - A user in Slack types in the message box with the command, and submits it.
> - A payload is sent via an HTTP POST request to your app.
> - Your app responds in some way. <- This repository's role
> (Enabling interactivity with Slash Commands)

`main.py` is responsible for the part that returns the message. This script will be placed at *"Devices"*(right bottom corner of the figure below).

![]()

## References

- [Enabling interactivity with Slash Commands | Slack](https://api.slack.com/interactivity/slash-commands)

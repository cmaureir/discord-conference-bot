# Functionality

## Available commands

* `$send #channel message`:
  Sends a message to a specific channel

*  `$warning <add> @user reason_message`
    Adds a warning to the @user with a specific reason.
    The 'add' positional argument is optional

*  `$warning list <@user>`
    List the warnings in the system. A @user is optional to list
    only those warnings.

*  `$warning remove ID`
    Removes a warning based on the ID that is displayed
    with the list command.

*  `$schedule <create> #channel date time message`
    Schedules a message in the future on a specific #channel.

*  `$schedule list`
    List scheduled messages.

*  `$schedule remove ID`
    Removes a schedule message by the ID displayed with the list command.

## Features (in progress)
* You can start the process by reacting to the message in #crea-programa
* The bot will send you a message on a new channel for you to select your preferred talks: #crea-programa-<username>
* Users can select one talk per time slot.
* The selected talks will be displayed on a new channel #programa-username

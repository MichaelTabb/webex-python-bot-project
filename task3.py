elif command == "help":
    if all_polls[roomId]:
        send_message_in_room(roomId, "These are all of the commands you can use:\n"
                            "\n"
                            "add option: Adds a poll option that you can choose from once you have created the poll\n"
                            "create poll: Creates a poll to use\n"
                            "end poll: Ends the poll and displays the results\n"
                            "help: Gives the list of active commands that can be used\n"
                            "ping poll: pings a reminder to anybody who hasn't voted in the poll\n"
                            "status poll: Gives the satus of the poll and whether it has started and if there are any results\n"
                            "start poll: starts the poll and allows for users to vote in the poll")
        



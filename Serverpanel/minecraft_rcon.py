from mcrcon import MCRcon

# Define the host and port for the Minecraft server
HOST = "127.0.0.1"  # Replace with your server's IP
PORT = 25575         # Default RCON port

class MinecraftRCON:
    def __init__(self, password):
        self.password = password

    def _connect(self):
        """Establish a connection to the server."""
        try:
            rcon = MCRcon(HOST, self.password, port=PORT)
            rcon.connect()
            return rcon
        except Exception as e:
            return None

    def get_player_count(self):
        """Fetch the current player count on the server."""
        rcon = self._connect()
        if not rcon:
            return 0

        try:
            response = rcon.command("list")  # Get the server's player list/status
            logging.debug(f"RCON response for 'list': {response}")

            # Check if the response contains the expected phrase
            if "There are" in response and "players online" in response:
                 # Extract the part that indicates the player count
                # Example: "There are 1 of a max of 20 players online"
                parts = response.split()
                current_players = parts[2]  # "1" is the third word (index 2)
                return int(current_players)

            # Fallback if the expected format is not found
            logging.warning("Failed to extract player count from response.")
            return 0
        except ValueError as ve:
            logging.error(f"Failed to parse player count as integer: {ve}")
            return 0
        except Exception as e:
            logging.error(f"Unexpected error while fetching player count: {e}")
            return 0
        finally:
            rcon.disconnect()

    def get_player_list(self):
        """Fetch the list of players currently online."""
        rcon = self._connect()
        if not rcon:
            return []

        try:
            response = rcon.command("list")  # Get the server's player list/status
            logging.debug(f"RCON response for 'list': {response}")

            # Check if the response contains the expected phrase
            if ":" in response:
                # Split response at the colon to extract player names
                player_info = response.split(":", 1)[-1].strip()
                if player_info:
                    # Split the player names into a list and return
                    players = [player.strip() for player in player_info.split(",")]
                    return players

            # Fallback if no players are listed
            return []
        except Exception as e:
            return []
        finally:
            rcon.disconnect()

    def is_server_online(self):
        """Check if the server is online by attempting a connection."""
        rcon = self._connect()
        if rcon:
            rcon.disconnect()
            return True
        return False

    def execute_command(self, command):
        """Send a custom command to the server."""
        rcon = self._connect()
        if not rcon:
            return []
            print("RCON = NONE")
        try:
            response = rcon.command(command)
            return response
            print("RCON = COMMAND")
        except Exception as e:
            return []
        finally:
            rcon.disconnect()

# Usage example (assuming this script is saved as 'minecraft_rcon.py')
if __name__ == "__main__":
    from serverpanel import RCON_PASSWORD  # This should be defined in a separate file

    rcon_handler = MinecraftRCON(RCON_PASSWORD)

    if rcon_handler.is_server_online():
        player_count = rcon_handler.get_player_count()
        if player_count is not None:
            pass
        else:
            pass
    else:
        pass

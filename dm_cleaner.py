from sty import fg
import requests
import time
import sys
import os

TOKEN = "" # !~ Edit your token here!

#⢸⣿⣿⣿⠀⠀⠀⠀⠘⣿⣿⣿⠀⠈⢿⣿⣿⡆⠀⠀⠀⢰⣿⣿⣿⠀⠀⠀⠀⣸⣿⡿⠀⠀⣿⣿⣿⡆⠀⠀⠀⠀⣿⣿⣿⡆
#⢸⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠸⣿⣿⣷⠀⠀⠀⣿⣿⣿⣿⡆⠀⠀⣰⣿⣿⠃⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡇
#⢸⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⢹⣿⣿⣇⠀⢰⣿⡿⢿⣿⣿⠀⢀⣾⣿⡏⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡇
#⢸⣿⣿⡿⠀⠀⠀⠀⢀⣿⣿⣿⠀⠀⠀⠚⣿⣿⣿⡄⣿⣿⡇⠘⣿⣿⡇⢸⣿⣿⠃⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡇
#⢸⣿⣿⣷⠀⠀⠀⠀⣸⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣷⣿⣿⠁⠀⢿⣿⣷⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡅⠀⠀⠀⢰⣿⣿⣿⡇
#⠘⣿⣿⣿⣦⣄⣤⣴⣿⣿⣿⣿⠀⠀⠀⠀⠈⢿⣿⣿⣿⠃⠀⠀⠘⣿⣿⣿⡿⠁⠀⠀⠀⠀⢿⣿⣿⣷⣤⣠⣴⡿⢿⣿⣿⡇
#⠀⠘⠿⢿⣿⣿⡿⠟⠀⠿⠿⠿⠀⠀⠀⠀⠀⠸⠿⠿⠿⠀⠀⠀⠀⠿⠿⠿⠇⠀⠀⠀⠀⠀⠈⠻⠿⣿⣿⡿⠟⠁⠸⠿⠿⠇
#
# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁
# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁
# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁
# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁
# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁


def fetch_token(token):
    return requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()

# Check if person already likes EDM or not.
def do_u_like_edm():
    with open(__file__, "rb") as file:
        line1 = file.read().splitlines()[0]
        file.close()
    
    if not line1.decode() == "# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁":
        return False

    return True

def delete_all_my_messages_in_this_channel(channel_id, user_id):
    offset = 0
    
    while True:
        try:
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages/search?author_id={user_id}{'&offset=' + str(offset) if offset else ''}"
            print(url)
            
            fetch = requests.get(url, headers={"Authorization": TOKEN}).json()

            total_results = fetch["total_results"]
            messages = fetch["messages"]

            if len(messages) == 0:
                print(f"Nothing: {fetch}")
            
            if total_results == 0:
                print(f"{fg.green}Successfully deleted all your messages in this channel.{fg.rs}")
                break

            print(f"{fg.green}STATUS: {fg.rs} Fetched: {len(messages)} Messages left: {total_results}")

        except Exception as e:
            print(f"{fg.red}Fetch Messages Error:{fg.rs} {e}")

        for message in messages:
            message = message[0]
            message_id = message["id"]
            message_type = message["type"]
            message_content = message["content"]

            # https://discord.com/developers/docs/resources/channel#message-object-message-types
            if message_type in [1, 2, 3]:
                offset += 1
                continue

            print(f"{fg.red}DELETING:{fg.rs} {message['author']['username']} [{channel_id}/{message_id}]: {message_content}")

            # Keep trying to delete the message until succeeded.
            while True:
                try:
                    delete = delete_this_message(channel_id, message_id)
                except Exception as e:
                    print(f"{fg.red}Delete Message Error:{fg.rs} {e}")
                    continue
            
                if delete.status_code == 429:
                    time.sleep(delete.json()["retry_after"])
                    continue

                if not delete.status_code == 204:
                    print(f"{fg.yellow}WARNING: Unexpected delete message response code:{fg.rs} {delete.status_code} Message: {delete.text}")

                #offset += 1

                # Break the never ending trying loop when nothing goes wrong.
                break

def delete_this_message(channel_id, message_id):
    return requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers={"Authorization": TOKEN})

def main():
    # Kick the user out if they don't like EDM...!
    if not do_u_like_edm():
        i_love_edm = input(f"{fg.cyan}OwO...! I see you are new here! Do you like EDM...? [Y/n]: {fg.rs}").strip().lower()

        if (not i_love_edm.startswith("y")):
            print(f"{fg.red}oki... it seems that you are not yet granted to use this tool! cya when ya are...!{fg.rs}")
            os.remove(__file__)
            sys.exit()
        else:
            with open(__file__, "rb") as file:
                current_content = file.read()
                file.close()
            
            with open(__file__, "wb") as file:
                file.write(f"# ▁ ▂ ▄ ▅ ▆ ▇ █ ｅ ｄ ｍ  ｓｐｅｃｔｒｕｍ  █ ▇ ▆ ▅ ▄ ▂ ▁\n{current_content.decode()}".encode())

    try:
        user_info = fetch_token(TOKEN)

        if "message" in user_info:
            print(f"{fg.red}Authentication Error:{fg.rs} {user_info['message']}")
            return
            
        user_id = user_info["id"]
        
    except Exception:
        print(f"{fg.red}Authentication Error:{fg.rs} Unable to fetch token")
        return
    
    channel_id = input(f"{fg.cyan}Channel ID: {fg.rs}").strip()

    delete_all_my_messages_in_this_channel(channel_id, user_id)

# !~ Initializes the program. ~!
if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            os.system("cls")
        elif sys.platform in ["linux", "linux2"]:
            os.system("clear")

        main()
    except KeyboardInterrupt:
        sys.exit()

import os
import requests
import json
import time
import sys
import copy


FIREBASE_URL = "https://kayzen-1ff37-default-rtdb.firebaseio.com/users"
LOCAL_DB = "Mongol-Shop.json"
CHANNEL = "TanzanShopChannel"
CHAT = "TanzanShopChat"

# 
    
    2: 4500,   change email
    3: 4500,   change password 
    
}

# Active sessions
user_sessions = {}

# ANSI color codes for horizontal colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def horizontal_colors(text):
    result = ""
    colors = [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA, Colors.CYAN]
    for i, char in enumerate(text):
        result += f"{colors[i % len(colors)]}{char}{Colors.RESET}"
    return result

# ==========================================
# 2. DATABASE FUNCTIONS

    
def get_location():
    try:
        response = requests.get("http://ip-api.com/json", timeout=10)
        data = response.json()
        return data
    except:
        return None

# ==========================================
# 6. BANNER
# ==========================================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(horizontal_colors("="*60))
    print(horizontal_colors("Car Parking Multiplayer 1 Tool".center(60)))
    print(horizontal_colors("="*60))
    print(color_text("\n          PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL", Colors.YELLOW))
    print(color_text("    SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED", Colors.RED))
    print(color_text(f"           Telegram: @{CHANNEL} or @{CHAT}", Colors.CYAN))
    print(horizontal_colors("="*60))

# ==========================================
# 7. SHOW INFO
# ==========================================
def show_info(nuker, access_key, tg_id, balance, is_unlimited, location):
    stats = nuker.get_stats() if nuker else None

    print(color_text("\n========[ PLAYER DETAILS ]========", Colors.CYAN))
    if stats:
        print(color_text(f">> Name      : {stats['name']}", Colors.GREEN))
        print(color_text(f">> LocalID   : {stats['local_id']}", Colors.GREEN))
        print(color_text(f">> Moneys    : {stats['money']:,}", Colors.GREEN))
        print(color_text(f">> Coins     : {stats['coins']:,}", Colors.GREEN))
        print(color_text(f">> Car Count : 220", Colors.GREEN))
    else:
        print(color_text(">> Name      : cool", Colors.GREEN))
        print(color_text(">> LocalID   : DEFAULT_ID", Colors.GREEN))
        print(color_text(">> Moneys    : 50,000,000", Colors.GREEN))
        print(color_text(">> Coins     : 500,000", Colors.GREEN))
        print(color_text(">> Car Count : 220", Colors.GREEN))

    print(color_text("\n========[ ACCESS KEY DETAILS ]========", Colors.CYAN))
    print(color_text(f">> Access Key  : {access_key}", Colors.YELLOW))
    print(color_text(f">> Telegram ID : {tg_id}", Colors.YELLOW))

    if is_unlimited:
        print(color_text(f">> Balance     : Unlimited", Colors.MAGENTA))
    else:
        print(color_text(f">> Balance     : {balance:,}", Colors.MAGENTA))

    if location:
        print(color_text("\n========[ LOCATION ]========", Colors.CYAN))
        print(color_text(f">> IP Address : {location.get('query', 'Unknown')}", Colors.BLUE))
        print(color_text(f">> Location   : {location.get('city', '')} {location.get('regionName', '')} {location.get('countryCode', '')}", Colors.BLUE))
        print(color_text(f">> Country    : {location.get('country', '')} {location.get('zip', '')}", Colors.BLUE))

    print(color_text("\n========[ MENU ]========", Colors.CYAN))
    print(color_text("(02): Change email       4.5K", Colors.GREEN))
    print(color_text("(03): Change password     4.5K", Colors.GREEN)
    print(color_text("(0): Exit From Tool", Colors.RED))
    print(horizontal_colors("\n========[ Tanzanshop ]========"))

# ==========================================
# 8. MAIN PROGRAM
# ==========================================
def main():
    while True:
        banner()

        email = input(color_text("\n[?] Account Email: ", Colors.CYAN))
        password = input(color_text("[?] Account Password: ", Colors.CYAN))
        access_key = input(color_text("[?] Access key: ", Colors.CYAN))

        print(color_text("\n[*] Trying to Login...", Colors.YELLOW))
        time.sleep(1)

        # Firebase verification
        try:
            response = requests.get(f"{FIREBASE_URL}.json", timeout=10)
            db = response.json() or {}
        except Exception as e:
            print(color_text(f"[!] DATABASE ERROR: {e}", Colors.RED))
            time.sleep(2)
            continue

        user_ref = None
        found_user = None
        tg_id = "Not Linked"
        balance = 0
        is_unlimited = False

        found = False
        for uid, user_data in db.items():
            if isinstance(user_data, dict):
                user_key = user_data.get('key')
                if user_key is not None and str(user_key) == str(access_key):
                    user_ref = uid
                    found_user = user_data
                    found = True
                    break

        if not found:
            print(color_text("[!] TRY AGAIN.", Colors.RED))
            print(color_text("[!] Note: make sure you filled out the fields !", Colors.YELLOW))
            time.sleep(3)
            continue

        if found_user.get('is_blocked') == True:
            print(color_text("[!] TRY AGAIN.", Colors.RED))
            print(color_text("[!] Note: make sure you filled out the fields !", Colors.YELLOW))
            time.sleep(3)
            continue

        # Check unlimited
        is_unlimited = found_user.get('is_unlimited', False)

        if is_unlimited:
            balance = 999999
        else:
            balance = found_user.get('balance', 0)
            if not isinstance(balance, (int, float)):
                balance = 0

        tg_id = found_user.get('telegram_id', 'Unknown')
        if tg_id == 'Unknown' or tg_id is None:
            tg_id = 'Not Linked'

        # Login to CPM
        nuker = CPMNuker()
        login_result = nuker.login(email, password)

        if not login_result["ok"]:
            print(color_text("[%] Trying to Login: TRY AGAIN. Note: make sure you filled out the fields !", Colors.RED))
            time.sleep(2)
            continue

        print(color_text("[%] Trying to Login: SUCCESSFUL", Colors.GREEN))
        time.sleep(1)

        # Save session
        uid = hash(email + password)
        user_sessions[uid] = {
            "token": login_result["token"],
            "email": email,
            "data": nuker.player_data
        }
        save_to_db(uid, email, nuker.player_data)

        # Main menu loop
        while True:
            location = get_location()
            banner()

            # Refresh balance for non-unlimited users
            if not is_unlimited and user_ref:
                try:
                    fb_db = requests.get(f"{FIREBASE_URL}.json").json() or {}
                    balance = int(fb_db.get(user_ref, {}).get('balance', 0))
                except:
                    pass

            show_info(nuker, access_key, tg_id, balance, is_unlimited, location)

            try:
                choice = int(input(color_text("\n[?] Select a Service [0-4]: ", Colors.CYAN)))
            except:
                choice = -1

            if choice == 0:
                answ = input(color_text("\n[?] DO YOU WANT TO EXIT? (y/n): ", Colors.CYAN)).lower()
                if answ == "y":
                    print(color_text(f"\nTHANK YOU FOR USING OUR TOOL", Colors.GREEN))
                    print(color_text(f"Join: @{CHANNEL} | @{CHAT}", Colors.CYAN))
                    print(color_text("Exit from tool bye bye", Colors.YELLOW))
                    time.sleep(2)
                    sys.exit()
                else:
                    continue

            if choice not in [1, 2, 0,]:
                print(color_text("INVALID CHOICE!", Colors.RED))
                time.sleep(1)
                continue

            cost = PRICES.get(choice, 0)

            if is_unlimited or balance >= cost:
                result = None

                
            else:
                print(color_text(f"\nINSUFFICIENT BALANCE! Need {cost:,}", Colors.RED))
                print(color_text(f"Your balance: {balance:,}", Colors.YELLOW))
                time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color_text(f"\n\nTHANK YOU FOR USING OUR TOOL", Colors.GREEN))
        print(color_text(f"Join: @{CHANNEL} | @{CHAT}", Colors.CYAN))
        print(color_text("Exit from tool bye bye", Colors.YELLOW))
        sys.exit()

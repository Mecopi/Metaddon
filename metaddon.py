import requests;
import time;
from datetime import datetime
from bs4 import BeautifulSoup;

username = ""; # Write your metamob email in quotes or replace by arguments
password = ""; # Write your metamob password here or replace by arguments
nickname = ""; # Write your metamob name (Not email, but your showed name on Metamob)
running_mode = "trade"; # You can switch this as 3 different values (trade / sell / buy) or replace by arguments
minimal_known_users_clear_interval = 120; # This will clear known_users and therefore reverify some already verified profiles with specific delay
known_users = []; # Do not modify
blacklisted_user = []; # You can add some metamob users name into this list, script will just ignore them

def main():
    print("Metamob addon running"); # Log running script
    session = requests.Session(); # Instanciating a new Session object
    connection_request = session.post("https://www.metamob.fr/connexion", data={"identifiant":username, 'password':password});  # Requesting connection to Metamob
    soup = BeautifulSoup(connection_request.text, 'html.parser'); # Parsing html into BeautifulSoup
    if(user_is_connected(soup)):
        last_cleared_known_users_list = datetime.now(); # Default setting first check
        while True:
            refresh_request = session.get('https://www.metamob.fr/'); # Actualizing home page
            soup = BeautifulSoup(refresh_request.text, 'html.parser'); 
            last_users_connected = get_last_users_list(soup); 
            for user in last_users_connected: # For each last users_connected
                if(user not in known_users and user not in blacklisted_user): # If user wasn't verified before
                    check_profile(session, user); 
                    known_users.append(user); # This user is now know
            if ((datetime.now()-last_cleared_known_users_list).seconds >= minimal_known_users_clear_interval): # Clear known users list time has reached
                known_users.clear(); # Clear known users list
                last_cleared_known_users_list = datetime.now(); # Update last checked
            time.sleep(5); # Just to be fair
    else: 
        print("Unable to connect account. Verify username and password"); 

def check_profile(session, user):
    profil_page_request = session.get("https://www.metamob.fr/profil/" + user); # Requesting profil page of target user
    soup = BeautifulSoup(profil_page_request.text, 'html.parser'); 
    alert_divs = soup.find_all('div', {'class':'alert'}); # Gettings alert divs
    user_contact = get_user_contact(soup, user); # Getting user contact
    if running_mode.lower() == "sell":
        if("alert-success" in alert_divs[0]['class']): # If you sell some of user search
            print(user + " seems interesting profile for your selling : " + user_contact + " to contact him (https://www.metamob.fr/profil/" + user+ ")"); 
    elif running_mode.lower() == "buy":
        if("alert-success" in alert_divs[1]['class']): # User have some of interesting for you
            print(user + " seems interesting profile for your buying : " + user_contact + " to contact him (https://www.metamob.fr/profil/" + user+ ")"); 
    else: # Trade or unrecognized so default trade options
        if(len(soup.find_all('div', {'class':'alert-success'})) == 2):
            print(user + " seems interesting profile for your trade attempt : " + user_contact + " to contact him (https://www.metamob.fr/profil/" + user+ ")"); 

def get_user_contact(soup, user):
    profile_items = soup.find_all('div', {'class':'profil-item'}); # Tryin to etablish an items list
    for item in profile_items:
        if("Contact: " in item.text):
            return item.find('span').text; 
    return "/w" + user; 


def get_last_users_list(soup):
    users = []; 
    users_items = soup.find('div', {'class':'derniers-connectes'}).find_all('a'); # Getting last connected users list on the same game server that metamob addon running on 
    for user_item in users_items:
        if(user_item.text != nickname):
            users.append(user_item.text); 
    return users; 

def user_is_connected(connection_result):
    return connection_result.find('a', {'href':'/utilisateur/mon_profil'}) is not None; # Check if connection worked with simple soup html verification


main(); 
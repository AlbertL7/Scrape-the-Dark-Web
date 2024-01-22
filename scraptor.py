import requests
import subprocess
import random
import re
import urllib3
import argparse
import psutil
import time
import sys
import json
import Cleaner #imported from Cleaner.py script

default_onion_sites = [
"mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion", # Ransomware Intel Gathering dark web sites
"noescapemsqxvizdxyl7f7rmg5cdjwp33pg2wpmiaaibilb4btwzttad.onion",
"7ukmkdtyxdkdivtjad57klqnd3kdsmq6tp45rrsxqnu76zzv3jvitlqd.onion",
"z6wkgghtoawog5noty5nxulmmt2zs7c3yvwr22v4czbffdoly2kl4uad.onion",
"ransomocmou6mnbquqz44ewosbkjk3o5qjsl3orawojexfook2j7esad.onion",
"santat7kpllt6iyvqbr7q4amdv6dzrh6paatvyrzl7ry3zm72zigf4ad.onion",
"omegalock5zxwbhswbisc42o2q2i54vdulyvtqqbudqousisjgc7j7yd.onion",
"lorenzmlwpzgxq736jzseuterytjueszsvznuibanxomlpkyxk6ksoyd.onion",
"zohlm7ahjwegcedoz7lrdrti7bvpofymcayotp744qhx6gjmxbuo2yid.onion",
"meow6xanhzfci2gbkn3lmbqq7xjjufskkdfocqdngt3ltvzgqpsg5mid.onion",
"basemmnnqwxevlymli5bs36o5ynti55xojzvn246spahniugwkff2pad.onion",
"stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion",
"pa32ymaeu62yo5th5mraikgw5fcvznnsiiwti42carjliarodltmqcqd.onion",
"3ev4metjirohtdpshsqlkrqmxq6zu3d7obrdhglpy5jpbr7whmlfgqd.onion",
"metacrptmytukkj7ajwjovpjqzd7esg5v3sg344uzhigagpezcqlpyd.onion",
"bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion",
"pdcizqzjitsgfcgqeyhuee5u6uki6zy5slzioinlhx6xjnsw25irdgqd.onion",
"alphvuzxyxv6ylumd2ngp46xzq3pw6zflomrghvxeuks6kklberrbmyd.onion",
"knight3xppu263m7g4ag3xlit2qxpryjwueobh7vjdc3zrscqlfu3pqd.onion",
"cactusbloguuodvqjmnzlwetjlpj6aggc6iocwhuupb47laukux7ckid.onion",
"incblog7vmuq7rktic73r4ha4j757m3ptym37tyvifzp2roedyyzzxid.onion",
"lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion",
"threeamkelxicjsaf2czjyz2lc4q3ngqkxhhlexyfcp2o6raw4rphyad.onion",
"lockbitapt2d73krlbewgv27tquljgxr33xbwwsp6rkyieto7u4ncead.onion",
"akiral2iz6a7qgd3ayp3l6yub7xx2uep76idk3u2kollpj5z3z636bad.onion",
"rnsm777cdsjrsdlbs4v5qoeppu3px6sb2igmh53jzrx7ipcrbjz5b2ad.onion",
"alphvmmm27o3abo3r2mlmjrpdmzle3rykajqc5xsj7j7ejksbpsa36ad.onion",
"hl66646wtlp2naoqnhattngigjp5palgqmbwixepcjyq5i534acgqyad.onion",
"mblogci3rudehaagbryjznltdp33ojwzkq6hn2pckvjq33rycmzczpid.onion",
"weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion",
"medusaxko7jxtrojdkxo66j7ck4q5tgktf7uqsqyfry4ebnxlcbkccyd.onion",
"kbsqoivihgdmwczmxkbovk7ss2dcynitwhhfu5yw725dboqo5kthfaad.onion",
"rhysidafohrhyy2aszi7bm32tnjat5xri65fopcxkdfxhi4tidsg7cad.onion",
"sbc2zv2qnz5vubwtx3aobfpkeao6l4igjegm3xx7tk5suqhjkp5jxtqd.onion"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_current_ip():
    try:
        ipv4 = requests.get("https://api.ipify.org").text
        ipv6 = requests.get("https://api64.ipify.org").text
        return ipv4, ipv6
    except Exception as e:
        print(f"[+] Error fetching IP addresses: {e}")
        return None, None

def start_tor():
    tor_path = "C:\\Users\\HOUSE-OF-L\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"
    torrc_custom_path = "C:\\Users\\HOUSE-OF-L\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Data\\Tor\\torrc_custom"

    # Terminate existing tor.exe processes
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'tor.exe':
            print("[+] Found existing Tor process. Terminating it.")
            psutil.Process(process.info['pid']).terminate()

    try:
        tor_process = subprocess.Popen([tor_path, '-f', torrc_custom_path])
        print("[+] Tor is starting...")
        time.sleep(10)  # Give Tor time to start
        if tor_process.poll() is None:
            print("[+] Tor started successfully.")
        else:
            print("[+] Tor failed to start.")
            return None
    except Exception as e:
        print(f"[+] Failed to start Tor: {e}")
        return None

    return tor_process

# Function to get a Tor session
def get_tor_session():
    session = requests.session()
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.proxies = proxies
    print("[+] Using SOCKS proxy:", proxies)
    return session

def test_tor_connection(session):
    try:
        test_url = "https://check.torproject.org/"
        response = session.get(test_url, timeout=10)
        if "Congratulations. This browser is configured to use Tor." in response.text:
            print("[+] Tor connection test successful.")
            return True
        else:
            print("[+] Tor connection test failed. Not using Tor.")
            return False
    except Exception as e:
        print(f"[+] Error testing Tor connection: {e}")
        return False

def fetch_onion_content(session, onion_url, custom_site, custom_timeout):
    MAX_RETRIES = 3
    default_timeout = 45  # Default timeout for other sites
    timeout = custom_timeout if custom_site in onion_url else default_timeout

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(onion_url, timeout=timeout)
            return response.text
        except requests.exceptions.Timeout:
            print(f"[+] Request to {onion_url} timed out after {timeout} seconds.")
        except requests.exceptions.RequestException as e:
            print(f"[+] Attempt {attempt + 1} failed for {onion_url}: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
    print(f"[+] Failed to fetch {onion_url} after {MAX_RETRIES} attempts.")
    return None

# Function to scrape ahmia.fi for dark web links
def tor_scraper(use_tor, custom_site="", custom_timeout=60):

    tor_process = None
    
    session = get_tor_session()
    
    if use_tor:
        tor_process = start_tor()
        if not test_tor_connection(session):
            print("[+] Exiting due to failed Tor connection test.")
            if tor_process is not None:
                tor_process.terminate()
            return
    
    mineddata = default_onion_sites

    # Fetch content of each .onion site using Tor and clean html / remove javascript / save image paths
    for link in mineddata:
        onion_url = f"http://{link}"
        onion_content = fetch_onion_content(session, onion_url, custom_site, custom_timeout)
        if onion_content:
            # Clean the fetched content using Cleaner
            cleaned_content = Cleaner.strip_html_tags_keep_images_remove_javascript(onion_content)

            # Write the cleaned content to a file
            content_filename = f"{link.replace('.onion/', '')}.txt"
            with open(content_filename, "w+", encoding="utf-8") as content_file:
                content_file.write(cleaned_content)
            print(f"[+] Cleaned content from {link} written to file: {content_filename}")

    if tor_process is not None:
        tor_process.terminate()
        print("[+] Tor service terminated.")

def scrape_ahmia(query):

    session = requests.session()

    if " " in query:
        query = query.replace(" ", "+")

    url = f"https://ahmia.fi/search/?q={query}"
    ua_list = [
    "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", 
    "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]

    ua = random.choice(ua_list)
    headers = {'User-Agent': ua}
    response = session.get(url, headers=headers)
    content = response.text
    regexquery = r"\w+\.onion"
    mineddata = re.findall(regexquery, content)
    links_filename = f"{query}_sites.txt"
    mineddata = list(dict.fromkeys(mineddata))

    with open(links_filename, "w+", encoding="utf-8") as file:
        for link in mineddata:
            file.write(link + "\n")
    print(f"[+] Links written to file: {links_filename}")
    
        # Fetch content of each default .onion site

def ahmia_query_to_tor(query, tor_session, timeout=60):
    if " " in query:
        query = query.replace(" ", "+")
    file_path = f"{query}_sites.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        onion_links = file.readlines()

    for link in onion_links:
        link = link.strip()  # Remove any trailing whitespace or newlines
        onion_url = f"http://{link}"
        content = fetch_onion_content(tor_session, onion_url, link, timeout)
        if content:
            # Process the fetched content as needed
            print(f"[+] Content fetched from {link}")

def query_onion_sites_from_file(file_path, tor_session, timeout=60):
    onion_site_pattern = re.compile(r'[a-zA-Z0-9]{16,56}\.onion\b')
    onion_links = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            matches = onion_site_pattern.findall(line)
            if matches:
                print(f"[+] Matches Found: {matches}")
                onion_links.extend(matches)

    for link in onion_links:
        onion_url = f"http://{link}"
        content = fetch_onion_content(tor_session, onion_url, "", timeout)
        if content:
            print(f"[+] Content fetched from {link}")

def get_tor_exit_node_ip(session):
    try:
        response = session.get("https://api.ipify.org")
        return response.text
    except Exception as e:
        print(f"[+] Error fetching exit node IP address: {e}")
        return None
    
def get_tor_ip_location(exit_node_ip, api_key):
    if not api_key:
        print("[+] API key is required for IP geolocation.")
        return None

    try:
        request = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={exit_node_ip}")
        response = json.loads(request.content)
        return response
    except Exception as e:
        print(f"[+] Error fetching IP location: {e}")
        return None
    
def create_date_based_directory():
    current_date = datetime.datetime.now().strftime("%m-%d-%Y")
    directory_name = f"saved_files_{current_date}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name


def main():
    try:
        parser = argparse.ArgumentParser(description="Web Scraper with Tor")
        parser.add_argument("--query", default="", help="Scrape ahmia.fi for dark .onion sites and save them to a file")
        parser.add_argument("--tor", action="store_true", help="Connect to Tor")
        parser.add_argument("--site", default="", help="Specify a specific .onion site")
        parser.add_argument("--timeout", type=int, default=60, help="Set a custom timeout in seconds, default is 60 seconds")
        parser.add_argument("--default_sites", action="store_true", help="Fetch content from default .onion sites, these are hard coded sites.")
        parser.add_argument("--query_to_tor", action="store_true", help="Get HTML content from the file created from the query you made.")
        parser.add_argument("--file", default="", help="Provide a file with .onion sites and fetch the content")
        parser.add_argument("--api-key", default="", help="API key for ipgeolocation.io, easy Exit Node IP location lookup")
        args = parser.parse_args()

        session = None
        tor_process = None

        ipv4, ipv6 = get_current_ip()
        if ipv4 or ipv6:
            print(f"[+] Current IPv4 address: {ipv4}")
            print(f"[+] Current IPv6 address: {ipv6}")
        else:
            print("[+] Unable to fetch current IP addresses")

        # Start Tor if needed
        if args.tor:
            tor_process = start_tor()
            if tor_process is not None:
                session = get_tor_session()
                if test_tor_connection(session):
                    # Get Tor exit node IP address
                    exit_node_ip = get_tor_exit_node_ip(session)
                    if exit_node_ip:
                        print(f"[+] Tor exit node IP address: {exit_node_ip}")
                        
                        # Get location of the Tor exit node IP
                        exit_node_location = get_tor_ip_location(exit_node_ip, args.api_key)
                        if exit_node_location:
                            print(f"[+] Exit node location: {exit_node_location.get('city')}, {exit_node_location.get('country_name')}")
                        else:
                            print("[+] Unable to fetch location for the exit node IP address.")
                    else:
                        print("[+] Unable to fetch Tor exit node IP address.")
                else:
                    print("[+] Failed to verify Tor connection.")
                    tor_process.terminate()
                    return
            else:
                return
        else:
            session = requests.session()

        # If Tor is not used, use a regular session
        if not args.tor:
            session = requests.session()

        # Check for Tor requirement for specific functionalities
        if (args.query_to_tor or args.default_sites) and not args.tor:
            print("***The --tor argument is required for --query_to_tor and --default_sites.***")
            return

        if args.query:
            scrape_ahmia(args.query)

        if args.query_to_tor and args.query:
            ahmia_query_to_tor(args.query, session, args.timeout)

        if args.file:
            query_onion_sites_from_file(args.file, session, args.timeout)

        if args.site:
            print(f"[+] Fetching content from: {args.site}")
            onion_content = fetch_onion_content(session, f"http://{args.site}", args.site, args.timeout)
            if onion_content:
                content_filename = f"{args.site.replace('.onion/', '')}.txt"
                with open(content_filename, "w+", encoding="utf-8") as content_file:
                    content_file.write(onion_content)
                print(f"Content from {args.site} written to file: {content_filename}")

        if args.default_sites:
            print("[+] Fetching content from default sites")
            for link in default_onion_sites:
                onion_url = f"http://{link}"
                onion_content = fetch_onion_content(session, onion_url, "", args.timeout)
                if onion_content:
                    content_filename = f"{link.replace('.onion/', '')}.txt"
                    with open(content_filename, "w+", encoding="utf-8") as content_file:
                        content_file.write(onion_content)
                    print(f"[+] Content from {link} written to file: {content_filename}")

        # Terminate Tor process if it was started
        if args.tor and tor_process:
            tor_process.terminate()
            print("[+] Tor service terminated.")

    except KeyboardInterrupt:
        print("\n[+] Program interrupted by user. Exiting gracefully.")
        # Perform any necessary cleanup here
        if tor_process is not None and tor_process.poll() is None:
            tor_process.terminate()
            print("[+] Tor service terminated.")
        sys.exit(0)

if __name__ == "__main__":
    main()

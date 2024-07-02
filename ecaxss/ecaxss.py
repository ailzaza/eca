import argparse
from lib.helper.Log import Log
from lib.core import core
from lib.crawler.crawler import crawler

# Tambahkan user-agents yang tersedia
user_agents = {
    "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "brave": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Brave/1.27.108",
    "edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.54 Safari/537.36 Edg/91.0.864.54"
}

def check():
    payload = core.generate(6)  # Menggunakan level payload default 6
    return payload

def main():
    parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, usage="ecaxss.py [options]", add_help=False)
    pos_opt = parse.add_argument_group("Options")
    pos_opt.add_argument("-h", "--help", action="store_true", default=False, help="Show this help message and exit")
    pos_opt.add_argument("-u", "--url", metavar="", help="Target URL (e.g. https://example.com)")
    pos_opt.add_argument("-a", "--agent", metavar="", choices=user_agents.keys(), help="User-Agent (options: firefox, chrome, brave, edge)")

    getopt = parse.parse_args()

    if getopt.help:
        parse.print_help()
        exit(0)

    if not (getopt.url and getopt.agent):
        print("Command tidak sesuai, untuk bantuan tekan -h")
        exit(1)

    Log.info("Starting ecaxss...")
    selected_method = user_choice()

    # Mengatur User-Agent
    user_agent = user_agents[getopt.agent]
    Log.info(f"Using User-Agent: {user_agent}")

    if getopt.url:
        if "mhs_jadkul.php" in getopt.url:
            results = core.main(getopt.url, check(), selected_method, user_agent) or []
            crawler_results = crawler.crawl(getopt.url, check(), selected_method, user_agent) or []
        else:
            print("URL yang diberikan tidak sesuai dengan endpoint yang diinginkan.")
    else:
        print("No target URL provided. Use -u <URL> to specify the target.")

    Log.generate_report()

def user_choice():
    print("Pilih method yang ingin digunakan:")
    print("1. Method GET")
    print("2. Method POST")
    print("3. Method GET dan POST")

    try:
        choice = int(input("Masukkan pilihan (1/2/3): "))
        if choice == 1:
            return 0  # GET
        elif choice == 2:
            return 1  # POST
        elif choice == 3:
            return 2  # GET dan POST
        else:
            print("Pilihan tidak valid, menggunakan default (GET dan POST)")
            return 2  # Default GET dan POST
    except ValueError:
        print("Input tidak valid, menggunakan default (GET dan POST)")
        return 2  # Default GET dan POST

if __name__ == "__main__":
    main()

import argparse

def read_user_cli_args():
    """Handle CLI args and options"""
    parser = argparse.ArgumentParser(description='Check if a website is up or down')
    parser.add_argument('--urls', "-u", metavar="URLS", nargs="+", type=str, default=[], help='enter one or more website URLs')
    parser.add_argument("--input-file", "-f", metavar="FILE", type=str, default=None, help="enter a file with URLs")
    parser.add_argument("--asynchronous", "-a", action="store_true", help="check websites asynchronously")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args() 
    return args

def display_check_results(result, url, error=""):
    """Display results of the check"""
    print(f"status for {url}: ", end=" ")
    if result:
        print("Online! 🤘🏼")
    else:  
        print("Offline! 😭")
        if error:
            print(f"Error: {error}")
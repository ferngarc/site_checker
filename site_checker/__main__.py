import asyncio
import pathlib
import sys
from site_checker.checker import site_is_online, site_is_online_async, site_is_online_async
from site_checker.cli import read_user_cli_args, display_check_results

def main():
    """Run site checker"""
    user_args = read_user_cli_args()
    urls = _get_websites_to_check(user_args)
    if not urls:
        print("No URLs to check! Exiting...")
        sys.exit(1)
    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)


def _get_websites_to_check(user_args):
    """Get websites to check"""
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_files(user_args.input_file)
    return urls

def _read_urls_from_files(file):
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with open(file_path, "r") as f:
            urls = [url.strip() for url in f.readlines()]
            if urls:
                return urls
            print(f"Erorr: {file} is empty!",
                file=sys.stderr)
    else:
        print(f"Error: {file} does not exist!",
            file=sys.stderr)
    return []

async def _asynchronous_check(urls):    
     """Check websites asynchronously"""
     async def _check(url):
        error = ""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_results(result, url, error)
     await asyncio.gather(*(_check(url) for url in urls))

def _synchronous_check(urls):
    """Check websites synchronously"""
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_results(result, url, error)


if __name__ == "__main__":
    main()
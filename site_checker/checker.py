import asyncio
import aiohttp

from http.client import HTTPConnection
from urllib.parse import urlparse


def site_is_online(url, timeout=2):
    """
    Check if site is online
    :param url: url to check
    :param timeout: timeout in seconds
    :return: True if site is online, False otherwise
    """
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for port in (80, 443):
        conn = HTTPConnection(host=host, port=port, timeout=timeout)
        try:        
            conn.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            conn.close()
    raise error
    

async def site_is_online_async(url, timeout=2):
    """Return True if the target URL is online. 
    Reaise an exception otherwise."""
    error = Exception("Unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for scheme in ("http", "https"):
        target_url = f"{scheme}://{host}"
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception("Timeout error")
            except Exception as e:
                error = e
    raise error
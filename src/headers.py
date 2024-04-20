import random
def get_headers(authority, method, path):
    headers = {
        "authority": authority,
        "method": method,
        "path": path,
        "scheme": "https",
        "accept": "text/html, application/xhtml+xml,application/xml;q=0.9, image/webp, image/apng,*/*;q=0.8,application/signed-exchange; v=b3;q=0.9",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language": "en-GB, en-US; q=0.9, en; q=0.8",
        "upgrade-insecure-requests": "1",
        "user-agent" : random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) Applewebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
            ])
    }
    return headers
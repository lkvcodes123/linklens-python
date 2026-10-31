"""Educational URL heuristics; does not fetch or certify websites."""
import ipaddress
import re
from urllib.parse import urlsplit


def analyze(raw):
    if not isinstance(raw, str):
        raise ValueError('Enter a website address.')
    raw = raw.strip()
    if not raw or re.search(r'\s', raw):
        raise ValueError('Enter a website address without spaces.')
    if len(raw) > 8192:
        raise ValueError('Address is too long (maximum 8192 characters).')
    if not re.match(r'^https?://', raw, re.I):
        if re.match(r'^[a-z][a-z0-9+.-]*:', raw, re.I) and not re.match(r'^[-\w.]+:\d+(/|$)', raw):
            raise ValueError('Only HTTP and HTTPS addresses are supported.')
        raw = 'https://' + raw
    try:
        url = urlsplit(raw)
        host = (url.hostname or '').encode('idna').decode('ascii').lower()
        port = url.port
    except (ValueError, UnicodeError):
        raise ValueError('That website address is not valid.') from None
    if not host or '\\' in url.netloc or '%' in host:
        raise ValueError('That website address is not valid.')
    try:
        ipaddress.ip_address(host)
        is_ip = True
    except ValueError:
        is_ip = False
    if not is_ip and (len(host) > 253 or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', p) for p in host.rstrip('.').split('.'))):
        raise ValueError('That domain name is not valid.')
    if '.' not in host and not is_ip and host != 'localhost':
        raise ValueError('Enter a complete domain, such as example.com.')
    notes = []
    score = 0

    def add(title, detail, weight):
        nonlocal score
        notes.append({'title': title, 'detail': detail})
        score += weight

    if url.scheme == 'http':
        add('Unencrypted connection', 'HTTP does not encrypt information sent to this website.', 2)
    if url.username is not None or url.password is not None:
        add('Disguised destination', f'Text before @ is user information. The actual host is {host}.', 4)
    if 'xn--' in host:
        add('Internationalized domain', 'Encoded characters can resemble other domains. Verify the spelling carefully.', 2)
    if is_ip:
        add('IP address instead of a domain', 'Numeric addresses obscure identity; they can also be legitimate.', 2)
    if host == 'localhost' or host.endswith(('.local', '.localhost')):
        add('Local address', 'This address refers to a local network or device.', 2)
    if len(host.split('.')) > 4:
        add('Many domain levels', 'Long subdomain chains can hide the real destination.', 2)
    for brand in ['paypal', 'google', 'microsoft', 'apple', 'amazon', 'facebook', 'netflix', 'instagram']:
        if brand in host and host != brand + '.com' and not host.endswith('.' + brand + '.com'):
            add('Possible brand impersonation', f'The host mentions {brand} but is not under {brand}.com. This alone is not proof of phishing.', 3)
            break
    if host in ['bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd', 'buff.ly']:
        add('Shortened link', 'The final destination is hidden. This checker does not follow redirects.', 2)
    if host.count('-') >= 3:
        add('Unusually hyphenated domain', 'Multiple hyphens can be used to make a misleading name.', 1)
    if re.search(r'verify|secure|account|login|password|wallet', host, re.I):
        add('Sensitive-action wording in host', 'Account or security wording can create false trust.', 1)
    if re.search(r'\.(exe|msi|scr|bat|cmd|apk|dmg|ps1|zip)$', url.path, re.I):
        add('Potential download', 'This address appears to point to an executable, installer, script, or archive.', 3)
    if port and port not in (80, 443):
        add('Unusual port', f'This URL uses a nonstandard website port: {port}.', 1)
    if len(raw) > 220:
        add('Very long address', 'Long addresses make destinations harder to inspect.', 1)
    return {'host': host, 'notes': notes, 'score': score, 'https': url.scheme == 'https'}

from urllib import request
from urllib.error import HTTPError
import json

REPO = 'ericjohnson00456-afk/xiaoling-esp32'


def fetch_releases():
    url = f'https://api.github.com/repos/{REPO}/releases'
    with request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))


def fetch_latest_release():
    url = f'https://api.github.com/repos/{REPO}/releases/latest'
    try:
        with request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError:
        return None


if __name__ == '__main__':
    latest_release = fetch_latest_release()
    releases = fetch_releases()

    data = [{
        'name': release['name'],
        'kind': 'latest' if latest_release and release['id'] == latest_release['id']
        else 'prerelease' if release['prerelease']
        else None,
        'tag': release['tag_name'],
        'url': release['html_url'],
        'assets': [{
            'name': asset['name'],
            'board': '_'.join(asset['name'].split('_')[1:-1]),
            'url': asset['browser_download_url'],
        } for asset in release['assets'] if asset['name'].startswith('xiaoling_')
            and asset['name'].endswith(f'_{release['name']}.zip')],
    } for release in releases]

    print(json.dumps(data))

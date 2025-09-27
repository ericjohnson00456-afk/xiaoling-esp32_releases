from urllib import request
from urllib.error import HTTPError
import json
from argparse import ArgumentParser

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


def is_for_version(name, version):
    return name.startswith('xiaoling_') and name.endswith(f'_{version}.zip')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--json', action='store_true',
                        help='Output releases as JSON')
    parser.add_argument('--urls',
                        help='Output only the download URLs for the specified version')
    args = parser.parse_args()

    latest_release = fetch_latest_release()
    releases = fetch_releases()

    if args.json:
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
                'url': f'https://raw.githubusercontent.com/{REPO}_releases/refs/tags/{release['name']}/{asset['name']}',
            } for asset in release['assets'] if is_for_version(asset['name'], release['name'])],
        } for release in releases]
        print(json.dumps(data))
    elif args.urls:
        for release in releases:
            if release['name'] == args.urls:
                for asset in release['assets']:
                    if is_for_version(asset['name'], release['name']):
                        print(asset['browser_download_url'])
                break

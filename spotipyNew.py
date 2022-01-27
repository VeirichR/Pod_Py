import spotipy
from spotipy.oauth2 import SpotifyOAuth
import scraper

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public",
                                               client_id='your-client-id',
                                               client_secret='your-client-secret',
                                               redirect_uri='http://127.0.0.1:9090',
                                               ))


def create_playlist():
    '''
    Create a new playlist and get his ID
    :return: new_playlist_id: string
    '''
    sp.user_playlist_create('veirich', 'PodPy')
    get_new_playlist_id = sp.user_playlists('veirich')
    new_playlist_id = get_new_playlist_id['items'][0]['id']
    return new_playlist_id


def get_library_pods():
    '''
    Get the name and URL from all the podcasts in my library
    :return: name_url: dict with {name: url}
    '''
    playlists = sp.current_user_saved_shows()
    print('==> Searching Podcasts in the library...')
    name_url = {playlists['items'][i]['show']['name']: playlists['items'][i]['show']['external_urls']['spotify']
                for i in range(playlists['total'])}  # get name and url
    return name_url


def list_breaker(name_url):
    '''
    Breake the dict in two lists, name and url, name[0] and url[0] are from the same show
    :param name_url:
    :return: l_urls: list with not played episodes URLs
    '''
    # breaking the information in two lists to facilitate the do_it function
    l_names = [key for key in name_url.keys()]
    l_links = [url for url in name_url.values()]
    l_urls = scraper.do_it(l_names, l_links)
    return l_urls


def cleaner(l_urls):
    '''
    Use the URl to get the URI with sp.episode
    :param l_urls:
    :return: l_uris: list: not played episodes URIs
    '''
    l_uris = []
    print('==> Cleaning the information...')
    # sp.episode get the episode URL and show every information. Saving the URI in a list
    for episode in l_urls:
        uri = sp.episode(episode)
        l_uris.append(uri['uri'])
    return l_uris


def playlist_add_shows(l_uris, new_playlist_id):
    '''
    Break the URI list in max 100 items, sp.playlist_add_items doesnt accept more than 100 each time
    :param l_uris: list: not played episodes URIs
    :param new_playlist_id: string with the id
    :return:
    '''
    n = 100
    l_divided = [l_uris[i:i + n] for i in range(0, len(l_uris), n)]
    # Passing every list to be add
    for i in range(len(l_divided)):
        sp.playlist_add_items(playlist_id=new_playlist_id, items=l_divided[i], position=None)
    print('==> Success, all episodes have been added!')


def start():
    '''
    Start all functions...
    :return:
    '''
    new_playlist_id = create_playlist()
    name_url = get_library_pods()
    l_urls = list_breaker(name_url)
    l_uris = cleaner(l_urls)
    playlist_add_shows(l_uris, new_playlist_id)

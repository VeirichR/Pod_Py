import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


def do_it(l_names, l_links):
    """
    Get the lists of names and url of my library shows, in order, name[0] and url[0] are from the same show,
    loop them and get the not played podcasts URLs
    :param l_names: list of episodes names
    :param l_links: list of episodes url
    :return: all_not_plyd: list with all the episodes not played URLs
    """
    try:
        chrome = ChromeAuto()

        all_not_plyd = []
        print('==> Plz wait... searching episodes...')
        try:
            for i in range(len(l_links)):
                print(f'    ==> Getting {l_names[i]} episodes...')
                logging.info(f'Searching episodes from {l_names[i]}')
                chrome.access(l_links[i])
                sleep(5)
                nt_played = chrome.get_urls_not_played()
                all_not_plyd.extend(nt_played)
                sleep(2)
            print(f'==> {len(all_not_plyd)} episodes found!')
        except Exception as error:
            print(f'==> Podcast loop error...')
            logging.error(f'==> Podcast loop error... {error}')

        finally:
            chrome.quit()

            return all_not_plyd
    except Exception as error:
        print(f'==> ChromeAuto error...')
        logging.error(f'==> ChromeAuto error... {error}')


class ChromeAuto:
    def __init__(self):
        self.driver_path = 'chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('user-data-dir=C:/Users/renat/PycharmProjects/selenium/Perfil')
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def access(self, link):
        """
        Open the link from the param on chrome
        :param link: URL
        :return:
        """
        try:
            self.chrome.get(link)
            logging.info(f'Chrome access ==> {link}')
        except Exception as error:
            print(f'Fail to access {link}')
            logging.error(f'Fail to access link! {error}')

    def quit(self):
        """
        Close chrome
        :return:
        """
        try:
            self.chrome.quit()
            logging.info(f'Chrome quit')
        except Exception as error:
            print('Fail to quit Chrome!')
            logging.error(f'Fail to quit Chrome! {error}')

    def get_urls_not_played(self):
        """
        Search in a dict for not played episodes and append them on a list
        :return: urls: list with episodes not played
        """
        try:
            urls = []
            dic_pods, names_podcast = self.search_url_names()
            l_names = self.search_not_played(names_podcast)

            # pega apenas os urls dos podcasts not played
            for key, item in dic_pods.items():
                if key in l_names:
                    urls.append(item)

            return urls
        except Exception as error:
            print(f'Fail to get not played URLs')
            logging.error(f'Fail to get not played URLs {error}',)

    def search_url_names(self):
        """
        Get episodes names and url in the podcast page.
        :return: dic_pods: dict with episodes names and url
        :return: nomes_podcast: list with all episodes from the shown on my library
        """
        try:
            dic_pods = {}
            names_podcast = self.chrome.find_elements(By.CLASS_NAME, 'V0pEigrddg3VxP_sTdAJ')
            l_url = [my_elem.get_attribute("href") for my_elem in
                     self.chrome.find_elements(By.CLASS_NAME, "g5gZaZVzR0tGT4pK6iEU")]
            for i in range(len(names_podcast)):
                dic_pods[names_podcast[i].text] = l_url[i]

            return dic_pods, names_podcast
        except Exception as error:
            print(f'Fail to get episodes data!')
            logging.error(f'Fail to get episodes data! {error}')

    def search_not_played(self, names_podcast):
        """
        Get a list with all the episodes names and delete all the played ones.
        :param names_podcast: list with every episode name
        :return: l_names: list with not played episodes
        """
        try:
            l_names = []
            pods_played = self.chrome.find_elements(By.CLASS_NAME, 'y9kEPjDek0J80YRf8JJw')
            # cria uma lista com todos os nomes dos podcasts not played
            for i in range(len(names_podcast)):
                if 'Played' not in pods_played[i].text:
                    l_names.append(names_podcast[i].text)
                    logging.info(f' ==> Episode {names_podcast[i].text} found')

            return l_names
        except Exception as error:
            print(f'Error trying to get not played episodes!')
            logging.error(f'Error trying to get not played episodes! {error}')

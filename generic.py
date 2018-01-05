import bs4 as bs
import urllib
from urllib import request
import os.path
import ast
from Python.help_me import *


class RecipeParse(object):
    def __init__(self, url):
        """
        Generates generic RecipeParse object
        :param url: Input url
        :return: None
        """
        self.url = url
        self.soup = self.lets_get_soup()
        self.title = ''
        self.img_url = ''
        self.recipe_yield = ''
        self.ingredients = {}
        self.instructions = []

    def __str__(self):
        """
        Generates markdown styled string
        :"""
        return: None

    def lets_get_soup(self):
        """
        Gets BeautifulSoup object from url
        :return: False or BeautifulSoup object
        """
        try:
            # pretend to be Firefox
            req = urllib.request.Request(self.url,
                                         headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as url_file:
                url_byte = url_file.read()
        except urllib.request.HTTPError as e:  # HTTP status code
            print(e.__str__())
            return False
        except urllib.request.URLError as e:  # General Error
            print(e.__str__())
            return False
        except OSError as e:  # Vague Error
            print(e.__str__())
            return False
        except Exception as e:  # Anything
            print(e.__str__())
            return False

        try:
            url_string = url_byte.decode(encoding='latin1').encode(
                encoding='utf-8')
        except UnicodeDecodeError as e:
            print(e.__str__())
            return False
        except Exception as e:
            print(e.__str__())
            return False
        return bs.BeautifulSoup(url_string, "html.parser")


    def make_markdown(self):
            """
            Creates and writes markdown styled recipe to a file
            :return: True or IOError is raised
            """
            new_file = ''
            directory = os.path.dirname(os.path.dirname(__file__)) + "/Recipes/"
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                self.title = ''.join(c for c in self.title if 0 < ord(c) < 127)
                if os.path.isfile(directory + self.title + ".md"):
                    raise FileExistsError
                x = str(directory + self.title + ".md")
                new_file = open(x, "w")
                new_file.write(self.__str__())
            except FileExistsError:
                raise FileExistsError(directory + self.title + ".md")
            except IOError:
                raise IOError
            except:
                raise Exception
            finally:
                if new_file:
                    try:
                        new_file.close()
                    except IOError:
                        raise IOError
                    except Exception:
                        raise Exception
            return True

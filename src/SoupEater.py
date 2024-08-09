from bs4 import BeautifulSoup
import json
import re
import logging
import logging.config
import yaml

try:
    logConf = yaml.safe_load(open("./logging.yaml").read())
    logging.config.dictConfig(logConf)
except OSError as e:
    print("Imposible configurar el logger")
    print(e.filename)
else:
    myLogger = logging.getLogger(__name__)


def munch(assist):
    name = assist["name"]
    clas = assist["class"]
    try:
        if assist["sameLevel"] == "True":
            sameLevel = True
    except:
        sameLevel = False
    try:
        struct = assist["struct"]
    except:
        struct = None
    return name, clas, sameLevel, struct


def digest(name, clas, page):
    res = page.find(name, {"class": clas})
    return res


class SoupEater():
    def __init__(self):
        self.myLogger = myLogger
        self.soup = None
        self.product = None
        self.web = None

    def prepare(self, product, web):
        self.product = product
        self.web = web

    def boil(self, data):
        self.soup = BeautifulSoup(data, 'html.parser')

    def eat(self):
        nums = re.compile(r"€?\d+(.|,)?\d+€?")
        self.myLogger.debug("Iniciant cerca de variables")
        struct = self.web["struct"]
        res = self.soup
        try:
            while True:
                name, clas, sameLevel, struct = munch(struct)
                if not sameLevel:
                    res = digest(name, clas, res)
                else:
                    temp = digest(name, clas, res)
                if struct is None:
                    preu = str(res.contents[0])
                    try:
                        alt = str(res.contents[1])
                    except:
                        alt = ".0"
                    break
        except:
            self.myLogger.error("Error en la definició de la variable", exc_info=True)
            raise
        else:
            preu = float(nums.search(preu).group(0).replace(",", "."))
            preu2 = float(nums.search(alt).group(0).replace(",", "."))
            self.myLogger.debug("Producte " + str(self.product) + " trobat. Preus: " + str(preu) + " i " + str(preu2))
            return preu, preu2


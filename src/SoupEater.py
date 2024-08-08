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
        nums = re.compile(r"[+-]?\d+(.|,)?\d+")
        self.myLogger.info("Iniciant cerca de variables")
        assist = self.web["struct"]
        res = self.soup
        try:
            while True:
                try:
                    next = assist["struct"]
                except:
                    next = ""
                if next == "":
                    i = 0
                    for name in assist["name"]:
                        tmp = res.find(name, {"class": assist["class"][i]})
                        if assist["class"][i] == "name":
                            name = str(tmp.contents[0])
                            continue
                        preu = str(tmp.contents[0])
                        try:
                            alt = str(tmp.contents[1])
                        except:
                            alt = "0"
                        i += 1
                    break
                assist = assist["struct"]
        except:
            self.myLogger.error("Error en la definició de la variable", exc_info=True)
            raise
        else:
            preu = float(nums.search(preu).group(0).replace(",", "."))
            preu2 = float(nums.search(alt).group(0).replace(",", "."))
            self.myLogger.info("Producte " + name + " trobat. Preus: " + str(preu) + " i " + str(preu2))
            return name, preu, preu2
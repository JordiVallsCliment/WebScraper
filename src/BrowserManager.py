import http.cookiejar as cookiejar
import mechanize

class BrowserManager():

    def __init__(self, config, myLogger):
        cj = cookiejar.CookieJar()
        self.br = mechanize.Browser()
        self.br.set_cookiejar(cj)
        self.config = config
        self.myLogger = myLogger

    def login(self, name):
        self.myLogger.info("Intentant login a la pàgina " + name)
        try:
            webs = self.config["webs"]
            web = webs[name]
            self.br.open(web["login"])
            try:
                self.br.select_form(name=web["form"])
            except:
                self.br.select_form(id=web["form"])
            try:
                self.br.form[web["userField"]] = web["usr"]
                self.br.form[web["passField"]] = web["pass"]
            except:
                self.myLogger.error("Identificadors de camps de usuari o contrasenya erronis", exc_info=True)
            self.myLogger.info("Iniciant sessió amb la pàgina...")
            try:
                self.br.submit()
            except:
                self.myLogger.error("Error durant l'entrega del formulari", exc_info=True)
            msgs = ["incorrecto", "error"]
            for msg in msgs:
                if str(self.br.response().read()).lower().__contains__(msg):
                    return False
            self.myLogger.info("Login correcte")
            return True
        except:
            self.myLogger.error("Error durant el procés de login", exc_info=True)
            return False

    def logout(self):
        self.br.close()

    def get(self, url):
        return self.br.open(url)

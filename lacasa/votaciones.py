import csv
import random
import time

from icecream import ic
from loguru import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from cfg import osenv
from cfg.webbrowser import WebBrowser, WebBrowserType

ic.configureOutput(includeContext=True)


class Target:

    def __init__(self, id_target: str, css_selector: str, tipo_votacion: str, votos: int = 0):
        self.id_target = id_target
        self.css_selector = css_selector
        self.tipo_votacion = tipo_votacion
        self.votos = votos

    def get_votos(self):
        return self.votos

    def sumar_voto(self):
        self.votos += 1

    def __str__(self):
        return f"{{ID_TARGET: {self.id_target}, CSS_SELECTOR: {self.css_selector}, TIPO_VOTACION: {self.tipo_votacion}, VOTOS: {self.votos}}}"

    def __repr__(self):
        return f"{{ID_TARGET: {self.id_target}, CSS_SELECTOR: {self.css_selector}, TIPO_VOTACION: {self.tipo_votacion}, VOTOS: {self.votos}}}"


class Votaciones:
    URL_VOTACIONES = osenv.get("URL_VOTACIONES")

    def __init__(self, multiple: bool = False):
        self.multiple = multiple
        self.targets = self._load_targets()
        if osenv.get("WEBBROWSER_TYPE") == WebBrowserType.FIREFOX.value:
            self.wb = WebBrowser(type_of_browser=WebBrowserType.FIREFOX)
        else:
            self.wb = WebBrowser()

    def _load_targets(self) -> [Target]:
        targets = []
        with open(osenv.get("CSV_TARGETS"), "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            [targets.append(Target(id_target=fila['ID_TARGET'], css_selector=fila['CSS_SELECTOR'],
                                   tipo_votacion=fila['TIPO_VOTACION'])) for fila in
             csv_reader]

        return targets

    def votar(self, target: Target = None) -> Target:
        self.wb.open()
        self.wb.go_to(self.URL_VOTACIONES)
        self.wb.driver.implicitly_wait(2)
        target = random.choice(self.targets) if not target else target

        try:

            btn_target = self.wb.driver.find_element(By.CSS_SELECTOR, target.css_selector)
            btn_target.click()

            time.sleep(1)
            self.wb.quit()

            # TODO: Verificar que el voto ha sido exitoso antes de sumar voto
            target.sumar_voto()

            while self.multiple:
                self.wb.open()
                self.wb.go_to(self.URL_VOTACIONES)

                target = random.choice(self.targets)
                btn_target = self.wb.driver.find_element(By.CSS_SELECTOR, target.css_selector)
                btn_target.click()

                time.sleep(1)
                self.wb.quit()

                # TODO: Verificar que el voto ha sido exitoso antes de sumar voto
                target.sumar_voto()

        except NoSuchElementException:
            logger.warning(f"No se encuentra target: {target}")
            self.wb.quit()
        finally:
            return target

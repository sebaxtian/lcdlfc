import csv
import random
import time
from enum import Enum
from typing import Dict

from icecream import ic
from loguru import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from cfg import osenv
from cfg.webbrowser import WebBrowser, WebBrowserType

ic.configureOutput(includeContext=True)


class Prioridad(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


class Target:

    def __init__(self, id_target: str, css_selector: str, tipo_votacion: str, prioridad: Prioridad = Prioridad.ALTA,
                 votos: int = 0):
        self.id_target = id_target
        self.css_selector = css_selector
        self.tipo_votacion = tipo_votacion
        self.prioridad = prioridad
        self.votos = votos

    def get_votos(self):
        return self.votos

    def sumar_voto(self):
        self.votos += 1

    def __str__(self):
        return f"{{ID_TARGET: {self.id_target}, CSS_SELECTOR: {self.css_selector}, TIPO_VOTACION: {self.tipo_votacion}, PRIORIDAD: {self.prioridad}, VOTOS: {self.votos}}}"

    def __repr__(self):
        return f"{{ID_TARGET: {self.id_target}, CSS_SELECTOR: {self.css_selector}, TIPO_VOTACION: {self.tipo_votacion}, PRIORIDAD: {self.prioridad}, VOTOS: {self.votos}}}"


class Votaciones:
    URL_VOTACIONES = osenv.get("URL_VOTACIONES")

    def __init__(self, multiple: bool = False):
        self.multiple = multiple
        if osenv.get("WEBBROWSER_TYPE") == WebBrowserType.FIREFOX.value:
            self.wb = WebBrowser(type_of_browser=WebBrowserType.FIREFOX)
        else:
            # Chrome
            self.wb = WebBrowser()

    @staticmethod
    def load_targets() -> Dict[str, Target]:
        targets: Dict[str, Target] = {}

        with open(osenv.get("CSV_TARGETS"), "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for fila in csv_reader:
                match fila['PRIORIDAD']:
                    case "BAJA":
                        p = Prioridad.BAJA
                    case "MEDIA":
                        p = Prioridad.MEDIA
                    case "ALTA":
                        p = Prioridad.ALTA
                    case _:
                        p = Prioridad.BAJA

                t = Target(id_target=fila['ID_TARGET'], css_selector=fila['CSS_SELECTOR'],
                           tipo_votacion=fila['TIPO_VOTACION'], prioridad=p)

                targets[fila['ID_TARGET']] = t

        return targets

    @staticmethod
    def choice_target(targets: Dict[str, Target]):
        # Selecciona aleatoriamente un target usando los pesos de las prioridades
        prioridades = [t[1].prioridad.value for t in list(targets.items())]
        return random.choices(list(targets.items()), weights=prioridades)[0][1]

    def votar(self) -> Dict[str, Target]:
        self.wb.open()
        self.wb.go_to(self.URL_VOTACIONES)
        self.wb.driver.implicitly_wait(2)

        # Los targets son cargados una sola vez al llamar el metodo
        targets = Votaciones.load_targets()

        # Selecciona aleatoriamente un target usando los pesos de las prioridades
        target = Votaciones.choice_target(targets)

        try:
            btn_target = self.wb.driver.find_element(By.CSS_SELECTOR, target.css_selector)
            # time.sleep(10)
            btn_target.click()

            time.sleep(1)
            self.wb.quit()

            # TODO: Verificar que el voto ha sido exitoso antes de sumar voto
            target.sumar_voto()

            # Actualiza el target en los targets
            targets[target.id_target] = target

            while self.multiple:
                self.wb.open()
                self.wb.go_to(self.URL_VOTACIONES)
                self.wb.driver.implicitly_wait(2)

                # Selecciona aleatoriamente un target usando los pesos de las prioridades
                target = Votaciones.choice_target(targets)

                btn_target = self.wb.driver.find_element(By.CSS_SELECTOR, target.css_selector)
                # time.sleep(10)
                btn_target.click()

                time.sleep(1)
                self.wb.quit()

                # TODO: Verificar que el voto ha sido exitoso antes de sumar voto
                target.sumar_voto()

                # Actualiza el target en los targets
                targets[target.id_target] = target

        except NoSuchElementException:
            logger.warning(f"No se encuentra target: {target}")
            self.wb.quit()
        finally:
            return targets

# This is a main Python script.
import csv
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from typing import Dict

import pendulum
from icecream import ic
from loguru import logger

from cfg import osenv
from lacasa.votaciones import Votaciones, Target


def set_logger_datetime(record):
    record['time'] = pendulum.now("America/Bogota")


logger.configure(patcher=set_logger_datetime)
logger.add(
    f"logs/lcdlfc_{pendulum.now('America/Bogota').to_iso8601_string()}.log",
    rotation="20 MB",
    level="DEBUG",
    format="{time} - {level} - {name} - {message}",
)

ic.configureOutput(includeContext=True)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def export_data(targets: [Dict[str, Target]]) -> None:
    now_iso8601 = pendulum.now("America/Bogota").to_iso8601_string()
    filename = f"data/targets_{now_iso8601}.csv"

    with open(filename, "w") as csv_file:
        header = ["DATETIME", "ID_TARGET", "CSS_SELECTOR", "TIPO_VOTACION", "PRIORIDAD", "VOTOS"]
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for target in targets:
            target = target.__dict__
            target = {key.upper(): value for key, value in target.items()}
            target['PRIORIDAD'] = str(target['PRIORIDAD']).split('.')[1]
            target['DATETIME'] = now_iso8601
            writer.writerow(target)

    logger.info(f"Datos exportados: {filename}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    num_threads = int(osenv.get("NUM_THREADS")) if int(osenv.get("NUM_THREADS")) < 9 else 8
    multiples_votos = True if osenv.get("MULTIPLES_VOTOS") == "True" else False
    targets: [Target] = Votaciones.load_targets()

    logger.info(f"Numero de threads: {num_threads}")
    logger.info(f"Multiples votos: {multiples_votos}")
    ic(targets)

    # Create a ThreadPoolExecutor with maximum 8 threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor and create threads
        threads = {}
        for i in range(num_threads):
            t = executor.submit(Votaciones(multiple=multiples_votos).votar)
            threads[f"Thread{i}"] = t

        # Wait for all threads to complete
        wait(threads.values())

        # Print targets
        [ic(key, thread.result()) for key, thread in threads.items()]

        # Logger targets
        [logger.info(f"{key} : {thread.result()}") for key, thread in threads.items()]

        # Obtener el total de votos
        total_votos = sum(target.votos for thread in threads.values() for target in thread.result().values())
        ic(total_votos)

        # Logger total votos
        logger.info(f"Total votos: {total_votos}")

        # Export data
        export_data([target for thread in threads.values() for target in thread.result().values()])

import logging
import time
import os


def generate_rename_log(old_dirfiles: list[str], new_dirfiles: list[str], midia_name: str, season: int, directory: str):
    
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')

    log_path = ".\\logs"
    
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path, exist_ok=True) # Ensure the log directory exists
    except OSError as e:
        logger.error(f"ERROR - - -> CAN'T CREATE A LOG DIRECTORY: {e}")

    logs_qty = len(os.listdir(log_path))
    log_file_path = os.path.join(log_path, f"rename_log_{logs_qty + 1}_{time.strftime('%d%m%Y%H%M%S', time.localtime())}.txt")

    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"GENERATED AT [{time.strftime('%d/%m/%Y - %H:%M:%S', time.localtime())}] FOR [{midia_name}] SEASON [{season}]") # Time format "day/month/year - hour:minute:second"
    logger.info(f"\n- - -> AFFECTED DIRECTORY PATH [{directory}]\n")

    files_qty = (len(old_dirfiles) + len(new_dirfiles)) // 2
    errors = []

    if ((files_qty % 2) != 0):
        if len(old_dirfiles) > len(new_dirfiles):
            for i in range(len(old_dirfiles), len(new_dirfiles), -1):
                errors.append(f"ERROR -> THE FILE [{old_dirfiles[i-1]}] WASN'T CHANGED BEACAUSE THERE WERE ANY CORRESPONDING NEW FILE NAME TO IT")
                old_dirfiles.pop(i-1)
        elif len(new_dirfiles) > len(old_dirfiles):
            for i in range(len(new_dirfiles), len(old_dirfiles), -1):
                errors.append(f"ERROR -> THE FILE [{new_dirfiles[-1]}] WASN'T CHANGED BEACAUSE THERE WERE ANY CORRESPONDING OLD FILE NAME TO IT")
                new_dirfiles.pop(i-1)

    files_qty = int((len(old_dirfiles) + len(new_dirfiles)) / 2)

    logger.info("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
    pipe = "|"
    for i in range(files_qty):
        logger.info(f"| OLD FILE NAME: {old_dirfiles[i].ljust(60)} | NEW FILE NAME: {new_dirfiles[i]} {pipe.rjust(51 - len(new_dirfiles[i]))}")

    logger.info("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

    if errors:
        for error in errors:
            logger.info(f"\n{error}")

    print(f"\nLOG GENERATED. YOU CAN LOOK AT THE EXPECTED RESULT IN THE LOGS FILES, PATH: [{log_file_path}].")


def generate_join_log():
    pass
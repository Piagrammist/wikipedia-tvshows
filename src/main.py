import logging
import ui

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s ~ %(module)s ~ %(levelname)s]: %(message)s',
                        datefmt='%m/%d %H:%M:%S', level=logging.INFO)
    ui.main()

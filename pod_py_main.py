import spotipyNew
import timeit
import logging


def main():
    start = timeit.default_timer()
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')

    spotipyNew.start()

    logging.info('Finished')
    end = timeit.default_timer()
    runtime = f'==> Runtime = {end - start:.2f} secs'
    logging.info(runtime)
    print(runtime)


if __name__ == '__main__':
    main()

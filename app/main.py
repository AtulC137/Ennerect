from pprint import pprint

from readers.csv_reader import CSVReader
from describe import Describe


def main():

    reader = CSVReader("app/data/random_numbers.csv")

    obj = Describe(reader)

    pprint(obj.describe())


if __name__ == "__main__":
    main()
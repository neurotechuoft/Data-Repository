import csv

from scipy import io
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process file name')
    parser.add_argument('-f', '--file', help='MATLAB file to convert')
    parser.add_argument('-o', '--output', help='CSV file to write to')

    args = parser.parse_args()
    matlab_file = args.file
    output_file = args.output

    matlab_dict = io.loadmat(matlab_file)

    print(matlab_dict)

    print(matlab_dict.keys())

    listWriter = csv.DictWriter(
        open(output_file, 'w'),
        fieldnames=list(matlab_dict.keys())[1:],
    )

    listWriter.writeheader()

    for key in matlab_dict:
        print()
        listWriter.writerow(key)

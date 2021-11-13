import os
import argparse

def run_everything(name, year_start, year_end):
    os.system(f'python load_data.py {year_start} {year_end} {name}')
    os.system(f'python preprocess_data.py {name}')
    os.system(f'python predict_scores.py {name}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script for downloading game data.')
    parser.add_argument('year_start', type=int)
    parser.add_argument('year_end', type=int)
    parser.add_argument('data_name', type=str)

    args = parser.parse_args()

    year_start, year_end = args.year_start, args.year_end
    name = args.data_name

    run_everything(name, year_start, year_end)

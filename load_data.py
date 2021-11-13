import argparse
import pandas as pd
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def load_data(year_start, year_end):
    every_seasons = pd.DataFrame()
    for year in range(year_start, year_end + 1):
        if year == 19:
            url = ('https://fbref.com/en/comps/9/schedule/Premier-League-Fixtures')
        else:
            if year == 14:
                marker = 733
            elif year == 15:
                marker = 1467
            elif year == 16:
                marker = 1526
            elif year == 17:
                marker = 1631
            else:
                marker = 1889
            url = 'https://fbref.com/en/comps/9/' + str(marker) + '/schedule/20' + str(year) + '-20' + str(year+1) +'-Premier-League-Fixtures'
        season = pd.read_html(url)[0]

        season['season'] = year

        every_seasons = every_seasons.append(season)

    every_seasons.drop(columns=['Day', 'Date', 'Time', 'xG', 'xG.1', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes'], inplace=True)
    newest_week = every_seasons[every_seasons['Score'].isna()]['Wk'].min()
    every_seasons = every_seasons[(~every_seasons['Score'].isna()) | (every_seasons['Wk'] == newest_week)]
    every_seasons.sort_values(['season', 'Wk'], inplace=True)
    every_seasons.reset_index(drop=True, inplace=True)
    return every_seasons

def save_data(data, name):
    data.to_csv('./Data/' + name + '.csv')

if __name__ == '__main__':

    logging.info('Start loading data')
    logging.info('Reading arguments')

    parser = argparse.ArgumentParser(description='Script for downloading game data.')
    parser.add_argument('year_start', type=int)
    parser.add_argument('year_end', type=int)
    parser.add_argument('data_name', type=str)

    args = parser.parse_args()

    year_start, year_end = args.year_start, args.year_end
    name = args.data_name

    logging.info('Loading seasons 20' + str(year_start) + '/20' + str(year_start+1) + ' to 20' + str(year_end) + '/20' + str(year_end+1))
    x = load_data(year_start, year_end)
    logging.info('Data loaded')
    save_data(x, name)
    logging.info('Saved as ' + name + '.csv')
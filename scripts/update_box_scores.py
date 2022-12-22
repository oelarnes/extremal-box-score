"""
update a repository of raw player stat lines using basketball_reference_web_scraper
"""
from datetime import datetime, timezone, timedelta
import os
import csv
from time import sleep

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

seasons = [
    2020, 2021, 2022
]

for season in seasons:
    season_string = f'{season-1}-{season}'
    season_path = f'./data/season_schedules/{season_string}.csv'
    
    if not os.path.isfile(season_path):
        print(f'Requesting Season Scedule for {season_string}')
        client.season_schedule(
            season_end_year=season, 
            output_type=OutputType.CSV, 
            output_file_path=season_path
        )
    with open(season_path) as csvfile:
        season_data = list(csv.DictReader(csvfile))
        dates = sorted(list(set([datetime.fromisoformat(row['start_time']).astimezone(tz=timezone(timedelta(hours=-8))).date() for row in season_data])))

        for gamedate in dates:
            date_path = f'./data/daily_stat_lines/{season_string}/{gamedate.isoformat()}.csv'
            if not os.path.isfile(date_path):
                print(f'Requesting Daily Stat Line for {gamedate.isoformat()}')
                client.player_box_scores(gamedate.day, gamedate.month, gamedate.year,
                    output_type=OutputType.CSV,
                    output_file_path=date_path 
                )
                sleep(1)

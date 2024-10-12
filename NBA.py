#importing and reading data
import pandas as pd

df = pd.read_csv("D:/NBA/Data/NBA2000-2009.csv")
df.head()
# processing best player 
df['REB'] = df['OREB'] + df['DREB']

df_filtered = df[['PLAYER', 'YEAR', 'PTS', 'AST', 'REB', 'STL', 'BLK']]


df_filtered['double_stats_count'] = ((df_filtered['PTS'] >= 10).astype(int) +
                                     (df_filtered['AST'] >= 10).astype(int) +
                                     (df_filtered['REB'] >= 10).astype(int) +
                                     (df_filtered['STL'] >= 10).astype(int) +
                                     (df_filtered['BLK'] >= 10).astype(int))


double_double = df_filtered[df_filtered['double_stats_count'] >= 2].drop(columns='double_stats_count')


double_double = double_double.sort_values(by=['YEAR', 'PLAYER'])

double_double.head()
# analysing the value of players
df['Missed FG'] = df['FGA'] - df['FGM']
df['Missed FT'] = df['FTA'] - df['FTM']


df['Value'] = (df['PTS'] + df['OREB'] + df['DREB'] +
                     df['AST'] + df['STL'] + df['BLK']) - \
                    (df['TOV'] + df['Missed FG'] + df['Missed FT'])

player_avg_value = df.groupby('PLAYER')['Value'].mean().reset_index()

player_avg_value['Value'] = player_avg_value['Value'].round(2)

best_player = player_avg_value.sort_values(by=['Value', 'PLAYER'], ascending=[False, True])

best_player.head()
# analysing and processing the taems and their points
team_total_pts_per_year = df.groupby(['YEAR', 'TEAM'])['PTS'].sum().reset_index()

max_PTS_of_year = team_total_pts_per_year.loc[team_total_pts_per_year.groupby('YEAR')['PTS'].idxmax()]

max_PTS_of_year['PTS'] = max_PTS_of_year['PTS'].round(2)

max_PTS_of_year = max_PTS_of_year.sort_values(by='YEAR')

max_PTS_of_year.head()
# making zip file
import os
import zipfile

if not os.path.exists(os.path.join(os.getcwd(), 'NBA.ipynb')):
    %notebook -e NBA.ipynb

double_double.to_csv('double_double.csv', index=False)
best_player.to_csv('best_player.csv', index=False)
max_PTS_of_year.to_csv('max_PTS_of_year.csv', index=False)

def compress(file_names):
    print("File Paths:")
    print(file_names)
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile("result.zip", mode="w") as zf:
        for file_name in file_names:
            zf.write('./' + file_name, file_name, compress_type=compression)

file_names = ['double_double.csv', 'best_player.csv', 'max_PTS_of_year.csv', 'NBA.ipynb']
compress(file_names)

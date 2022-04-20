
import pandas as pd



def format_excel(name):
    path = name.lower().replace(' ', '_')
    df = pd.read_csv(path + '.tsv', delimiter='\t', names=['date', 'rating', 'text'])



    current_day = 8
    current_month = 4
    current_year = 2022

    days_in_previous_month = 31

    for j in range(len(df)):


        ####FIXING THE DATE FORMAT
        day = current_day
        month = current_month
        year = current_year

        i = df.iat[j, 0]

        if i[0] == 'a': number = 1
        else: number = int(i.split(' ')[0])

        scale = i.split(' ')[1].replace('s', '')

        if scale=='weeks':
            number *= 3
            scael = 'day'

        if scale == 'year':
            day = 1
            month = 1
            year = current_year - number

        elif scale == 'month':
            day = 1
            month = current_month - number
            year = current_year
            if month < 1:
                month += 12
                year -= 1


        elif scale=='day':
            day = current_day - number
            month = current_month
            if day < 1:
                day += days_in_previous_month
                month -= 1
            year = current_year



        if day < 10: day = '0' + str(day)
        else: day = str(day)

        if month < 10: month = '0' + str(month)
        else: month = str(month)

        df.iat[j, 0] = pd.to_datetime('{}/{}/{}'.format(day, month, year))


        #####Cleaning the text a little

        df.iat[j, 2] = df.iat[j, 2].replace('</span> </div>', '').replace('////', '\n')





    #df.to_csv('run_with_better_dates.tsv', sep='\t')
    df.to_excel(path + '.xlsx')

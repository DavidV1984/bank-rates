#!/usr/bin/python
# -*- coding: windows-1250 -*-

import pandas as pd
import datetime as dt
import numpy as np

# nastavimo pogled za pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# na html kodi poi��emo vse tabele in izlu��imo le tisto, ki jo potrebujemo [9]. Nastavimo indeks.
df = pd.read_html('https://www.global-rates.com/interest-rates/central-banks/central-banks.aspx', header=0)[9].set_index('country/region')
df.drop(['direction', 'Name of interest rate'], axis=1, inplace=True)

df['current rate'] = [x.strip().replace(u'\xa0%', u'') for x in df['current rate']]
df['current rate'] = pd.to_numeric(df['current rate'])

df['previous rate'] = [x.strip().replace(u'\xa0%', u'') for x in df['previous rate']]
df['previous rate'] = pd.to_numeric(df['previous rate'])

df['change'] = pd.to_datetime(df['change'])

df['razlika'] = dt.datetime.today() - df['change']
df['OMt'] = np.where(df['razlika'] > dt.timedelta(183), 0, np.where(df['current rate'] - df['previous rate'] > 0, -1, +1))

df = df[['current rate', 'OMt']]

ECB_current_rate = df.at['Europe', 'current rate']
ECB_OMt = df.at['Europe', 'OMt']
#print(ECB_current_rate, ECB_OMt)


new_index = ['United States', 'Germany', 'Japan', 'China', 'India', 'Russia',
             'Brazil', 'Slovenia', 'Turkey', 'Mexico', 'Indonesia', 'Poland',
             'Italy', 'France', 'Australia', 'Spain', 'South Korea', 'Great Britain']

df = df.reindex(new_index)

list = ['Germany', 'Slovenia', 'Italy', 'France', 'Spain']

for i in list:
    df.at[i, 'current rate'] = ECB_current_rate
    df.at[i, 'OMt'] = ECB_OMt

df.index.names = ['Dr�ava']
df.rename(columns={'current rate': 'OM'}, inplace=True)

df.reset_index(inplace=True)

preimenovanje = [(df['Dr�ava'] == 'United States'), (df['Dr�ava'] == 'Japan'), (df['Dr�ava'] == 'Slovenia'),
                 (df['Dr�ava'] == 'Germany'), (df['Dr�ava'] == 'Turkey'), (df['Dr�ava'] == 'Mexico'),
                 (df['Dr�ava'] == 'India'), (df['Dr�ava'] == 'Indonesia'), (df['Dr�ava'] == 'Italy'),
                 (df['Dr�ava'] == 'Russia'), (df['Dr�ava'] == 'China'), (df['Dr�ava'] == 'Brazil'),
                 (df['Dr�ava'] == 'Poland'), (df['Dr�ava'] == 'France'), (df['Dr�ava'] == 'Spain'),
                 (df['Dr�ava'] == 'Great Britain'), (df['Dr�ava'] == 'Australia'), (df['Dr�ava'] == 'South Korea')]

izbira = ['ZDA', 'Japonska', 'Slovenija', 'Nem�ija', 'Tur�ija', 'Mehika', 'Indija', 'Indonezija', 'Italija',
              'Rusija', 'Kitajska', 'Brazilija', 'Poljska', 'Francija', '�panija', 'Velika Britanija', 'Avstralija',
              'Ju�na Koreja']

df['Dr�ava'] = np.select(preimenovanje, izbira)

print(df)
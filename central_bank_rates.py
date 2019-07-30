#!/usr/bin/python
# -*- coding: windows-1250 -*-

import pandas as pd
import datetime as dt
import numpy as np


# na html kodi poiščemo vse tabele in izluščimo le tisto, ki jo potrebujemo [9]. Nastavimo indeks.
df = pd.read_html('https://www.global-rates.com/interest-rates/central-banks/central-banks.aspx', header=0)[9].set_index('country/region')

# odstranimo dva stolpca
df.drop(['direction', 'Name of interest rate'], axis=1, inplace=True)

# popravimo trenutno in preteklo stopnjo
df['current rate'] = [x.strip().replace(u'\xa0%', u'') for x in df['current rate']]
df['current rate'] = pd.to_numeric(df['current rate'])
df['previous rate'] = [x.strip().replace(u'\xa0%', u'') for x in df['previous rate']]
df['previous rate'] = pd.to_numeric(df['previous rate'])

# spremenimo v datetime
df['change'] = pd.to_datetime(df['change'])

# izračunamo razliko v dnevih in nastavimo trend
df['razlika'] = dt.datetime.today() - df['change']
df['OMt'] = np.where(df['razlika'] > dt.timedelta(183), 0, np.where(df['current rate'] - df['previous rate'] > 0, -1, +1))

# uporabimo samo trnutno stopnjo in trend
df = df[{'current rate', 'OMt'}]

# nastavimo ECB rate, ki ga uporabimo za vse evropske države
ECB_current_rate = df.at['Europe', 'current rate']
ECB_OMt = df.at['Europe', 'OMt']
#print(ECB_current_rate, ECB_OMt)

# pripravimo nov indeks z državami, ki nas zanimajo
new_index = ['United States', 'Germany', 'Japan', 'China', 'India', 'Russia',
             'Brazil', 'Slovenia', 'Turkey', 'Mexico', 'Indonesia', 'Poland',
             'Italy', 'France', 'Australia', 'Spain', 'South Korea', 'Great Britain']

# reindeksiramo z novim indeksom
df = df.reindex(new_index)

# za evropske države določimo obrestno mero
list = ['Germany', 'Slovenia', 'Italy', 'France', 'Spain']

for i in list:
    df.at[i, 'current rate'] = ECB_current_rate
    df.at[i, 'OMt'] = ECB_OMt

# spremenimo ime indeksa in stolpca
df.index.names = ['Država']
df.rename(columns={'current rate': 'OM'}, inplace=True)

# resetiramo indeks
df.reset_index(inplace=True)

# preimenujemo države v slovenščino
preimenovanje = [(df['Država'] == 'United States'), (df['Država'] == 'Japan'), (df['Država'] == 'Slovenia'),
                 (df['Država'] == 'Germany'), (df['Država'] == 'Turkey'), (df['Država'] == 'Mexico'),
                 (df['Država'] == 'India'), (df['Država'] == 'Indonesia'), (df['Država'] == 'Italy'),
                 (df['Država'] == 'Russia'), (df['Država'] == 'China'), (df['Država'] == 'Brazil'),
                 (df['Država'] == 'Poland'), (df['Država'] == 'France'), (df['Država'] == 'Spain'),
                 (df['Država'] == 'Great Britain'), (df['Država'] == 'Australia'), (df['Država'] == 'South Korea')]

izbira = ['ZDA', 'Japonska', 'Slovenija', 'Nemčija', 'Turčija', 'Mehika', 'Indija', 'Indonezija', 'Italija',
              'Rusija', 'Kitajska', 'Brazilija', 'Poljska', 'Francija', 'Španija', 'Velika Britanija', 'Avstralija',
              'Južna Koreja']

df['Država'] = np.select(preimenovanje, izbira)

print(df)
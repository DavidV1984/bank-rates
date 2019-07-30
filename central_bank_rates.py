#!/usr/bin/python
# -*- coding: windows-1250 -*-

import pandas as pd
import datetime as dt
import numpy as np


# na html kodi poi��emo vse tabele in izlu��imo le tisto, ki jo potrebujemo [9]. Nastavimo indeks.
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

# izra�unamo razliko v dnevih in nastavimo trend
df['razlika'] = dt.datetime.today() - df['change']
df['OMt'] = np.where(df['razlika'] > dt.timedelta(183), 0, np.where(df['current rate'] - df['previous rate'] > 0, -1, +1))

# uporabimo samo trnutno stopnjo in trend
df = df[{'current rate', 'OMt'}]

# nastavimo ECB rate, ki ga uporabimo za vse evropske dr�ave
ECB_current_rate = df.at['Europe', 'current rate']
ECB_OMt = df.at['Europe', 'OMt']
#print(ECB_current_rate, ECB_OMt)

# pripravimo nov indeks z dr�avami, ki nas zanimajo
new_index = ['United States', 'Germany', 'Japan', 'China', 'India', 'Russia',
             'Brazil', 'Slovenia', 'Turkey', 'Mexico', 'Indonesia', 'Poland',
             'Italy', 'France', 'Australia', 'Spain', 'South Korea', 'Great Britain']

# reindeksiramo z novim indeksom
df = df.reindex(new_index)

# za evropske dr�ave dolo�imo obrestno mero
list = ['Germany', 'Slovenia', 'Italy', 'France', 'Spain']

for i in list:
    df.at[i, 'current rate'] = ECB_current_rate
    df.at[i, 'OMt'] = ECB_OMt

# spremenimo ime indeksa in stolpca
df.index.names = ['Dr�ava']
df.rename(columns={'current rate': 'OM'}, inplace=True)

# resetiramo indeks
df.reset_index(inplace=True)

# preimenujemo dr�ave v sloven��ino
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
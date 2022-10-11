# linear algebra
import numpy as np 

# data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd 

# data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# stocks related missing info
import yfinance as yf

# ignoring the warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# pandas options to display maximum possible rows and columns for every dataframe 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

SP500_Comp = pd.read_csv('sp500_companies.csv')
""" print(SP500_Comp.head(5)) """

def replace_null(df, sym, col, missing):
    ticker = yf.Ticker(sym)
    df.loc[df['Symbol']==sym, col]= ticker.info[missing]

SP500_Comp = SP500_Comp.drop([53, 419])

print(SP500_Comp.shape)

print(SP500_Comp.count(axis=0))

replace_null(SP500_Comp,'ROP', 'Revenuegrowth', 'revenueGrowth')

SP500_Comp = SP500_Comp.drop(['State'], axis=1)

SP500_Comp.loc[SP500_Comp['Fulltimeemployees'].isnull(), 'Fulltimeemployees'] = SP500_Comp['Fulltimeemployees'].mode()[0]

missing_EBITDA = SP500_Comp[SP500_Comp['Ebitda'].isnull()]
count_EBITDA = missing_EBITDA.groupby(['Sector', 'Industry'])['Industry'].count()


for col in SP500_Comp.columns:
    b = SP500_Comp[col].unique()
    if len(b)<20:
        print(f'{col} has {len(b)} unique values -->> {b}', end = '\n\n')


sns.set(style='darkgrid')
plt.figure(figsize=(15,12))
sns.pairplot(SP500_Comp, corner=True, hue='Exchange')
plt.tight_layout()
plt.savefig('foo.png')

SP_corr = SP500_Comp.corr()
mask = np.zeros_like(SP_corr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(12, 10))
    ax = sns.heatmap(SP_corr, mask=mask, vmax=1, vmin=-1, linewidths=.5, square=True, cmap='coolwarm', annot=True)
    plt.title('Correlation Heatmap of S&P 500 Companies dataset', fontsize = 15)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('foo1.png')

d2 = sns.displot(data=SP500_Comp, x='Currentprice', kde=True, height=8, aspect=1.6, bins=100, binrange=(0, 2100), color='dodgerblue')
d2.set(xlabel='Current Price')
plt.xlim(0, 3100)
plt.savefig('foo2.png')

print(f'The mode of the Current Price column is {SP500_Comp.Currentprice.mode()[0]}.')

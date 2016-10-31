import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt

# Read data files

fpath = 'baseballdatabank-master/core'

fname_salary = 'Salaries.csv'
fname_teams = 'Teams.csv'

Salary = pd.read_csv(fpath+'/'+fname_salary)
Teams = pd.read_csv(fpath+'/'+fname_teams)

# Team Data import --------------------
# Focus on team data after 1985

Teams_a = Teams[Teams['yearID']>=1985]
Salary_a = Salary[Salary['yearID']>=1985]

Teams_a.insert(0,'Top1', pd.Series(0, index = Teams_a.index))
Teams_a['Top1'][Teams_a['Rank']==1] =1

# add winning percentage
Teams_a['WinPct'] = Teams_a['W']/(Teams_a['W']+Teams_a['L'])

# Salary Data import -------------------

# Compute the total yearly team salary 
# and compare it with team's winning pct in that year

salary_grouped = Salary_a.groupby(['yearID','teamID']).sum() 
salary_grouped_a = \
Salary[Salary.yearID >= 1985].groupby(['yearID','teamID'], as_index = False).sum() 

## Merge Team + Salary data
Team_Salary = pd.merge(Teams_a[['yearID','teamID','WinPct','name','Rank','Top1']],salary_grouped_a,on=['teamID','yearID'],right_index = False, how = 'left')
         
## PLOTTING

# Salary increase per year
#plt.figure(figsize=(12, 6))
#sns.boxplot(x="yearID",y="salary",data=Team_Salary)

# correlation function
def calc_corr(df):
    corr_val =  sp.stats.pearsonr(df.WinPct, df.salary)
    return corr_val[0]

Corr = Team_Salary.groupby('yearID')
corr2 = Corr.apply(calc_corr)

plt.figure(figsize=(12, 6))
plt.plot(corr2.to_frame(), 'ro-' )
plt.xlabel("year")
plt.title("Pearson correlation coeff. between winning percentage and salary")

# This dataframe compares mean between division winner and the rest of team in each division
Team_Salary_compare = Team_Salary.groupby(['yearID','Top1']).mean()
Team_Salary_compare.reset_index(inplace=True)

g = sns.FacetGrid(Team_Salary_compare, hue="Top1", size = 6)
g.map(plt.scatter, "yearID", "salary", s=50, alpha=.7, linewidth=.5, edgecolor="white")
g.add_legend();
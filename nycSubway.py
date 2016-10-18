import numpy
import scipy
import scipy.stats
import pandas
import statsmodels.api as sm
from ggplot import *


#read in the csv to a pandas dataframe
turnstileweather = pandas.read_csv('turnstile.csv')
turnstile = pandas.DataFrame(turnstileweather)



print ('mean for everyone is %s' % numpy.mean(turnstile['ENTRIESn_hourly']))

#split into seperate groups
rain = turnstile[turnstile.rain == 1]
no_rain = turnstile[turnstile.rain ==0]

# discover the size of each group
print('length of rain is %s' %len(rain))
print('length of no rain is %s' %len(no_rain))

#grab the means for each
print ('mean for rain is %s' % numpy.mean(rain['ENTRIESn_hourly']))
print ('mean for no rain is %s' % numpy.mean(no_rain['ENTRIESn_hourly']))

# run the mann whitney u test on the two samples
u,p = scipy.stats.mannwhitneyu(rain["ENTRIESn_hourly"],no_rain["ENTRIESn_hourly"])

# p value is p * 2
p = p*2
print ("u is %s" % u)
print ("p is %s" % p)
print ("p <= 0.05 so I reject the null hypothesis")
print('//////')
print('//////')
print('//////')
print('//////')

# create a linear regression
def linear_regression(features, values):
	features = sm.add_constant(features)
	model = sm.OLS(values, features)
	results = model.fit()
	intercept = results.params[0]
	params = results.params[1:]
	return intercept, params

features = turnstile[[ 'Hour']]
dummy_units = pandas.get_dummies(turnstile['UNIT'], prefix='unit')
features = features.join(dummy_units)
values = turnstile['ENTRIESn_hourly']
intercept, params = linear_regression(features, values)
predictions = intercept + numpy.dot(features, params)
print("the intercept is %s" % intercept)
print("the weights are %s" % params)
#print (intercept, params)
print ("my predictions")
print (predictions)


#get R squared value
top = ((predictions - turnstile['ENTRIESn_hourly'])**2).sum()
bottom = ((turnstile['ENTRIESn_hourly']-numpy.mean(turnstile['ENTRIESn_hourly']))**2).sum()
r_squared = 1 - top / bottom
print ("r squared is %s" % r_squared)

# print out visualizations
pandas.options.mode.chained_assignment = None
turnstileweather['UNIT'] = turnstileweather['UNIT'].map(lambda x: float(x.lstrip('R')))
water = ggplot(turnstileweather, aes(x = 'ENTRIESn_hourly', fill =
'rain'))+geom_histogram(binwidth = 1000)+ggtitle("Ridership on rain vs nonraindays")+
labs("Hourly Entries","# of Recorded Occurances")+xlim(0,15000)+ylim(0,100000)
fire = ggplot(rain,aes(y ='Hour', x ='ENTRIESn_hourly')) + geom_boxplot()+labs(x= 'Hourly Entries', y= 'Hour in the day')+ggtitle('Hourly Entries by hour in the day when raining')
print (water)
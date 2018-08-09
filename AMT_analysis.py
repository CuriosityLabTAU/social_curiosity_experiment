import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


AMT_data=pd.read_csv('AMT_demo.csv')


number_of_bins=9

plt.figure()
hist=AMT_data.hist(bins=number_of_bins)
plt.show()


bins = [i*(1.0/number_of_bins) for i in xrange(number_of_bins+1)]
labels = [(bins[i]+bins[i+1])/2.0 for i in xrange(number_of_bins)]
labels=list(np.around(np.array(labels),3))
shape=AMT_data.count()
print shape

print "------------------------AMT_data--------------------------------------------"
for i in list(AMT_data):
    AMT_data[i] = pd.cut(AMT_data[i], bins=bins, labels=labels,include_lowest=True)
print AMT_data


#value counts
print "---------------------------hist_df--------------------------------------"
hist_list=[]
for i in list(AMT_data):
    hist_list.append(AMT_data[i].value_counts())
hist_df=pd.DataFrame(hist_list)
print hist_df

#/ by shape
print "---------------------------hist_prob_df--------------------------------------"
hist_prob_df=hist_df.div(shape,axis=0)
print hist_prob_df

#norem bins prob
print "---------------------------probs--------------------------------------"
probs_df=hist_prob_df.div(hist_prob_df.sum(axis=0),axis=1)
print probs_df

probs_df.to_csv('probs_from_AMT.csv')
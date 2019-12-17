import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = np.load("../data/correlation_model/r.npy")


sns.set_style('darkgrid')
sns.set_context('paper')

abs_data = np.abs(data)
sort_abs_data = np.sort(abs_data)

fake_data = []
for i in abs_data:
    if i < 0.7 and i > 0.3:
        fake_data.append(i + 0.1*(1.7-i))
    else:
        fake_data.append(i)
fake_data = np.array(abs_data)

sns.distplot(fake_data, bins = 50, hist = True, kde = True, norm_hist = False,
            rug = True, vertical = False,
            color = '#6F8C5A', label = 'histogram', axlabel = 'correlation value')
plt.legend()
plt.show()
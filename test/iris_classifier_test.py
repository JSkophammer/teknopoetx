from ai2 import Perceptron
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def plot_decision_regions(X, y, classifier, resolution=0.02):

    # set up marker generator and color map
    markers = ('x', 's', 'o', '^', 'v')
    colors = ('blue', 'red', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, 1.2, resolution), np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    #plt.xlim(xx1.min(), xx1.max())
    #plt.ylim(xx2.min(), xx2.max())
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)

    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8, c=cmap(idx), marker=markers[idx], label=cl)


df = pd.read_csv('csv/trn_data.csv', header=None)
#print(df)
y = df.iloc[0:4000, 4].values
y2 = df.iloc[4000:, 4].values
X1 = df.iloc[0:4000, [2, 3]].values
X2 = df.iloc[4000:, [2, 3]].values
ppn = Perceptron(eta=0.0001, n_iter=100)
ppn.fit(X1, y)
table = {}
errors = 0
for xi,targ in zip(X2,y2):
    #print(xi)
    p = ppn.predict(xi).tolist()
    if p != targ:
        errors += 1
    xil = xi.tolist()
    ratio = xil[1]/xil[0]
    table[ratio] = int(p)
print(errors)
yes = sorted([round(x, 2) for x in table.keys() if table[x] == 1])
print('min yes:', min(yes))
print('max yes:', max(yes))
no = sorted([round(x, 2) for x in table.keys() if table[x] == -1])
print('min no:', min(no))
print('max no:', max(no))
#print(yes[:25])
#print(no[:25])

"""plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='sestosa')
plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='versicolor')
plt.xlabel('petal length')
plt.ylabel('sepal length')
plt.legend(loc='upper left')
plt.show()

plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of misclassifications')
plt.show()"""

plot_decision_regions(X1, y, classifier=ppn)
plt.xlabel('word frequency')
plt.ylabel('number of syllables')
plt.legend(loc='upper left')
plt.show()
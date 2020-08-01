#Topic: Clustering - Test and Shopping Data
#-----------------------------
#libraries

import numpy as np
X = np.array([[5,3],  [10,15], [15,12],  [24,10],  [30,30],  [85,70],   [71,80],  [60,78],    [70,55],    [80,91],])
X

import matplotlib.pyplot as plt

#run these lines till plt.show together
labels = range(1, 11)
plt.figure(figsize=(10, 7))
plt.subplots_adjust(bottom=0.1)
plt.scatter(X[:,0],X[:,1], label='True Position')
for label, x, y in zip(labels, X[:, 0], X[:, 1]):
    plt.annotate(  label,   xy=(x, y), xytext=(-3, 3), textcoords='offset points', ha='right', va='bottom')
plt.show()
#draws the data points in the X numpy array and label data points from 1 to 10.
#It can be seen from the naked eye that the data points form two clusters: first at the bottom left consisting of points 1-5 while second at the top right consisting of points 6-10.
#However, in the real world, we may have thousands of data points in many more than 2 dimensions. In that case it would not be possible to spot clusters with the naked eye. This is why clustering algorithms have been developed.

from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

linked = linkage(X, 'single')
linked
labelList = range(1, 11)

plt.figure(figsize=(10, 7))
dendrogram(linked,  orientation='top',  labels=labelList,  distance_sort='descending', show_leaf_counts=True)
plt.show();


#The algorithm starts by finding the two points that are closest to each other on the basis of Euclidean distance. If we look back at Graph1, we can see that points 2 and 3 are closest to each other while points 7 and 8 are closes to each other. Therefore a cluster will be formed between these two points first. In Graph2, you can see that the dendograms have been created joining points 2 with 3, and 8 with 7. The vertical height of the dendogram shows the Euclidean distances between points. From Graph2, it can be seen that Euclidean distance between points 8 and 7 is greater than the distance between point 2 and 3.

#The next step is to join the cluster formed by joining two points to the next nearest cluster or point which in turn results in another cluster. If you look at Graph1, point 4 is closest to cluster of point 2 and 3, therefore in Graph2 dendrogram is generated by joining point 4 with dendrogram of point 2 and 3. This process continues until all the points are joined together to form one big cluster.

#Once one big cluster is formed, the longest vertical distance without any horizontal line passing through it is selected and a horizontal line is drawn through it. The number of vertical lines this newly created horizontal line passes is equal to number of clusters. Take a look at the following plot:
    
#We can see that the largest vertical distance without any horizontal line passing through it is represented by blue line. So we draw a new horizontal red line that passes through the blue line. Since it crosses the blue line at two points, therefore the number of clusters will be 2.

#Basically the horizontal line is a threshold, which defines the minimum distance required to be a separate cluster. If we draw a line further down, the threshold required to be a new cluster will be decreased and more clusters will be formed as see in the image below:
    
#In the above plot, the horizontal line passes through four vertical lines resulting in four clusters: cluster of points 6,7,8 and 10, cluster of points 3,2,4 and points 9 and 5 will be treated as single point clusters.    
    
    
#https://stackabuse.com/hierarchical-clustering-with-python-and-scikit-learn/


#%%%
from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')

#n the code above we import the AgglomerativeClustering class from the "sklearn.cluster" library. The number of parameters is set to 2 using the n_clusters parameter while the affinity is set to "euclidean" (distance between the datapoints). Finally linkage parameter is set to "ward", which minimizes the variant between the clusters.

cluster.fit_predict(X)

#Next we call the fit_predict method from the AgglomerativeClustering class variable cluster. This method returns the names of the clusters that each data point belongs to. Execute the following script to see how the data points have been clustered.

print(cluster.labels_)
#The output is a one-dimensional array of 10 elements corresponding to the clusters assigned to our 10 data points. #[1 1 1 1 1 0 0 0 0]
#As expected the first five points have been clustered together while the last five points have been clustered together. It is important to mention here that these ones and zeros are merely labels assigned to the clusters and have no mathematical implications.

#Finally, let's plot our clusters. To do so, execute the following code:

plt.scatter(X[:,0],X[:,1], c=cluster.labels_, cmap='rainbow')
#You can see points in two clusters where the first five points clustered together and the last five points clustered together.


#%%%
#In the last section we performed hierarchical clustering on dummy data. In this example, we will perform hierarchical clustering on real-world data and see how it can be used to solve an actual problem.

#The problem that we are going to solve in this section is to segment customers into different groups based on their shopping trends.
#The dataset for this problem can be downloaded from the following link:
url='https://stackabuse.s3.amazonaws.com/files/hierarchical-clustering-with-python-and-scikit-learn-shopping-data.csv'
import matplotlib.pyplot as plt
import pandas as pd
#%matplotlib inline
import numpy as np
df = pd.read_csv(url)
#customer_data = pd.read_csv('data/shopping-data.csv')
customer_data = df.copy()
customer_data.head()
#explore data
customer_data
customer_data.head()
customer_data.shape
customer_data.describe()
customer_data.columns

#rename columns
customer_data.columns = ['customerID', 'genre', 'age', 'income', 'spendscore']
customer_data.head()
#Our dataset has five columns: CustomerID, Genre, Age, Annual Income, and Spending Score. To view the results in two-dimensional feature space, we will retain only two of these five columns. We can remove CustomerID column, Genre, and Age column. We will retain the Annual Income (in thousands of dollars) and Spending Score (1-100) columns. The Spending Score column signifies how often a person spends money in a mall on a scale of 1 to 100 with 100 being the highest spender. 

data = customer_data.iloc[:, 3:5].values
data

#Next, we need to know the clusters that we want our data to be split to. We will again use the scipy library to create the dendrograms for our dataset. Execute the following script to do so:
    
import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("Customer Dendograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))    
plt.show();

#In the script above we import the hierarchy class of the scipy.cluster library as shc. The hierarchy class has a dendrogram method which takes the value returned by the linkage method of the same class. The linkage method takes the dataset and the method to minimize distances as parameters. We use 'ward' as the method since it minimizes then variants of distances between the clusters.
#If we draw a horizontal line that passes through longest distance without a horizontal line, we get 5 clusters as shown in the following figure:

#Now we know the number of clusters for our dataset, the next step is to group the data points into these five clusters. To do so we will again use the AgglomerativeClustering class of the sklearn.cluster library. Take a look at the following script:

from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
cluster.fit_predict(data)

#You can see the cluster labels from all of your data points. Since we had five clusters, we have five labels in the output i.e. 0 to 4.
#As a final step, let's plot the clusters to see how actually our data has been clustered:

plt.figure(figsize=(10, 7))
plt.scatter(data[:,0], data[:,1], c=cluster.labels_, cmap='rainbow')
plt.show();

#You can see the data points in the form of five clusters. The data points in the bottom right belong to the customers with high salaries but low spending. These are the customers that spend their money carefully. Similarly, the customers at top right (green data points), these are the customers with high salaries and high spending. These are the type of customers that companies target. The customers in the middle (blue data points) are the ones with average income and average salaries. The highest numbers of customers belong to this category. Companies can also target these customers given the fact that they are in huge numbers, etc
#The clustering technique can be very handy when it comes to unlabeled data. Since most of the data in the real-world is unlabeled and annotating the data has higher costs, clustering techniques can be used to label unlabeled data.

#%%%kmeans

import matplotlib.pyplot as plt
import numpy as np
X2 = np.array([[1,2], [1.5, 1.8], [5,8], [8,8], [1, 0.6], [9,11]])
X2
from matplotlib import style

plt.scatter(X2[:,0], X2[:,1], s=150)
plt.show();

from sklearn.cluster import KMeans
Kmean2 = KMeans(n_clusters=2)
Kmean2.fit(X2)
centers2 = Kmean2.cluster_centers_
X2
centers2
Kmean2.labels_

plt.scatter(X2[:,0], X2[:,1], s=50, c = Kmean2.labels_)
plt.scatter(centers2[:,0], centers2[:,1], s=100, marker='*', color =['red'])
plt.show();

#%%%iris 

from pydataset import data
iris = data('iris')
data = iris.copy()
data.head()
#how many groups
data.Species.value_counts()
data.columns
X3 = data[['Sepal.Length','Sepal.Width']]
X3
y3 = data.Species.values
y3
X3.shape

plt.scatter(X3['Sepal.Length'], X3['Sepal.Width'], s=50)
#group them into 3 categories
irisCluster = KMeans(n_clusters=3)
irisCluster.fit(X3)
irisCenters= irisCluster.cluster_centers_
irisCenters
irisCluster.labels_

plt.scatter(X3['Sepal.Length'], X3['Sepal.Width'], s=50, c=irisCluster.labels_)
plt.scatter(irisCenters[:, 0], irisCenters[:, 1], s=200, marker='*',  c='red')
plt.show();

irisCluster.labels_
import collections
collections.Counter(irisCluster.labels_)

#optimal no of clusters
from sklearn.cluster import KMeans
X3
SSdistance = []
K = range(1,10)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(X3)
    SSdistance.append(km.inertia_)

SSdistance  #inertia for 10 differents sets of clusters

plt.plot(K, SSdistance, 'bx-')
plt.xlabel('k -no of clusters')
plt.ylabel('Sum of Sq Distance')
plt.title('Elbow method to find optimal no of clusters')
plt.show();


#%% Eg use case
#Behavioural segmenation - segment by purchase history, Segment by activities on application, website or platform, Define persona on interests, Create profiles based on activity monitoring
#Inventory Categorisation - Gp inventory by sales activity, Gp inventory by manufacturing metrics
#Sorting sensor measurement : Detect activity types in motion sensors, group images, separate audio, Identify groups in health monitoring
#Detecting bots or anomalies : Seperate valid activity gps from bots, Gp valid activity t clean up outlier detection



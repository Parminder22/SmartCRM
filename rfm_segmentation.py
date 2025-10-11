
# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import time, warnings
import datetime as dt
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# %matplotlib inline
import seaborn as sns
warnings.filterwarnings("ignore")
import io

data = pd.read_csv("data.csv", encoding = 'unicode_escape')
data.head()

data = data[data['Quantity']>0]
data.dropna(subset=['CustomerID'],how='all',inplace=True)

"""#RFM Table Preparation

**Recency**
"""

data['date'] = pd.DatetimeIndex(data['InvoiceDate']).date
now = data['date'].max()

# Grouping data by 'CustomerID' and finding most recent purchase date for each customer
recency = data.groupby(by='CustomerID', as_index=False)['date'].max()
recency.columns = ['CustomerID','LastPurshaceDate']

# 'Recency' = 'now' - 'LastPurchaseDate'
recency['Recency'] = recency['LastPurshaceDate'].apply(lambda x: (now - x).days)
recency.head()

recency.drop('LastPurshaceDate',axis=1,inplace=True)

"""**Frequency**"""

data_copy = data
data_copy.drop_duplicates(subset=['InvoiceNo', 'CustomerID'], keep="first", inplace=True)

#counting number of unique 'InvoiceNo' for each customer
frequency = data_copy.groupby(by=['CustomerID'], as_index=False)['InvoiceNo'].count()
frequency.columns = ['CustomerID','Frequency']
frequency.head()

"""**Monetary**"""

data['TotalCost'] = data['Quantity'] * data['UnitPrice']

#summing the 'TotalCost' for each customer
monetary = data.groupby(by='CustomerID',as_index=False).agg({'TotalCost': 'sum'})
monetary.columns = ['CustomerID','Monetary']
monetary.head()

"""**RFM Table**"""

temp = recency.merge(frequency,on='CustomerID')
rfm= temp.merge(monetary,on='CustomerID')

rfm.set_index('CustomerID',inplace=True)
rfm.head()

"""#EDA / Cleaning / Dealing With Outliers"""

# Counting duplicate rows
duplicate_count = rfm.duplicated().sum()
print("Number of duplicate rows:", duplicate_count)

rfm.drop_duplicates(inplace=True)

duplicate_count_new = rfm.duplicated().sum()
print("Number of duplicate rows:", duplicate_count_new)

print(rfm.isnull().sum())

rfm.describe()

#Boxplot to see outliers
attributes = ['Recency', 'Frequency', 'Monetary']

plt.figure(figsize=(10, 8))

sns.boxplot(data = rfm[attributes], orient="h", palette="Set2" ,whis=1.5,saturation=1, width=0.7)
plt.title("Outliers Variable Distribution", fontsize = 12)

#Removing outliers
attributes = ['Monetary', 'Recency', 'Frequency']

for attribute in attributes:
    # Calculate quartiles and IQR
    Q1 = rfm[attribute].quantile(0.05)
    Q3 = rfm[attribute].quantile(0.95)
    IQR = Q3 - Q1

    # Remove outliers
    rfm = rfm[(rfm[attribute] >= Q1 - 1.5*IQR) & (rfm[attribute] <= Q3 + 1.5*IQR)]

# heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(rfm.corr(), annot=True, cmap='coolwarm', fmt=".2f")

plt.title('Heatmap of Correlation Matrix for RFM Data')
plt.show()

"""# PCA / K-mean Clustering

Applying PCA with 2 dimensions
"""

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

rfm_cluster = pd.DataFrame(data=rfm)

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(rfm_cluster)

# Apply PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_features)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

"""Determine optimal number of K using Elbow Method

"""

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(pca_df)
    wcss.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='-', color='b')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.xticks(range(1, 11))
plt.grid(True)
plt.show()

"""The optimal K=5

PCA KMean Clustering
"""

# Apply KMeans clustering
kmeans = KMeans(n_clusters=5)
kmeans.fit(pca_df)

pca_df['Cluster'] = kmeans.labels_

#Plot PCA Clustering
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Cluster', palette='viridis')
plt.title('PCA Clustering')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# Calculate mean values for each cluster
rfm_cluster['Cluster'] = kmeans.labels_
cluster_means = rfm_cluster.groupby('Cluster').mean()

print("Mean values for each cluster:")
print(cluster_means)

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# Create catplot 'Recency'
sns.violinplot(data=rfm_cluster, x="Cluster", y="Recency", hue="Cluster", ax=axes[0])
axes[0].set_title('Recency')

# Create catplot 'Frequency'
sns.violinplot(data=rfm_cluster, x="Cluster", y="Frequency", hue="Cluster", ax=axes[1])
axes[1].set_title('Frequency')

# Create catplot 'Monetary'
sns.violinplot(data=rfm_cluster, x="Cluster", y="Monetary", hue="Cluster", ax=axes[2])
axes[2].set_title('Monetary')

plt.tight_layout()
plt.show()

"""* Cluster 0: **Inactive Shoppers**
Recency: 253.20, Frequency: 1.47, Monetary: 49.19
Customers who haven't been active for an extended period, with no recent purchases.

* Cluster 1: **Occasional Shoppers**
Recency: 54.58, Frequency: 2.04, Monetary: 39.59
Customers with recent but infrequent purchases and low spending.

* Cluster 2: **Frequent Spenders**
Recency: 30.66, Frequency: 10.41, Monetary: 406.19
Customers who shop frequently with moderate to High spending. They engage often and spend moderately.

* Cluster 3: **High-Value Loyal Shopper**
Recency: 19.74, Frequency: 16.10, Monetary: 913.78
VIP Customers who shop very often and spend significantly.They engage frequently and spend generously.

* Cluster 4 : **Regular Shoppers**
Recency: 29.88, Frequency: 5.72, Monetary: 149.89
Customers who shop regularly, with recent purchases. Moderate frequency and  moderate spending.
"""

rfm['Cluster'] = kmeans.labels_

segment_names = {
    0: 'Inactive Shoppers',
    1: 'Occasional Shoppers',
    2: 'Frequent Spenders',
    3: 'High-Value Loyal Shoppers',
    4: 'Regular Shoppers' }

# Map the cluster values to segment names
rfm['Segment'] = rfm['Cluster'].map(segment_names)
print(rfm)

import matplotlib.pyplot as plt

segment_counts = rfm['Segment'].value_counts()

# legend
legend_labels = [f'{segment} ({count})' for segment, count in segment_counts.items()]

plt.figure(figsize=(10, 6))
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('muted', len(segment_counts)))
plt.title('Distribution of Customer Segments')
plt.axis('equal')

plt.show()

#rfm = rfm.drop('Cluster', axis=1)
rfm.to_csv("customer_segments.csv")
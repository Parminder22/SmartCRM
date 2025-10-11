# RFM Customer Segmentation using PCA and K-Means Clustering
## Introduction 
RFM segmentation is a marketing analysis method that involves analyzing customer behavior based on three key factors: recency, frequency, and monetary value. It helps businesses group customers into segments, enabling targeted and personalized marketing strategies. 

Recency indicates how recently a customer has made a purchase, while Frequency measures how often they make purchases, and Monetary represents the amount of money a customer spends on purchases.
## Data Collection 
The data is available on [Kaggle](https://www.kaggle.com/datasets/ersany/online-retail-dataset) with an Open Database License (ODbL).

This is a transnational dataset that contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.
## Data Preparation 
- Calculate Recency, Frequency, and Monetary value for each customer. 
- Perform data cleaning by checking for duplicates, missing values, and dealing with outliers.
- Standardize the data to make it suitable for the machine learning model.
## Data Modeling
- **Principal component analysis (PCA)** is a linear dimensionality reduction technique used to reduce the number of variables of a data set, while preserving as much information as possible. It makes analyzing data points much easier and faster for machine learning algorithms. In this project, we used PCA with 2 dimensions to enhance the effectiveness of our K-Means clustering algorithm, enabling more accurate and efficient segmentation of our customer data.
  
- **K-Means Clustering** is an Unsupervised Learning algorithm, which groups the unlabeled dataset into k-number clusters. It allows us to cluster the data into different groups and a convenient way to discover the categories of groups in the unlabeled dataset on its own without the need for any training.
  
  We first used The **Elbow Method**, which is a graphical method for finding the optimal K value.
  ![Elbow](https://github.com/maissaladjimi/RFM_Customer_Segmentation/assets/94018321/e7f5f120-944d-488e-8515-d6aad646fb8f)
  
  It revealed that the optimal K=5. After running the model, the following clusters were revealed
  
  ![PCA_KMeans](https://github.com/maissaladjimi/RFM_Customer_Segmentation/assets/94018321/a059ef81-4c32-4e7a-bbc7-8fb77794bb57)

## Cluster Interpretation 
In order to understand the characteristics of each cluster and identify the segment properties, we calculated the mean values for Recency, Frequency, and Monetary for each cluster. Additionally, for more visual interpretation, we visualized the distribution of clusters against each variable. 

![Means](https://github.com/maissaladjimi/RFM_Customer_Segmentation/assets/94018321/80b8bb61-27ba-4a21-ba17-d19ccff6658c)

![catplots](https://github.com/maissaladjimi/RFM_Customer_Segmentation/assets/94018321/62d7dc41-494d-4571-9811-f9ab7d869efe)

- **Cluster 0: **Inactive Shoppers**** Recency: 253.20, Frequency: 1.47, Monetary: 49.19 Customers who haven't been active for an extended period, with no recent purchases.

- **Cluster 1: **Occasional Shoppers**** Recency: 54.58, Frequency: 2.04, Monetary: 39.59 Customers with recent but infrequent purchases and low spending.

- **Cluster 2: **Frequent Spenders**** Recency: 30.66, Frequency: 10.41, Monetary: 406.19 Customers who shop frequently with moderate to High spending. They engage often and spend moderately.

- **Cluster 3: **High-Value Loyal Shopper**** Recency: 19.74, Frequency: 16.10, Monetary: 913.78 VIP Customers who shop very often and spend significantly.They engage frequently and spend generously.

- **Cluster 4 : **Regular Shoppers**** Recency: 29.88, Frequency: 5.72, Monetary: 149.89 Customers who shop regularly, with recent purchases. Moderate frequency and moderate spending.
## Customer Segments
After Identifying the clusters, each customer was assigned its respective segment.These segments are essential  for more effective and targeted marketing strategies tailored to their specific engagement and spending patterns. 

<div align="center">
  <img src="https://github.com/maissaladjimi/RFM_Customer_Segmentation/assets/94018321/65bce3e4-75d6-49b4-978b-414888d1ade0" alt="Customer Segments">
</div>

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
students_df = pd.read_csv('Expanded_data_with_more_features.csv', index_col='student_id')
df_cleaned = students_df.dropna().copy()  # Make a copy to avoid "SettingWithCopyWarning"

# Compute average score using .loc to avoid SettingWithCopyWarning
df_cleaned['score'] = df_cleaned[['MathScore', 'ReadingScore', 'WritingScore']].mean(axis=1)

# Select only exam score columns for clustering
exam_scores_df = df_cleaned[['MathScore', 'ReadingScore', 'WritingScore']]

# Elbow Method to determine the optimal number of clusters
inertia = []
k_range = range(1, 11)  # Try clustering from 1 to 10 clusters

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(exam_scores_df)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Method graph
plt.figure(figsize=(8,6))
plt.plot(k_range, inertia, marker='o', color='b')
plt.title("Elbow Method for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia (Sum of Squared Distances)")
plt.grid(True)
plt.show()

# Set final number of clusters to 3 based on elbow analysis and fit model
kmeans = KMeans(n_clusters=3, random_state=42)
df_cleaned['cluster'] = kmeans.fit_predict(exam_scores_df)

# Probabilities for Math > 70
target_math = df_cleaned[df_cleaned['MathScore'] > 70]
grouped_math = target_math.groupby('cluster', group_keys=False)

print("\nProbabilities for Math > 70:")
for cluster_id in range(3):  # Ensure all clusters from 0 to 2 are considered
    group = grouped_math.get_group(cluster_id) if cluster_id in grouped_math.groups else pd.DataFrame()
    prob = len(group) / len(target_math) if len(target_math) > 0 else 0
    print(f"P(Cluster {cluster_id} | Math > 70): {prob}")

# Probabilities for Reading > 70
target_reading = df_cleaned[df_cleaned['ReadingScore'] > 70]
grouped_reading = target_reading.groupby('cluster', group_keys=False)

print("\nProbabilities for Reading > 70:")
for cluster_id in range(3):  # Ensure all clusters from 0 to 2 are considered
    group = grouped_reading.get_group(cluster_id) if cluster_id in grouped_reading.groups else pd.DataFrame()
    prob = len(group) / len(target_reading) if len(target_reading) > 0 else 0
    print(f"P(Cluster {cluster_id} | Reading > 70): {prob}")

# Probabilities for Writing > 70
target_writing = df_cleaned[df_cleaned['WritingScore'] > 70]
grouped_writing = target_writing.groupby('cluster', group_keys=False)

print("\nProbabilities for Writing > 70:")
for cluster_id in range(3):  # Ensure all clusters from 0 to 2 are considered
    group = grouped_writing.get_group(cluster_id) if cluster_id in grouped_writing.groups else pd.DataFrame()
    prob = len(group) / len(target_writing) if len(target_writing) > 0 else 0
    print(f"P(Cluster {cluster_id} | Writing > 70): {prob}")

# Plot: Distribution of average scores 

plt.figure(figsize=(8,5))
sns.histplot(df_cleaned["score"], bins=10, kde=True, color='skyblue')
plt.title("Distribution of Average Exam Scores")
plt.xlabel("Average Score")
plt.ylabel("Frequency")
plt.show()


# Plot: Boxplot of scores by exam 

plt.figure(figsize=(8,5))
df_melted = df_cleaned.melt(value_vars=['MathScore', 'ReadingScore', 'WritingScore'],
                            var_name='Exam', value_name='Score')
sns.boxplot(x="Exam", y="Score", data=df_melted)
plt.title("Score Distribution by Exam")
plt.show()


# Top 5 students by average score
top_students = df_cleaned.sort_values("score", ascending=False).head(5)
print("\nTop 5 Students:\n", top_students[['MathScore', 'ReadingScore', 'WritingScore', 'score', 'cluster']])
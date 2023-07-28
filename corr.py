import pandas as pd
import numpy as np
import seaborn as sns
from utility import find_maximum_matching

df = pd.read_csv('output/resume.csv')
df.drop(columns=df.columns[0], axis=1, inplace=True)

df.drop(columns=df.columns[0], axis=1, inplace=True)

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Set the diagonal elements to 0
np.fill_diagonal(correlation_matrix.values, 0)

# Display the correlation matrix
print(correlation_matrix)

correlation_matrix.to_csv('output/inbuilt_function_correlation.csv')

sns.heatmap(correlation_matrix);
            
find_maximum_matching(correlation_matrix)

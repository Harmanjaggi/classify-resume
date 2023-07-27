import pandas as pd
import numpy as np
import seaborn as sns
from utility import find_maximum_matching

df = pd.read_csv('output/resume_without_0.csv')

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Set the diagonal elements to 0
np.fill_diagonal(correlation_matrix.values, 0)

# Display the correlation matrix
print(correlation_matrix)

sns.heatmap(correlation_matrix);
            
print(find_maximum_matching(correlation_matrix))

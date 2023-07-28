import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utility import find_category, word_matching_bins, word_matching_labels

df = pd.read_csv('output/resume_without_0.csv')
df.drop(columns=df.columns[1], axis=1, inplace=True)

def word_matching(df, bins, label):
    wm = [0] * len(df.index)
    rows_list = df.values.tolist()
    for idx, row in enumerate(rows_list):
        category = find_category(row[1])
        for i in range(2, len(row)):
            if(category != find_category(row[i])):
                category = -1
                break
        wm[idx] = category
    return(wm)

# df['Word_Matching_Category'] = pd.cut(df['pdf 0'], bins=word_matching_bins, labels=word_matching_labels)
word_Matching_Category = word_matching(df, word_matching_bins, word_matching_labels)
df.insert(1, 'Word_Matching_Category', word_Matching_Category)
print(df)

df.to_csv('output/word_matching_category.csv')

df=pd.read_csv("output/word_matching_category.csv")  
sns.countplot(x='Word_Matching_Category',data=df)  
plt.show()  
    
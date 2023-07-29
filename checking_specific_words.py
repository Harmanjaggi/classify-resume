import pandas as pd

word_set = {'ai', 'legislative', 'data', 'privacy', 'cyber', 'security', 
                'vulnerability', 'non', 'compliances'}

df = pd.read_csv('output/resume.csv')

condition = df['Words'].apply(lambda x: any(str(word) == str(x) for word in word_set))
filtered_df = df[condition]

print(filtered_df)

filtered_df.to_csv('output/chosen_words.csv', index = False)

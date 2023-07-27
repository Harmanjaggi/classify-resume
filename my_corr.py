import pandas as pd
import seaborn as sns
from utility import find_category
from utility import find_maximum_matching

df = pd.read_csv('output/resume_without_0.csv')

def relation_between_two_pdf(pdf1, pdf2):
    df1 = pd.DataFrame()
    sum_category = None
    n = len(pdf1)
    category_list = [0] * n
    for itr in range(n):
        category1 = find_category(pdf1[itr])
        category2 = find_category(pdf2[itr])
        category_list[itr] = min(category1, category2)
        if(sum_category == None): sum_category = category_list[itr]
        else: sum_category += category_list[itr]
        
    df1.insert(0, 'pdf 1', pdf1)
    df1.insert(1, 'pdf 2', pdf2)
    df1.insert(2, 'category_list', category_list)
    
    print(df1)
    
    return(sum_category / n)

num_of_pdf = df.shape[1] - 1
    
combined_df = pd.DataFrame()

my_corr = [[0] * num_of_pdf for i in range(num_of_pdf)]
for i in range(num_of_pdf):
    for j in range(num_of_pdf):
        if i == j:
            continue
        else:
            pdf1_idx = 'pdf ' + str(i)
            pdf2_idx = 'pdf ' + str(j)
            my_corr[i][j] = relation_between_two_pdf(df[pdf1_idx], df[pdf2_idx])
my_corr = pd.DataFrame(my_corr)

# Change the column names
my_corr.columns = ['pdf ' + str(i) for i in range(num_of_pdf)]
  
# Change the row indexes
my_corr.index = ['pdf ' + str(i) for i in range(num_of_pdf)]

print(my_corr)
sns.heatmap(my_corr);
        
print(find_maximum_matching(my_corr))

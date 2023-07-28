import pandas as pd
import seaborn as sns
from utility import find_category
import matplotlib.pyplot as plt
from utility import find_maximum_matching, find_matching_category, matching_category_label

df = pd.read_csv('output/resume.csv')
df.drop(columns=df.columns[0], axis=1, inplace=True)

pdf_name = df.keys()

def relation_between_two_pdf(pdf1_name, pdf1, pdf2_name, pdf2):
    df1 = pd.DataFrame()
    sum_category = None
    n = len(pdf1)
    num_non_zero = 0
    category_list = [0] * n
    for itr in range(n):
        category1 = find_category(pdf1[itr])
        category2 = find_category(pdf2[itr])
        category_list[itr] = min(category1, category2)
        if(category_list[itr] != 0): num_non_zero += 1
        if(sum_category == None): sum_category = category_list[itr]
        else: sum_category += category_list[itr]
        
    df1.insert(0, pdf1_name, pdf1)
    df1.insert(1, pdf2_name, pdf2)
    df1.insert(2, 'category_list', category_list)
    
    # print(df1)
    
    return(sum_category / num_non_zero, df1)

num_of_pdf = df.shape[1] - 1

# print(df)

# Create an ExcelWriter object
excel_file = pd.ExcelWriter('output/multiple_dataframes.xlsx')

my_corr = [[0] * num_of_pdf for i in range(num_of_pdf)]
for i in range(num_of_pdf):
    for j in range(num_of_pdf):
        if i == j:
            continue
        else:
            pdf1_idx = pdf_name[i]
            pdf2_idx = pdf_name[j]
            my_corr[i][j], temp_df = relation_between_two_pdf(pdf1_idx, df[pdf1_idx], pdf2_idx, df[pdf2_idx])
            if(i < j):
                s = pdf1_idx + ' and ' + pdf2_idx
                # temp_df.rename(columns={'pdf 1': pdf1_idx, 'pdf 2': pdf2_idx}, inplace=True)
                temp_df.to_excel(excel_file, sheet_name=s, index=False)
            
# Save the data and close the ExcelWriter object
excel_file.save()

my_corr = pd.DataFrame(my_corr)

# Change the column names
my_corr.columns = [pdf_name[i] for i in range(num_of_pdf)]
  
# Change the row indexes
my_corr.index = [pdf_name[i] for i in range(num_of_pdf)]

# matching_category = dict.fromkeys(matching_category_label,[])

num_of_matching = int(num_of_pdf * (num_of_pdf - 1) / 2)

matching_category = [[0] * len(matching_category_label) for i in range(num_of_matching)]
t = 0
pdf1 = []
pdf2 = []
matching_value = []
for i in range(num_of_pdf):
    for j in range(i):
        value = my_corr.values[i][j]
        category = find_matching_category(value)
        matching_value.append(value)
        pdf1.append(pdf_name[i])
        pdf2.append(pdf_name[j])
        for cat_idx, cat in enumerate(matching_category_label):
            if(category == cat) : matching_category[t][cat_idx] = 1
        t += 1
            
matching_category = pd.DataFrame(matching_category)
category_value = matching_category.sum()
matching_category.rename(columns={matching_category.columns[0]: 'very poor', matching_category.columns[1]: 'poor', matching_category.columns[2]: 'average', matching_category.columns[3]: 'high', matching_category.columns[4]: 'excellent'}, inplace=True)
matching_category.insert(0, 'Matching_Value', matching_value)
matching_category.insert(0, 'pdf2', pdf2)
matching_category.insert(0, 'pdf1', pdf1)
matching_category.to_csv('output/matching_category.csv')
print(matching_category)

plt.bar(matching_category_label, category_value, width = 0.4)
 
plt.xlabel("Category")
plt.ylabel("No. of matching")
plt.title("Matching category")
plt.show()

my_corr.to_csv('output/custom_correlation.csv')

sns.heatmap(my_corr);
        
find_maximum_matching(my_corr)

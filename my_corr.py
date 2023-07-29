import pandas as pd
import seaborn as sns
from utility import find_category
import matplotlib.pyplot as plt
from utility import find_maximum_matching, find_matching_category, matching_category_label

def relation_between_two_pdf(pdf1_name, pdf1, pdf2_name, pdf2):
    sum_category = None
    num_non_zero = 0
    category_list = []
    for itr in range(len(pdf1)):
        category1 = find_category(pdf1[itr])
        category2 = find_category(pdf2[itr])
        category = min(category1, category2)
        
        if(category == 0): continue
        num_non_zero += 1
        row = [pdf1[itr], pdf2[itr], category]
        category_list.append(row)
        if(sum_category == None): sum_category = category
        else: sum_category += category
    df1 = pd.DataFrame(category_list)
    df1.rename(columns={df1.columns[0]: pdf1_name, df1.columns[1]: pdf2_name, df1.columns[2]: 'category_list'}, inplace=True)
    
    # print(df1)
    
    return(sum_category / num_non_zero, df1)

df = pd.read_csv('output/chosen_words.csv')
df.drop(columns=df.columns[0], axis=1, inplace=True)

pdf_name = df.keys()

num_of_pdf = df.shape[1]

# print(df)

# Create an ExcelWriter object
# excel_file = pd.ExcelWriter('output/multiple_dataframes.xlsx')

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
                # temp_df.to_excel(excel_file, sheet_name=s, index=False)
                address = 'output/two_pdf_matching/' + pdf1_idx + ' and ' + pdf2_idx + '.csv'
                temp_df.to_csv(address, index=False)
            
# Save the data and close the ExcelWriter object
# excel_file.save()

my_corr = pd.DataFrame(my_corr)

# Change the column names
my_corr.columns = [pdf_name[i] for i in range(num_of_pdf)]
  
# Change the row indexes
my_corr.index = [pdf_name[i] for i in range(num_of_pdf)]

my_corr.to_csv('output/custom_correlation.csv')

sns.heatmap(my_corr);
        
pdf1, pdf2, max_val = find_maximum_matching(my_corr)


# Machine Category
threshold = max_val / 2;
num_parts = len(matching_category_label)
step = (max_val - threshold) / num_parts
matching_category_bin = [threshold + i * step for i in range(1, num_parts + 1)]

print(matching_category_bin)

num_of_matching = int(num_of_pdf * (num_of_pdf - 1) / 2)

matching_category = [[0] * len(matching_category_label) for i in range(num_of_matching)]

t = 0
pdf1 = []
pdf2 = []
matching_value = []
matching_category_value = []
for i in range(num_of_pdf):
    for j in range(i):
        value = my_corr.values[i][j]
        category = find_matching_category(value, matching_category_bin)
        matching_value.append(value)
        pdf1.append(pdf_name[i])
        pdf2.append(pdf_name[j])
        matching_category_value.append(category)
        for cat_idx, cat in enumerate(matching_category_label):
            if(category == cat) : matching_category[t][cat_idx] = 1
        t += 1
            
matching_category = pd.DataFrame(matching_category)
category_value = matching_category.sum()
matching_category.rename(columns={matching_category.columns[0]: 'poor', matching_category.columns[1]: 'average', matching_category.columns[2]: 'above average', matching_category.columns[3]: 'good', matching_category.columns[4]: 'very good', matching_category.columns[5]: 'excellent'}, inplace=True)
matching_category.insert(0, 'Matching_Category', matching_category_value)
matching_category.insert(0, 'Matching_Value', matching_value)
matching_category.insert(0, 'pdf2', pdf2)
matching_category.insert(0, 'pdf1', pdf1)

temp_df =  matching_category.sort_values(by=['Matching_Value'])
temp_df.to_csv('output/matching_category.csv', index = False)
# print(matching_category)

plt.bar(matching_category_label, category_value.values, width = 0.4)

# print(matching_category_label)
# print(category_value.values)
 
plt.xlabel("Category")
plt.ylabel("No. of matching")
plt.title("Matching category")
plt.show()

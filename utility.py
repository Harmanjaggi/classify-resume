
word_matching_bins = [1, 3, 5, 7, 9, 11, float('inf')]
word_matching_labels = [10, 20, 30, 40, 50, 60]



def find_category(num):
    if(num == 0): return(0)
    for idx, b in enumerate(word_matching_bins):
        if(b > num):
            return(word_matching_labels[idx - 1])
    return(-1)

matching_category_label = ['poor', 'average', 'above average', 'good', 'very good', 'excellent']

def find_matching_category(num, matching_category_bin):
    for idx, b in enumerate(matching_category_bin):
        if(b >= num):
            return(matching_category_label[idx])
    return(-1)


def find_maximum_matching(correlation_matrix):
    max_val = None
    pdf1 = None
    pdf2 = None
    
    pdf_name = correlation_matrix.keys()

    for r_idx, row in enumerate(correlation_matrix.values):
        for c_idx, val in enumerate(row):
            if(max_val == None or max_val < val):
                max_val = val
                pdf1 = r_idx
                pdf2 = c_idx
    print('pdf ->' + pdf_name[pdf1])
    print('pdf ->' + pdf_name[pdf2])
    print('Matching % ->' + str(max_val))
    return(pdf1, pdf2, max_val)
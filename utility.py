
word_matching_bins = [1, 3, 5, 7, 9, 11, float('inf')]
word_matching_labels = [10, 20, 30, 40, 50, 60]

def find_category(num):
    for idx, b in enumerate(word_matching_bins):
        if(b > num):
            return(word_matching_labels[idx - 1])
    return(-1)

def find_maximum_matching(correlation_matrix):
    max_val = None
    pdf1 = None
    pdf2 = None

    for r_idx, row in enumerate(correlation_matrix.values):
        for c_idx, val in enumerate(row):
            if(max_val == None or max_val < val):
                max_val = val
                pdf1 = r_idx
                pdf2 = c_idx
    return(pdf1, pdf2, max_val)
import numpy as np
import csv
import os
from collections import Counter


def import_data(file):
    with open(file,'r',  encoding='latin-1') as rf:
        r=csv.reader(rf)
        # next(r)
        data=[]
        for row in r:
            data.append(row)
        return data


data = import_data('/home/user/ALIGN/data/GC_NIST17/StdNP.csv')
# print(len(data))
smL = [row[0] for row in data]

smiles_counts = Counter(smL)
data = [row for row in data if smiles_counts[row[0]] == 1]

# if not data:
#     print("All SMILES were duplicates and have been removed.")
# else:
#     print(f"Data after removing duplicates contains {len(data)} entries.")
# print(len(data))
# exit()
data = list(set(tuple(row) for row in data)) ## making sure all instances are unique


# header = [data[0]]

# data = data[1:]

seed = 10
for seed in range(1, 11):
    print(data[:10])
    np.random.seed(seed)
    np.random.shuffle(data)


    # header.extend(data)
    train_val_split = 0.9

    split_index = int(len(data) * train_val_split)
    train_data = data[:split_index]
    test_data = data[split_index:]
    train_dir = '/home/user/ALIGN/data/GC_NIST17/Nonpolar'
    os.makedirs(train_dir, exist_ok=True)

    train_file = os.path.join(train_dir, str(seed) + '_train.csv')
    test_file = os.path.join(train_dir, str(seed) + '_test.csv')

    # print((set(tuple(row) for row in train_data) & set(tuple(row) for row in test_data)))

    print(list(set(tuple(row) for row in train_data) & set(tuple(row) for row in test_data)))
    assert list(set(tuple(row) for row in train_data) & set(tuple(row) for row in test_data)) == []

    with open(train_file, 'w', newline='') as train_wf:
        train_writer = csv.writer(train_wf)
        train_writer.writerows(train_data)
        print(f"Train data saved to {train_file}")

    with open(test_file, 'w', newline='') as test_wf:
        test_writer = csv.writer(test_wf)
        test_writer.writerows(test_data)
        print(f"Test data saved to {test_file}")

    # output_file = '/home/user/Desktop/RT_data/split_42/filter_METLIN' + str(seed) + '.csv'
    # with open(output_file, 'w', newline='') as wf:
    #     writer = csv.writer(wf)
    #     writer.writerows(header)
    #     print(f"Shuffled data saved to {output_file}")

import csv
import random
import string

MAX_DATASET_ENTRIES_NUMBER = 50

header = ['cid', 'size_of_asset_avanza_sek']
data = ['Afghanistan', 652090, 'AF', 'AFG']


def get_random_string(length) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


with open('testing_sample.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(MAX_DATASET_ENTRIES_NUMBER):
        col_1 = get_random_string(8)
        col_2 = random.randint(1, 10000)
        writer.writerow([col_1, col_2])

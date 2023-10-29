import fasttext
import csv
import os 

model = fasttext.load_model('/workspace/datasets/fasttext/title_model_v1_10_20.bin')

neighbors = model.get_nearest_neighbors('inkjet')

top_words_file = '/workspace/datasets/fasttext/top_words.txt'
synonyms_file = '/workspace/datasets/fasttext/synonyms_v1_10_20.csv'

if os.path.exists(synonyms_file):
    # Remove the old file
    os.remove(synonyms_file)


with open(top_words_file, 'r') as top_words:
    with open(synonyms_file, mode = 'w', newline = '') as synonyms: 
        csv_writer = csv.writer(synonyms)
        count = 0
        for line in top_words: 
            top_word = line.strip()
            nearest_neighbors = model.get_nearest_neighbors(top_word)
            candidates = []
            for neighbor in nearest_neighbors:
                # print(f'current neighbor is {neighbor[0]}, {neighbor[1]}')
                if float(neighbor[0]) > 0.75:
                    candidates.append(neighbor[1]);

            

            if len(candidates) > 0:
                candidates = [top_word] + candidates
                count = count + 1
                csv_writer.writerow(candidates)        

                    
                    


import pandas as pd

def split_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    segments = []
    segment = []
    for line in lines:
        if line[0].isdigit() and '|' in line:
            if segment:
                segments.append(''.join(segment))
            segment = [line]
        else:
            segment.append(line)
    if segment:
        segments.append(''.join(segment))
    return segments

target_str = split_file(r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\pulled_texts_new.txt')

def process_strings(strings):
    data = []
    no_genres = []
    for string in strings:
        movie_id = string.split('|')[0]
        genres_start = string.find('Genres')
        genres_end = string.find('Links')
        genres = string[genres_start+len('Genres'):genres_end].strip().lower()
        if genres:
            genres = genres.split(',')
            genres = [i.strip() for i in genres]
            data.append([movie_id, genres])
        else:
            no_genres.append(movie_id)
    df = pd.DataFrame(data, columns=['MovieId', 'Genres'])
    df.to_csv(r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\output_clean.csv', index=False, encoding='utf-8')
    with open(r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\no_genres_mvs.txt', mode='w', encoding='utf-8') as f2:
        for i in no_genres:
            f2.write(str(i)+'\n')
    pass

process_strings(target_str)
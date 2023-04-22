import json
import random
from tqdm import tqdm
from os.path import join
from dataloader import JsonLoader
from segmentor import TopicSegmentor
from extractor import ProductExtractor, RoleExtractor
from utils import process_reactions

def text_segmentation(data_path):
    segmentor = TopicSegmentor(device='cuda:0')
    results = segmentor.segment(context=data_path)
    return [' '.join(segment) for segment in results]

def extract_prod(data):
    prod_extractor = ProductExtractor()
    prods = prod_extractor.extract(data)
    assert len(prods) == len(data)

    # remove the last '.' token in the products
    for i in range(len(prods)):
        if prods[i][-1] == '.':
            prods[i] = prods[i][:-1]
    
    # return text-product pairs
    reactions = []
    for i in range(len(prods)):
        if prods[i] != 'None':
            prod_list = prods[i].split(', ')
            for cur_prod in prod_list:
                cur = {}
                cur['text'] = data[i]
                cur['product'] = cur_prod
                reactions.append(cur)
    return reactions

def extract_role(reactions):
    role_extractor = RoleExtractor()
    for i in range(len(reactions)):
        roles = role_extractor.extract(reactions[i]['text'], reactions[i]['product'])
        reactions[i].update(roles)
    return reactions

def main(data_path):
    # load data
    data_loader = JsonLoader(json_format='acs')
    data = data_loader.load(data_path)

    random.shuffle(data)

    max_count = 100
    cur_count = 0

    for i in tqdm(range(len(data))):
        try:
            cur_data = data_loader.process(data[i])

            # load data and text segmentation
            segmented_text = text_segmentation(cur_data)

            # extract products
            reactions = extract_prod(segmented_text)

            # extract roles
            reactions = extract_role(reactions)

            # post-processing of the extracted results
            reactions = process_reactions(reactions)

            if len(reactions) < 3:
                continue

            result = {}
            result['title'] = data[i]['title']
            result['id'] = data[i]['id']
            result['journal'] = data[i]['journal']
            result['reactions'] = reactions
            with open(join('output', '{}.json'.format(cur_count)), 'w') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            cur_count += 1
            if cur_count >= max_count:
                break
            
        except:
            print(data[i]['id'])

if __name__ == "__main__":
    # data_path = 'data/Stereodivergent_Synthesis.json'
    data_path = '../data/ACS/acs_data.jsonl'
    main(data_path)
    
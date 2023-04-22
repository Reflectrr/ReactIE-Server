import json
from tqdm import tqdm
from .dataloader import JsonLoader
from .segmentor import TopicSegmentor
from .extractor import ProductExtractor, RoleExtractor
from .utils import process_reactions

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
    for i in tqdm(range(len(reactions))):
        roles = role_extractor.extract(reactions[i]['text'], reactions[i]['product'])
        reactions[i].update(roles)
    return reactions

def main(data_path):
    # load data
    data_loader = JsonLoader()
    data = data_loader.load(data_path)
    data = data_loader.process(data)

    # load data and text segmentation
    print('Start Text Segmentation !!!')
    segmented_text = text_segmentation(data)

    # extract products
    print('Start Extracting Products !!!')
    reactions = extract_prod(segmented_text)

    # extract roles
    print('Start Extracting Roles !!!')
    reactions = extract_role(reactions)

    # post-processing of the extracted results
    reactions = process_reactions(reactions)

    # print results
    if len(reactions) == 0:
        print('There is no reactions in this file!')
    else:
        for i in range(len(reactions)):
            print('\nReaction {}:'.format(i + 1))
            for k, v in reactions[i].items():
                print("{}: {}".format(k, v))

def get_extraction(data_path):
    # load data
    data_loader = JsonLoader()
    data = data_loader.load(data_path)
    data = data_loader.process(data)

    # load data and text segmentation
    print('Start Text Segmentation !!!')
    segmented_text = text_segmentation(data)

    # extract products
    print('Start Extracting Products !!!')
    reactions = extract_prod(segmented_text)

    # extract roles
    print('Start Extracting Roles !!!')
    reactions = extract_role(reactions)

    # post-processing of the extracted results
    reactions = process_reactions(reactions)

    return reactions

    # print results
    if len(reactions) == 0:
        print('There is no reactions in this file!')
    else:
        return reactions
        # for i in range(len(reactions)):
        #     print('\nReaction {}:'.format(i + 1))
        #     for k, v in reactions[i].items():
        #         print("{}: {}".format(k, v))

if __name__ == "__main__":
    data_path = 'data/Stereodivergent_Synthesis.json'
    # data_path = '../data/ACS/acs_data.jsonl'
    main(data_path)
    
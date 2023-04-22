import torch
from tqdm import tqdm
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM

class ProductExtractor:
    def __init__(self, model_name_or_path=None, max_length=256, device='cuda:0', cache_dir=None):
        """ Set up model """
        if model_name_or_path is None:
            model_name_or_path = '/shared/data3/mingz5/chem/prod_extraction/best_model/checkpoint-3860'

        self.device = device
        self.max_length = max_length

        self.config = AutoConfig.from_pretrained(model_name_or_path, cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, cache_dir=cache_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, config=self.config,
                                                           cache_dir=cache_dir)
        
        self.model.eval()
        self.model.to(device)
        
        self.q = 'What are the products of the chemical reactions in the text?'
    
    def extract(self, inputs, batch_size=16):
        inputs_with_q = []
        for i in range(len(inputs)):
            inputs_with_q.append(self.q + ' \n ' + inputs[i])
        results = []
        for i in tqdm(range(0, len(inputs_with_q), batch_size)):
        # for i in range(0, len(inputs_with_q), batch_size):
            input_text = inputs_with_q[i: i + batch_size]
            with torch.no_grad():
                input_ids = self.tokenizer(
                    input_text,
                    max_length=self.max_length,
                    truncation=True,
                    padding=True,
                    return_tensors='pt'
                ).to(self.device)
                output_ids = self.model.generate(**input_ids)
                results += self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return results

class RoleExtractor:
    def __init__(self, model_name_or_path=None, max_length=256, device='cuda:0', cache_dir=None):
        """ Set up model """
        if model_name_or_path is None:
            model_name_or_path = '/shared/data3/mingz5/chem/role_extraction/best_model/checkpoint-2358'

        self.device = device
        self.max_length = max_length

        self.config = AutoConfig.from_pretrained(model_name_or_path, cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, cache_dir=cache_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, config=self.config,
                                                           cache_dir=cache_dir)
        
        self.model.eval()
        self.model.to(device)
        
        self.roles = ['reactants', 'yield', 'temperature', 'time', 'reaction type', 'solvent', 'catalyst']
    
    @staticmethod
    def get_query(prod, role):
        if role == 'reactants':
            query = 'If the final product is ' + prod + ', what are the reactants for this chemical reaction?'
        else:
            query = 'If the final product is ' + prod + ', what is the ' + role + ' for this chemical reaction?'
        return query

    # text is a string here
    def extract(self, text, prod):
        input_text = []
        for role in self.roles:
            query = self.get_query(prod, role)
            cur_input = query + ' \n ' + text
            input_text.append(cur_input)
        with torch.no_grad():
            input_ids = self.tokenizer(
                    input_text,
                    max_length=self.max_length,
                    truncation=True,
                    padding=True,
                    return_tensors='pt'
                ).to(self.device)
            output_ids = self.model.generate(**input_ids)
            results = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        assert len(self.roles) == len(results)
        role_results = {}
        for i in range(len(results)):
            if results[i] != 'None':
                cur_role = self.roles[i]
                role_results[cur_role] = results[i]
        return role_results

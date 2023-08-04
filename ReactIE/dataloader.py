import json

def flat(doc):
    res = []
    for i in doc:
        if isinstance(i, dict):
            res.extend(flat(i['content']))
        else:
            res.append(i)
    return res

class JsonLoader:
    def __init__(self, json_format='default', section=None):
        """ 
            default: our PDF-to-json format
            acs:     format of processed acs_data.jsonl
        """
        self.format = json_format
        assert self.format in ['default', 'acs']

        self.section = ['content']

    # load json/jsonl files, and return one or a list of dictionaries
    def load(self, data_path):
        data = []
        with open(data_path) as f:
            if self.format == 'default':
                data = json.loads(f.read())
            elif self.format == 'acs':
                for line in f:
                    data.append(json.loads(line))
        return data

    # process one json data, and return a list of paragraphs
    def process(self, data):
        # Section filtering is available by default, 
        # while data processing in ACS format does not include section filtering
        context = []
        if self.format == 'default':
            # section filtering
            for sec in self.section:
                context += data[sec]
        elif self.format == 'acs':
            for instance in data['full_text']:
                context += flat(instance['content'])
        return context
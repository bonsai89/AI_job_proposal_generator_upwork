from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

uncommon_names = [
    "Amaya", "Anya", "Bexley", "Briar", "Ellerie", "Effie", "Evelina",
    "Imani", "Lyra", "Shiloh", "Axton", "Rhett"
]

def get_client_name(output):
    text = output #" ".join(output['review'])
    
    for uncommon_name in uncommon_names:
        if uncommon_name in text.split():
            return uncommon_name
    
    entities = nlp(text)
    name_freq = {}
    for entity in entities:
        if entity['entity_group'] == "PER":
            person_name = entity['word']
            if person_name[0].isupper() and person_name!="Client":
                if person_name in name_freq.keys():
                    name_freq[person_name] += 1
                else:
                    name_freq[person_name] = 1
    
    if len(name_freq) == 0:
        return "Client"
    else:
        mx_freq = -1
        mx_name = ""
        for key, value in name_freq.items():
            if value > mx_freq:
                mx_freq = value
                mx_name = key
        return mx_name

if __name__ == "__main__":
    with open("outputs\outputs-0.json", "r") as fp:
        output = json.load(fp)
        print(get_client_name(output))
    
    with open("outputs\outputs-1.json", "r") as fp:
        output = json.load(fp)
        print(get_client_name(output))
    
    with open("outputs\outputs-2.json", "r") as fp:
        output = json.load(fp)
        print(get_client_name(output))


import os, pypdf, logging, tiktoken, json

from tqdm import tqdm

# scan the PDF ro get the String
def policy_processing(data_path):
    # silence non-critical errors while parsing PDF files
    logging.getLogger("pypdf").setLevel(logging.CRITICAL)

    data = {}

    files = os.listdir(data_path)
    print(f"reading {len(files)} files in {data_path}")
    for f in files:
        path = os.path.join(data_path, f)

        # each datum will have at least these attributes
        d = {'filepath': None, 'title': None, 'text': None}

        # parse pdf text, if exists
        if path.endswith('.pdf'):
            if path[:-4] in data:
                d = data[path[:-4]]

            print('  File: %s' % f)
            text = ''
            reader = pypdf.PdfReader(path)
            for page in reader.pages:
                text += page.extract_text()
            d['filepath'] = path
            d['text'] = text
            data[path[:-4]] = d

    policy_txt = [d for d in data.values()]
    return policy_txt

# tokenize the string of policy
def policy_tokenize(policy_txt, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(policy_txt)
    print(f"{len(tokens)} are generated")
    return tokens

def token_to_text(tokens, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    policy_text = enc.decode(tokens)
    return policy_text



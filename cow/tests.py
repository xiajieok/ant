import os
id_file = os.path.join(os.getcwd(), '.asset_id')

with open(id_file) as f:
    print(f.read())
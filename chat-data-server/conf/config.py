import yaml
with open('conf/config.yml', 'r') as f:
    yml = yaml.load(f, Loader=yaml.FullLoader)
    OPENAI_KEY=yml.get('openai').get('api_key')
    DB_URI=yml.get('database').get('db_uri')
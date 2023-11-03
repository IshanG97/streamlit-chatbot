def load_api_key(api_key_file):
    with open("api_keys/" + api_key_file, "r") as f:
        api_key = f.read().strip()
        return api_key
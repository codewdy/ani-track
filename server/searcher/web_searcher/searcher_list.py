from searcher.web_searcher.searcher import Searcher
import json
from pathlib import Path
from functools import cache

def searcher_config():
    with open(Path(__file__).parent / "searcher.json", "r") as f:
        return json.load(f)

@cache
def searcher_list():
    return [Searcher(config) for config in searcher_config()["searchers"]]

if __name__ == "__main__":
    print(searcher_list())

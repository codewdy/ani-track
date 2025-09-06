from context import Context
import json


async def search(keyword: str):
    url = "https://api.bgm.tv/v0/search/subjects"
    params = {
        "keyword": keyword,
        "sort": "rank",
        "filter": {
            "type": [
                2
            ],
            "nsfw": True
        }
    }
    async with Context.client.post(url, data=json.dumps(params)) as response:
        data = await response.json()
    result = []
    for item in data["data"]:
        result.append({
            "id": str(item["id"]),
            "name": item["name_cn"] or item["name"],
            "image": item["image"],
        })
    return result

if __name__ == "__main__":
    from context import Context
    import asyncio

    async def run():
        async with Context() as ctx:
            return await search(
                "碧蓝之海"
            )

    print(asyncio.run(run()))

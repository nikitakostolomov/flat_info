import asyncio
from time import perf_counter
from typing import List

import aiohttp
import requests
from bs4 import BeautifulSoup

# par = {"cd":'1'}
# r = requests.get('https://www.avito.ru/magnitogorsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1', headers={'Accept-Encoding': 'gzip, deflate, br'})
#
# soup = BeautifulSoup(r.text, 'html.parser')
# print(len(soup.findAll(attrs={"data-marker": "item-address"})))
# for flat in soup.findAll(attrs={"data-marker": "item-address"}):
#     print(flat.text)


def get_flat_refs(flat_page_url: str) -> List[str]:
    r = requests.get(flat_page_url)
    print(r.request.headers)
    soup = BeautifulSoup(r.text, "html.parser")
    flat_refs = []
    # print(len(soup.findAll(attrs={"data-marker": "item-address"})))
    for flat in soup.findAll(attrs={"data-marker": "item-address"}):
        ref_class = flat.findPreviousSibling(
            attrs={"class": "iva-item-titleStep-pdebR"}
        )
        # 'a' is tag inside ref_class, 'a' contains ref to flat
        flat_refs.append(ref_class.a["href"])
        # print(ref_class.a["href"])
        ref = ref_class.find("a", href=True)
        # print(ref["href"])
    return flat_refs


headers = {
    "Referer": "https://www.avito.ru/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'max-age=0', 'Cookie': 'u=2tme79y7.omvmk8.4gjjymhm8mm0; _gcl_au=1.1.1582788589.1670590761; tmr_lvid=d7e0d8fe834ea83fde30ff77442b5393; tmr_lvidTS=1670590761545; _ga=GA1.1.1717383372.1670590762; _ym_uid=1670590781403404084; _ym_d=1670590781; buyer_location_id=661100; uxs_uid=6946bb30-77c1-11ed-8d22-79268682b424; buyer_laas_location=661100; luri=magnitogorsk; _ym_isad=1; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b92e1d4a3283ded56a90d83bac5e6e82bd59c9621b2c0fa58f915ac1de0d034112251851063192bbc234d62295fceb188df88859c11ff008953de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa87fde300814b1e8553de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2b5b87f59517a23f280a995c83bf64175352c31daf983fa077a7b6c33f74d335cb88de1666d503ec6bd292828d78d788602c730c0109b9fbb963daedbf4968a60f63c1114aca04b6a0e28148569569b79aa3dbdc979b77fcef8850595920be5cd46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dcc6532bf1f581629c62da10fb74cac1eab2da10fb74cac1eabf67834b86360393cfa48ea3860c445aadb1614ea79b06f8db841da6c7dc79d0b; ft="kDDVf3pyHYNB38PgcNll1GEGSA9O+DRvH5Y+LgpFUJ624hK7s03jG7K54yLJxQSInTyoeJkrWE7ZXMELfM7bdM9tMNsBuqIAkIVirTPnCofxvZWvAdbGz4g9TnCbwYK8D71tf2zrz6hqspZamPdXHONh8tyg71YvsJJLfDJ2CKrmFnNX9RPPKHiHx1HXYwxP"; __zzatw-avito=MDA0dBA=Fz2+aQ==; __zzatw-avito=MDA0dBA=Fz2+aQ==; cfidsw-avito=oTvYGDXS9yIfAWSkaPBPvxAHw1aJpn0Dv8Ej9ush0PQTAxBBL9TzCSlzET3tgJK4p4+/DJcrnblIN7NOCWqXot9HRhknuuzblniepjRmNh9JAMt0Oe2lPfN3duNZK6UTScFxybnmmwWKz7uen8LqI0datvf4zq/cL+yP0g==; cfidsw-avito=oTvYGDXS9yIfAWSkaPBPvxAHw1aJpn0Dv8Ej9ush0PQTAxBBL9TzCSlzET3tgJK4p4+/DJcrnblIN7NOCWqXot9HRhknuuzblniepjRmNh9JAMt0Oe2lPfN3duNZK6UTScFxybnmmwWKz7uen8LqI0datvf4zq/cL+yP0g==; gsscw-avito=UpPcto17ffc5GELsrF/L90FQ4UPm8eG5oKe52KSnt1t528OuG4KtuZKzXA+GRIpZH5w4R9E1gLRA2tIsSMoom/1MlX+FwpiDgff+owpg5Cr3UytiDBACKFkpxs2xgXxJ5UzFZPdSrUpCGqGtBamUjNeNREwOiDJenCdEXmI/+jpYCYutmnBPkPOkES2hhEK/06NbvqK6627k7sNxlXFN3Vjus7P6F5xZOYbgYtIWXDXbesFu3vVjwVT8aRHF1Ix5EQ==; gsscw-avito=UpPcto17ffc5GELsrF/L90FQ4UPm8eG5oKe52KSnt1t528OuG4KtuZKzXA+GRIpZH5w4R9E1gLRA2tIsSMoom/1MlX+FwpiDgff+owpg5Cr3UytiDBACKFkpxs2xgXxJ5UzFZPdSrUpCGqGtBamUjNeNREwOiDJenCdEXmI/+jpYCYutmnBPkPOkES2hhEK/06NbvqK6627k7sNxlXFN3Vjus7P6F5xZOYbgYtIWXDXbesFu3vVjwVT8aRHF1Ix5EQ==; fgsscw-avito=c4SH8c60018bddf62abf929ae12369aa6b9d5d1f; fgsscw-avito=c4SH8c60018bddf62abf929ae12369aa6b9d5d1f; cfidsw-avito=fa1+1bWP6tz9Au9vnnOIGZqESuzTarbHh90fN8W1dl5AESP6t9kCZ83yBEY47TLoHORQzx0CisrMcpfcv8mVYx1piVcWW7l8yCP/4k7oFTVdiCS2PteKA3yRDxPSpdc/yHCBFEln/nCtHQkvxYRTcCIxDsRKj9DCeukV5w==; v=1670865372; sx=H4sIAAAAAAAC%2F1TSSZLqMAzG8btkzcKTJKtvY1tyCGSAhpDhFXd%2FxYIuWHn3K9df37%2FGB9BQxEv0UgApMqswiOSo5DI3P%2F%2BaR%2FPT7EhbOI46j2f5LcehW3eGcGnpXJKpoTk02vxYJMMeQnTPQwNO6vE6LvP9dpuWJSwhmNC2t%2FIm%2BX4vZuZ9Hi3mvlNa5kvpprK0tkpqP0kDwb5ILOrZa7RMGbwp1Ul2xILFO5T4lgMvly10j3w8wX3Go11dttc4yrnvzzp9yCECv2Q0pULIMWWEZIsxyVsfnCuYQH0Mbzndhw1T38uRlzDS%2Bao9xDv%2BrsDDMn5lcMbwS0bEIoSVkQEDslJWz0JgSiH5C3wBvFKAJRjbku2mdmPAYd9u7mLqTh8yWKJX4KhZvKs1AkUUQYmGKKvkiinnWN9yt7iwl3E93tu1u8bdPtbJrHB0t4mX2X2dDox5Hpqk4EOCSg5NMbEm53zFqhq4mpT%2BakydM2Km9kwrOygsjxLLqb9DnrtLtp%2ByZaTnoSlgMgJ6ZCtoY3ZRLIkCMZMPHt9yXod9ZduNPm%2BDJWrTaT9dL9Oqed90%2BJAds4kvGTEExqyY1VZfvC8egzWROQVS%2B5bHfk4ofpTUGz%2FcJ439igsOe0%2Femvh9Qff6s7jqg4CaVExJISEji4gkVY3E8rfn37XL3WhPwylHKpvfVfff4SiPsdel%2B5YtPg9NNQycE8ZgICXnhJ1AYYP29dDfntdBIPUb1dzvKjF2j3paoZ%2F3cK56Gr%2F27Bw%2Bn%2F8DAAD%2F%2F017HaDYAwAA; dfp_group=12; abp=1; cto_bundle=xFIXW19NOFUzY2s3SUE5UWZFVENQYmJJT0pFUDg1VjR4NVQlMkZqZFVpQzVEcFJES2U3NFJUS0laUGZrOTNSa2JZZVhJc2dreiUyRkhoRTN1YW5KQ1pYZDAzQW5kUEw4OUIwNzZLUzUzalQ3eTJpNFhUd1BtVUFDTTRnJTJGYklZQURTanB0ODBaeXpNdmduZGUyMiUyRkEzbTRGUm94THJuQSUzRCUzRA; _ga_M29JC28873=GS1.1.1670865379.8.0.1670865379.60.0.0; _ym_visorc=b; isCriteoSetNew=true; tmr_detect=0%7C1670865382807', 'If-None-Match': 'W/"1da581-wzixAg17JfEogo7kVYapW2WfcKk"', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Linux"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


async def fetch(s, flat_pagination_number: int):
    async with s.get(
        "https://www.avito.ru/magnitogorsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1",
        ssl=False,
    ) as r:
        return await r.text()
        if r.status != 200:
            r.raise_for_status()
        return await r.text()


async def fetch_all(s, page_numbers):
    # tasks = []
    # for number in page_numbers:
    #     task = asyncio.create_task(fetch(s, number))
    #     tasks.append(task)
    # print(tasks)
    task = asyncio.create_task(fetch(s, 1))
    res = await task
    return res


async def main():
    page_numbers = range(1, 2)
    async with aiohttp.ClientSession(headers=headers) as session:
        htmls = await fetch_all(session, page_numbers)
        print(htmls)


if __name__ == "__main__":
    # a = get_flat_refs(
    #     "https://www.avito.ru/magnitogorsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1"
    # )
    # print(a)
    # start = perf_counter()
    asyncio.run(main())
    # stop = perf_counter()
    # print("time taken:", stop - start)

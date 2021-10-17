import csv
import math

fields = ['name','url','address','access','category','description','average_price','pet_dog_small','pet_dog_medium','pet_dog_large','pet_cat','pet_others','pet_otherInfo']

def main():
    lists = read_from_CSV('../data/raw/gnavi_fix_missing.csv')
    lists.sort(key=lambda x: x['category'])
    list_count =  math.ceil(len(lists) / 2000)
    for i in range(list_count):
        sub_list = lists[(i*2000) : (i+1)*2000]
        write_to_file(sub_list, i)

def write_to_file(lists, index):
    path = '../data/gnavi_' + str(index) + '.csv'
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(lists)

def read_from_CSV(path):
    with open(path, newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lists = []
        data_set = set()
        for rows in csv_reader:
            if rows['address'] in data_set:
                continue

            data = {}
            data['name'] = rows['name']
            data['url'] = rows['url']
            data['address'] = rows['address']
            data['access'] = rows['access']
            data['average_price'] = rows['average_price']
            data['pet_dog_small'] = rows['pet_dog_small']
            data['pet_dog_medium'] = rows['pet_dog_medium']
            data['pet_dog_large'] = rows['pet_dog_large']
            data['pet_cat'] = rows['pet_cat']
            data['pet_others'] = rows['pet_others']
            data['pet_otherInfo'] = rows['pet_otherInfo']
            data['description'] = rows['description']

            category = rows['description']

            if "ドッグ" in category or "犬" in category:
                category = "ドッグカフェ"
            elif "CHEF" in category or "シェフ" in category:
                category = "CHEF's Bar"
            elif "上海" in category or "中華" in category or "四川" in category:
                category = "中華料理"
            elif "海鮮" in category:
                category = "海鮮料理"
            elif "イタリア" in category or "イタリア" in data['name'] or "ピザ" in category or "イタリアン" in category:
                category = "イタリアン料理"
            elif "フランス" in category or "フレンチ" in category:
                category = "フランス料理"
            elif "肉" in category or "ハンバーガー" in category or "鉄板焼" in category or "炭火" in category or "焼き" in category or "牛" in category:
                category = "肉料理"
            elif "ケーキ" in category:
                category = "ケーキ"
            elif "カフェ" in category or "Cafe" in category or "CAFE" in category or "タピオカ" in category or "ハブ" in category or "サンド" in category or "飲め" in category or "喫茶" in category or "洋菓子" in category:
                category = "カフェ"
            elif "メキシコ" in category:
                category = "メキシコ料理"
            elif "鶏" in category or "チキン" in category or "串" in category:
                category = "鶏料理"
            elif "バー" in category or "BAR" in category:
                category = "バー"
            elif "BBQ" in category:
                category = "BBQ"
            elif "CURRY" in category:
                category = "カレー"
            elif "アイス" in category or "クリーム" in category:
                category = "アイスクリーム"
            elif "アジア" in category:
                category = "アジア料理"
            elif "アフリカ" in category:
                category = "アフリカ料理"
            elif "アメリカ" in category:
                category = "アメリカ料理"
            elif "そば" in category or "うどん" in category:
                category = "麺料理"
            elif "タイ" in category:
                category = "タイ料理"
            elif "欧" in category:
                category = "欧風料理"
            elif "居酒屋" in category or "和風" in category or "和食" in category or "日本" in category or "酒" in category or "沖縄":
                category = "和食"
            elif "ドイツ" in category:
                category = "ドイツ料理"
            elif "韓国" in category:
                category = "韓国料理"
            elif "ビア" in category:
                category = "ビアホール・ビアガーデン"

            data['category'] = category

            print(data['description'], category)
            lists.append(data)

            data_set.add(data['address'])
    return lists


if __name__ == '__main__':
    main()

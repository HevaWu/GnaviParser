import csv
import math

fields = ['area_list', 'tags_list', 'name', 'description', 'url', 'category', 'address', 'access', 'business_hours', 'regular_holidays', 'price', 'phone_no', 'if_reservation_needed']

param = 'shopping'
base_path = '../data/raw/walkerplus_' + param + '_fix_missing.csv'
sub_path = '../data/walkerplus_' + param + '_'

def main():
    lists = read_from_CSV(base_path)
    lists.sort(key=lambda x: x['tags_list'])
    list_count =  math.ceil(len(lists) / 2000)
    for i in range(list_count):
        sub_list = lists[(i*2000) : (i+1)*2000]
        write_to_file(sub_list, i)

def write_to_file(lists, index):
    path = sub_path + str(index) + '.csv'
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(lists)

def read_from_CSV(path):
    with open(path) as csvFile:
        csvReader = csv.DictReader(csvFile)
        lists = []
        for rows in csvReader:
            data = {}
            data['name'] = rows['name']
            data['area_list'] = rows[' area_list']
            data['description'] = rows[' description']
            data['url'] = rows[' url']
            data['category'] = rows[' category']
            data['tags_list'] = rows[' tags_list']
            data['address'] = rows[' address']
            data['access'] = rows[' access']
            data['business_hours'] = rows[' business_hours']
            data['regular_holidays'] = rows[' regular_holidays']
            data['price'] = rows[' tarif']
            data['phone_no'] = rows[' phone_no']
            data['if_reservation_needed'] = rows[' if_reservation_needed']

            tags = data['tags_list'].split()
            areas = data['area_list'].split()

            if tags and areas:
                for tag in tags:
                    for area in areas:
                        newData = data.copy()
                        newData['tags_list'] = tag.replace("'", "")
                        newData['area_list'] = area.replace("'", "")
                        lists.append(newData)
            elif tags:
                for tag in tags:
                    newData = data.copy()
                    newData['tags_list'] = tag
                    lists.append(newData)
            elif areas:
                for area in areas:
                    newData = data.copy()
                    newData['area_list'] = area
                    lists.append(newData)
            else:
                lists.append(data)

        return lists

if __name__ == "__main__":
    main()

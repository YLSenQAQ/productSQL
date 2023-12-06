# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import xlrd
import json
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def print_os():

    print("123")
    workbook = xlrd.open_workbook("C:\\Users\\wawuw\\Desktop\\osImage.xls")

    sheet1_object = workbook.sheet_by_index(0)

    # 获取sheet1中的有效行数
    nrows = sheet1_object.nrows
    ncols = sheet1_object.ncols

    row2 = sheet1_object.row_values(rowx=1)
    familyNum = 0
    imageTypeCode = row2[1]
    imageCode = row2[2]
    imageVersionCode = row2[3]
    print("code=", imageTypeCode, imageCode, imageVersionCode)

    row3 = sheet1_object.row_values(rowx=2)
    typeName = row3[1]

    i = 0
    print(nrows, ncols)
    top = {}
    top2 = {}
    allObj = {}
    for i in range(2, nrows):
        row = sheet1_object.row_values(rowx=i)
        # print(row)

        num = int(row[0])
        imageType = row[1]
        image = row[2]
        top[row[1]] = {}
        top2[row[1]] = {}
        alist = [imageType]
        allObj[image + "-" + imageType] = alist

    for i in range(2, nrows):
        row = sheet1_object.row_values(rowx=i)
        # print(row)

        num = int(row[0])
        imageType = row[1]
        image = row[2]
        version = row[3]
        top[imageType][image + "-" + imageType] = image
        top2[imageType][image + "-" + imageType] = image + "-" + imageType
        dirImage = {}
        dirImage['num'] = num
        dirImage['ver'] = version
        allObj[image + "-" + imageType].append(dirImage)

        print(num, imageType, image, version)
    # print(top)
    print(" -- image type:--------------")
    print(
        "INSERT INTO `product_attr_enum` (`attr_enum_code`, `enum_value`, `enum_label`, `state`, `sequence`, `extend_info`) VALUES")
    for key in top:
        print("('" + imageTypeCode + "','" + key.lower() + "','" + key + "','" + "ENA" + "'," + str(
            familyNum) + ",'" + json.dumps(top[key]) + "'),")
        familyNum = familyNum + 1
    print(" -- image-------------------")
    # print(allObj)
    imgNum = 0
    for key in allObj:
        # print(key + str(allObj[key]))
        verMap = {}
        ImgType = ""

        for item in allObj[key]:
            if (isinstance(item, str)):
                ImgType = item
            else:
                verMap[item['ver']] = item['ver']
        # print(json.dumps(verMap))
        print("('" + imageCode + "','" + key + "','" + top[ImgType][key] + "','" + "ENA" + "'," + str(
            imgNum) + ",'" + json.dumps(verMap) + "'),")
        imgNum = imgNum + 1
    print(" -- version-------------------")
    for key in allObj:
        for item in allObj[key]:
            # print(item['ver'])
            # print(item['num'])
            if (isinstance(item, dict)):
                print("('" + imageVersionCode + "','" + item['ver'] + "','" + item['ver'] + "','" + "ENA" + "'," + str(
                    item['num']) + "," + "NULL" + "),")
    # print(allObj)

    print(" -- third_part_config_mapping-------------------")
    print(
        "INSERT INTO `third_part_config_mapping` (`config_key`, `config_value`, `config_description`, `create_time`) VALUES")
    for key in allObj:
        for item in allObj[key]:
            # print(item['ver'])
            # print(item['num'])
            if (isinstance(item, dict)):
                print(" -- " + item['ver'] + "-------------------")
                print("('ecsImageType', '{\"imageId\":\"" + item[
                    'ver'] + "\",\"imageGbSize\":20,\"imageUuid\":\"3568e64c5a3f4ef59eeb510dcd0c93c7\"}', 'ECS镜像', NOW()),")
                print("('ecsImageType', '{\"imageId\":\"" + item[
                    'ver'] + "\",\"imageGbSize\":40,\"imageUuid\":\"3568e64c5a3f4ef59eeb510dcd0c93c7\"}', 'ECS镜像', NOW()),")
                print("('ecsImageType', '{\"imageId\":\"" + item[
                    'ver'] + "\",\"imageGbSize\":100,\"imageUuid\":\"3568e64c5a3f4ef59eeb510dcd0c93c7\"}', 'ECS镜像', NOW()),")
                print("('ecsImageType', '{\"imageId\":\"" + item[
                    'ver'] + "\",\"imageGbSize\":200,\"imageUuid\":\"3568e64c5a3f4ef59eeb510dcd0c93c7\"}', 'ECS镜像', NOW()),")
                print("('ecsImageType', '{\"imageId\":\"" + item[
                    'ver'] + "\",\"imageGbSize\":500,\"imageUuid\":\"3568e64c5a3f4ef59eeb510dcd0c93c7\"}', 'ECS镜像', NOW()),")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print_os()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

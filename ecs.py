# This is a sample Python script.
from decimal import Decimal, ROUND_HALF_UP

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import xlrd
import json


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


INSTANCE_TYPE = "Instance Type"
Instance_Family = "Instance Family"

Attr_enum_code = "attr_enum_code"
Family_Attr_enum_code = "family_attr_enum_code"
InstanceType = "Instance Type"
VCPU = "vCPU (Core)"
Vgpu = "GPUs"
Clock_Speed = "Clock Speed"
Physical_Processor = "Physical Processor"
GPU_Specifications = "GPU Specifications"
Bandwidth = "Internal Network Bandwidth (Gbit/s)"
MemoryNum = "Memory (GiB)"
Category = "Category"
SUB = "包年包月"
PAYG = "按量付费"

Attr_enum_code_row = 1
First_Value_row = 1
State_ENA = "ENA"
No_value1 = "-"
Blank_value = "\"\""
Comma = " ,"
SQL_INS_product_attr_enum = "INSERT INTO `product_attr_enum` (`attr_enum_code`, `enum_value`, `enum_label`, `extend_info`, `state`, `sequence`) VALUES"
SQL_INS_pricing_tariff = "INSERT INTO `pricing_tariff`(`parent_id`, `charge_item_id`, `seq_no`, `rate_var_value`, `min_val`, `max_val`, `start_value_included` ,`end_value_included`, `scaled_rate_value`, `fixed_rate_value`, `tariff_code`) VALUES"

SQL_ItemIdPBH = "@ItemIdPBH"
SQL_ItemIdSUB = "@ItemIdSUB"
SQL_NULL = "NULL"
SQL_UUID = "replace(uuid(), '-', '')"


# ecs规格枚举入库
def print_ecs_instance_product_attr_enum():
    # ecs Instance    product attr enum

    workbook = xlrd.open_workbook("C:\\Users\\wawuw\\Desktop\\workbak\\ecsType.xls")
    # 第一个sheet
    sheet1_object = workbook.sheet_by_index(0)
    # uuid
    enumCodeUUID = sheet1_object.cell_value(Attr_enum_code_row, getColByValue(sheet1_object, Attr_enum_code))
    Family_enumCodeUUID = sheet1_object.cell_value(Attr_enum_code_row,
                                                   getColByValue(sheet1_object, Family_Attr_enum_code))
    print(enumCodeUUID)
    # 获取sheet1中的有效行数
    nrows = sheet1_object.nrows
    ncols = sheet1_object.ncols

    col_InstanceType = getColByValue(sheet1_object, InstanceType)
    col_cpu = getColByValue(sheet1_object, VCPU)
    col_gpu = getColByValue(sheet1_object, Vgpu)
    col_Clock_Speed = getColByValue(sheet1_object, Clock_Speed)
    col_Physical_Processor = getColByValue(sheet1_object, Physical_Processor)
    col_GPU_Specifications = getColByValue(sheet1_object, GPU_Specifications)
    col_Bandwidth = getColByValue(sheet1_object, Bandwidth)
    col_MemoryNum = getColByValue(sheet1_object, MemoryNum)
    col_Category = getColByValue(sheet1_object, Category)
    col_Instance_Family = getColByValue(sheet1_object, Instance_Family)
    family = {}
    enum_values = []
    seq = 0
    print("----------------------ecs instance type----------------------------")

    print(SQL_INS_product_attr_enum)
    for row in range(First_Value_row, nrows):
        var_Instance_Family = sheet1_object.cell_value(row, col_Instance_Family)
        var_Instance_Family = var_Instance_Family[len("ecs."): len(var_Instance_Family)]
        seq = seq + 1
        enum_value = replaceWithBlankNo_doubleQuote(sheet1_object.cell_value(row, col_InstanceType))
        enum_label = replaceWithBlankNo_doubleQuote(sheet1_object.cell_value(row, col_InstanceType))
        ex_info_cpu = replaceWithBlank(int(sheet1_object.cell_value(row, col_cpu)))
        ex_info_memory = replaceWithBlank(int(sheet1_object.cell_value(row, col_MemoryNum)))
        ex_info_gpu = replaceWithBlank(int(sheet1_object.cell_value(row, col_gpu)))
        ex_info_Clock_Speed = replaceWithBlank(sheet1_object.cell_value(row, col_Clock_Speed))
        ex_info_Physical_Processor = replaceWithBlank(sheet1_object.cell_value(row, col_Physical_Processor))
        ex_info_GPU_Specifications = replaceWithBlank(sheet1_object.cell_value(row, col_GPU_Specifications))
        ex_info_Bandwidth = replaceWithBlank(sheet1_object.cell_value(row, col_Bandwidth))
        ex_info_Category = replaceWithBlank(sheet1_object.cell_value(row, col_Category))
        enum_values.append(enum_value)
        if var_Instance_Family in family:
            family[var_Instance_Family].append(enum_value)
        else:
            family[var_Instance_Family] = [enum_value]
        extend_info = ("{\"GPUSpecifications\":" + ex_info_GPU_Specifications
                       + ",\"GPUs\":" + ex_info_gpu
                       + ",\"internalNetworkBandwidth\":" + ex_info_Bandwidth
                       + ",\"memory\":" + ex_info_memory
                       + ",\"vCPU\":" + ex_info_cpu
                       + ",\"category\":[" + ex_info_Category + "]"
                       + "}")
        sql = ("(" + addFormat(enumCodeUUID) + Comma
               + addFormat(enum_value) + Comma
               + addFormat(enum_label) + Comma
               + addFormat(extend_info) + Comma
               + addFormat(State_ENA) + Comma
               + str(seq)
               + "),")
        print(sql)
    print("----------------------------ecs family---------------------------------")
    seq = 0
    print(SQL_INS_product_attr_enum)
    for e in family:
        seq = seq + 1
        # print(e)
        family_info = {}
        for e2 in family[e]:
            family_info[e2] = e2
        sql = ("(" + addFormat(Family_enumCodeUUID) + Comma
               + addFormat(e) + Comma
               + addFormat(e) + Comma
               + addFormat(json.dumps(family_info)) + Comma
               + addFormat(State_ENA) + Comma
               + str(seq)
               + "),")
        print(sql)

    print("--------------------------10070 instanceType pricing traffic --------------------------")
    print(SQL_INS_pricing_tariff)
    col_SUB = getColByValue(sheet1_object, SUB)
    col_PAYG = getColByValue(sheet1_object, PAYG)

    for enum_value in enum_values:
        enum_value_row = getRowByValueWithCol(sheet1_object, col_InstanceType, enum_value)
        sub_Pricing = (Decimal(sheet1_object.cell(enum_value_row, col_SUB).value)
                       .quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        payg_Pricing = (Decimal(sheet1_object.cell(enum_value_row, col_PAYG).value)
                        .quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
        sql_PBH = ("(" + SQL_ItemIdPBH + Comma
                   + SQL_ItemIdPBH + Comma
                   + SQL_NULL + Comma
                   + addFormat(enum_value) + Comma
                   + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma
                   + str(payg_Pricing) + Comma
                   + SQL_UUID
                   + "),")
        sql_SUB = ("(" + SQL_ItemIdSUB + Comma
                   + SQL_ItemIdSUB + Comma
                   + SQL_NULL + Comma
                   + addFormat(enum_value) + Comma
                   + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma + SQL_NULL + Comma
                   + str(sub_Pricing) + Comma
                   + SQL_UUID
                   + "),")
        print(sql_PBH)
        print(sql_SUB)


def getColByValue(sheet, value):
    for col in range(sheet.ncols):
        if value in sheet.col_values(col):
            return col
    return -1


# 已知行获取列
def getRowByValueWithCol(sheet, colIndex, value):
    for row in range(sheet.nrows):
        if value == sheet.cell(row, colIndex).value:
            return row
    return -1


def replaceWithBlank(value):
    if value == No_value1:
        return Blank_value
    return "\"" + str(value) + "\""


def replaceWithBlankNo_doubleQuote(value):
    if value == No_value1:
        return Blank_value
    return str(value)


def addFormat(value):
    return "\'" + str(value) + "\'"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('ecs')
    print_ecs_instance_product_attr_enum()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

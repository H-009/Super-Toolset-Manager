import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import Theme

def str_to_bool(str_bool):
    if str_bool == "True" or str_bool == "true":
        return True
    if str_bool == "False" or str_bool == "false":
        return False

def str_to_theme(mode_str: str, default: Theme = Theme.AUTO) -> Theme:
    """
    将字符串安全地转换为 qfluentwidgets 的 Theme 枚举。
    如果字符串不匹配，自动返回你指定的默认值（默认是 Theme.AUTO）。
    """
    # 核心逻辑：遍历 Theme 的所有成员，比对名字，找到了就返回对应的枚举
    return next((m for m in Theme if m.name == mode_str.upper()), default)

# 表格添加行 1列
def table_add_row_1(table,c1):
    row = table.rowCount()
    table.insertRow(row)
    table.setItem(row, 0,QTableWidgetItem(c1))

# 表格添加行 2列
def table_add_row_2(table,c1, c2,v1):
    row = table.rowCount()
    table.insertRow(row)
    item1 = QTableWidgetItem(c1)
    item1.setData(Qt.UserRole, v1)

    table.setItem(row, 0,item1)
    table.setItem(row, 1,QTableWidgetItem(c2))

# 表格添加行 4列
def table_add_row_4(table,c1, c2, c3, c4,v1):
    row = table.rowCount()
    table.insertRow(row)
    item1 = QTableWidgetItem(c1)
    item1.setData(Qt.UserRole, v1)

    table.setItem(row, 0,item1)
    table.setItem(row, 1,QTableWidgetItem(c2))
    table.setItem(row, 2,QTableWidgetItem(c3))
    table.setItem(row, 3,QTableWidgetItem(c4))

# 表格添加行 5列
def table_add_row_5(table,c1, c2, c3, c4, c5,v1):
    row = table.rowCount()
    table.insertRow(row)
    item1 = QTableWidgetItem(c1)
    item1.setData(Qt.UserRole, v1)
    table.setItem(row, 0, item1)
    table.setItem(row, 1, QTableWidgetItem(c2))
    table.setItem(row, 2, QTableWidgetItem(c3))
    table.setItem(row, 3, QTableWidgetItem(c4))
    table.setItem(row, 4, QTableWidgetItem(c5))

# 表格添加行 7列
def table_add_row_7(table,c1, c2, c3, c4, c5,c6,c7,v1):
    row = table.rowCount()
    table.insertRow(row)
    item1 = QTableWidgetItem(c1)
    item1.setData(Qt.UserRole, v1)
    table.setItem(row, 0, item1)
    table.setItem(row, 1, QTableWidgetItem(c2))
    table.setItem(row, 2, QTableWidgetItem(c3))
    table.setItem(row, 3, QTableWidgetItem(c4))
    table.setItem(row, 4, QTableWidgetItem(c5))
    table.setItem(row, 5, QTableWidgetItem(c6))
    table.setItem(row, 6, QTableWidgetItem(c7))

# 表格添加行 带图标
def table_add_row_ico(table, c1, c2, c3, icon=None):
    """
    icon: QIcon 对象，传 None 就不设行头图标
    """
    row = table.rowCount()
    table.insertRow(row)

    table.setItem(row, 0, QTableWidgetItem(c1))
    table.setItem(row, 1, QTableWidgetItem(c2))
    table.setItem(row, 2, QTableWidgetItem(c3))

    # 给新行的行头设 SVG 图标
    if icon is not None:
        item = QTableWidgetItem()
        item.setIcon(icon)
        item.setText(f" {row + 1}")   # 行号
        table.setVerticalHeaderItem(row, item)

def get_unique_name(path, name, is_file=True):
    """
    在指定路径下获取唯一的文件或文件夹名称

    :param path: str, 目标目录路径
    :param name: str, 基础名称（不含路径）
    :param is_file: bool, True为文件模式(保留扩展名), False为文件夹模式
    :return: str, 唯一的完整绝对路径
    """
    # 构建初始完整路径
    full_path = os.path.join(path, name)

    # 如果不存在，直接返回
    if not os.path.exists(full_path):
        return full_path

    # 如果存在，根据模式生成唯一名称
    base, ext = os.path.splitext(name)
    counter = 1
    max_retries = 100  # 设置上限 1000

    while counter <= max_retries:
        if is_file:
            # 文件模式: name(1).txt (序号插在名与扩展名之间)
            new_name = f"{base} ({counter}){ext}"
        else:
            # 文件夹模式: name(1) (序号直接追加)
            new_name = f"{name} ({counter})"

        new_full_path = os.path.join(path, new_name)

        if not os.path.exists(new_full_path):
            return new_full_path

        counter += 1
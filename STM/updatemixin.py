from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import datetime

import psutil
from MetaverseSDK.MetaverseAPI.Url import UrlBuilder, UrlSynthesizer
from MetaverseSDK.MetaverseAPI.UrlKey import ContributorKey, RepoKey
from MetaverseSDK.MetaverseTool.Config import JsonConfigTool
from MetaverseSDK.MetaverseTool.Config.JsonConfigPool import JCP
from MetaverseSDK.MetaverseUI.MCore.MAnimation.MWidgetAnimation import MissionBallAnimation
from MetaverseSDK.MetaverseUI.MCore.MPool.MBaseIconPool import BIP
from MetaverseSDK.MetaverseUI.MCore.MPool.MBasePixmapPool import BPP
from MetaverseSDK.MetaverseUI.MCore.MPool.MBaseSoundPool import BSP
from MetaverseSDK.MetaverseUI.MCore.MPool.MSvgIconPool import SIP
from MetaverseSDK.MetaverseUI.MCore.MThread.MNetWorker import GetPythonVersions, GetPythonFile, GetGitHubReleaseThread
from MetaverseSDK.MetaverseUI.MFluentWidgets.MIndeterminateProgressBarDialog import IndeterminateProgressBarDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QTreeWidgetItem, QListWidgetItem, QFileDialog
from packaging.version import Version
from qfluentwidgets import InfoBarPosition, InfoBar, FluentIcon, Dialog, BodyLabel, SimpleCardWidget, EditableComboBox, \
    StateToolTip

from typing import TYPE_CHECKING

import tool
from Dialog import DetailsConfigDialog, DetailsPresetScriptsDialog, DetailsPinDialog, DetailsPythonDialog, \
    DetailsEmbDialog, DetailsVenvDialog

from MetaverseSDK.MetaverseUI.MFluentWidgets.MDialog import DangerCountdownDialog, TextEditDialog, ReleaseDialog, \
    NotificationDialog

if TYPE_CHECKING:
    from STM import MainUI
    _MixinBase = MainUI   # 类型检查时 MainUI
else:
    _MixinBase = object   # 运行时 object

class UpdateMixin(_MixinBase):
    # 更新设置启动动画时长
    def update_set_startup_animation_duration_ico(self):
        # 慢
        if self.startup_animation_duration in self.startup_animation_off:
            self.startup_animation_duration_card.setIcon(FluentIcon.SPEED_OFF)
        # 中
        elif self.startup_animation_duration in self.startup_animation_medium:
            self.startup_animation_duration_card.setIcon(FluentIcon.SPEED_MEDIUM)
        # 快
        elif self.startup_animation_duration in self.startup_animation_high:
            self.startup_animation_duration_card.setIcon(FluentIcon.SPEED_HIGH)

    # 更新设置启动图标大小
    def update_set_startup_ico_size_ico(self):
        # 小
        if self.startup_ico_size == "小-80px":
            self.sstartup_ico_size_card.setIcon(FluentIcon.SPEED_OFF)
        # 中
        elif self.startup_ico_size == "中-120px":
            self.sstartup_ico_size_card.setIcon(FluentIcon.SPEED_MEDIUM)
        # 快
        elif self.startup_ico_size == "大-240px":
            self.sstartup_ico_size_card.setIcon(FluentIcon.SPEED_HIGH)

    # 更新启动动画时长
    def update_startup_animation_duration(self, index):
        duration = self.startup_animation_off[0]  # 默认
        # 快
        if index == 0:
            duration = self.startup_animation_high[0]
        elif index == 1:
            duration = self.startup_animation_high[1]
        elif index == 2:
            duration = self.startup_animation_high[2]
        elif index == 3:
            duration = self.startup_animation_high[3]
        # 中
        elif index == 4:
            duration = self.startup_animation_medium[0]
        elif index == 5:
            duration = self.startup_animation_medium[1]
        elif index == 6:
            duration = self.startup_animation_medium[2]
        # 慢
        elif index == 7:
            duration = self.startup_animation_off[0]
        elif index == 8:
            duration = self.startup_animation_off[1]
        elif index == 9:
            duration = self.startup_animation_off[2]
        elif index == 10:
            duration = self.startup_animation_off[3]

        self.startup_animation_duration = duration
        JCP.update("config.json",["setting","startup_animation_duration"], duration)
        InfoBar.info(
            title="通知",
            content=f"启动页面动画时长切为 {duration}",
            parent=self,
            position=InfoBarPosition.TOP
        )

        # 更新图标
        self.update_set_startup_animation_duration_ico()

    # 更新启动图标大小
    def update_startup_ico_size(self, index):
        duration = self.startup_ico_list[0]  # 默认
        # 快
        if index == 0:
            duration = self.startup_ico_list[0]
        elif index == 1:
            duration = self.startup_ico_list[1]
        elif index == 2:
            duration = self.startup_ico_list[2]

        self.startup_ico_size = duration
        JCP.update("config.json", ["setting","startup_ico_size"], duration)
        InfoBar.info(
            title="通知",
            content=f"启动页面图标大小切为 {duration}",
            parent=self,
            position=InfoBarPosition.TOP
        )

        # 更新图标
        self.update_set_startup_ico_size_ico()

    # 更新关闭启动延迟
    def update_close_startup_delay(self):
        # 设置启动页面时长
        self.startup_animation_duration_card.setCurrentIndex(0)
        # 手动触发槽函数
        self.update_startup_animation_duration(0)

        # 设置窗口过渡时长
        self.transition_duration_card.setCurrentIndex(0)
        # 手动触发槽函数
        self.update_transition_duration(0)

        # 设置启动页面过渡时长
        self.startup_animation_transition_duration_card.setCurrentIndex(0)
        # 手动触发槽函数
        self.update_startup_animation_transition_duration(0)

    # 更新启动图标阴影
    def update_shadow(self,key):
        JCP.update("config.json", ["setting","startup_ico_shadow"], key)

        if key:
            InfoBar.info(
                title="已开启",
                content="启动页面图标阴影已开启 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
        else:
            InfoBar.info(
                title="已关闭",
                content="启动页面图标阴影已关闭 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )

    # 启用DPI缩放
    def update_dpi_zoom(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="DPI感知已开启 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","DPI_zoom"], True)
        else:
            InfoBar.info(
                title="已关闭",
                content="DPI感知已关闭 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","DPI_zoom"], False)

    # 启用非整数缩放
    def update_dpi_non_int_zoom(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="非整数缩放已开启 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","DPI_non_int_zoom"], True)
        else:
            InfoBar.info(
                title="已关闭",
                content="非整数缩放已关闭 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","DPI_non_int_zoom"], False)

    # 启用高DPI像素映射
    def update_high_DPI_pixel_mapping(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="高DPI像素映射已开启 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","high_DPI_pixel_mapping"], True)
        else:
            InfoBar.info(
                title="已关闭",
                content="高DPI像素映射已关闭 重启应用生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","high_DPI_pixel_mapping"], False)

    # 启动时全屏
    def full_screen_startup(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="启动时全屏已开启 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","full_screen_startup"], True)

            # 临时阻塞信号
            self.full_screen_after_startup_switch.blockSignals(True)
            self.maximize_after_startup_switch.blockSignals(True)
            # 互斥
            self.full_screen_after_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","full_screen_after_startup"], False)
            self.maximize_after_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","maximize_after_startup"], False)
            # 释放阻塞
            self.full_screen_after_startup_switch.blockSignals(False)
            self.maximize_after_startup_switch.blockSignals(False)
        else:
            InfoBar.info(
                title="已关闭",
                content="启动时全屏已关闭 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","full_screen_startup"], False)

    # 启动后全屏
    def full_screen_after_startup(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="启动后全屏已开启 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","full_screen_after_startup"], True)

            # 临时阻塞信号
            self.full_screen_startup_switch.blockSignals(True)
            self.maximize_after_startup_switch.blockSignals(True)
            # 互斥
            self.full_screen_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","full_screen_startup"], False)
            self.maximize_after_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","maximize_after_startup"], False)
            # 释放阻塞
            self.full_screen_startup_switch.blockSignals(False)
            self.maximize_after_startup_switch.blockSignals(False)
        else:
            InfoBar.info(
                title="已关闭",
                content="启动后全屏已关闭 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","full_screen_after_startup"], False)

    # 启动后最大化
    def maximize_after_startup(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="启动后最大化已开启 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","maximize_after_startup"], True)

            # 临时阻塞信号
            self.full_screen_after_startup_switch.blockSignals(True)
            self.full_screen_startup_switch.blockSignals(True)
            # 互斥
            self.full_screen_after_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","full_screen_after_startup"], False)
            self.full_screen_startup_switch.setChecked(False)
            JCP.update("config.json", ["setting","full_screen_startup"], False)
            # 释放阻塞
            self.full_screen_after_startup_switch.blockSignals(False)
            self.full_screen_startup_switch.blockSignals(False)
        else:
            InfoBar.info(
                title="已关闭",
                content="启动后最大化已关闭 下次启动时生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","maximize_after_startup"], False)

    # 更新云母效果
    def update_mica_effect(self,key):
        self.setMicaEffectEnabled(key)
        JCP.update("config.json", ["setting","mica_effect"], key)
        self.mica_effect = key

    # 更新懒加载
    def update_lazy(self,key):
        JCP.update("config.json", ["setting","lazy"], key)
        self.lazy = key

    # 更新音效
    def update_play_sound(self, key):
        self.play_sound = key
        JCP.update("config.json", ["setting","play_sound"], key)

    # 更新警告音效
    def update_play_sound_warning(self, key):
        self.play_sound_warning = key
        JCP.update("config.json", ["setting","play_sound_warning"], key)

    # 更新操作完成音效
    def update_play_sound_operation_completed(self, key):
        self.play_sound_operation_completed = key
        JCP.update("config.json", ["setting","play_sound_operation_completed"], key)

    # 更新下载完成音效
    def update_play_sound_download_complete(self, key):
        self.play_sound_download_complete = key
        JCP.update("config.json", ["setting","play_sound_download_complete"], key)

    # 更新提示音效
    def update_play_sound_important_tip(self, key):
        self.play_sound_important_tip = key
        JCP.update("config.json", ["setting","play_sound_important_tip"], key)

    # 更新动画实现的平滑滚动区域
    def update_smooth_scrolling_area(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="将由平滑滚动区域代替滚动区域 重启生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","smooth_scrolling_area"], True)

        else:
            InfoBar.info(
                title="已关闭",
                content="将由滚动区域代替平滑滚动区域 重启生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            JCP.update("config.json", ["setting","smooth_scrolling_area"], False)

    # 更新上下翻页堆叠部件
    def update_page_up_down_stacked_widget(self, key):
        # 开启
        if key:
            InfoBar.info(
                title="已开启",
                content="将由上下翻页堆叠部件代替上下弹出堆叠部件 重启生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )

        else:
            InfoBar.info(
                title="已关闭",
                content="将由上下弹出堆叠部件代替上下翻页堆叠部件 重启生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
        JCP.update("config.json", ["setting","page_up_down_stacked_widget"], key)

    # 更新基础环境
    def update_python(self):
        self.python_table.setRowCount(0)

        # 更新表格
        python_json = JCP.get("config.json",["python"])
        for value,key in python_json.items():
            tool.table_add_row_4(self.python_table, key["name"], key["version"], key["dir"], key["path"],value)

        # 更新环境树
        self.update_venv_tree()

    # 更新便携式环境
    def update_emb(self):
        self.emb_table.setRowCount(0)

        # 更新表格
        emb_json = JCP.get("config.json",["emb"])
        for value,key in emb_json.items():
            tool.table_add_row_5(self.emb_table, key["name"], key["version"],key["dir"],key["start_script"],str(key["pth"]),value)

        # 更新环境树
        self.update_venv_tree()

    # 更新虚拟环境
    def update_venv(self):
        self.venv_table.setRowCount(0)

        # 更新表格
        venv_json = JCP.get("config.json",["venv"])
        for value,key in venv_json.items():
            tool.table_add_row_7(self.venv_table, key["name"], key["version"],key["dir"],key["cfg_file"],
                                 key['start_parameter'],key['python'],str(key["include-system-site-packages"]),value)

        # 更新环境树
        self.update_venv_tree()

    # 更新图钉
    def update_pin(self):
        self.pin_table.setRowCount(0)

        # 更新表格
        pin_json = JCP.get("config.json",["pin"],[]) # 默认列表
        for key in pin_json:
            tool.table_add_row_1(self.pin_table, key)

        self.update_thumbtack_list() #更新图钉列表

    # 更新预设脚本
    def update_preset_scripts(self):
        self.preset_scripts_table.setRowCount(0)

        preset_scripts_json = JCP.get("config.json",["preset_scripts"],{}) # 默认空集合
        for value,key in preset_scripts_json.items():
            tool.table_add_row_4(self.preset_scripts_table, key["name"], key["description"],key["older"],str(key["parameters_dict"]),value)

    # 更新配置文件
    def update_config(self):
        self.config_table.setRowCount(0)

        config_json = JCP.get("config.json",["config"],{}) # 默认空集合
        for value,key in config_json.items():
            tool.table_add_row_2(self.config_table, key["name"], str(key["older_list"]),value)

    # 更新配置基础环境下拉列表
    def update_config_python_combox(self,box):
        box.clear()

        for row in range(self.python_table.rowCount()):
            item_col0 = self.python_table.item(row, 0)  # 第1列
            item_col3 = self.python_table.item(row, 3)  # 第4列

            if item_col3 is not None and item_col0 is not None:
                box.addItem(f"{item_col0.text()}    {item_col3.text()}", SIP.get("Python"),userData=item_col3.text())

        box.setCurrentIndex(-1) # 取消选中

        # 更新命令
        self.update_config_venv_command()

    # 更新配置文件下拉列表
    def update_config_combox(self,box):
        box.clear()

        for row in range(self.config_table.rowCount()):
            item_col0 = self.config_table.item(row, 0)  # 第1列

            if item_col0 is not None:
                # 存储的父级
                box.addItem(item_col0.text(), FluentIcon.DOCUMENT,userData=item_col0.data(Qt.UserRole))

        box.setCurrentIndex(-1) # 取消选中

    # 更新配置启动参数
    def update_config_start_parameter(self, text):
        # 不为空
        if text != "":
            if text.endswith("/") or text.endswith("\\"):  # 以/\结尾
                self.config_startup_parameters_line.setText(text + "Scripts/activate")
            else:
                self.config_startup_parameters_line.setText(text + "/Scripts/activate")

        # 否则重置
        else:
            self.config_startup_parameters_line.setText("")

        # 最后刷新 防止停滞
        # 刷新命令
        self.update_config_venv_command()

    # 刷新配置虚拟环境命令
    def update_config_venv_command(self):
        # 选中基础解释器
        if self.config_base_python_box.text() != "":
            # 基础命令
            if not self.config_custom_prompts_prefix_box.isChecked():
                base = f'"{self.config_base_python_box.text()}" -m venv "{self.config_venv_Loca_line.text()}"'
            else:
                base = f'"{self.config_base_python_box.text()}" -m venv "{self.config_venv_Loca_line.text()}" --prompt "{self.config_prompts_prefix_line.text()}"' # 提示符命令
            # 将列表元素用空格连接
            params_str = ' '.join(self.config_python_batch_list)
            full_cmd = f"{base} {params_str}" if params_str else base

            self.config_created_parameter_line.setText(full_cmd)
        # 否则清空
        else:
            self.config_created_parameter_line.setText("")

    # 基础环境详情
    def details_python(self):
        # 获取当前所在行第0列item
        item = self.python_table.item(self.python_table.currentRow(), 0)
        # 获取json
        json_data = JCP.get("config.json",["python",item.data(Qt.UserRole)])

        dialog = DetailsPythonDialog("详情",SIP.get("Python"),
                                     "Python 基础环境",
                                     f"环境名称 {json_data['name']}",
                                     f"解释器版本 {json_data['version']}",
                                     f"环境路径 {json_data['dir']}",
                                     f"解释器路径 {json_data['path']}",self)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 便携式环境详情
    def details_emb(self):
        # 获取当前所在行第0列item
        item = self.emb_table.item(self.emb_table.currentRow(), 0)
        # 获取json
        json_data = JCP.get("config.json",["emb",item.data(Qt.UserRole)])

        dialog = DetailsEmbDialog("详情",self.ZIP_FOLDER_icon,
                                                           "Python Emb便携式环境",
                                                           f"环境名称 {json_data['name']}",
                                                           f"解释器版本 {json_data['version']}",
                                                           f"环境路径 {json_data['dir']}",
                                                           f"启动脚本路径 {json_data['start_script']}",
                                                           f"第三方库解锁 {json_data['pth']}",self)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 虚拟环境详情
    def details_venv(self):
        # 获取当前所在行第0列item
        item = self.venv_table.item(self.venv_table.currentRow(), 0)
        # 获取json
        json_data = JCP.get("config.json",["venv",item.data(Qt.UserRole)])

        dialog = DetailsVenvDialog("详情",self.IOT_icon,
                                                         "Python Venv虚拟环境",
                                                         f"环境名称 {json_data['name']}",
                                                         f"解释器版本 {json_data['version']}",
                                                         f"环境路径 {json_data['dir']}",
                                                         f"配置路径 {json_data['cfg_file']}",
                                                         f"启动参数 {json_data['start_parameter']}",
                                                         f"基础环境路径 {json_data['python']}",
                                                         f"继承全局包 {json_data['include-system-site-packages']}",self)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 图钉详情
    def details_pin(self):
        # 获取json
        json_data = JCP.get("config.json",["pin"])[self.pin_table.currentRow()]

        dialog = DetailsPinDialog("详情",FluentIcon.PIN,
                                 "VEM 图钉",
                                 f"图钉命令 {json_data}",self)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 预设脚本详情
    def details_preset_scripts(self):
        # 获取当前所在行第0列item
        item = self.preset_scripts_table.item(self.preset_scripts_table.currentRow(), 0)
        # 获取json
        json_data = JCP.get("config.json",["preset_scripts",item.data(Qt.UserRole)])

        dialog = DetailsPresetScriptsDialog("详情",FluentIcon.QUICK_NOTE,
                                                         "VEM 预设脚本",
                                                         f"预设名称 {json_data['name']}",
                                                         f"预设描述 {json_data['description']}",
                                                         f"原始命令 {json_data['older']}","参数字典",self)
        for t in json_data['parameters_dict']:
            dialog.textedit.append(f"{t} : {json_data['parameters_dict'][t]}")
        # 移动光标到文档最开头
        cursor = dialog.textedit.textCursor()
        cursor.setPosition(0)
        dialog.textedit.setTextCursor(cursor)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 配置文件详情
    def details_config(self):
        # 获取当前所在行第0列item
        item = self.config_table.item(self.config_table.currentRow(), 0)
        # 获取json
        json_data = JCP.get("config.json",["config",item.data(Qt.UserRole)])

        dialog = DetailsConfigDialog("详情",FluentIcon.DOCUMENT,
                                                         "VEM 配置文件",
                                                         f"配置名称 {json_data['name']}",
                                                         f"命令列表",self)
        for t in json_data['older_list']:
            dialog.textedit.append(t)
        # 移动光标到文档最开头
        cursor = dialog.textedit.textCursor()
        cursor.setPosition(0)
        dialog.textedit.setTextCursor(cursor)
        if dialog.exec():
            # 销毁
            dialog.accept()
            dialog.deleteLater()

    # 更新窗口过渡时长
    def update_transition_duration(self,index):
        if index == 0:
            self.transition_duration = "0ms"
        elif index == 1:
            self.transition_duration = "10ms"
        elif index == 2:
            self.transition_duration = "20ms"
        elif index == 3:
            self.transition_duration = "30ms"
        JCP.update("config.json", ["setting","transition_duration"],self.transition_duration)
        InfoBar.info(
            title="通知",
            content=f"过渡时长换为 {self.transition_duration} 重启生效",
            parent=self,
            position=InfoBarPosition.TOP
        )

    # 更新窗口过渡时长
    def update_startup_animation_transition_duration(self,index):
        if index == 0:
            self.startup_animation_transition_duration = "0ms"
        elif index == 1:
            self.startup_animation_transition_duration = "10ms"
        elif index == 2:
            self.startup_animation_transition_duration = "20ms"
        elif index == 3:
            self.startup_animation_transition_duration = "30ms"
        JCP.update("config.json", ["setting","startup_animation_transition_duration"],self.startup_animation_transition_duration)
        InfoBar.info(
            title="通知",
            content=f"过渡时长换为 {self.startup_animation_transition_duration} 重启生效",
            parent=self,
            position=InfoBarPosition.TOP
        )

    # 更新禁止创建原生控件同级窗口
    def update_prohibit_creating_native_control_windows_same_level(self, key):
        # 关闭状态下
        if not key:
            # 危险倒计时消息框
            w = DangerCountdownDialog(
                title='您正在进行危险操作⚠️',
                content="""您当前的操作正在允许创建原生控件同级窗口!!\n允许创建原生控件后\n打开模态对话框和模态遮罩对话框会出现焦点残留
                            导致焦点丢失 并且导致窗口无法拉伸 必须关闭软件解决 并且会有数据丢失的风险
                            \n如果您是误触 请点击右下角取消按钮 继续禁用创建 \n 如果仍需继续允许 请等待左下角继续按钮倒计时结束后再点击""",
                parent=self,
                countdown_seconds=25,
                text="继续"
            )
            # 确认
            if w.exec():
                InfoBar.warning(
                    title="已关闭",
                    content="已允许创建原生控件同级窗口 重启生效",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=1500
                )
                # 关闭
                JCP.update("config.json", ["setting","prohibit_creating_native_control_windows_same_level"], False)
            # 取消
            else:
                # 临时阻塞信号
                self.prohibit_creating_native_control_windows_same_level_card.blockSignals(True)  # 开始阻塞
                self.prohibit_creating_native_control_windows_same_level_card.setChecked(True)
                self.prohibit_creating_native_control_windows_same_level_card.blockSignals(False)  # 恢复信号

        else:
            InfoBar.info(
                title="已开启",
                content="已禁止创建原生控件同级窗口 重启生效",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=1500
            )
            # 开启
            JCP.update("config.json", ["setting","prohibit_creating_native_control_windows_same_level"], True)

    # 更新启动时检查更新
    def update_startup_check_update(self,key):
        self.startup_check_update = key
        JCP.update("config.json", ["setting","startup_check_update"], key)

    # 强制退出
    def force_quit(self):
        w = DangerCountdownDialog(
            title='强制退出⚠️',
            content="""是否放弃保存本次配置并强制退出VEM""",
            parent=self,
            countdown_seconds=3,
            text="退出"
        )
        # 确认
        if w.exec():
            sys.exit()

    # 删除配置
    def delete_config_file(self):
        # 配置文件保护
        if not self.config_file_protect:
            w = DangerCountdownDialog(
                title='删除配置⚠️',
                content="""是否删除当前配置文件并清空配置池\n此操作不可撤销! 会丢失全部配置数据!!!\n是否继续?""",
                parent=self,
                countdown_seconds=10,
                text="删除"
            )
            # 确认
            if w.exec():

                if os.path.exists("config.json"):
                    data = JCP.read("config.json")
                    w2 = DangerCountdownDialog(
                        title='数据安全警告⚠️',
                        content=f"""是否继续删除配置文件并清空配置池 会丢失全部配置数据!\n当前配置中包含:\n
                        {len(data["setting"])} 项设置
                        {len(data["python"])} 个基础环境
                        {len(data["venv"])} 个虚拟环境
                        {len(data["emb"])} 个便携式环境
                        {len(data["pin"])} 个图钉
                        {len(data["preset_scripts"])} 个预设脚本
                        {len(data["config"])} 个配置文件""",
                        parent=self,
                        countdown_seconds=15,
                        text="继续删除"
                    )

                    if w2.exec():
                        try:
                            os.remove("config.json")
                            JCP.clear()
                        except Exception as a:
                            InfoBar.error(title="错误",
                                          content=str(a),
                                          parent=self,
                                          position=InfoBarPosition.TOP,
                                          duration=2000
                                          )

                        dialog = NotificationDialog("通知","配置文件与配置池删除完成\nVEM需要强制退出程序完成新配置更新",self)
                        dialog.exec()

                        sys.exit()

                else:
                    InfoBar.warning(title="警告",
                                  content="配置不存在",
                                  parent=self,
                                  position=InfoBarPosition.TOP
                                  )

        else:
            w = NotificationDialog("操作被阻止❌","为了保护配置文件 当前删除操作被配置文件保护阻止\n如果需要删除配置文件\n\n前往👉设置-配置-配置文件保护",self)
            w.exec()

    # 获取新版本
    def get_new_version(self):
        # 防止多次获取
        if self.github_release_thread is None:
            # 状态工具提示
            self.new_version_state_tooltip = StateToolTip("正在检查更新", "正在获取最新版本,请耐心等待...", self)
            self.new_version_state_tooltip.adjustSize()

            x = self.width() - self.new_version_state_tooltip.width() - 20

            self.new_version_state_tooltip.move(x, 55)
            self.new_version_state_tooltip.show()

            # 获取更新线程
            self.github_release_thread = GetGitHubReleaseThread(UrlBuilder.GithubRepoLatestRelease(ContributorKey.H009,RepoKey.VEM))
            self.github_release_thread.release_fetched.connect(self.get_new_version_success)
            self.github_release_thread.error_occurred.connect(self.get_new_version_error)
            self.github_release_thread.start()

    # 获取最新版本错误
    def get_new_version_error(self,error):
        try:
            InfoBar.error(title="错误",
                          content=error,
                          parent=self,
                          position=InfoBarPosition.BOTTOM_RIGHT,
                          duration=3000
                          )
            # 销毁状态提示
            self.new_version_state_tooltip.setTitle("获取失败")
            self.new_version_state_tooltip.setContent("未找到任何版本")
            self.new_version_state_tooltip.setState(True)
            # 销毁线程
            self.github_release_thread.deleteLater()
            # 清空引用
            self.github_release_thread = None
        except Exception as a:
            print(a)

    # 获取最新版本成功
    def get_new_version_success(self,release):
        try:
            self.new_version_state_tooltip.setTitle("获取成功")
            self.new_version_state_tooltip.setState(True)

            # 播放音效 操作完成音效未禁用
            if self.play_sound and not self.play_sound_operation_completed:
                BSP.play("OperationCompleted")

            # 找到新版本
            if Version(self.VEM_Version) < Version(release["version"]):
                self.new_version_state_tooltip.setContent("找到新版本")

                dialog = ReleaseDialog(release,self)
                dialog.exec()

            # 当前为新版本
            else:
                self.new_version_state_tooltip.setContent("当前为新版本")

            # 销毁线程
            self.github_release_thread.deleteLater()
            # 清空引用
            self.github_release_thread = None
        except Exception as a:
            print(a)

    # 更新跳过退出保存
    def update_skip_exit_save(self,key):
        self.skip_exit_save = key
        JCP.update("config.json", ["setting","skip_exit_save"], key)

    # 更新配置文件保护
    def update_config_file_protect(self,key):
        self.config_file_protect = key
        JCP.update("config.json", ["setting","config_file_protect"], key)

    # 更新演示模式
    def update_demo_mode(self,key):
        if key:
            dialog = Dialog("是否立即将池保存到配置?", "请注意 当前改动并未保存\n\n演示模式仅在当前生效一次 如需持久化生效需立即将池落盘"
                                                       "\n是否将池落盘 否则演示模式仅生效一次", self)
            if dialog.exec():
                # 立即保存
                JCP.update("config.json", ["setting", "demo_mode"], key)
                # 落盘
                self.write_disk_pool()

            self.demo_mode = key
        else:
            self.demo_mode = key
            JCP.update("config.json", ["setting", "demo_mode"], key)

    # 更新备份路径
    def update_backup_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "选择 备份位置",
            "C:/"
        )

        if path != '':
            InfoBar.success(title="成功",
                            content=f"备份位置已更新为 {path}",
                            parent=self,
                            position=InfoBarPosition.TOP,
                            duration=1500
                            )
            self.backup_path = path
            self.backup_path_card.setContentText(path) # 更新字幕标签
            JCP.update("config.json",["setting","backup_path"],path)

    # 恢复默认备份路径
    def restore_default_backup_path(self):
        path = os.getcwd()+"\\Backup"
        self.backup_path = path
        self.backup_path_card.setContentText(path)  # 更新字幕标签
        JCP.update("config.json", ["setting", "backup_path"],path) # 更新配置

    # 更新完整备份
    def update_full_backup(self,key):
        self.full_backup = key
        JCP.update("config.json", ["setting","full_backup"], key)

    # 备份配置文件
    def backup_config_file(self):
        try:
            # 获取格式化时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "-" + datetime.now().strftime("%f")[:3]
            file_name = f"config_backup_{timestamp}.json.bak"
            file_path = self.backup_path+"\\"+file_name

            # 目录不存在则创建目录
            os.makedirs(self.backup_path, exist_ok=True)

            # 完整备份
            if not self.full_backup:
                # 复制
                shutil.copy("config.json",file_path)
            else:
                # 完整复制
                shutil.copy2("config.json",file_path)

            InfoBar.success(title="成功",
                            content=f"备份保存到 {file_path}",
                            parent=self,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=1500
                            )
        except Exception as a:
            InfoBar.error(title="错误",
                          content=str(a),
                          parent=self,
                          position=InfoBarPosition.BOTTOM_RIGHT,
                          duration=3000
                          )

    # 恢复备份
    def restore_backup(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 VEM 备份",
            self.backup_path,
            "VEM Backup (*.json.bak);;"
            "All Files (*.*)"
        )
        if path != '':
            dialog = Dialog("恢复备份","是否立即将当前配置恢复到备份",self)
            if dialog.exec():

                try:
                    old = JsonConfigTool.read_json(path)
                    JsonConfigTool.write_json(self.config_file,old)

                    InfoBar.success(title="成功",
                                    content=f"备份恢复成功",
                                    parent=self,
                                    position=InfoBarPosition.TOP,
                                    duration=1500
                                    )

                    if self.auto_reload:
                        self.overload_disk_pool()

                    if self.auto_exit:
                        sys.exit()
                except Exception as a:
                    InfoBar.error(title="错误",
                                    content=str(a),
                                    parent=self,
                                    position=InfoBarPosition.TOP,
                                    duration=1500
                                    )

    # 更新自动重载
    def update_auto_reload(self,key):
        self.auto_reload = key
        JCP.update("config.json", ["setting","auto_reload"], key)

    # 更新自动退出
    def update_auto_exit(self,key):
        self.auto_exit = key
        JCP.update("config.json", ["setting","auto_exit"], key)

    # 同步本地
    def sync_loca(self):

        if os.path.exists("config.json"):
            old = JsonConfigTool.read_json("config.json")

            JsonConfigTool.write_json(os.path.join(self.APPDATA_ROAMING,"config.json"),old) # 拼接路径

            InfoBar.success(title="成功",
                            content=f"配置同步成功",
                            parent=self,
                            position=InfoBarPosition.TOP,
                            duration=1500
                            )
        else:
            InfoBar.error(title="错误",
                          content="配置不可用",
                          parent=self,
                          position=InfoBarPosition.TOP,
                          duration=2000
                          )

    # 同步配置
    def sync_config(self):

        if os.path.exists(os.path.join(self.APPDATA_ROAMING,"config.json")):
            old = JsonConfigTool.read_json(os.path.join(self.APPDATA_ROAMING,"config.json")) # 拼接路径

            JsonConfigTool.write_json("config.json",old)

            InfoBar.success(title="成功",
                            content=f"配置同步成功",
                            parent=self,
                            position=InfoBarPosition.TOP,
                            duration=1500
                            )

            # 备份同步
            if self.auto_backup_sync:
                # 自动备份
                try:
                    # 获取格式化时间戳
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "-" + datetime.now().strftime("%f")[:3]
                    file_name = f"config_sync_{timestamp}.json.bak"
                    file_path = self.backup_path+"\\"+file_name

                    # 目录不存在则创建目录
                    os.makedirs(self.backup_path, exist_ok=True)
                    # 复制
                    shutil.copy("config.json",file_path)

                    InfoBar.success(title="成功",
                                    content=f"备份保存到 {file_path}",
                                    parent=self,
                                    position=InfoBarPosition.BOTTOM_RIGHT,
                                    duration=1500
                                    )
                except Exception as a:
                    InfoBar.error(title="错误",
                                  content=str(a),
                                  parent=self,
                                  position=InfoBarPosition.BOTTOM_RIGHT,
                                  duration=3000
                                  )

            # 同步重载
            if self.sync_reload:
                self.overload_disk_pool()
        else:
            InfoBar.error(title="错误",
                          content="没有可用配置",
                          parent=self,
                          position=InfoBarPosition.TOP,
                          duration=2000
                          )

    # 更新自动备份同步
    def update_auto_backup_sync(self,key):
        self.auto_backup_sync = key
        JCP.update("config.json", ["setting","auto_backup_sync"], key)

    # 更新同步重载
    def update_sync_reload(self,key):
        self.sync_reload = key
        JCP.update("config.json", ["setting","sync_reload"], key)

    # 落盘池
    def write_disk_pool(self):
        JCP.save()
        InfoBar.success(title="成功",
                        content=f"配置落盘成功",
                        parent=self,
                        position=InfoBarPosition.TOP,
                        duration=1500
                        )

    # 重载池
    def overload_disk_pool(self):
        JCP.clear() # 清空池
        JCP.load(self.config_file) # 重载
        InfoBar.success(title="成功",
                        content=f"配置重载成功",
                        parent=self,
                        position=InfoBarPosition.TOP,
                        duration=1500
                        )

    # 排序池
    def update_sort_jcp_pool(self,key):
        self.sort_jcp_pool = key
        JCP.update("config.json", ["setting","sort_jcp_pool"], key)

    # 打开配置池
    def open_jcp_pool(self):
        w = TextEditDialog(
            title='配置池',
            content="查看在内存中的配置池",
            parent=self
        )

        # 排序池
        if not self.sort_jcp_pool:
            w.line.setText(str(JCP.all()))
        else:
            w.line.setText(str(JCP.sort()))

        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()

    # 打开CMD池
    def open_cmd_pool(self):
        w = TextEditDialog(
            title='CMD池',
            content="查看在内存中的CMD池",
            parent=self
        )

        w.line.setText(str(self.cmd_obj_dict)+"\n"+str(self.console_obj_dict))
        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()

    # 打开图标池
    def open_bip_pool(self):
        w = TextEditDialog(
            title='图标池',
            content="查看在内存中的图标池",
            parent=self
        )

        w.line.setText(str(BIP.older()))
        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()

    # 打开图像池
    def open_bpp_pool(self):
        w = TextEditDialog(
            title='图像池',
            content="查看在内存中的图像池",
            parent=self
        )

        w.line.setText(str(BPP.older()))
        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()

    # 打开矢量图池
    def open_sip_pool(self):
        w = TextEditDialog(
            title='矢量图池',
            content="查看在内存中的矢量图池",
            parent=self
        )

        w.line.setText(str(SIP.older()))
        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()

    # 打开音效池
    def open_bsp_pool(self):
        w = TextEditDialog(
            title='音效池',
            content="查看在内存中的音效池",
            parent=self
        )

        w.line.setText(str(BSP.older()))
        w.line.setReadOnly(True)
        w.cancelButton.hide()
        w.line.setFixedSize(800,500)

        w.exec()


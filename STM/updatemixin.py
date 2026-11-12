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

    # 更新基础环境
    def update_python(self):
        self.python_table.setRowCount(0)

        # 更新表格
        python_json = JCP.get("config.json",["python"])
        for value,key in python_json.items():
            tool.table_add_row_4(self.python_table, key["name"], key["version"], key["dir"], key["path"],value)

        # 更新环境树
        self.update_venv_tree()

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


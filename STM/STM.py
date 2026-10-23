import ctypes
import os
import subprocess
import sys
from pathlib import Path

import darkdetect
from MetaverseSDK.MetaverseTool.Config import JsonConfigTool
from MetaverseSDK.MetaverseUI.MCore.MPool.MBaseIconPool import BIP
from MetaverseSDK.MetaverseUI.MCore.MPool.MBasePixmapPool import BPP
from MetaverseSDK.MetaverseUI.MCore.MPool.MSvgIconPool import SIP
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog
from PyQt5.QtCore import Qt, QLocale, QTimer, QSize, QEventLoop
from pathvalidate import is_valid_filepath
from qfluentwidgets import FluentWindow, setTheme, FluentIcon, NavigationItemPosition, setThemeColor, SimpleCardWidget,\
    InfoBar, InfoBarPosition, Dialog,FluentTranslator,SplashScreen

from MetaverseSDK.MetaverseTool.Config.JsonConfigPool import JCP

from MetaverseSDK.MetaverseResource import MetaverseSVG, MetaverseOGG, MetaverseICO, MetaversePNG

import tool

from uimixin import UiMixin
from updatemixin import UpdateMixin

class MainUI(UiMixin,UpdateMixin,FluentWindow):
    def __init__(self):
        super().__init__()
        # 启动动画-快列表
        self.startup_animation_high = ["不显示-0ms","非常快-10ms","快-100ms","稍快-500ms"]
        # 启动动画-中列表
        self.startup_animation_medium = ["中-700ms","常规-1000ms","一般-1500ms"]
        # 启动动画-慢列表
        self.startup_animation_off = ["稍慢-2000ms","慢-2500ms","非常慢-5000ms","久-10000ms"]
        # 启动图标列表
        self.startup_ico_list = ["小-80px","中-120px","大-240px"]
        # 主题映射表
        self.theme_map = {"明亮": "LIGHT", "黑暗": "DARK", "自动": "AUTO"}
        # 反转主题映射表
        self.twist_theme_map = {"LIGHT": "明亮", "DARK": "黑暗", "AUTO": "自动"}

        # 版本
        self.STM_Version = "v1.10.1"
        self.CMD_Version = "v0.1.5"

        # 配置文件
        self.config_file = "config.json"
        # 本地文件夹
        self.APPDATA_ROAMING = os.getenv('APPDATA')+"\\STD Studio\\Super Toolset Manager"

        # 预制图标
        # 绿色开始
        self.PLAY_SOLID_icon = FluentIcon.PLAY_SOLID.icon(color=QColor("#00ff00"))
        # 绿色发送
        self.SEND_FILL_icon = FluentIcon.SEND_FILL.icon(color=QColor("#00ff00"))
        # 红色电源
        self.POWER_BUTTON_icon = FluentIcon.POWER_BUTTON.icon(color=QColor("#ff0000"))
        # 红色扫把
        self.BROOM_icon = FluentIcon.BROOM.icon(color=QColor("#ff0000"))
        # 橙色压缩包
        self.ZIP_FOLDER_icon = FluentIcon.ZIP_FOLDER.icon(color=QColor("#ffA500"))
        # 蓝色物联网
        self.IOT_icon = FluentIcon.IOT.icon(color=QColor("#00A5ff"))

        # 载入图标池
        BIP.load("STM",MetaverseICO.STM)
        # 载入图像池
        BPP.load("STM",MetaversePNG.STM)

        # 读取主题色
        self.theme_model = JCP.get("config.json", ["setting","theme_model"],"LIGHT")
        # 读取强调色
        self.theme_color = JCP.get("config.json", ["setting","theme_color"],"#ff009faa")
        # 读取云母效果
        self.mica_effect = JCP.get("config.json", ["setting","mica_effect"],True)
        # 读取懒加载
        self.lazy = JCP.get("config.json", ["setting","lazy"],False)
        # 自动强调色
        self.theme_color_auto = JCP.get("config.json", ["setting","theme_color_auto"],True)
        # 启用DPI缩放
        self.activated_dpi_zoom_switch = JCP.get("config.json", ["setting","DPI_zoom"],False)
        # 启用非整数缩放
        self.activated_dpi_non_int_zoom_switch = JCP.get("config.json", ["setting","DPI_non_int_zoom"],False)
        # 启用高DPI像素映射
        self.high_DPI_pixel_mapping = JCP.get("config.json", ["setting","high_DPI_pixel_mapping"],False)
        # 启动时全屏
        self.full_screen_startup_init_switch = JCP.get("config.json", ["setting","full_screen_startup"],False)
        # 启动后全屏
        self.full_screen_after_startup_init_switch = JCP.get("config.json", ["setting","full_screen_after_startup"],False)
        # 启动后最大化
        self.maximize_after_startup_init_switch = JCP.get("config.json", ["setting","maximize_after_startup"],False)
        # 自动进入环境
        self.auto_enter_venv = JCP.get("config.json", ["setting","auto_enter_venv"], True)
        # 启动动画时长
        self.startup_animation_duration = JCP.get("config.json", ["setting","startup_animation_duration"], "常规-1000ms")
        # 启动图标大小
        self.startup_ico_size = JCP.get("config.json", ["setting","startup_ico_size"], "中-120px")
        # 启动图标阴影
        self.startup_ico_shadow = JCP.get("config.json", ["setting","startup_ico_shadow"], False)
        # 备份路径
        self.backup_path = JCP.get("config.json", ["setting","backup_path"],os.getcwd()+"\\Backup")
        # 过渡时长
        self.transition_duration = JCP.get("config.json", ["setting","transition_duration"], "10ms")
        # 启动页面过渡时长
        self.startup_animation_transition_duration = JCP.get("config.json",["setting","startup_animation_transition_duration"],"10ms")
        # 禁止创建原生控件同级窗口
        self.prohibit_creating_native_control_windows_same_level = JCP.get("config.json", ["setting","prohibit_creating_native_control_windows_same_level"], False)
        # 启动时检查更新
        self.startup_check_update = JCP.get("config.json", ["setting","startup_check_update"], False)
        # 跳过退出保存
        self.skip_exit_save = JCP.get("config.json", ["setting","skip_exit_save"], False)
        # 配置文件保护
        self.config_file_protect = JCP.get("config.json", ["setting","config_file_protect"], True)
        # 演示模式
        self.demo_mode = JCP.get("config.json", ["setting","demo_mode"], False)
        # 完整备份
        self.full_backup = JCP.get("config.json", ["setting","full_backup"], False)
        # 自动重载
        self.auto_reload = JCP.get("config.json", ["setting","auto_reload"], True)
        # 自动退出
        self.auto_exit = JCP.get("config.json", ["setting","auto_exit"], False)
        # 自动备份同步
        self.auto_backup_sync = JCP.get("config.json", ["setting","auto_backup_sync"], True)
        # 同步重载
        self.sync_reload = JCP.get("config.json", ["setting","sync_reload"], True)
        # 排序池
        self.sort_jcp_pool = JCP.get("config.json", ["setting","sort_jcp_pool"], False)

        # 后台线程引用
        self.github_release_thread = None

        self.init_window()  # 初始化窗口
        self.init_navigationInterface()  # 初始化导航栏

    # 初始化窗口
    def init_window(self):
        # 基础属性
        self.setWindowTitle("STM 超工具集管理器")
        self.setWindowIcon(BIP.get("STM"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("STM")

        # 更新云母效果
        self.setMicaEffectEnabled(self.mica_effect)

        # 如果不是不显示-0ms 开始
        if self.startup_animation_duration != "不显示-0ms":
            # 创建启动页面
            self.splashScreen = SplashScreen(self.windowIcon(), self, enableShadow=self.startup_ico_shadow)

            size = {"小-80px":80,"中-120px":120,"大-240px":240}.get(self.startup_ico_size,120)
            self.splashScreen.setIconSize(QSize(size, size))
            #self.splashScreen.titleBar.closeBtn.setEnabled(False)
            self.splashScreen.titleBar.closeBtn.clicked.connect(lambda :sys.exit())

        screen_size = QApplication.primaryScreen().availableGeometry()
        # 中心坐标
        h = 1200
        w = 800
        x = (screen_size.width() - h) // 2
        y = (screen_size.height() - w) // 2
        self.setGeometry(x, y, h, w)  # 窗口大小 还原

        # 全屏
        if self.full_screen_startup_init_switch:
            self.showFullScreen()

        # 如果不是不显示-0ms 结束
        if self.startup_animation_duration != "不显示-0ms":
            startup_animation_duration = {"0ms": 0, "10ms": 10, "20ms": 20, "30ms": 30}.get(self.startup_animation_transition_duration, 10)
            # 提前显示主窗口 防止启动页面饿死 并延时显示防止出现Win7窗口
            time = QTimer()
            time.singleShot(startup_animation_duration, lambda: self.show())

            # 延时
            self.createSubInterface()

            # 关闭启动页
            self.splashScreen.finish()

        # 启动设置
        # 启动时检查更新
        if self.startup_check_update:
            self.get_new_version()

    # 初始化导航栏
    def init_navigationInterface(self):
        self.navigationInterface.setExpandWidth(170)  # 固定抽屉长度

        # 主页
        self.Home = QWidget(self)
        self.Home.setObjectName("Home")
        self.init_homepage()  # 初始化主页
        self.addSubInterface(
            self.Home,
            FluentIcon.HOME,
            "主页"
        )

        # 命令面板
        self.CommandPanel = QWidget(self)
        self.CommandPanel.setObjectName("CommandPanel")
        self.init_command_panel()  # 初始化环境管理
        self.addSubInterface(
            self.CommandPanel,
            FluentIcon.COMMAND_PROMPT,
            "命令面板"
        )

        # 虚拟环境管理
        self.Venv = QWidget(self)
        self.Venv.setObjectName("Venv")
        self.init_venv()  # 初始化环境管理
        self.addSubInterface(
            self.Venv,
            self.IOT_icon,
            "虚拟环境"
        )

        # 创建
        self.Created = QWidget(self)
        self.Created.setObjectName("Created")
        self.init_created()  # 初始化创建环境
        self.addSubInterface(
            self.Created,
            FluentIcon.ADD,
            "创建",
            position=NavigationItemPosition.BOTTOM
        )

        # 设置
        self.Setting = QWidget(self)
        self.Setting.setObjectName("setting")
        self.init_setting()  # 初始化设置
        self.addSubInterface(
            self.Setting,
            FluentIcon.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM
        )

    # 启动页面延时
    def createSubInterface(self):
        duration = self.startup_animation_duration.split('-')
        loop = QEventLoop(self)
        QTimer.singleShot(int(duration[1][:-2]), loop.quit)
        loop.exec()

    # 关闭事件
    def closeEvent(self, event):
        super().closeEvent(event)

        # 不在演示模式中
        if not self.demo_mode:
            # 跳过退出保存
            if self.skip_exit_save:
                # 判断是否修改
                # 池中Json
                new_json = JCP.read("config.json")
                # 本地Json
                old_json = JsonConfigTool.read_json("config.json")
                # 是否相同
                same = JsonConfigTool.json_equal(new_json,old_json)
                # 不相同
                if not same:
                    # 保存池
                    JCP.save()
            else:
                # 保存池
                JCP.save()

    # 更新主题模式
    def update_theme_model(self, theme):
        try:
            theme_name = (self.theme_map[theme])
            setTheme(tool.str_to_theme(theme_name),lazy=self.lazy)
            JCP.update("config.json", ["setting","theme_model"], theme_name)
            self.theme_model = theme_name
            self.theme_color_auto = JCP.get("config.json", ["setting","theme_color_auto"],True)
            if self.theme_color_auto:
                if self.theme_model == "DARK":  # 暗
                    self.select_color_button.setColor(QColor("#ff29f1ff"))
                    JCP.update("config.json", ["setting","theme_color"], "#ff29f1ff")
                    self.hyperlink_file_label.set_text_color("#ff29f1ff")
                elif self.theme_model == "LIGHT":  # 亮
                    self.select_color_button.setColor(QColor("#ff009faa"))
                    JCP.update("config.json", ["setting","theme_color"], "#ff009faa")
                    self.hyperlink_file_label.set_text_color("#ff009faa")
                elif self.theme_model == "AUTO":  # 自动
                    current_theme = darkdetect.theme()  # 获取系统主题
                    if current_theme == 'Dark':
                        self.select_color_button.setColor(QColor("#ff29f1ff"))
                        JCP.update("config.json", ["setting","theme_color"], "#ff29f1ff")
                        self.hyperlink_file_label.set_text_color("#ff29f1ff")
                    if current_theme == 'Light':
                        self.select_color_button.setColor(QColor("#ff009faa"))
                        JCP.update("config.json", ["setting","theme_color"], "#ff009faa")
                        self.hyperlink_file_label.set_text_color("#ff009faa")

        except Exception as a:
            print(a)

    # 更新主题强调色
    def update_theme_color(self, color):
        try:
            setThemeColor(color,lazy=self.lazy)
            JCP.update("config.json", ["setting","theme_color"], color)
            JCP.update("config.json", ["setting","theme_color_auto"], False)
            self.theme_color = color
            self.hyperlink_file_label.set_text_color(color)

            # 不处在隐藏
            if self.downloadBadge.text() != "":
                # 更新背景颜色 强制使用强调色
                self.downloadBadge.setCustomBackgroundColor(self.theme_color, self.theme_color)
        except Exception as a:
            print(a)

    # 恢复默认强调色
    def restore_default_color(self):
        try:
            content = """黑暗主题模式下换回 十六进制颜色代码#ff29f1ff
            明亮主题模式下换回 十六进制颜色代码#ff009faa
            并切换回自动强调色模式 随主题模式切换"""

            w = Dialog('确认恢复主题默认强调色？', content, self)

            if w.exec():
                if self.theme_model == "DARK":  # 暗
                    self.theme_color = "#ff29f1ff"

                elif self.theme_model == "LIGHT":  # 亮
                    self.theme_color = "#ff009faa"

                elif self.theme_model == "AUTO":  # 自动
                    current_theme = darkdetect.theme()  # 获取系统主题
                    if current_theme == 'Dark':
                        self.theme_color = "#ff29f1ff"

                    if current_theme == 'Light':
                        self.theme_color = "#ff009faa"

                setThemeColor(QColor(self.theme_color),lazy=self.lazy)
                JCP.update("config.json", ["setting","theme_color"], self.theme_color)
                self.select_color_button.setColor(QColor(self.theme_color))
                self.hyperlink_file_label.set_text_color(self.theme_color)

                # 徽章不处在隐藏
                if self.downloadBadge.text() != "":
                    # 更新背景颜色 强制使用强调色
                    self.downloadBadge.setCustomBackgroundColor(self.theme_color, self.theme_color)

                InfoBar.success(
                    title="完成",
                    content="默认颜色已恢复",
                    parent=self,
                    position=InfoBarPosition.TOP
                )

                JCP.update("config.json", ["setting","theme_color_auto"], True)
        except Exception as a:
            print(a)

    # 切换堆叠创建窗口
    def created_stacked_update(self,page):
        if page == "虚拟环境":
            self.created_stacked.setCurrentIndex(0)
        elif page == "便携式环境":
            self.created_stacked.setCurrentIndex(1)
        elif page == "基础环境":
            self.created_stacked.setCurrentIndex(2)
        elif page == "配置文件":
            self.created_stacked.setCurrentIndex(3)
        elif page == "预设脚本":
            self.created_stacked.setCurrentIndex(4)
        elif page == "图钉":
            self.created_stacked.setCurrentIndex(5)

    # 切换分段创建窗口
    def segmented_stacked_update(self,page):
        if page == "现有":
            self.segmented_venv_stacked.setCurrentIndex(0)
        if page == "新建":
            self.segmented_venv_stacked.setCurrentIndex(1)
        if page == "配置":
            self.segmented_venv_stacked.setCurrentIndex(2)

        if page == "路径":
            self.segmented_python_stacked.setCurrentIndex(0)
        if page == "环境变量":
            self.segmented_python_stacked.setCurrentIndex(1)
        if page == "搜索":
            self.segmented_python_stacked.setCurrentIndex(2)

        if page == "快速":
            self.segmented_install_stacked.setCurrentIndex(0)
        if page == "完全":
            self.segmented_install_stacked.setCurrentIndex(1)
        if page == "静默":
            self.segmented_install_stacked.setCurrentIndex(2)
        if page == "批量":
            self.segmented_install_stacked.setCurrentIndex(3)

    # 获取python版本
    def get_python_version_by_cmd(self,python_exe: str):
        try:
            proc = subprocess.run(
                [python_exe, "--version"],
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )
            return (proc.stdout or proc.stderr).strip()
        except subprocess.TimeoutExpired as e:
            InfoBar.warning(
                title="超时",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP
            )
            return "超时"
        except Exception as e:
            InfoBar.warning(
                title="警告",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP
            )
            return "未知"

    # 打开添加基础环境窗口
    def open_add_python_window(self):
        python_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 Python 解释器",
            "C:/",
            "Python Executable (python.exe pythonw.exe);;"
            "All Files (*.*)"
        )
        if python_path != '':
            self.add_python_path_line.setText(python_path)

    # 添加基础环境
    def add_python(self):
        try:
            # 判断路径是否存在
            path = self.add_python_path_line.text()
            if os.path.exists(path):
                name = Path(path).name.lower()
                if "python" in name and name.endswith(".exe"):

                    # 获取python版本
                    python_v = self.get_python_version_by_cmd(path)
                    JCP.update(
                        "config.json",
                        ["python",os.path.dirname(path)],
                        {
                            "name": python_v, # 名称
                            "path": path, # 解释器路径
                            "dir": os.path.dirname(path), # 解释器目录
                            "version": python_v[7:] # 版本
                        }
                    )
                    self.add_python_path_line.setText("")
                    InfoBar.success(
                        title="成功",
                        content=f"基础环境 {python_v} 添加成功",
                        parent=self,
                        position=InfoBarPosition.TOP
                    )
                    self.update_python() # 刷新基础环境

            else:
                InfoBar.error(
                    title="错误",
                    content="基础解释器不存在",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
        except Exception as a:
            InfoBar.error(
                title="错误",
                content=str(a),
                parent=self,
                position=InfoBarPosition.TOP
            )


if __name__ == "__main__":
    # 加入池
    JCP.load("config.json")

    # 创建翻译器
    translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))

    #尝试启用 OpenGL 或 ANGLE 后端（视显卡驱动而定，有时能显著提升 Fluent 效果性能）
    #app.setAttribute(Qt.AA_UseSoftwareOpenGL, False)

    # 共享 OpenGL 对象
    #QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # 解决同时使用 Dialog 和 FluentWindow 可能导致窗口无法拉伸
    # Dialog 和 MessageBox 一同使用导致焦点残留存在
    # 焦点统一修复
    # 禁止创建原生控件同级窗口
    if JCP.get("config.json",["setting","prohibit_creating_native_control_windows_same_level"],False):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # 启用DPI缩放
    if JCP.get("config.json", ["setting","DPI_zoom"],False):
        # 启用高DPI缩放
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # 启用非整数缩放
    if JCP.get("config.json", ["setting","DPI_non_int_zoom"], False):
        # 支持非整数缩放比
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # 使用高 DPI 像素映射
    if JCP.get("config.json", ["setting","high_DPI_pixel_mapping"], False):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication([])

    # 安装翻译器
    app.installTranslator(translator)

    # 主题
    Theme_Model = JCP.get("config.json", ["setting","theme_model"],"LIGHT")

    setTheme(tool.str_to_theme(Theme_Model))

    # 自动强调色模式 默认自动
    if not JCP.get("config.json", ["setting","theme_color_auto"],True):
            setThemeColor(JCP.get("config.json", ["setting","theme_color"], "#ff009faa"))
    mainWin = MainUI()

    transition_duration = JCP.get("config.json", ["setting","transition_duration"],"0ms")
    duration = {"0ms": 0, "10ms": 10, "20ms": 20, "30ms": 30}.get(transition_duration,10)
    # 延时显示 解决Win7窗口过渡
    timer = QTimer()
    if JCP.get("config.json", ["setting","full_screen_after_startup"],False):
        timer.singleShot(duration, lambda: mainWin.showFullScreen()) # 启动后全屏
    elif JCP.get("config.json", ["setting","maximize_after_startup"],False):
        timer.singleShot(duration, lambda: mainWin.showMaximized()) # 启动后最大化
    else:
        timer.singleShot(duration, lambda: mainWin.show()) # 常规

    sys.exit(app.exec_())

# ff29f1ff
# ff009faa

# 在启动页面关闭时 执行 强制关闭 拒绝关闭 隐藏控制按钮

# 紧急修复 和一次性通知

# 内存泄漏调试器
# objgraph.show_growth()

# 背景音乐 枚举值 MUSIC

#downloadBadge 徽章终点位置

#table.verticalHeader().hide() # 隐藏表头 / 表格头图标

# 环境表格更新是否联动环境树
# 编辑是否继承

# 备份与恢复 公告 重置
# 内部信息

# 去掉外部cmd创建 配置创建后续待验证

# 禁用侧边栏指示器滑动动画
# self.navigationInterface.setIndicatorAnimationEnabled(False)

# 自定义背景颜色
# self.setCustomBackgroundColor(QColor(73, 156, 84), QColor(25, 33, 42))

# from BlurWindow.blurWindow import GlobalBlur 透明亚克力
# GlobalBlur(self.winId(),Acrylic=True,Dark=True, QWidget=self)

# 窗口自定义分辨率

# CMD std流历史 当前cmd详情

# 全局控制台 使用持续嵌入 意外退出重启控制台

# 各个cmd 控制台状态 加入图表

# 选择配置文件优先 APPDATA还是工作目录的配置

# 徽章跟随强调色

# 工作站工作模式 源码/程序/虚拟环境

# 自动配置查找环境 和 依据树查找cmd改为用 item data存的唯一值

# 读取版本信息
# JCP.get("config.json", ["info", "version"], "LIGHT")

# 控制台自动配置名称
# 控制台自动创建

# 自检
# 扫描环境

# 创建-别名 venv python embed uv

# 路径不统bug

# 文件锁

# 虚拟环境快照

# 开启cmd后 布局刷新策略变更
# 图标有时失效

# ex_style |= (
#         win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_NOACTIVATE
# )
# 去前台焦点 GWL_EXSTYLE 设置
#
# WS_EX_TOOLWINDOW
# Window Style Extended Tool Window
# 不显示在任务栏/Alt+Tab
# WS_EX_NOACTIVATE
# Window Style Extended No Activate
# 点击不抢焦点
# WS_EX_WINDOWEDGE
# Window Style Extended Window Edge
# 立体边框（你已去掉）

# items = ['shoko', '西宫硝子', '宝多六花', '小鸟游六花']
# completer = QCompleter(items, self.download_version_combox)
#
# # 设置显示的选项数
# completer.setMaxVisibleItems(10)
#
# # 设置补全器
# self.download_version_combox.setCompleter(completer)
# # 补全

# 更换编辑下拉框 默认回车添加新控件

# 强制退出关闭计时

# 下载列表快导致徽章计时多2

# 配置同步 把配置放到appdata

# 自动保存

# 工具集

# 配置模式与立即克隆配置到同步文件夹

# 安装成功 匹配成功视为异步操作
from __future__ import annotations

from MetaverseSDK.MetaverseAPI.Url import UrlBuilder
from MetaverseSDK.MetaverseAPI.UrlKey import ContributorKey, RepoKey
from MetaverseSDK.MetaverseTool.Config.JsonConfigPool import JCP
from MetaverseSDK.MetaverseUI.MCore.MPool.MBasePixmapPool import BPP
from MetaverseSDK.MetaverseUI.MFluentWidgets.MCmdCommandPanelWidget import CmdCommandPanel
from MetaverseSDK.MetaverseUI.MFluentWidgets.MColorPickerButton import NoMaskColorPickerButton
from MetaverseSDK.MetaverseUI.MFluentWidgets.MLayoutSettingCard import LayoutSettingCard, LayoutSwitchButtonSettingCard, \
    LayoutHyperlinkButtonSettingCard, LayoutDangerButtonSettingCard, \
    LayoutButtonSettingCard, LayoutPrimaryButtonSettingCard, LayoutComboBoxSettingCard
from MetaverseSDK.MetaverseUI.MFluentWidgets.MTableWidget import RoundedTableListWidget
from MetaverseSDK.MetaverseUI.MWidgets.MStackedWidget import PopUpAniUpDownStackedWidget, \
    PageLeftRightStackedWidget, PageFreezeUpDownStackedWidget
from MetaverseSDK.MetaverseUI.MWidgets.MLabel import HyperlinkFileLabel, ImageLabel
from MetaverseSDK.MetaverseUI.MReviseWidgets.MLabel import BodyLabel, CaptionLabel,TitleLabel
from PyQt5.QtGui import QIcon, QFont, QDesktopServices
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QSpacerItem, QGridLayout
from qfluentwidgets import FluentIcon, SimpleCardWidget, EditableComboBox, ListWidget, IconWidget, ToolButton, \
    PopUpAniStackedWidget, Pivot, LineEdit, SegmentedWidget, PushButton, ComboBox, CheckBox, TextEdit, \
    SmoothScrollArea, SwitchButton, getFont, ToolTipFilter
from typing import TYPE_CHECKING

import tool
from MetaverseSDK.MetaverseResource.MetaverseFluentIcon import MetaverseFluentIcon

from qfluentwidgets import __version__ as QFW__version__
from PyQt5.QtCore import QT_VERSION_STR as QT__version__, QUrl
from MetaverseSDK import __version__ as SDK__version__

# 资源文件
import MetaverseSDK.MetaverseResource.MetaverseQRC

if TYPE_CHECKING:
    from STM import MainUI
    _MixinBase = MainUI   # 类型检查时 MainUI
else:
    _MixinBase = object   # 运行时 object

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout, QWidget

from qfluentwidgets import PrimaryPushButton


class UiMixin(_MixinBase):
    # 初始化主页
    def init_homepage(self):
        # 嵌入垂直布局
        vlayout = QVBoxLayout(self.Home)

        # 顶部弹簧
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vlayout.addWidget(ImageLabel(BPP.get("STM"),110,165),alignment=Qt.AlignCenter)
        vlayout.addWidget(TitleLabel("Super Toolset Manager"),alignment=Qt.AlignCenter)

        vlayout.addWidget(BodyLabel(f"STM | 版本 {self.STM_Version}"),alignment=Qt.AlignCenter)
        vlayout.addWidget(BodyLabel("更加可读,快捷,方便的管理Python环境"),alignment=Qt.AlignCenter)

        # 间隔弹簧
        vlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        # 居中弹簧
        btn_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed))
        add_btn = PrimaryPushButton("创建")
        add_btn.setIcon(FluentIcon.ADD)
        add_btn.setFixedWidth(100)
        add_btn.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.Created))
        btn_layout.addWidget(add_btn, alignment=Qt.AlignCenter)

        iot_btn = PushButton("环境")
        iot_btn.setIcon(FluentIcon.IOT)
        iot_btn.setFixedWidth(100)
        iot_btn.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.VenvManage))
        btn_layout.addWidget(iot_btn, alignment=Qt.AlignCenter)

        # 居中弹簧
        btn_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed))
        vlayout.addLayout(btn_layout)

        # 底部弹簧
        vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

    # 初始化环境管理
    def init_command_panel(self):
        # 嵌入垂直布局
        vlayout = QHBoxLayout(self.CommandPanel)

        self.cmd = CmdCommandPanel()
        vlayout.addWidget(self.cmd)

    # 初始化虚拟环境
    def init_venv(self):
        # 嵌入垂直布局
        layout = QHBoxLayout(self.Venv)

        # 圆角表格列表控件
        self.venv_table = RoundedTableListWidget()

        # 设置行列
        self.venv_table.setColumnCount(7)
        self.venv_table.setRowCount(0)

        # 更新表格
        config_json = JCP.get("config.json", ["venv"], {})  # 默认空集合
        for value, key in config_json.items():
            tool.table_add_row_7(self.venv_table, key["name"], key["version"], key["dir"], key["cfg_file"],
                                 key['start_parameter'], key['python'], str(key["include-system-site-packages"]), value)

        # 设置标头
        self.venv_table.setHorizontalHeaderLabels(
            ['名称', '版本', '环境路径', '配置路径', '启动参数', '基础环境路径', '继承'])

        # 先全部按内容算
        header = self.venv_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # 四列平分剩余空间
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)

        layout.addWidget(self.venv_table)

    # 初始化便携式环境
    def init_emb(self):
        # 嵌入垂直布局
        layout = QHBoxLayout(self.EmbEnv)

        # 圆角表格列表控件
        self.emb_table = RoundedTableListWidget()

        # 设置行列
        self.emb_table.setColumnCount(5)
        self.emb_table.setRowCount(0)

        # 更新表格
        emb_json = JCP.get("config.json", ["emb"], {})  # 默认空集合
        for value, key in emb_json.items():
            tool.table_add_row_5(self.emb_table, key["name"], key["version"], key["dir"], key["start_script"],
                                 str(key["pth"]), value)

        # 设置标头
        self.emb_table.setHorizontalHeaderLabels(['名称', '版本', '环境路径', '启动脚本路径', '解锁'])

        # 先全部按内容算
        header = self.emb_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # 第三列吃掉剩余空间
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        layout.addWidget(self.emb_table)

    # 初始化基础环境
    def init_python(self):
        # 嵌入垂直布局
        layout = QHBoxLayout(self.BaseEnv)

        # 圆角表格列表控件
        self.python_table = RoundedTableListWidget()

        # 设置行列
        self.python_table.setColumnCount(4)
        self.python_table.setRowCount(0)

        # 更新表格
        python_json = JCP.get("config.json", ["python"], {})  # 默认空集合
        for value, key in python_json.items():
            tool.table_add_row_4(self.python_table, key["name"], key["version"], key["dir"], key["path"], value)

        # 设置标头
        self.python_table.setHorizontalHeaderLabels(['名称', '版本', '环境路径', '解释器'])

        # 先全部按内容算
        header = self.python_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # 两列平分剩余空间
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        layout.addWidget(self.python_table)

    # 初始化创建
    def init_created(self):
        # 嵌入垂直布局
        created_vlayout = QVBoxLayout(self.Created)

        # 导航卡片
        card = SimpleCardWidget()  # 简单卡片
        navigation_hBoxLayout = QHBoxLayout()  # 水平布局
        card.setLayout(navigation_hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        created_vlayout.addWidget(card)  # 嵌入到布局
        # 创建导航栏
        self.create_navigation = Pivot()  # 简单卡片
        self.create_navigation.addItem('虚拟环境', "虚拟环境")
        self.create_navigation.addItem('便携式环境', "便携式环境")
        self.create_navigation.addItem('基础环境', "基础环境")
        self.create_navigation.addItem('配置文件', "配置文件")
        self.create_navigation.addItem('预设脚本', "预设脚本")
        self.create_navigation.addItem('图钉', "图钉")
        self.create_navigation.setCurrentItem('虚拟环境')
        self.create_navigation.setFixedWidth(500)
        self.create_navigation.currentItemChanged.connect(self.created_stacked_update)
        navigation_hBoxLayout.addWidget(self.create_navigation)  # 添加

        # 堆叠创建窗口
        self.created_stacked = PageLeftRightStackedWidget()
        created_vlayout.addWidget(self.created_stacked)  # 嵌入到布局

        # 创建虚拟环境
        card = SimpleCardWidget()
        layout = QVBoxLayout()
        card.setLayout(layout)
        # 标题间隔弹簧
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        title_layout = QHBoxLayout() # 标题布局
        title_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)) # 居中弹簧
        ico_widget = IconWidget(FluentIcon.IOT) # 图标
        ico_widget.setFixedSize(24,24)
        title_layout.addWidget(ico_widget)
        title_layout.addWidget(TitleLabel("创建虚拟环境"))
        title_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)) # 居中弹簧
        layout.addLayout(title_layout) # 添加标题布局
        # 标题间隔弹簧
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        # 分段导航栏
        segmented = SegmentedWidget()
        segmented.addItem("现有","现有")
        segmented.addItem("新建","新建")
        segmented.addItem("配置","配置")
        segmented.setCurrentItem("现有") # 默认选中
        segmented.currentItemChanged.connect(self.segmented_stacked_update)
        layout.addWidget(segmented,alignment=Qt.AlignHCenter)
        # 子堆叠窗口
        self.segmented_venv_stacked = PopUpAniStackedWidget()
        layout.addWidget(self.segmented_venv_stacked)
        # 新建卡片
        new_card = SimpleCardWidget()
        new_card_external_layout = QVBoxLayout() # 外部布局
        new_card_layout = QGridLayout() # 格栅布局
        new_card.setLayout(new_card_external_layout)
        new_card_external_layout.addLayout(new_card_layout) # 外部布局添加格栅布局
        self.venv_loca_name = LineEdit() # 行输入框
        self.venv_loca_name.setPlaceholderText("venv")
        new_card_layout.addWidget(BodyLabel("环境名称:"),0,0)
        new_card_layout.addWidget(self.venv_loca_name,0,1,1,2)
        self.venv_loca_line = LineEdit() # 行输入框
        self.venv_loca_line.setPlaceholderText(".venvs/venv")
        self.venv_loca_button = ToolButton(FluentIcon.FOLDER) # 图标按钮
        new_card_layout.setColumnStretch(1, 1) # 伸缩 第一列吃掉剩下空间
        new_card_layout.addWidget(BodyLabel("环境位置:"),1,0)
        new_card_layout.addWidget(self.venv_loca_line,1,1)
        new_card_layout.addWidget(self.venv_loca_button,1,2)
        self.base_python_box = ComboBox() # 下拉框
        self.base_python_box.clicked.connect(lambda :self.update_python_combox(self.base_python_box)) # 下拉列表点击信号
        self.base_python_box.activated.connect(lambda :self.base_python_box.setText(self.base_python_box.currentData())) # 选中信号
        new_card_layout.addWidget(BodyLabel("基础解释器:"),2,0)
        new_card_layout.addWidget(self.base_python_box,2,1,1,2)
        self.inherits_global_site_software_packages_box = CheckBox() # 继承全局站点软件包 复选框
        self.inherits_global_site_software_packages_box.setText("继承全局站点软件包")
        self.inherits_global_site_software_packages_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--system-site-packages"))
        new_card_layout.addWidget(self.inherits_global_site_software_packages_box,3,0,1,3)  # 跨行
        self.try_using_symbolic_links_box = CheckBox() # 尝试使用符号链接 复选框
        self.try_using_symbolic_links_box.setText("尝试使用符号链接")
        self.try_using_symbolic_links_box.stateChanged.connect(lambda s:self.forced_file_copying_box.setEnabled(not s))
        self.try_using_symbolic_links_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--symlinks"))
        new_card_layout.addWidget(self.try_using_symbolic_links_box,4,0,1,3)  # 跨行
        self.forced_file_copying_box = CheckBox() # 强制复制文件 复选框
        self.forced_file_copying_box.setText("强制复制文件")
        self.forced_file_copying_box.stateChanged.connect(lambda s:self.try_using_symbolic_links_box.setEnabled(not s))
        self.forced_file_copying_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--copies"))
        new_card_layout.addWidget(self.forced_file_copying_box,5,0,1,3)  # 跨行
        self.clear_existing_directories_box = CheckBox() # 清空已存在目录 复选框
        self.clear_existing_directories_box.setText("清空已存在目录")
        self.clear_existing_directories_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--clear"))
        new_card_layout.addWidget(self.clear_existing_directories_box,6,0,1,3)  # 跨行
        self.upgrade_package_box = CheckBox() # 升级软件包 复选框
        self.upgrade_package_box.setText("升级软件包")
        self.upgrade_package_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--upgrade"))
        new_card_layout.addWidget(self.upgrade_package_box,7,0,1,3)  # 跨行
        self.skip_installing_pip_box = CheckBox() # 跳过安装pip 复选框
        self.skip_installing_pip_box.setText("跳过安装pip")
        self.skip_installing_pip_box.stateChanged.connect(lambda s:self.skip_installing_pip_mutual_exclusion(s))
        self.skip_installing_pip_box.stateChanged.connect(lambda state: self.venv_command_batch(state,"--without-pip"))
        new_card_layout.addWidget(self.skip_installing_pip_box,8,0,1,3)  # 跨行
        self.custom_prompts_prefix_box = CheckBox() # 自定义提示符前缀 复选框
        self.custom_prompts_prefix_box.setText("自定义提示符前缀")
        self.custom_prompts_prefix_box.stateChanged.connect(lambda s:self.prompts_prefix_line.setEnabled(s))
        new_card_layout.addWidget(self.custom_prompts_prefix_box,9,0,1,3)  # 跨行
        self.prompts_prefix_line = LineEdit() # 行输入框
        self.prompts_prefix_line.setPlaceholderText("venv")
        self.prompts_prefix_line.setEnabled(False)
        self.venv_startup_parameters_line = LineEdit() # 行输入框
        new_card_layout.addWidget(BodyLabel("提示符前缀:"),10,0) # 跨行
        new_card_layout.addWidget(self.prompts_prefix_line,10,1,1,3) # 跨行
        new_card_layout.addWidget(BodyLabel("启动参数:"),11,0) # 跨行
        new_card_layout.addWidget(self.venv_startup_parameters_line,11,1,1,3) # 跨行
        new_card_layout.addWidget(BodyLabel("创建命令:"),12,0)
        self.created_parameter_line = LineEdit() # 行输入框
        self.created_parameter_line.setPlaceholderText("python -m venv")
        new_card_layout.addWidget(self.created_parameter_line, 12, 1, 1, 2)  # 跨行
        button_layout = QHBoxLayout() # 按钮布局
        self.created_new_venv = PrimaryPushButton("创建")# 添加现有按钮
        self.created_new_venv.setFixedSize(100,30)
        self.reset_new_venv = PushButton("重置")# 重置现有按钮
        self.reset_new_venv.setFixedSize(100,30)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed))# 间隔调小 防止撑开主窗口
        button_layout.addWidget(self.created_new_venv)
        button_layout.addWidget(self.reset_new_venv)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed))# 水平居中弹簧
        new_card_external_layout.addLayout(button_layout)
        new_card_external_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))  # 底部弹簧
        self.segmented_venv_stacked.addWidget(new_card) # 添加新建页

        # 添加便携式环境
        card = SimpleCardWidget()
        layout = QVBoxLayout()
        card.setLayout(layout)
        # 标题间隔弹簧
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        title_layout = QHBoxLayout() # 标题布局
        title_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)) # 居中弹簧
        ico_widget = IconWidget() # 图标
        ico_widget.setIcon(FluentIcon.ZIP_FOLDER)
        ico_widget.setFixedSize(24,24)
        title_layout.addWidget(ico_widget)
        title_layout.addWidget(TitleLabel("添加便携式环境"))
        title_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)) # 居中弹簧
        layout.addLayout(title_layout) # 添加标题布局
        # 标题间隔弹簧
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        add_card = SimpleCardWidget()
        add_card_layout_base = QVBoxLayout()
        add_card_layout = QGridLayout() # 格栅布局
        add_card_layout_base.addLayout(add_card_layout)
        add_card.setLayout(add_card_layout_base)
        add_card_layout.addWidget(BodyLabel("嵌入包路径:"),0,0)
        self.add_emb_path_line = LineEdit()
        self.add_emb_path_line.setPlaceholderText("python-embed.zip")
        self.add_emb_path_button = ToolButton(FluentIcon.FOLDER)  # 图标按钮
        add_card_layout.addWidget(self.add_emb_path_line,0,1)
        add_card_layout.addWidget(self.add_emb_path_button,0,2)
        add_card_layout.addWidget(BodyLabel("安装位置:"),1,0)
        self.add_emb_install_path_line = LineEdit()
        self.add_emb_install_path_line.setPlaceholderText(".embs/emb")
        self.add_emb_install_path_line.textChanged.connect(lambda text:self.custom_pip_acquisition_line.setText(f'curl https://bootstrap.pypa.io/get-pip.py -o "{text}/get-pip.py"'))
        self.add_emb_install_path_button = ToolButton(FluentIcon.FOLDER)  # 图标按钮
        add_card_layout.addWidget(self.add_emb_install_path_line,1,1)
        add_card_layout.addWidget(self.add_emb_install_path_button,1,2)
        self.unlock_library_box = CheckBox() # 解锁第三方库 复选框
        self.unlock_library_box.setText("解锁第三方库")
        self.unlock_library_box.toggled.connect(lambda c:self.emb_batch("解锁第三方库",c))
        self.unlock_library_box.stateChanged.connect(lambda s:self.unlock_pth_dynamic_disabled(s))
        add_card_layout.addWidget(self.unlock_library_box,2,0,1,3) # 跨列
        self.create_startup_script_box = CheckBox() # 创建启动脚本 复选框
        self.create_startup_script_box.setText("创建启动脚本")
        self.create_startup_script_box.toggled.connect(lambda c:self.emb_batch("创建启动脚本",c))
        add_card_layout.addWidget(self.create_startup_script_box,3,0,1,3)
        self.creat_CMD_box = CheckBox() # 使用外部CMD创建 复选框
        self.creat_CMD_box.setText("使用外部CMD创建")
        self.creat_CMD_box.toggled.connect(lambda c:self.emb_batch("使用外部CMD创建",c)) # 双连接
        self.creat_CMD_box.toggled.connect(lambda s:self.CMD_dynamic_disabled(s))
        add_card_layout.addWidget(self.creat_CMD_box,4,0,1,3)
        self.creat_CMD_open_box = CheckBox() # CMD创建后保持打开 复选框
        self.creat_CMD_open_box.setText("CMD创建后保持打开")
        self.creat_CMD_open_box.toggled.connect(lambda c:self.emb_batch("CMD创建后保持打开",c))
        add_card_layout.addWidget(self.creat_CMD_open_box,5,0,1,3)
        self.creat_CMD_open_box.setEnabled(False)
        self.automatically_obtain_install_pip_box = CheckBox() # 自动获取pip 复选框
        self.automatically_obtain_install_pip_box.setText("自动获取pip并安装")
        self.automatically_obtain_install_pip_box.toggled.connect(lambda c:self.emb_batch("自动获取pip并安装",c))
        self.automatically_obtain_install_pip_box.stateChanged.connect(lambda s:self.automatic_acquisition_dynamic_disabled(s))
        self.automatically_obtain_install_pip_box.setEnabled(False) # 临时禁用
        add_card_layout.addWidget(self.automatically_obtain_install_pip_box,6,0,1,3)
        self.custom_pip_acquisition_box = CheckBox()
        self.custom_pip_acquisition_box.setText("自定义获取pip")
        self.custom_pip_acquisition_box.toggled.connect(lambda c:self.emb_batch("自定义获取pip",c))
        self.custom_pip_acquisition_box.stateChanged.connect(lambda s:self.custom_get_dynamic_disabled(s))
        self.custom_pip_acquisition_box.setEnabled(False) # 临时禁用
        add_card_layout.addWidget(self.custom_pip_acquisition_box,7,0,1,3)
        add_card_layout.addWidget(BodyLabel("pip获取命令:"),8,0)
        self.custom_pip_acquisition_line = LineEdit() # 自动安装pip 复选框
        self.custom_pip_acquisition_line.setText("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        self.custom_pip_acquisition_line.setPlaceholderText("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        self.custom_pip_acquisition_line.setEnabled(False)
        add_card_layout.addWidget(self.custom_pip_acquisition_line,8,1,1,3)
        self.custom_install_pip_box = CheckBox() # 自动安装pip 复选框
        self.custom_install_pip_box.setText("自定义安装pip")
        self.custom_install_pip_box.toggled.connect(lambda c:self.emb_batch("自定义安装pip",c))
        self.custom_install_pip_box.stateChanged.connect(lambda s:self.custom_install_dynamic_disabled(s))
        self.custom_install_pip_box.setEnabled(False) # 临时禁用
        add_card_layout.addWidget(self.custom_install_pip_box,9,0,1,3)
        add_card_layout.addWidget(BodyLabel("引导脚本位置:"),10,0)
        self.custom_install_pip_line = LineEdit() # 自动安装pip 复选框
        self.custom_install_pip_line.setPlaceholderText("C:\get-pip.py")
        self.custom_install_pip_line.setEnabled(False)
        add_card_layout.addWidget(self.custom_install_pip_line,10,1)
        self.custom_install_pip_path_button = ToolButton(FluentIcon.FOLDER)  # 图标按钮
        self.custom_install_pip_path_button.setEnabled(False)
        add_card_layout.addWidget(self.custom_install_pip_path_button,10,2)
        button_layout = QHBoxLayout() # 按钮布局
        self.unpack_activate_button = PrimaryPushButton("解包并激活")
        self.unpack_activate_button.setFixedSize(100,30)
        self.unpack_button = PushButton("仅解包")
        self.unpack_button.setFixedSize(100,30)
        self.reset_emb_button = PushButton("重置")
        self.reset_emb_button.setFixedSize(100,30)
        button_layout.addItem(QSpacerItem(20, 50, QSizePolicy.Expanding, QSizePolicy.Fixed))  # 居中间隔弹簧
        button_layout.addWidget(self.unpack_activate_button)
        button_layout.addWidget(self.unpack_button)
        button_layout.addWidget(self.reset_emb_button)
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Fixed))  # 居中弹簧
        add_card_layout_base.addLayout(button_layout)
        add_card_layout_base.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))  # 底部弹簧
        layout.addWidget(add_card)
        self.created_stacked.addWidget(card) # 添页

    # 初始化设置
    def init_setting(self):
        # 嵌入垂直布局
        self.setting_vlayout = QVBoxLayout(self.Setting)
        # 标题布局
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 10, 0, 0)
        title_layout.addWidget(TitleLabel("设置"))
        self.setting_vlayout.addLayout(title_layout)

        # 平滑滚动画布
        self.setting_scrollArea = SmoothScrollArea()
        self.setting_scrollArea.setWidgetResizable(True)  # 内部控件可调整大小
        self.setting_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setting_scrollArea.setStyleSheet("QScrollArea{background: transparent; border: none}")  # 滚动区域透明

        # 设置视图
        self.setting_view = QWidget()
        self.setting_view.setStyleSheet("QWidget{background: transparent}")  # 视图透明
        self.setting_view_layout = QVBoxLayout(self.setting_view)  # 视图布局

        # 主题标题
        self.setting_view_layout.addWidget(BodyLabel("主题"))
        # 主题卡片
        card = LayoutComboBoxSettingCard(FluentIcon.PALETTE,"主题模式","设置配色方案")
        card.addItems(["明亮", "黑暗", "自动"])
        card.setCurrentText(self.twist_theme_map[JCP.get("config.json", ["setting","theme_model"],"LIGHT")])# 默认选中
        card.currentTextChanged.connect(self.update_theme_model) # 等待初始化后绑定信号
        self.setting_view_layout.addWidget(card)
        # 强调色卡片
        card = SimpleCardWidget()  # 简单卡片
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.HIGHTLIGHT)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("强调色"))  # 文字标签
        contentLabel = CaptionLabel("设置主题强调色")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.select_color_button = NoMaskColorPickerButton(QColor(self.theme_color), '强调色', self,enableAlpha=True)  # 颜色选择器按钮
        self.select_color_button.setFixedWidth(120)
        self.select_color_button.colorChanged.connect(lambda color: self.update_theme_color(color.name()))
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.select_color_button)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 恢复默认强调色卡片
        card = SimpleCardWidget()  # 简单卡片
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.HIGHTLIGHT)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("恢复默认强调色"))  # 文字标签
        contentLabel = CaptionLabel("恢复当前主题默认强调色")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        button = PushButton("恢复默认")
        button.setFixedWidth(120)
        button.clicked.connect(self.restore_default_color)
        vBoxLayout.addWidget(contentLabel)
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(button)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 云母卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.TRANSPARENT)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("云母效果"))  # 文字标签
        contentLabel = CaptionLabel("窗口和表面显示半透明")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.mica_effect_switch = SwitchButton()  # 强制刷新按钮
        self.mica_effect_switch.setChecked(self.mica_effect)
        self.mica_effect_switch.checkedChanged.connect(lambda key: self.update_mica_effect(key))
        self.mica_effect_switch.setFixedWidth(80)
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.mica_effect_switch)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 懒加载卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.LEAF)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("懒加载"))  # 文字标签
        contentLabel = CaptionLabel("延时加载完整主题")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.lazy_switch = SwitchButton()  # 强制刷新按钮
        self.lazy_switch.setChecked(self.lazy)
        self.lazy_switch.checkedChanged.connect(lambda key: self.update_lazy(key))
        self.lazy_switch.setFixedWidth(80)
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.lazy_switch)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # CMD嵌入标题
        self.setting_view_layout.addWidget(BodyLabel("CMD命令面板"))

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 缩放标题
        self.setting_view_layout.addWidget(BodyLabel("缩放"))
        # 启用DPI缩放卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.ZOOM,"开启DPI缩放","开启高DPI感知缩放")
        card.setChecked(self.activated_dpi_zoom_switch)
        card.checkedChanged.connect(self.update_dpi_zoom)
        self.setting_view_layout.addWidget(card)
        # 启用非整数缩放卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.ZOOM,"启用非整数缩放","支持高DPI感知非整数缩放比")
        card.setChecked(self.activated_dpi_non_int_zoom_switch)
        card.checkedChanged.connect(self.update_dpi_non_int_zoom)
        self.setting_view_layout.addWidget(card)
        # 启用高DPI像素映射
        card = LayoutSwitchButtonSettingCard(FluentIcon.ZOOM,"启用高DPI像素映射","启用高DPI图像资源自动适配")
        card.setChecked(self.high_DPI_pixel_mapping)
        card.checkedChanged.connect(self.update_high_DPI_pixel_mapping)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 窗口标题
        self.setting_view_layout.addWidget(BodyLabel("窗口"))
        # 启动时全屏卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.FULL_SCREEN)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("启动时全屏"))  # 文字标签
        contentLabel = CaptionLabel("启动时默认展开全屏")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.full_screen_startup_switch = SwitchButton()  # 开关按钮
        self.full_screen_startup_switch.setChecked(self.full_screen_startup_init_switch)
        self.full_screen_startup_switch.setFixedWidth(80)
        self.full_screen_startup_switch.checkedChanged.connect(lambda key: self.full_screen_startup(key))
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.full_screen_startup_switch)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 启动后全屏卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.FULL_SCREEN)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("启动后全屏"))  # 文字标签
        contentLabel = CaptionLabel("启动后默认展开全屏")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.full_screen_after_startup_switch = SwitchButton()  # 开关按钮
        self.full_screen_after_startup_switch.setChecked(self.full_screen_after_startup_init_switch)
        self.full_screen_after_startup_switch.setFixedWidth(80)
        self.full_screen_after_startup_switch.checkedChanged.connect(lambda key: self.full_screen_after_startup(key))
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.full_screen_after_startup_switch)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 启动后最大化卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.MINIMIZE)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("启动后最大化"))  # 文字标签
        contentLabel = CaptionLabel("启动后默认最大化窗口")  # 字幕标签
        contentLabel.setTextColor("#606060", "#d2d2d2")
        vBoxLayout.addWidget(contentLabel)
        self.maximize_after_startup_switch = SwitchButton()  # 开关按钮
        self.maximize_after_startup_switch.setChecked(self.maximize_after_startup_init_switch)
        self.maximize_after_startup_switch.setFixedWidth(80)
        self.maximize_after_startup_switch.checkedChanged.connect(lambda key: self.maximize_after_startup(key))
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        hBoxLayout.addWidget(self.maximize_after_startup_switch)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 启动页面动画标题
        self.setting_view_layout.addWidget(BodyLabel("启动页面"))
        # 设置启动页面动画时长卡片
        self.startup_animation_duration_card = LayoutComboBoxSettingCard(FluentIcon.SPEED_OFF,"启动页面动画时长","程序初始化时的启动页面动画时长",150)
        self.startup_animation_duration_card.addItems(self.startup_animation_high+self.startup_animation_medium+self.startup_animation_off)
        self.startup_animation_duration_card.setCurrentText(self.startup_animation_duration)
        self.startup_animation_duration_card.activated.connect(self.update_startup_animation_duration)
        self.update_set_startup_animation_duration_ico() # 更新图标
        self.setting_view_layout.addWidget(self.startup_animation_duration_card)
        # 设置启动页面动画时长卡片
        self.sstartup_ico_size_card = LayoutComboBoxSettingCard(FluentIcon.SPEED_OFF,"启动页面图标大小","程序初始化时的启动页面图标大小",150)
        self.sstartup_ico_size_card.addItems(self.startup_ico_list)
        self.sstartup_ico_size_card.setCurrentText(self.startup_ico_size)
        self.sstartup_ico_size_card.activated.connect(self.update_startup_ico_size)
        self.update_set_startup_ico_size_ico() # 更新图标
        self.setting_view_layout.addWidget(self.sstartup_ico_size_card)
        # 关闭启动延迟卡片
        card = LayoutButtonSettingCard(FluentIcon.SPEED_HIGH, "关闭启动延迟", "关闭有关启动延时的设置","关闭延时")
        card.clickedChanged.connect(self.update_close_startup_delay)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 图标阴影卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.TRANSPARENT,"图标阴影","启动页面图标阴影效果")
        card.setChecked(self.startup_ico_shadow)
        card.checkedChanged.connect(lambda key: self.update_shadow(key))
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 修复标题
        self.setting_view_layout.addWidget(BodyLabel("修复"))
        # 窗口过渡时长卡片
        self.transition_duration_card = LayoutComboBoxSettingCard(FluentIcon.DEVELOPER_TOOLS,"窗口过渡时长","修复Win7窗口过渡与任务栏图标异常",150)
        self.transition_duration_card.addItems(["0ms","10ms","20ms","30ms"])
        self.transition_duration_card.setCurrentText(self.transition_duration)
        self.transition_duration_card.activated.connect(self.update_transition_duration)
        self.setting_view_layout.addWidget(self.transition_duration_card)
        # 启动页面过渡时长卡片
        self.startup_animation_transition_duration_card = LayoutComboBoxSettingCard(FluentIcon.DEVELOPER_TOOLS,"启动页面过渡时长","修复Win7启动页面窗口过渡",150)
        self.startup_animation_transition_duration_card.addItems(["0ms","10ms","20ms","30ms"])
        self.startup_animation_transition_duration_card.setCurrentText(self.startup_animation_transition_duration)
        self.startup_animation_transition_duration_card.activated.connect(self.update_startup_animation_transition_duration)
        self.setting_view_layout.addWidget(self.startup_animation_transition_duration_card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 修复标题
        self.setting_view_layout.addWidget(BodyLabel("紧急修复"))
        # 禁止创建原生控件同级窗口卡片
        self.prohibit_creating_native_control_windows_same_level_card = LayoutSwitchButtonSettingCard(FluentIcon.VPN,"禁止创建原生控件同级窗口","紧急修复FluentWindow窗口拉伸与Dialog和MessageBox焦点统一")
        self.prohibit_creating_native_control_windows_same_level_card.setChecked(self.prohibit_creating_native_control_windows_same_level)
        self.prohibit_creating_native_control_windows_same_level_card.checkedChanged.connect(self.update_prohibit_creating_native_control_windows_same_level)
        self.setting_view_layout.addWidget(self.prohibit_creating_native_control_windows_same_level_card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 关于标题
        self.setting_view_layout.addWidget(BodyLabel("关于"))
        # CMD卡片
        card = LayoutSettingCard(FluentIcon.COMMAND_PROMPT, "CMD", f"CMD命令面板 {self.CMD_Version}")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # QFluentWidgets卡片
        card = LayoutSettingCard(QIcon(":/qfluentwidgets/images/logo.png"), "QFluentWidgets", f"版本 v{QFW__version__}")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # PyQt5卡片
        card = LayoutSettingCard(MetaverseFluentIcon.Qt, "PyQt5", f"版本 v{QT__version__}")
        card.iconWidget.setFixedSize(24, 18)
        self.setting_view_layout.addWidget(card)
        # SDK卡片
        card = LayoutSettingCard(FluentIcon.INFO, "MetaverseSDK", f"版本 v{SDK__version__}")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 关于卡片
        card = LayoutSettingCard(FluentIcon.INFO,"版本",f"STM 超工具集管理器 {self.STM_Version}")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 系列卡片
        card = LayoutSettingCard(FluentIcon.INFO,"系列","Metaverse 4")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 工作室卡片
        card = LayoutSettingCard(FluentIcon.INFO,"工作室","STD Studio")
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # Github标题
        self.setting_view_layout.addWidget(BodyLabel("Github"))
        # Github卡片
        card = LayoutHyperlinkButtonSettingCard(FluentIcon.GITHUB,"仓库页","前往VEM仓库页","前往",UrlBuilder.GithubRepo(ContributorKey.H009,RepoKey.VEM))
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        card = LayoutHyperlinkButtonSettingCard(FluentIcon.GITHUB,"发布页","前往VEM发布页","前往",UrlBuilder.GithubRepoReleases(ContributorKey.H009,RepoKey.VEM))
        self.setting_view_layout.addWidget(card)
        card = LayoutPrimaryButtonSettingCard(FluentIcon.GITHUB,"提交反馈","通过提交反馈帮助改进VEM","提交反馈")
        card.clickedChanged.connect(lambda :QDesktopServices.openUrl(QUrl(UrlBuilder.GithubRepoIssues(ContributorKey.H009,RepoKey.VEM))))
        self.setting_view_layout.addWidget(card)
        card = LayoutPrimaryButtonSettingCard(FluentIcon.GITHUB,"检查更新","检查是否有可用更新","检查更新")
        card.clickedChanged.connect(self.get_new_version)
        self.setting_view_layout.addWidget(card)
        card = LayoutSwitchButtonSettingCard(FluentIcon.GITHUB,"启动时检查更新","启动程序时检查是否有可用更新")
        card.setChecked(self.startup_check_update)
        card.checkedChanged.connect(self.update_startup_check_update)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 配置标题
        self.setting_view_layout.addWidget(BodyLabel("配置"))
        # 配置文件卡片
        card = SimpleCardWidget()
        hBoxLayout = QHBoxLayout()  # 水平布局
        hBoxLayout.setContentsMargins(20, 10, 10, 10)
        hBoxLayout.setSpacing(15)
        iconWidget = IconWidget(FluentIcon.SETTING)  # 图标界面
        iconWidget.setFixedSize(24, 24)
        vBoxLayout = QVBoxLayout()  # 垂直布局
        vBoxLayout.setSpacing(0)
        vBoxLayout.addWidget(BodyLabel("配置文件"))  # 文字标签
        self.hyperlink_file_label = HyperlinkFileLabel('编辑 config.json') #文件超链接标签按钮
        self.hyperlink_file_label.set_file_path("config.json")
        self.hyperlink_file_label.set_text_color(self.theme_color)
        self.hyperlink_file_label.setFont(getFont(14, weight=QFont.Normal)) # 加入字体管理系统
        vBoxLayout.addWidget(self.hyperlink_file_label)
        hBoxLayout.addWidget(iconWidget)  # 添加到布局
        hBoxLayout.addLayout(vBoxLayout)
        card.setLayout(hBoxLayout)  # 设置卡片布局
        card.setFixedHeight(70)
        self.setting_view_layout.addWidget(card)  # 添加卡片到滚动窗口
        # 退出自动保存卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.SETTING,"跳过退出保存","退出时跳过未修改的保存")
        card.setChecked(self.skip_exit_save)
        card.checkedChanged.connect(self.update_skip_exit_save)
        self.setting_view_layout.addWidget(card)
        # 配置文件保护卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.SETTING,"配置文件保护","阻止删除配置文件")
        card.setChecked(self.config_file_protect)
        card.checkedChanged.connect(self.update_config_file_protect)
        self.setting_view_layout.addWidget(card)
        # 强制退出卡片
        card = LayoutDangerButtonSettingCard(FluentIcon.SETTING,"强制退出","放弃本次保存强制退出程序","强制退出")
        card.clickedChanged.connect(self.force_quit)
        self.setting_view_layout.addWidget(card)
        # 删除配置卡片
        card = LayoutDangerButtonSettingCard(FluentIcon.SETTING,"删除配置","删除配置文件并清空配置池","删除配置")
        card.clickedChanged.connect(self.delete_config_file)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 备份标题
        self.setting_view_layout.addWidget(BodyLabel("备份"))
        # 关闭便携式环境的脱控通知卡片
        self.backup_path_card = LayoutButtonSettingCard(FluentIcon.HISTORY,"备份路径",self.backup_path,"选择路径")
        self.backup_path_card.clickedChanged.connect(self.update_backup_path)
        self.setting_view_layout.addWidget(self.backup_path_card)
        # 恢复默认备份路径卡片
        card = LayoutButtonSettingCard(FluentIcon.HISTORY,"恢复默认备份路径","恢复当前路径默认备份路径","恢复默认")
        card.clickedChanged.connect(self.restore_default_backup_path)
        self.setting_view_layout.addWidget(card)
        # 完整备份卡片
        card = LayoutSwitchButtonSettingCard(FluentIcon.HISTORY,"完整备份","同时保存文件元数据")
        card.setChecked(self.full_backup)
        card.checkedChanged.connect(self.update_full_backup)
        self.setting_view_layout.addWidget(card)
        # 备份配置卡片
        card = LayoutPrimaryButtonSettingCard(FluentIcon.HISTORY,"备份配置","立即备份当前配置文件","立即备份")
        card.clickedChanged.connect(self.backup_config_file)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 备份标题
        self.setting_view_layout.addWidget(BodyLabel("恢复"))
        # 恢复默认备份路径卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.Redo,"恢复备份","从备份中恢复","恢复")
        card.clickedChanged.connect(self.restore_backup)
        self.setting_view_layout.addWidget(card)
        # 自动重载池卡片
        card = LayoutSwitchButtonSettingCard(MetaverseFluentIcon.Redo,"自动重载","恢复备份后自动重载池")
        card.setChecked(self.auto_reload)
        card.checkedChanged.connect(self.update_auto_reload)
        self.setting_view_layout.addWidget(card)
        # 自动退出卡片
        card = LayoutSwitchButtonSettingCard(MetaverseFluentIcon.Redo,"自动退出","恢复备份后自动强制退出")
        card.setChecked(self.auto_exit)
        card.checkedChanged.connect(self.update_auto_exit)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 同步标题
        self.setting_view_layout.addWidget(BodyLabel("同步"))
        # 同步路径卡片
        card = LayoutSettingCard(MetaverseFluentIcon.DataBaseSync,"同步路径",self.APPDATA_ROAMING)
        self.setting_view_layout.addWidget(card)
        # 数据持久化卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.DataBaseSync,"同步本地","从VEM同步到本地","同步")
        card.clickedChanged.connect(self.sync_loca)
        self.setting_view_layout.addWidget(card)
        # 配置同步卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.DataBaseSync,"同步配置","从本地同步到VEM","同步")
        card.clickedChanged.connect(self.sync_config)
        self.setting_view_layout.addWidget(card)
        # 自动备份同步卡片
        card = LayoutSwitchButtonSettingCard(MetaverseFluentIcon.DataBaseSync,"自动备份同步","同步配置时自动备份旧配置")
        card.setChecked(self.auto_backup_sync)
        card.checkedChanged.connect(self.update_auto_backup_sync)
        self.setting_view_layout.addWidget(card)
        # 同步池卡片
        card = LayoutSwitchButtonSettingCard(MetaverseFluentIcon.DataBaseSync,"同步重载","同步配置时自动同步池")
        card.setChecked(self.sync_reload)
        card.checkedChanged.connect(self.update_sync_reload)
        self.setting_view_layout.addWidget(card)

        # 间隔弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 配置标题
        self.setting_view_layout.addWidget(BodyLabel("池"))
        # 落盘池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"落盘池","将配置池保存到配置文件","落盘")
        card.clickedChanged.connect(self.write_disk_pool)
        self.setting_view_layout.addWidget(card)
        # 重载池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"重载池","重新读取配置文件到池","重载")
        card.clickedChanged.connect(self.overload_disk_pool)
        self.setting_view_layout.addWidget(card)
        # 配置池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"配置池","打开配置池","打开")
        card.clickedChanged.connect(self.open_jcp_pool)
        self.setting_view_layout.addWidget(card)
        # CMD池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"CMD池","打开CMD池","打开")
        card.clickedChanged.connect(self.open_cmd_pool)
        self.setting_view_layout.addWidget(card)
        # 图标池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"图标池","打开图标池","打开")
        card.clickedChanged.connect(self.open_bip_pool)
        self.setting_view_layout.addWidget(card)
        # 图像池卡片
        card = LayoutButtonSettingCard(MetaverseFluentIcon.InternalData,"图像池","打开图像池","打开")
        card.clickedChanged.connect(self.open_bpp_pool)
        self.setting_view_layout.addWidget(card)

        # 底部弹簧
        self.setting_view_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # 滚动画布嵌入视图
        self.setting_scrollArea.setWidget(self.setting_view)
        # 嵌入滚动画布
        self.setting_vlayout.addWidget(self.setting_scrollArea)
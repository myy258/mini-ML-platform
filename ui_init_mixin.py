from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QLineEdit, QTextEdit, QTabWidget,
                             QGroupBox, QCheckBox, QScrollArea, QSpinBox,
                             QListWidget, QRadioButton, QButtonGroup, QTextBrowser)
from PyQt5.QtGui import QFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def _check_transformers():
    try:
        import transformers  # noqa: F401
        import torch         # noqa: F401
        return True
    except ImportError:
        return False

class UIInitMixin:
    def initUI(self):
        self.setWindowTitle('Mini ML Platform')
        self.setGeometry(100, 100, 1400, 800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        self.btn_open = QPushButton('\U0001f4c2 \u6253\u5f00Excel\u6587\u4ef6')
        self.btn_open.clicked.connect(self.load_excel)
        self.btn_open.setMinimumHeight(35)
        button_layout.addWidget(self.btn_open)

        self.btn_export = QPushButton('\U0001f4be \u5bfc\u51fa\u4e3aCSV')
        self.btn_export.clicked.connect(self.export_csv)
        self.btn_export.setMinimumHeight(35)
        self.btn_export.setEnabled(False)
        button_layout.addWidget(self.btn_export)

        self.btn_refresh = QPushButton('\U0001f504 \u5237\u65b0')
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_refresh.setMinimumHeight(35)
        self.btn_refresh.setEnabled(False)
        button_layout.addWidget(self.btn_refresh)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('\u641c\u7d22\u5217:'))
        self.combo_columns = QComboBox()
        self.combo_columns.setMinimumWidth(150)
        filter_layout.addWidget(self.combo_columns)
        filter_layout.addWidget(QLabel('\u5173\u952e\u8bcd:'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('\u8f93\u5165\u641c\u7d22\u5173\u952e\u8bcd...')
        self.search_input.textChanged.connect(self.filter_data)
        self.search_input.setMinimumWidth(200)
        filter_layout.addWidget(self.search_input)
        self.btn_clear_filter = QPushButton('\u2716 \u6e05\u9664\u7b5b\u9009')
        self.btn_clear_filter.clicked.connect(self.clear_filter)
        filter_layout.addWidget(self.btn_clear_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.tabs = QTabWidget()
        self.data_tab = QWidget()
        data_layout = QVBoxLayout()
        from PyQt5.QtWidgets import QTableWidget
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setStyleSheet("""
            QTableWidget { gridline-color: #d0d0d0; background-color: white; }
            QTableWidget::item { padding: 5px; }
            QHeaderView::section { background-color: #5a6c7d; color: white; padding: 8px;
                font-weight: bold; border: 1px solid #4a5c6d; }
            QHeaderView::section:hover { background-color: #6b7d8e; }
        """)
        data_layout.addWidget(self.table)
        self.data_tab.setLayout(data_layout)

        self.stats_tab = QWidget()
        self.init_stats_tab()
        self.ml_tab = QWidget()
        self.init_ml_tab()
        self.ensemble_tab = QWidget()
        self.init_ensemble_tab()
        self.viz_tab = QWidget()
        self.init_viz_tab()
        self.ai_tab = QWidget()
        self.init_ai_tab()
        self.db_tab = QWidget()
        self.init_db_tab()

        self.tabs.addTab(self.data_tab,     "\U0001f4ca Data Review")
        self.tabs.addTab(self.stats_tab,    "\U0001f4c8 Statistics Analysis")
        self.tabs.addTab(self.ml_tab,       "\U0001f916 Machine Learning")
        self.tabs.addTab(self.ensemble_tab, "\U0001f3af Ensemble Model")
        self.tabs.addTab(self.viz_tab,      "\U0001f4c9 Visualization")
        self.tabs.addTab(self.ai_tab,       "\U0001f9e0 LLM")
        self.tabs.addTab(self.db_tab,       "\U0001f5c4\ufe0f MySQL")
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.statusBar().showMessage('\u5c31\u7eea - \u8bf7\u6253\u5f00Excel\u6587\u4ef6')
        self.setStyleSheet("""
            QPushButton { background-color: #5a6c7d; color: white; border: none;
                padding: 8px 15px; border-radius: 4px; font-weight: 500; }
            QPushButton:hover { background-color: #6b7d8e; }
            QPushButton:pressed { background-color: #4a5c6d; }
            QPushButton:disabled { background-color: #d0d0d0; color: #888888; }
            QGroupBox { font-weight: 600; border: 2px solid #5a6c7d; border-radius: 5px;
                margin-top: 10px; padding-top: 10px; }
            QGroupBox::title { color: #5a6c7d; }
        """)

    def init_stats_tab(self):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    
        layout = QVBoxLayout()
    
        button_group = QHBoxLayout()
        self.btn_desc_stats = QPushButton('\U0001f4ca \u63cf\u8ff0\u6027\u7edf\u8ba1')
        self.btn_desc_stats.clicked.connect(self.show_descriptive_stats)
        button_group.addWidget(self.btn_desc_stats)
        self.btn_correlation = QPushButton('\U0001f517 \u76f8\u5173\u6027\u5206\u6790')
        self.btn_correlation.clicked.connect(self.show_correlation)
        button_group.addWidget(self.btn_correlation)
        self.btn_normality = QPushButton('\U0001f4d0 \u6b63\u6001\u5206\u5e03\u68c0\u9a8c')
        self.btn_normality.clicked.connect(self.test_normality)
        button_group.addWidget(self.btn_normality)
        self.btn_outliers = QPushButton('\U0001f3af \u5f02\u5e38\u503c\u68c0\u6d4b')
        self.btn_outliers.clicked.connect(self.detect_outliers)
        button_group.addWidget(self.btn_outliers)
        self.btn_distribution = QPushButton('\U0001f4ca \u5b57\u6bb5\u5206\u5e03\u89c2\u5bdf')
        self.btn_distribution.clicked.connect(self.show_distribution_analysis)
        button_group.addWidget(self.btn_distribution)
        button_group.addStretch()
        layout.addLayout(button_group)
    
        self.stats_result = QTextEdit()
        self.stats_result.setReadOnly(True)
        self.stats_result.setFont(QFont("Courier New", 9))
        layout.addWidget(self.stats_result)
    
        self.stats_figure = Figure(figsize=(14, 8), dpi=100)
        self.stats_canvas = FigureCanvas(self.stats_figure)
        self.stats_canvas.hide()
        layout.addWidget(self.stats_canvas)
    
        self.stats_tab.setLayout(layout)

    def init_ml_tab(self):
        main_layout = QHBoxLayout()
        control_panel = QVBoxLayout()

        task_group = QGroupBox("1\ufe0f\u20e3 \u9009\u62e9\u4efb\u52a1\u7c7b\u578b")
        task_layout = QVBoxLayout()
        self.ml_task_combo = QComboBox()
        self.ml_task_combo.addItems(['\u5206\u7c7b (Classification)', '\u56de\u5f52 (Regression)', '\u805a\u7c7b (Clustering)'])
        self.ml_task_combo.currentIndexChanged.connect(self.update_ml_models)
        task_layout.addWidget(self.ml_task_combo)
        task_group.setLayout(task_layout)
        control_panel.addWidget(task_group)

        model_group = QGroupBox("2\ufe0f\u20e3 \u9009\u62e9\u6a21\u578b")
        model_layout = QVBoxLayout()
        self.ml_model_combo = QComboBox()
        self.ml_model_combo.currentIndexChanged.connect(self.update_hyperparameters)
        model_layout.addWidget(self.ml_model_combo)
        model_group.setLayout(model_layout)
        control_panel.addWidget(model_group)

        self.param_group = QGroupBox("\u2699\ufe0f \u8d85\u53c2\u6570\u8c03\u6574 (\u53ef\u9009)")
        self.param_scroll = QScrollArea()
        self.param_scroll.setWidgetResizable(True)
        self.param_scroll.setMaximumHeight(200)
        self.param_widget = QWidget()
        self.param_layout = QVBoxLayout()
        self.param_widget.setLayout(self.param_layout)
        self.param_scroll.setWidget(self.param_widget)
        param_group_layout = QVBoxLayout()
        param_group_layout.addWidget(self.param_scroll)
        self.param_group.setLayout(param_group_layout)
        control_panel.addWidget(self.param_group)

        feature_group = QGroupBox("3\ufe0f\u20e3 \u9009\u62e9\u7279\u5f81\u5217")
        feature_layout = QVBoxLayout()
        feature_btn_layout = QHBoxLayout()
        self.btn_select_all = QPushButton('\u2713 \u5168\u9009')
        self.btn_select_all.clicked.connect(self.select_all_features)
        feature_btn_layout.addWidget(self.btn_select_all)
        self.btn_select_none = QPushButton('\u2717 \u5168\u4e0d\u9009')
        self.btn_select_none.clicked.connect(self.select_none_features)
        feature_btn_layout.addWidget(self.btn_select_none)
        feature_layout.addLayout(feature_btn_layout)
        feature_scroll = QScrollArea()
        feature_scroll.setWidgetResizable(True)
        feature_scroll.setMaximumHeight(120)
        self.feature_widget = QWidget()
        self.feature_checkboxes_layout = QVBoxLayout()
        self.feature_widget.setLayout(self.feature_checkboxes_layout)
        feature_scroll.setWidget(self.feature_widget)
        feature_layout.addWidget(feature_scroll)
        feature_group.setLayout(feature_layout)
        control_panel.addWidget(feature_group)

        target_group = QGroupBox("4\ufe0f\u20e3 \u9009\u62e9\u76ee\u6807\u5217")
        target_layout = QVBoxLayout()
        self.ml_target_combo = QComboBox()
        target_layout.addWidget(self.ml_target_combo)
        target_group.setLayout(target_layout)
        control_panel.addWidget(target_group)
        self.target_group = target_group

        cluster_group = QGroupBox("4\ufe0f\u20e3 \u805a\u7c7b\u53c2\u6570")
        cluster_layout = QHBoxLayout()
        cluster_layout.addWidget(QLabel("\u805a\u7c7b\u6570\u91cf:"))
        self.cluster_n = QSpinBox()
        self.cluster_n.setMinimum(2)
        self.cluster_n.setMaximum(20)
        self.cluster_n.setValue(3)
        cluster_layout.addWidget(self.cluster_n)
        cluster_group.setLayout(cluster_layout)
        control_panel.addWidget(cluster_group)
        self.cluster_group = cluster_group
        self.cluster_group.hide()

        model_buttons_layout = QHBoxLayout()
        self.btn_train = QPushButton('\U0001f680 \u8bad\u7ec3\u6a21\u578b')
        self.btn_train.clicked.connect(self.train_model)
        self.btn_train.setMinimumHeight(40)
        model_buttons_layout.addWidget(self.btn_train)
        self.btn_reset = QPushButton('\U0001f504 \u91cd\u7f6e\u7ed3\u679c')
        self.btn_reset.clicked.connect(self.reset_ml_results)
        self.btn_reset.setMinimumHeight(40)
        self.btn_reset.setEnabled(False)
        model_buttons_layout.addWidget(self.btn_reset)
        control_panel.addLayout(model_buttons_layout)

        model_buttons_layout2 = QHBoxLayout()
        self.btn_save_model = QPushButton('\U0001f4be \u5bfc\u51fa\u6a21\u578b')
        self.btn_save_model.clicked.connect(self.save_model)
        self.btn_save_model.setMinimumHeight(40)
        self.btn_save_model.setEnabled(False)
        model_buttons_layout2.addWidget(self.btn_save_model)
        self.btn_load_model = QPushButton('\U0001f4c2 \u5bfc\u5165\u6a21\u578b')
        self.btn_load_model.clicked.connect(self.load_model)
        self.btn_load_model.setMinimumHeight(40)
        model_buttons_layout2.addWidget(self.btn_load_model)
        control_panel.addLayout(model_buttons_layout2)
        control_panel.addStretch()

        result_layout = QVBoxLayout()
        self.ml_result = QTextEdit()
        self.ml_result.setReadOnly(True)
        self.ml_result.setFont(QFont("Courier New", 9))
        result_layout.addWidget(self.ml_result)

        main_layout.addLayout(control_panel, 1)
        main_layout.addLayout(result_layout, 2)
        self.ml_tab.setLayout(main_layout)
        self.update_ml_models()

    def init_ensemble_tab(self):
        main_layout = QHBoxLayout()
        control_panel = QVBoxLayout()

        task_group = QGroupBox("1\ufe0f\u20e3 \u9009\u62e9\u4efb\u52a1\u7c7b\u578b")
        task_layout = QVBoxLayout()
        self.ensemble_task_combo = QComboBox()
        self.ensemble_task_combo.addItems(['\u5206\u7c7b (Classification)', '\u56de\u5f52 (Regression)'])
        task_layout.addWidget(self.ensemble_task_combo)
        task_group.setLayout(task_layout)
        control_panel.addWidget(task_group)

        model_manage_group = QGroupBox("2\ufe0f\u20e3 \u6a21\u578b\u7ba1\u7406")
        model_manage_layout = QVBoxLayout()
        self.btn_add_model = QPushButton('\u2795 \u6dfb\u52a0\u6a21\u578b')
        self.btn_add_model.clicked.connect(self.add_ensemble_model)
        model_manage_layout.addWidget(self.btn_add_model)
        self.ensemble_models_list = QListWidget()
        self.ensemble_models_list.setMaximumHeight(150)
        model_manage_layout.addWidget(QLabel('\u5df2\u6dfb\u52a0\u7684\u6a21\u578b:'))
        model_manage_layout.addWidget(self.ensemble_models_list)
        self.btn_remove_model = QPushButton('\u2796 \u79fb\u9664\u9009\u4e2d\u6a21\u578b')
        self.btn_remove_model.clicked.connect(self.remove_ensemble_model)
        model_manage_layout.addWidget(self.btn_remove_model)
        model_manage_group.setLayout(model_manage_layout)
        control_panel.addWidget(model_manage_group)

        feature_group = QGroupBox("3\ufe0f\u20e3 \u9009\u62e9\u7279\u5f81\u5217")
        feature_layout = QVBoxLayout()
        feature_btn_layout = QHBoxLayout()
        self.btn_ensemble_select_all = QPushButton('\u2713 \u5168\u9009')
        self.btn_ensemble_select_all.clicked.connect(self.select_all_ensemble_features)
        feature_btn_layout.addWidget(self.btn_ensemble_select_all)
        self.btn_ensemble_select_none = QPushButton('\u2717 \u5168\u4e0d\u9009')
        self.btn_ensemble_select_none.clicked.connect(self.select_none_ensemble_features)
        feature_btn_layout.addWidget(self.btn_ensemble_select_none)
        feature_layout.addLayout(feature_btn_layout)
        feature_scroll = QScrollArea()
        feature_scroll.setWidgetResizable(True)
        feature_scroll.setMaximumHeight(120)
        self.ensemble_feature_widget = QWidget()
        self.ensemble_feature_checkboxes_layout = QVBoxLayout()
        self.ensemble_feature_widget.setLayout(self.ensemble_feature_checkboxes_layout)
        feature_scroll.setWidget(self.ensemble_feature_widget)
        feature_layout.addWidget(feature_scroll)
        feature_group.setLayout(feature_layout)
        control_panel.addWidget(feature_group)

        target_group = QGroupBox("4\ufe0f\u20e3 \u9009\u62e9\u76ee\u6807\u5217")
        target_layout = QVBoxLayout()
        self.ensemble_target_combo = QComboBox()
        target_layout.addWidget(self.ensemble_target_combo)
        target_group.setLayout(target_layout)
        control_panel.addWidget(target_group)

        ensemble_buttons_layout = QHBoxLayout()
        self.btn_train_ensemble = QPushButton('\U0001f680 \u8bad\u7ec3\u96c6\u6210\u6a21\u578b')
        self.btn_train_ensemble.clicked.connect(self.train_ensemble_model)
        self.btn_train_ensemble.setMinimumHeight(40)
        ensemble_buttons_layout.addWidget(self.btn_train_ensemble)
        self.btn_reset_ensemble = QPushButton('\U0001f504 \u91cd\u7f6e\u7ed3\u679c')
        self.btn_reset_ensemble.clicked.connect(self.reset_ensemble_results)
        self.btn_reset_ensemble.setMinimumHeight(40)
        self.btn_reset_ensemble.setEnabled(False)
        ensemble_buttons_layout.addWidget(self.btn_reset_ensemble)
        control_panel.addLayout(ensemble_buttons_layout)

        ensemble_io_layout = QHBoxLayout()
        self.btn_save_ensemble = QPushButton('\U0001f4be \u5bfc\u51fa\u96c6\u6210\u6a21\u578b')
        self.btn_save_ensemble.clicked.connect(self.save_ensemble_model)
        self.btn_save_ensemble.setMinimumHeight(40)
        self.btn_save_ensemble.setEnabled(False)
        ensemble_io_layout.addWidget(self.btn_save_ensemble)
        self.btn_load_ensemble = QPushButton('\U0001f4c2 \u5bfc\u5165\u96c6\u6210\u6a21\u578b')
        self.btn_load_ensemble.clicked.connect(self.load_ensemble_model)
        self.btn_load_ensemble.setMinimumHeight(40)
        ensemble_io_layout.addWidget(self.btn_load_ensemble)
        control_panel.addLayout(ensemble_io_layout)
        control_panel.addStretch()

        result_layout = QVBoxLayout()
        self.ensemble_result = QTextEdit()
        self.ensemble_result.setReadOnly(True)
        self.ensemble_result.setFont(QFont("Courier New", 9))
        result_layout.addWidget(self.ensemble_result)

        main_layout.addLayout(control_panel, 1)
        main_layout.addLayout(result_layout, 2)
        self.ensemble_tab.setLayout(main_layout)

    def init_viz_tab(self):
        layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel('\u56fe\u8868\u7c7b\u578b:'))
        self.viz_type_combo = QComboBox()
        self.viz_type_combo.addItems([
            '\u76f4\u65b9\u56fe (Histogram)',
            '\u6563\u70b9\u56fe+\u62df\u5408\u7ebf (Scatter+Fit)',
            '\u7b71\u7ebf\u56fe (Boxplot)',
            '\u70ed\u529b\u56fe (Heatmap)',
            '\u9884\u6d4bvs\u5b9e\u9645 (Prediction vs Actual)',
            '\u591a\u53d8\u91cf\u5bf9\u6bd4 (Multi-Variable)'
        ])
        self.viz_type_combo.currentIndexChanged.connect(self.update_viz_controls)
        control_layout.addWidget(self.viz_type_combo)

        self.viz_x_label = QLabel('X\u8f74:')
        control_layout.addWidget(self.viz_x_label)
        from widgets import CheckableComboBox
        self.viz_x_combo = CheckableComboBox()
        self.viz_x_combo.setMinimumWidth(200)
        control_layout.addWidget(self.viz_x_combo)

        self.viz_y_label = QLabel('Y\u8f74:')
        control_layout.addWidget(self.viz_y_label)
        self.viz_y_combo = CheckableComboBox()
        self.viz_y_combo.setMinimumWidth(200)
        control_layout.addWidget(self.viz_y_combo)

        self.btn_plot = QPushButton('\U0001f4ca \u751f\u6210\u56fe\u8868')
        self.btn_plot.clicked.connect(self.generate_plot)
        control_layout.addWidget(self.btn_plot)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        self.figure = Figure(figsize=(14, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.viz_tab.setLayout(layout)

    def init_ai_tab(self):
        layout = QVBoxLayout()
        transformers_available = _check_transformers()

        config_group = QGroupBox("\U0001f527 AI\u914d\u7f6e")
        config_layout = QVBoxLayout()

        model_type_layout = QHBoxLayout()
        self.ai_model_type_group = QButtonGroup()
        self.radio_transformers = QRadioButton("\u672c\u5730\u6a21\u578b (Transformers)")
        self.radio_api = QRadioButton("API\u8c03\u7528")
        self.radio_api.setChecked(True)
        self.ai_model_type_group.addButton(self.radio_transformers, 1)
        self.ai_model_type_group.addButton(self.radio_api, 2)
        model_type_layout.addWidget(self.radio_transformers)
        model_type_layout.addWidget(self.radio_api)
        model_type_layout.addStretch()
        config_layout.addLayout(model_type_layout)

        transformers_layout = QHBoxLayout()
        transformers_layout.addWidget(QLabel('\u6a21\u578b\u8def\u5f84/\u540d\u79f0:'))
        self.ai_transformers_path = QLineEdit()
        self.ai_transformers_path.setPlaceholderText(
            'HuggingFace ID \u6216\u672c\u5730\u8def\u5f84\uff0c\u4f8b\u5982: Qwen/Qwen3-0.6B  |  Qwen/Qwen3-1.7B')
        transformers_layout.addWidget(self.ai_transformers_path)
        self.btn_load_transformers = QPushButton('\u52a0\u8f7d\u6a21\u578b')
        self.btn_load_transformers.clicked.connect(self.load_transformers_model)
        transformers_layout.addWidget(self.btn_load_transformers)
        config_layout.addLayout(transformers_layout)

        hint_label = QLabel(
            '\U0001f4a1 \u672c\u5730\u6a21\u578b\u63d0\u793a: \u9996\u6b21\u52a0\u8f7d\u4f1a\u81ea\u52a8\u4ece HuggingFace \u4e0b\u8f7d\u3002'
            'Qwen3-0.6B (~1.2GB) \u9002\u5408CPU\u8fd0\u884c\uff1bQwen3-1.7B \u6548\u679c\u66f4\u597d\u4f46\u8f83\u6162\u3002'
        )
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet("color: #666; font-size: 11px; padding: 2px 0;")
        config_layout.addWidget(hint_label)

        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel('API \u5730\u5740:'))
        self.ai_api_url = QLineEdit()
        self.ai_api_url.setText('https://api.siliconflow.cn/v1/chat/completions')
        self.ai_api_url.setPlaceholderText('OpenAI \u517c\u5bb9\u63a5\u53e3\u5730\u5740')
        api_layout.addWidget(self.ai_api_url)
        config_layout.addLayout(api_layout)

        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel('API Key:'))
        self.ai_api_key = QLineEdit()
        self.ai_api_key.setPlaceholderText('\u5728 siliconflow.cn \u514d\u8d39\u6ce8\u518c\u540e\u83b7\u53d6 API Key')
        self.ai_api_key.setEchoMode(QLineEdit.Password)
        api_key_layout.addWidget(self.ai_api_key)
        config_layout.addLayout(api_key_layout)

        model_name_layout = QHBoxLayout()
        model_name_layout.addWidget(QLabel('\u6a21\u578b\u540d\u79f0:'))
        self.ai_model_name = QLineEdit()
        self.ai_model_name.setText('Qwen/Qwen3-8B')
        self.ai_model_name.setPlaceholderText('\u6a21\u578b\u540d\u79f0')
        model_name_layout.addWidget(self.ai_model_name)

        self.ai_model_preset = QComboBox()
        self.ai_model_preset.setMinimumWidth(230)
        self.ai_model_preset.addItems([
            '-- \u5feb\u901f\u9009\u62e9\u6a21\u578b --',
            'Qwen/Qwen3-8B',
            'Qwen/Qwen3-14B',
            'Qwen/Qwen2.5-7B-Instruct',
            'deepseek-ai/DeepSeek-V3',
            'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
            'THUDM/glm-4-9b-chat',
        ])
        self.ai_model_preset.currentIndexChanged.connect(self._on_model_preset_changed)
        model_name_layout.addWidget(self.ai_model_preset)
        config_layout.addLayout(model_name_layout)

        api_hint = QLabel(
            '\U0001f4a1 API\u63d0\u793a: \u4f7f\u7528\u785c\u57fa\u6d41\u52a8 (SiliconFlow) \u5e73\u53f0\uff0c\u6ce8\u518c\u5373\u9001\u514d\u8d39\u989d\u5ea6\uff0c\u652f\u6301 Qwen3\u3001DeepSeek \u7b49\u4e3b\u6d41\u6a21\u578b\u3002'
        )
        api_hint.setWordWrap(True)
        api_hint.setStyleSheet("color: #666; font-size: 11px; padding: 2px 0;")
        config_layout.addWidget(api_hint)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        chat_group = QGroupBox("\U0001f4ac \u5bf9\u8bdd (\u6a21\u578b\u5df2\u4e86\u89e3\u5f53\u524d\u6570\u636e\u548c\u6a21\u578b\u5206\u6790\u7ed3\u679c\uff0c\u53ef\u76f4\u63a5\u63d0\u95ee)")
        chat_layout = QVBoxLayout()
        self.ai_chat_history = QTextBrowser()
        self.ai_chat_history.setMinimumHeight(300)
        chat_layout.addWidget(self.ai_chat_history)

        input_layout = QHBoxLayout()
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText(
            '\u4f8b\u5982: \u6a21\u578b\u51c6\u786e\u7387\u5982\u4f55\uff1f\u6709\u4ec0\u4e48\u6539\u8fdb\u5efa\u8bae\uff1f  /  \u6570\u636e\u4e2d\u54ea\u4e9b\u7279\u5f81\u6700\u91cd\u8981\uff1f')
        self.ai_input.returnPressed.connect(self.send_ai_message)
        input_layout.addWidget(self.ai_input)
        self.btn_send = QPushButton('\u53d1\u9001')
        self.btn_send.clicked.connect(self.send_ai_message)
        self.btn_send.setMinimumHeight(40)
        input_layout.addWidget(self.btn_send)
        self.btn_clear_chat = QPushButton('\u6e05\u7a7a')
        self.btn_clear_chat.clicked.connect(self.clear_ai_chat)
        self.btn_clear_chat.setMinimumHeight(40)
        input_layout.addWidget(self.btn_clear_chat)
        chat_layout.addLayout(input_layout)
        chat_group.setLayout(chat_layout)
        layout.addWidget(chat_group)
        self.ai_tab.setLayout(layout)

    def _on_model_preset_changed(self, index):
        if index > 0:
            self.ai_model_name.setText(self.ai_model_preset.currentText())
            self.ai_model_preset.setCurrentIndex(0)

    def init_db_tab(self):
        from PyQt5.QtWidgets import (QFormLayout, QPlainTextEdit)
        layout = QVBoxLayout()

        conn_group = QGroupBox('\U0001f50c \u8fde\u63a5\u914d\u7f6e')
        form = QFormLayout()
        form.setSpacing(8)

        self.db_host_input = QLineEdit()
        self.db_host_input.setText('localhost')
        self.db_host_input.setPlaceholderText('\u4f8b\u5982: 127.0.0.1')
        form.addRow('\u4e3b\u673a Host:', self.db_host_input)

        self.db_port_input = QLineEdit()
        self.db_port_input.setText('3306')
        form.addRow('\u7aef\u53e3 Port:', self.db_port_input)

        self.db_user_input = QLineEdit()
        self.db_user_input.setPlaceholderText('\u6570\u636e\u5e93\u7528\u6237\u540d')
        form.addRow('\u7528\u6237\u540d User:', self.db_user_input)

        self.db_pass_input = QLineEdit()
        self.db_pass_input.setPlaceholderText('\u6570\u636e\u5e93\u5bc6\u7801')
        self.db_pass_input.setEchoMode(QLineEdit.Password)
        form.addRow('\u5bc6\u7801 Password:', self.db_pass_input)

        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText('\u8981\u8fde\u63a5\u7684\u6570\u636e\u5e93\u540d')
        form.addRow('\u6570\u636e\u5e93\u540d DB:', self.db_name_input)

        conn_group.setLayout(form)
        layout.addWidget(conn_group)

        btn_connect = QPushButton('\U0001f517 \u8fde\u63a5\u6570\u636e\u5e93')
        btn_connect.setMinimumHeight(38)
        btn_connect.clicked.connect(self.db_connect)
        layout.addWidget(btn_connect)

        table_group = QGroupBox('\U0001f4cb \u52a0\u8f7d\u6574\u5f20\u8868')
        table_layout = QHBoxLayout()
        table_layout.addWidget(QLabel('\u9009\u62e9\u8868:'))
        self.db_table_combo = QComboBox()
        self.db_table_combo.setMinimumWidth(240)
        table_layout.addWidget(self.db_table_combo)
        self.btn_db_load = QPushButton('\U0001f4e5 \u52a0\u8f7d\u8868\u6570\u636e')
        self.btn_db_load.setMinimumHeight(35)
        self.btn_db_load.setEnabled(False)
        self.btn_db_load.clicked.connect(self.db_load_table)
        table_layout.addWidget(self.btn_db_load)
        table_layout.addStretch()
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

        query_group = QGroupBox('\U0001f50d \u81ea\u5b9a\u4e49 SQL \u67e5\u8be2')
        query_layout = QVBoxLayout()
        self.db_query_input = QPlainTextEdit()
        self.db_query_input.setPlaceholderText(
            "\u8f93\u5165 SQL\uff0c\u4f8b\u5982:\nSELECT * FROM orders WHERE status = 'paid' LIMIT 1000"
        )
        self.db_query_input.setMaximumHeight(120)
        query_layout.addWidget(self.db_query_input)
        self.btn_db_query = QPushButton('\u25b6 \u6267\u884c\u67e5\u8be2\u5e76\u52a0\u8f7d\u5230\u5e73\u53f0')
        self.btn_db_query.setMinimumHeight(35)
        self.btn_db_query.setEnabled(False)
        self.btn_db_query.clicked.connect(self.db_run_query)
        query_layout.addWidget(self.btn_db_query)
        query_group.setLayout(query_layout)
        layout.addWidget(query_group)

        hint = QLabel('\U0001f4a1 \u6570\u636e\u52a0\u8f7d\u540e\u5c06\u81ea\u52a8\u540c\u6b65\u81f3 Data Review / Statistics / ML \u7b49\u6240\u6709\u529f\u80fd\u6a21\u5757')
        hint.setWordWrap(True)
        hint.setStyleSheet('color: #666; font-size: 11px; padding: 4px 0;')
        layout.addWidget(hint)
        layout.addStretch()
        self.db_tab.setLayout(layout)
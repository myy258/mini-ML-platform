import pandas as pd
from PyQt5.QtWidgets import QMessageBox, QApplication

class DBMixin:
    def db_connect(self):
        try:
            import pymysql
        except ImportError:
            QMessageBox.critical(
                self, '缺少依赖',
                '请先安装 pymysql:\n\npip install pymysql'
            )
            return

        host     = self.db_host_input.text().strip()
        port_str = self.db_port_input.text().strip()
        user     = self.db_user_input.text().strip()
        password = self.db_pass_input.text()
        database = self.db_name_input.text().strip()

        if not all([host, user, database]):
            QMessageBox.warning(self, '提示', '请填写主机、用户名和数据库名')
            return

        try:
            port = int(port_str) if port_str else 3306
        except ValueError:
            QMessageBox.warning(self, '提示', '端口号必须为整数')
            return

        try:
            self.statusBar().showMessage('正在连接数据库...')
            QApplication.processEvents()
            conn = pymysql.connect(
                host=host, port=port, user=user,
                password=password, database=database,
                charset='utf8mb4', connect_timeout=10
            )
            self._db_conn_params = dict(
                host=host, port=port, user=user,
                password=password, database=database,
                charset='utf8mb4'
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()

            self.db_table_combo.clear()
            self.db_table_combo.addItems(tables)
            self.btn_db_load.setEnabled(True)
            self.btn_db_query.setEnabled(True)
            self.statusBar().showMessage(
                f'✓ 已连接: {user}@{host}:{port}/{database}  |  共 {len(tables)} 张表'
            )
            QMessageBox.information(
                self, '连接成功',
                f'已连接到 {host}:{port}/{database}\n共找到 {len(tables)} 张表'
            )
        except Exception as e:
            self.statusBar().showMessage('数据库连接失败')
            QMessageBox.critical(self, '连接失败', f'无法连接数据库:\n{str(e)}')

    def db_load_table(self):
        table = self.db_table_combo.currentText()
        if not table:
            QMessageBox.warning(self, '提示', '请先连接数据库并选择表')
            return
        self._db_execute_query(f'SELECT * FROM `{table}`', label=table)

    def db_run_query(self):
        sql = self.db_query_input.toPlainText().strip()
        if not sql:
            QMessageBox.warning(self, '提示', '请输入 SQL 查询语句')
            return
        self._db_execute_query(sql, label='自定义查询')

    def _db_execute_query(self, sql, label='查询结果'):
        if not hasattr(self, '_db_conn_params'):
            QMessageBox.warning(self, '提示', '请先连接数据库')
            return
        try:
            import pymysql
            self.statusBar().showMessage('正在查询数据...')
            QApplication.processEvents()
            conn = pymysql.connect(**self._db_conn_params)
            df = pd.read_sql(sql, conn)
            conn.close()

            if df.empty:
                QMessageBox.information(self, '提示', '查询结果为空')
                self.statusBar().showMessage('查询完成，结果为空')
                return

            self.df = df
            self.filtered_df = self.df.copy()

            self.combo_columns.clear()
            self.combo_columns.addItem('全部列')
            self.combo_columns.addItems(self.df.columns.tolist())
            self.update_ml_feature_list()
            self.update_ensemble_feature_list()
            self.ml_target_combo.clear()
            self.ml_target_combo.addItems(self.df.columns.tolist())
            self.ensemble_target_combo.clear()
            self.ensemble_target_combo.addItems(self.df.columns.tolist())
            self.viz_x_combo.add_items(self.df.columns.tolist())
            self.viz_y_combo.add_items(self.df.columns.tolist())
            self.display_data(self.df)
            self.btn_export.setEnabled(True)
            self.btn_refresh.setEnabled(True)
            self.tabs.setCurrentIndex(0)

            self.statusBar().showMessage(
                f'✓ [{label}] {len(self.df)} 行 × {len(self.df.columns)} 列'
            )
        except Exception as e:
            self.statusBar().showMessage('查询失败')
            QMessageBox.critical(self, '查询失败', f'执行 SQL 失败:\n{str(e)}')

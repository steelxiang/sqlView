import npyscreen
from npyscreen import TreeData, GridColTitles

import dataService

# 全局变量，用于存储当前选中的数据库名
select_db = "test"


class MLTreeActionData(npyscreen.MLTreeAction):
    """
    自定义树操作类，用于处理树节点的展开、折叠以及查询表数据。
    """

    def actionHighlighted(self, line, key_press):
        """
        当选中树节点时触发的操作。

        :param line: 选中的树节点
        :param key_press: 按键事件
        """
        global select_db
        if line.has_children():  # 如果节点有子节点
            select_db = line.get_content_for_display()  # 更新当前数据库名
            if line.expanded:  # 如果节点已展开
                self.h_collapse_tree("")  # 折叠节点
            else:  # 否则
                self.h_expand_tree("")  # 展开节点
        else:  # 如果节点没有子节点，说明是一个表
            table = line.get_content_for_display()  # 获取表名
            select_db = line.get_parent().get_content_for_display()  # 获取当前数据库名
            sql = f'SELECT * FROM {select_db}.{table}'  # 构造SQL查询语句
            try:
                col, dt = dataService.get_data(self.parent.cursor, sql)  # 执行查询
                rows = [list(e) for e in dt]  # 将结果转换为列表形式
                self.parent.table_data.updateData(col, rows)  # 更新表格数据
            except Exception as ex:
                npyscreen.notify_confirm(str(ex))  # 显示错误信息


class MyGrid(GridColTitles):
    """
    自定义表格类，用于展示查询结果。
    """

    def updateData(self, title, data):
        """
        更新表格数据。

        :param title: 列标题
        :param data: 数据行
        """
        self.col_titles = title
        self.values = data
        self.update(True)  # 刷新表格

    def showValue(self, inpt):
        """
        当单元格内容过长时，通过回车键弹出对话框显示完整内容。

        :param inpt: 输入事件
        """
        v = self.values[self.edit_cell[0]][self.edit_cell[1]]  # 获取当前单元格内容
        npyscreen.notify_confirm(v)  # 弹出对话框显示内容

    def set_up_handlers(self):
        """
        设置事件处理器，绑定回车键事件。
        """
        super(GridColTitles, self).set_up_handlers()  # 调用父类方法
        self.handlers.update({10: self.showValue})  # 绑定回车键到showValue方法


class DataForm(npyscreen.ActionFormV2):
    """
    主窗体类，用于展示数据库和表结构，以及执行SQL查询。
    """
    OK_BUTTON_TEXT = "Exec"  # 确定按钮文本
    CANCEL_BUTTON_TEXT = "Exit"  # 取消按钮文本

    def create(self):
        """
        初始化窗体。
        """
        self.name = "DATA"  # 窗体名称
        self.data = [['a', 'b'], ['c', 'd']]  # 初始表格数据（占位）
        self.title = ['1', '2']  # 初始表格列标题（占位）
        self.root = TreeData(content="root")  # 创建根节点

        self.db_list = self.add(MLTreeActionData, name="Database List:", values=self.root, rely=1, relx=1,
                                max_width=30)  # 添加数据库树

        # 添加表数据展示区
        self.table_data = self.add(MyGrid, name="Table Data:", values=self.data, col_titles=self.title,
                                   rely=1, relx=40, column_width=10, max_height=25, always_show_cursor=True)

        # 添加SQL输入区
        self.sql_input = self.add(npyscreen.MultiLineEditableBoxed, name="SQL Input:",
                                  rely=28, relx=40, scroll_exit=True, editable=True, contained_widget_arguments={
                'color': "WARNING",
                'widgets_inherit_color': True,
            })

    def on_cancel(self):
        """
        退出窗体时触发的操作。
        """
        self.parentApp.switchForm(None)

    def on_ok(self):
        """
        点击确定按钮时触发的操作，执行SQL查询并更新表格数据。
        """
        global select_db
        try:
            # 选择当前数据库
            self.cursor.execute(f"USE {select_db}")
            sql = "\n".join(self.sql_input.get_values())  # 获取SQL输入区内容并拼接成完整SQL语句
            col, dt = dataService.get_data(self.cursor, sql)  # 执行查询
            rows = [list(e) for e in dt]  # 将结果转换为列表形式
            self.table_data.updateData(col, rows)  # 更新表格数据
        except Exception as ex:
            npyscreen.notify_confirm(str(ex))  # 显示错误信息

    def initDatabase(self):
        """
        初始化数据库树，加载数据库和表信息。
        """
        self.checkConnect()  # 检查数据库连接
        databases = dataService.show_databases(self.cursor)  # 获取数据库列表
        for row in databases:
            db = self.root.new_child(row[0])  # 创建数据库节点
            tables = dataService.show_tables(self.cursor, db.get_content_for_display())  # 获取表列表
            for tb in tables:
                db.new_child(tb[0])  # 创建表节点
        self.db_list.h_collapse_all("")  # 折叠所有节点

    def checkConnect(self):
        """
        检查数据库连接，并创建数据库游标。
        """
        host = self.parentApp.host  # 获取数据库主机地址
        port = self.parentApp.port  # 获取数据库端口号
        username = self.parentApp.username  # 获取数据库用户名
        password = self.parentApp.password  # 获取数据库密码
        self.cursor = dataService.create_connection(host, port, username, password)  # 创建数据库连接
        if isinstance(self.cursor, str):  # 如果连接失败，返回错误信息
            npyscreen.notify_confirm(self.cursor)


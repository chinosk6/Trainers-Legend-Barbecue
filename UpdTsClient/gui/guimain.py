import json
import re
import sys
import os
import time
from hashlib import md5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, QDir
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QStyleFactory, QDirModel, QFileDialog, \
    QTreeWidgetItem, QStyle, QMenu, QInputDialog
from .qtui.ui_import import MainUI, MainTabUI, FilePreviewUI
import ctypes
from threading import Thread
from .user_config import user_config
from . import api as uapi
from . import mtools
import webbrowser

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
except:
    pass

local_language = ctypes.windll.kernel32.GetUserDefaultUILanguage()
sChinese_lang_id = [0x0004, 0x0804, 0x1004]  # zh-Hans, zh-CN, zh-SG
tChinese_lang_id = [0x0404, 0x0c04, 0x1404, 0x048E]  # zh-TW, zh-HK, zh-MO, zh-yue-HK


translate = QtCore.QCoreApplication.translate

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = MainUI()
        self.ui.setupUi(self)


class UIChange(QObject):
    show_msgbox_signal = QtCore.pyqtSignal(str, str)
    set_refresh_action_signal = QtCore.pyqtSignal(bool)
    update_server_files_tree_signal = QtCore.pyqtSignal()
    build_different_file_view_signal = QtCore.pyqtSignal()
    set_bar_value_signal = QtCore.pyqtSignal(int)
    set_bar_visibility_signal = QtCore.pyqtSignal(bool)
    set_label_log_text_signal = QtCore.pyqtSignal(str)
    refresh_all_ui_signal = QtCore.pyqtSignal()
    show_preview_window_signal = QtCore.pyqtSignal(str, str, str, str, str)


    def __init__(self):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        QApplication.setStyle(QStyleFactory.create("Fusion"))  # ['windowsvista', 'Windows', 'Fusion']
        super(UIChange, self).__init__()
        self.app = QApplication(sys.argv)

        self.trans = QtCore.QTranslator()
        self.trans2 = QtCore.QTranslator()
        self.trans3 = QtCore.QTranslator()
        self.trans4 = QtCore.QTranslator()
        self.load_i18n()

        self.window = QMainWindow()
        self.window.setWindowIcon(QtGui.QIcon(":/img/jibai.ico"))
        self.ui = MainUI()
        self.ui.setupUi(self.window)

        self.window_main_tab = QMainWindow()
        self.window_main_tab.setWindowIcon(QtGui.QIcon(":/img/jibai.ico"))
        self.ui_main_tab = MainTabUI()
        self.ui_main_tab.setupUi(self.window_main_tab)

        self.window_preview = QMainWindow(self.window_main_tab)
        self.window_main_tab.setWindowIcon(QtGui.QIcon(":/img/jibai.ico"))
        self.ui_preview = FilePreviewUI()
        self.ui_preview.setupUi(self.window_preview)

        self.model_localfile = QDirModel(self.ui_main_tab)
        self.model_localfile.setReadOnly(True)
        self.model_localfile.setSorting(QDir.Name | QDir.IgnoreCase | QDir.Type)
        self.ui_main_tab.progressBar.hide()

        self.server_file_data = []
        self.local_file_data = {}
        self.need_update_files = []
        self.need_add_files = []
        self.need_delete_files = []
        self.commit_list = []
        self.reg_clicked_connects()
        self.signal_reg()

        self._server_load_finished = False

    def load_i18n(self):
        if local_language in sChinese_lang_id:
            self.trans.load(":/trans/file_preview_ui.qm")
            self.trans2.load(":/trans/guimain.qm")
            self.trans3.load(":/trans/main_tab_ui.qm")
            self.trans4.load(":/trans/main_ui.qm")

            self.app.installTranslator(self.trans)
            self.app.installTranslator(self.trans2)
            self.app.installTranslator(self.trans3)
            self.app.installTranslator(self.trans4)

    def reg_clicked_connects(self):  # 点击回调注册
        self.ui.pushButton_ok.clicked.connect(self.user_login)
        self.ui_main_tab.pushButton_set_file_root.clicked.connect(self.update_file_root)
        self.ui_main_tab.treeWidget_different.clicked.connect(self.different_file_view_onclick)
        self.ui_main_tab.treeWidget_different.customContextMenuRequested.connect(self.diff_file_menu)
        self.ui_main_tab.treeWidget_commit.customContextMenuRequested.connect(self.commit_menu)
        self.ui_main_tab.treeWidget_ignore.customContextMenuRequested.connect(self.ignore_menu)
        self.ui_main_tab.treeWidget_server_files.customContextMenuRequested.connect(self.server_file_menu)
        self.ui_main_tab.treeView_local_files.customContextMenuRequested.connect(self.local_file_menu)
        self.ui_main_tab.actionRefresh.triggered.connect(self.refresh_all_ui)
        self.ui_main_tab.actionPull_From_Server.triggered.connect(self.pull_data_from_server)
        self.ui_main_tab.pushButton_commit.clicked.connect(self.commit_data_to_server)
        self.ui_main_tab.actionAbout.triggered.connect(lambda *x: webbrowser.open(
            "https://github.com/chinosk6/Trainers-Legend-Barbecue"
        ))
        self.ui_main_tab.actionChange_Token.triggered.connect(self.change_token)

    def signal_reg(self):  # 信号槽注册
        self.show_msgbox_signal.connect(self.show_message_box)
        self.set_refresh_action_signal.connect(self.set_refresh_stat)
        self.update_server_files_tree_signal.connect(self.update_server_files_tree)
        self.build_different_file_view_signal.connect(self.build_different_file_view)
        self.set_bar_value_signal.connect(self.set_bar_value)
        self.set_label_log_text_signal.connect(self.set_label_log_text)
        self.set_bar_visibility_signal.connect(lambda x: self.ui_main_tab.progressBar.setVisible(x))
        self.refresh_all_ui_signal.connect(self.refresh_all_ui)
        self.show_preview_window_signal.connect(self.show_preview_window)

    def show_message_box(self, title, text, btn=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No):
        return QtWidgets.QMessageBox.information(self.window, title, text, btn)

    def set_bar_value(self, value: int):
        self.ui_main_tab.progressBar.setValue(value)

    def set_label_log_text(self, text: str):
        self.ui_main_tab.label_log.setText(text)

    def set_refresh_stat(self, enable: bool):
        self.ui_main_tab.actionRefresh.setEnabled(enable)
        self.ui_main_tab.actionPlease_Wait.setVisible(False if enable else True)

    def change_token(self):
        text, ok = QInputDialog.getText(self.window_main_tab, translate("MainWindow", "Update token"),
                                        translate("MainWindow", "Input your new token. (Left blank will be modified randomly)"))
        if ok:
            new_token = uapi.update_token(text.strip())
            if new_token:
                self.show_message_box(translate("MainWindow", "Success"),
                                      translate("MainWindow", "Your new token is:") + f"\n{new_token}")
            else:
                self.show_message_box(translate("MainWindow", "Failed"),
                                      translate("MainWindow", "Update token failed."))

    def user_login(self, *args):
        try:
            token = self.ui.lineEdit_token.text().strip()
            api_adderss = self.ui.lineEdit_api.text().strip()
            user_config.set_api_endpoint(api_adderss)
            data = json.loads(uapi.get_userinfo(token))["data"]
            if data.get("permission", 0) < 2:
                self.show_message_box(translate("MainWindow", "Login Failed"),
                                      translate("MainWindow", "Permission Denied"))
                return
            user_config.set_userinfo(
                data["uid"], data["name"], data["token"], data["permission"]
            )
            self.window.close()
            self.show_maintab_window()
        except BaseException as e:
            self.show_message_box(translate("MainWindow", "Login Failed"), repr(e))

    def update_file_root(self, *args, update_tree=True):
        folder_path = QFileDialog.getExistingDirectory(self.ui_main_tab,
                                                       translate("MainWindow", "Choose root folder"))
        if folder_path == "":
            self.show_message_box("Error", translate("MainWindow", "Please select a folder."))
            return
        user_config.config["file_root"] = folder_path
        user_config.save_config()
        if update_tree:
            self.ui_main_tab.lineEdit_file_root.setText(folder_path)
            self.refresh_all_ui()
        return folder_path

    def update_local_files_tree(self):
        file_root = user_config.config.get("file_root", "")
        if file_root == "":
            file_root = self.update_file_root(update_tree=False)
            if file_root == "":
                return
        self.ui_main_tab.lineEdit_file_root.setText(file_root)
        self.ui_main_tab.treeView_local_files.setModel(self.model_localfile)
        self.ui_main_tab.treeView_local_files.setRootIndex(self.model_localfile.index(file_root))

    def start_sync_server_files(self):
        def _():
            try:
                # self.set_refresh_action_signal.emit(False)
                self._server_load_finished = False
                data = json.loads(uapi.get_server_all_files())
                self.server_file_data = data.get("data", [])
                self._server_load_finished = True
            except BaseException as e:
                self.show_msgbox_signal.emit(translate("MainWindow", "Sync Server Files Failed"), repr(e))
            finally:
                self.update_server_files_tree_signal.emit()
                # self.set_refresh_action_signal.emit(True)
        Thread(target=_).start()

    @staticmethod
    def tree_item_generate(parent, data: list):
        item = QTreeWidgetItem(parent)
        for n, i in enumerate(data):
            if not isinstance(i, tuple):
                item.setText(n, str(i))
            else:
                item.setText(n, str(i[0]))
                for nm, k in enumerate(i[1:]):
                    item.setData(n, 114 + nm, str(k))
        return item

    @staticmethod
    def get_file_md5(file_name, remove_starts_zero=False):
        try:
            md = md5()
            with open(file_name, "rb") as f:
                block = f.read(1024)
                while block:
                    md.update(block)
                    block = f.read(1024)
            ret = md.hexdigest()
            if remove_starts_zero:
                while ret[0] == "0":
                    ret = ret[1:]
            return ret
        except BaseException:
            return None

    def build_path_tree_view(self, tree_widget, file_lst: list, header_labels: list, file_lst_items: list):
        """
        filename 为 file_list 内的必需项, file_lst_items 不用加 filename
        """
        tree_widget.setHeaderLabels(header_labels)
        tree_widget.header().setDefaultSectionSize(300)
        root_trees = [{} for _ in range(128)]
        do_after = []

        for i in file_lst:
            filename: str = i["filename"]
            if "updateTime" in i:
                if isinstance(i["updateTime"], int):
                    i["updateTime"] = mtools.timestamp_to_text(i["updateTime"])

            if filename.startswith("/"):
                filename = filename[1:]
            path, filename = os.path.split(filename)
            if path == "":
                do_after.append((self.tree_item_generate,
                                 (tree_widget,
                                  [(filename, f"/{filename}", "file")] + [i[k] for k in file_lst_items])))
            else:
                last_parent = None
                now_path = ""
                for n, p in enumerate(path.split("/")):
                    now_path = f"{now_path}/{p}"
                    root_in_lst = root_trees[n].get(now_path, None)
                    if root_in_lst is None:
                        item = self.tree_item_generate(tree_widget if last_parent is None else last_parent,
                                                       [(p, now_path, "folder")])
                        item.setIcon(0, QApplication.style().standardIcon(QStyle.StandardPixmap(38)))
                        root_trees[n][now_path] = item
                        last_parent = item
                    else:
                        last_parent = root_in_lst
                do_after.append((self.tree_item_generate,
                                 (tree_widget if last_parent is None else last_parent,
                                  [(filename, f"{now_path}/{filename}", "file")] + [i[k] for k in file_lst_items])))
        for func, args in do_after:
            func(*args).setIcon(0, QApplication.style().standardIcon(QStyle.StandardPixmap(25)))

    def update_server_files_tree(self):
        self.build_path_tree_view(self.ui_main_tab.treeWidget_server_files,
                                  self.server_file_data, ["Name", "User", "Time", "Description"],
                                  ["updateUserName", "updateTime", "description"])


    def build_local_file_list(self):
        file_root = user_config.config.get("file_root", None)
        if file_root is None:
            self.show_message_box("Error", translate("MainWindow", "Please set your file root."))
            return

        def _():
            self.local_file_data = {}
            for root, dirs, files in os.walk(file_root):
                for f in files:
                    full_name = os.path.normpath(os.path.join(root, f)).replace("\\", "/")
                    relative_path = full_name.replace(file_root, "")
                    self.local_file_data[relative_path] = self.get_file_md5(full_name, True)
            self.build_different_file_view_signal.emit()
            self.ui_main_tab.actionRefresh.setEnabled(True)
            self.ui_main_tab.actionPlease_Wait.setVisible(False)
            self.ui_main_tab.label_log.setText("")
        Thread(target=_).start()

    def build_different_file_view(self, *args):
        def recheck_file_list(file_list: list):
            ret = []
            for i in file_list:
                add_flg = True
                for ic in self.commit_list:
                    if ic in i:
                        add_flg = False
                        break
                if not add_flg:
                    continue
                for ic in user_config.ignore_list:
                    if ic in i:
                        add_flg = False
                        break
                if add_flg:
                    ret.append(i)
            return ret

        if not self.server_file_data:
            if not self._server_load_finished:
                self.ui_main_tab.label_log.setText("Please wait a minute...")

                def _():
                    while not self._server_load_finished:
                        time.sleep(1)
                    self.build_different_file_view_signal.emit()
                Thread(target=_).start()
                return

        server_files = {}
        self.need_add_files.clear()
        self.need_update_files.clear()
        self.need_delete_files.clear()
        for i in self.server_file_data:
            file_hash = i["hash"]
            filename: str = i["filename"]
            server_files[filename] = file_hash
        for local_name in self.local_file_data:
            if local_name not in server_files:  # 增加文件
                self.need_add_files.append(local_name)
            else:
                local_hash = self.local_file_data[local_name]
                server_hash = server_files[local_name]
                if local_hash != server_hash:  # 更新文件
                    self.need_update_files.append(local_name)
                server_files.pop(local_name)
        for server_name in server_files:  # 删除文件
            self.need_delete_files.append(server_name)

        tree_file_list = []
        for i in recheck_file_list(self.need_add_files):
            tree_file_list.append({"filename": i, "type": "Add"})
        for i in recheck_file_list(self.need_delete_files):
            tree_file_list.append({"filename": i, "type": "Delete"})
        for i in recheck_file_list(self.need_update_files):
            tree_file_list.append({"filename": i, "type": "Modified"})
        self.ui_main_tab.treeWidget_different.clear()
        self.build_path_tree_view(self.ui_main_tab.treeWidget_different, tree_file_list, ["Name", "Type"], ["type"])
        self.update_ignore_tree(build_view=False)
        self.ui_main_tab.label_log.setText("")

    def diff_file_menu(self):
        self.ui_main_tab.treeWidget_different.contextMenu = QMenu()
        action1 = self.ui_main_tab.treeWidget_different.contextMenu.addAction(
            translate("MainWindow", "Add to commit list.")
        )
        action2 = self.ui_main_tab.treeWidget_different.contextMenu.addAction(
            translate("MainWindow", "Add to ignore list.")
        )
        action1.triggered.connect(self.different_file_add_commit)
        action2.triggered.connect(self.different_file_add_ignore)
        self.ui_main_tab.treeWidget_different.contextMenu.popup(QCursor.pos())
        self.ui_main_tab.treeWidget_different.contextMenu.show()

    def commit_menu(self):
        self.ui_main_tab.treeWidget_commit.contextMenu = QMenu()
        action1 = self.ui_main_tab.treeWidget_commit.contextMenu.addAction(translate("MainWindow", "Cancel Commit"))
        action1.triggered.connect(self.remove_commit_list)
        self.ui_main_tab.treeWidget_commit.contextMenu.popup(QCursor.pos())
        self.ui_main_tab.treeWidget_commit.contextMenu.show()

    def ignore_menu(self):
        self.ui_main_tab.treeWidget_ignore.contextMenu = QMenu()
        action1 = self.ui_main_tab.treeWidget_ignore.contextMenu.addAction(translate("MainWindow", "Cancel Ignore"))
        action1.triggered.connect(self.remove_ignore_list)
        self.ui_main_tab.treeWidget_ignore.contextMenu.popup(QCursor.pos())
        self.ui_main_tab.treeWidget_ignore.contextMenu.show()

    def server_file_menu(self):
        self.ui_main_tab.treeWidget_server_files.contextMenu = QMenu()
        action1 = self.ui_main_tab.treeWidget_server_files.contextMenu.addAction(translate("MainWindow", "File Preview"))
        action2 = self.ui_main_tab.treeWidget_server_files.contextMenu.addAction(translate("MainWindow", "File Download"))
        action1.triggered.connect(self.preview_server_file)
        action2.triggered.connect(self.download_server_file)
        self.ui_main_tab.treeWidget_server_files.contextMenu.popup(QCursor.pos())
        self.ui_main_tab.treeWidget_server_files.contextMenu.show()

    def local_file_menu(self):
        self.ui_main_tab.treeView_local_files.contextMenu = QMenu()
        action1 = self.ui_main_tab.treeView_local_files.contextMenu.addAction(translate("MainWindow", "Open Folder"))
        action1.triggered.connect(self.local_open_folder)
        self.ui_main_tab.treeView_local_files.contextMenu.popup(QCursor.pos())
        self.ui_main_tab.treeView_local_files.contextMenu.show()

    def local_open_folder(self):
        selected_indexs = self.ui_main_tab.treeView_local_files.selectedIndexes()
        if len(selected_indexs) <= 0:
            return
        selected_index = selected_indexs[0]
        data = self.model_localfile.filePath(selected_index)
        if os.path.isfile(data):
            os.system(f'explorer /select, {os.path.realpath(data)}')
        elif os.path.isdir(data):
            os.startfile(data)

    def preview_server_file(self):
        selected = self.get_file_selected_list(self.ui_main_tab.treeWidget_server_files, itor_subfiles=False)
        if len(selected) <= 0:
            return
        file_name, file_type = selected[0]
        if file_type != "file":
            self.show_message_box("Tip", translate("MainWindow", "Please select a file."))
            return
        fname_re = re.compile(r"(\.txt|\.json|\.yml|\.yaml|\.c|\.cpp|\.h|\.hpp|\.py|\.cs)$", re.I)
        if not fname_re.findall(file_name):
            res = self.show_message_box("Warning",
                                        translate("MainWindow", "This file may not support preview, continue?"))
            if res != QtWidgets.QMessageBox.Yes:
                return

        file_hash = self.get_server_file_hash(file_name)
        if file_hash is None:
            self.show_message_box("Error", translate("MainWindow", "Get file hash failed."))
            return

        def _():
            try:
                self.set_label_log_text_signal.emit(translate("MainWindow", "Downloading file..."))

                response = uapi.get_file(file_name, file_hash)
                if response.status_code != 200:
                    self.show_msgbox_signal.emit("Error", f"Get file failed:\n{response.text}")
                    return
                file_bytes = response.content
                try:
                    file_text = file_bytes.decode("utf8")
                except BaseException as e:
                    file_text = f"Can't preview this file.\n{e}"
                self.set_label_log_text_signal.emit("")
                for i in self.server_file_data:
                    if i["filename"] == file_name:
                        self.show_preview_window_signal.emit(i.get("updateUserName", ""), str(i.get("updateTime", 0)),
                                                             i.get("hash", ""), i.get("description", ""), file_text)
                        return
                self.show_preview_window_signal.emit("", "0", "", "", file_text)
            except BaseException as e:
                self.show_msgbox_signal.emit("Exception Occurred", repr(e))
        Thread(target=_).start()

    def download_server_file(self, *args):
        selected = self.get_file_selected_list(self.ui_main_tab.treeWidget_server_files, itor_subfiles=False)
        if len(selected) <= 0:
            return
        file_name, file_type = selected[0]
        if file_type != "file":
            self.show_message_box("Tip", translate("MainWindow", "Please select a file."))
            return
        file_hash = self.get_server_file_hash(file_name)
        if file_hash is None:
            self.show_message_box("Error", translate("MainWindow", "Get file hash failed."))
            return
        save_path = QFileDialog.getSaveFileName(self.ui_main_tab, "Save File", os.path.split(file_name)[1])[0]
        if save_path == "":
            return

        def _():
            try:
                self.set_label_log_text_signal.emit(translate("MainWindow", "Downloading file..."))

                response = uapi.get_file(file_name, file_hash)
                if response.status_code != 200:
                    self.show_msgbox_signal.emit("Error", f"Get file failed:\n{response.text}")
                    return
                with open(save_path, "wb") as f:
                    f.write(response.content)

                self.set_label_log_text_signal.emit("")
            except BaseException as e:
                self.show_msgbox_signal.emit("Exception Occurred", repr(e))
        Thread(target=_).start()


    def append_from_different_lst(self, target_list: list):
        for name, ftype in self.get_file_selected_list():
            if ftype == "folder":
                name += "/"
            continue_flg = False
            for i in target_list:
                if name in i:
                    continue_flg = True
                    break
            if not continue_flg:
                target_list.append(name)

    def different_file_add_commit(self, *args):
        self.append_from_different_lst(self.commit_list)
        self.update_commit_tree()

    def different_file_add_ignore(self, *args):
        self.append_from_different_lst(user_config.ignore_list)
        user_config.save_config()
        self.update_ignore_tree()

    def remove_commit_list(self, *args):
        rm_lst = self.get_file_selected_list(self.ui_main_tab.treeWidget_commit)
        for i in rm_lst:
            name = i[0]
            if name in self.commit_list:
                self.commit_list.remove(name)
        self.update_commit_tree()

    def remove_ignore_list(self, *args):
        rm_lst = self.get_file_selected_list(self.ui_main_tab.treeWidget_ignore)
        for i in rm_lst:
            name = i[0]
            if name in user_config.ignore_list:
                user_config.ignore_list.remove(name)
        user_config.save_config()
        self.update_ignore_tree()

    def get_file_selected_list(self, target_widget=None, itor_subfiles=True):
        if target_widget is None:
            target_widget = self.ui_main_tab.treeWidget_different
        ret = []
        for i in target_widget.selectedIndexes():
            if i.column() != 0:
                continue
            file_name = i.model().data(i, 114)
            file_type = i.model().data(i, 115)

            if itor_subfiles and (file_type == "folder"):
                iterator = QtWidgets.QTreeWidgetItemIterator(target_widget)
                while iterator.value():
                    if iterator.value().data(0, 115) == "file":
                        curr_name = iterator.value().data(0, 114)
                        if file_name in curr_name:
                            ret.append((curr_name, "file"))
                    iterator.__iadd__(1)

            ret.append((file_name, file_type))  # (fileName, fileType[file, folder])
        return ret

    def different_file_view_onclick(self, mindex: QtCore.QModelIndex):
        pass

    def update_commit_tree(self, build_diff_tree=True):
        self.ui_main_tab.treeWidget_commit.clear()
        tree_file_list = []
        for m in self.need_add_files:
            for i in self.commit_list:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Add"})
        for m in self.need_delete_files:
            for i in self.commit_list:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Delete"})
        for m in self.need_update_files:
            for i in self.commit_list:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Modified"})
        self.build_path_tree_view(self.ui_main_tab.treeWidget_commit, tree_file_list,
                                  ["Name", "Type"], ["type"])
        if build_diff_tree:
            self.build_different_file_view()

    def update_ignore_tree(self, build_view=True):
        self.ui_main_tab.treeWidget_ignore.clear()
        tree_file_list = []
        for i in user_config.ignore_list:
            for m in self.need_add_files:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Add"})
            for m in self.need_delete_files:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Delete"})
            for m in self.need_update_files:
                if i in m:
                    tree_file_list.append({"filename": i, "type": "Modified"})
        self.build_path_tree_view(self.ui_main_tab.treeWidget_ignore, tree_file_list,
                                  ["Name", "Type"], ["type"])
        if build_view:
            self.build_different_file_view()

    def show_maintab_window(self):
        self.window_main_tab.setWindowTitle(f"{self.window_main_tab.windowTitle()} - {user_config.username}")

        self.window_main_tab.show()
        self.refresh_all_ui()

    def refresh_all_ui(self, *args):
        self.ui_main_tab.actionPlease_Wait.setVisible(True)
        self.ui_main_tab.actionRefresh.setEnabled(False)
        self.ui_main_tab.label_log.setText(translate("MainWindow", "Synchronizing data, please wait"))

        self.ui_main_tab.treeWidget_ignore.clear()
        self.ui_main_tab.treeWidget_commit.clear()
        self.ui_main_tab.treeWidget_different.clear()
        self.ui_main_tab.treeWidget_server_files.clear()
        self.update_local_files_tree()
        self.start_sync_server_files()
        self.build_local_file_list()
        self.update_commit_tree(build_diff_tree=False)

    def get_server_file_hash(self, file_name: str):
        for i in self.server_file_data:
            if i["filename"] == file_name:
                return i["hash"]
        return None

    def pull_data_from_server(self, *args):
        result = self.show_message_box("Pull Data",
                                       translate("MainWindow", "This will overwrite your local data. "
                                                               "Do you want to continue?"))
        if result != QtWidgets.QMessageBox.Yes:
            return
        self.commit_list.clear()
        iterator = QtWidgets.QTreeWidgetItemIterator(self.ui_main_tab.treeWidget_different)
        sync_file_list = []
        while iterator.value():
            if iterator.value().data(0, 115) == "file":
                edit_type = iterator.value().data(1, 0)
                if edit_type not in ["Delete", "Modified"]:
                    continue
                file_name = iterator.value().data(0, 114)
                file_hash = self.get_server_file_hash(file_name)
                sync_file_list.append((file_name, file_hash))
            iterator.__iadd__(1)
        file_root = user_config.config.get("file_root", None)
        if file_root is None:
            return

        def _():
            tlen = len(sync_file_list)
            count = 0
            self.set_bar_visibility_signal.emit(True)
            for i in sync_file_list:
                f_name, f_hash = i
                response = uapi.get_file(f_name, f_hash)
                if response.status_code != 200:
                    self.set_label_log_text_signal.emit(f"Get file: {f_name} failed ({response.status_code}).")
                    continue
                full_name = f"{file_root}/{f_name}"
                f_dir = os.path.split(full_name)[0]
                if not os.path.isdir(f_dir):
                    os.makedirs(f_dir)
                with open(full_name, "wb") as f:
                    f.write(response.content)
                count += 1
                self.set_bar_value_signal.emit(int(count / tlen * 100))
            self.set_bar_visibility_signal.emit(False)
            self.show_msgbox_signal.emit("Tip", translate("MainWindow", "Pull finished."))
            if tlen > 0:
                self.refresh_all_ui_signal.emit()
        Thread(target=_).start()

    def commit_data_to_server(self, *args):
        result = self.show_message_box("Commit", translate("MainWindow", "Are you sure?"))
        if result != QtWidgets.QMessageBox.Yes:
            return
        description = self.ui_main_tab.textEdit_commit_desc.toPlainText().strip()
        if not description:
            self.show_message_box("Tip", translate("MainWindow", "Please input your description."))
            return
        iterator = QtWidgets.QTreeWidgetItemIterator(self.ui_main_tab.treeWidget_commit)
        upload_file_list = []
        delete_file_list = []
        while iterator.value():
            if iterator.value().data(0, 115) == "file":
                edit_type = iterator.value().data(1, 0)
                file_name = iterator.value().data(0, 114)
                if edit_type in ["Add", "Modified"]:
                    upload_file_list.append(file_name)
                else:
                    delete_file_list.append(file_name)
            iterator.__iadd__(1)
        file_root = user_config.config.get("file_root", None)
        if file_root is None:
            return

        def _():
            tlen = len(upload_file_list) + len(delete_file_list)
            count = 0
            self.set_bar_visibility_signal.emit(True)
            for i in upload_file_list:
                full_name = f"{file_root}/{i}"
                response = uapi.upload_file(i, full_name, description)
                if isinstance(response, BaseException):
                    self.show_msgbox_signal.emit("Exception Occurred", repr(response))
                else:
                    if response.status_code != 200:
                        self.set_label_log_text_signal.emit(f"Upload file: {i} failed ({response.status_code}).")
                count += 1
                self.set_bar_value_signal.emit(int(count / tlen * 100))

            for i in delete_file_list:
                response = uapi.delete_file(i)
                if isinstance(response, BaseException):
                    self.show_msgbox_signal.emit("Exception Occurred", repr(response))
                else:
                    if response.status_code != 200:
                        self.set_label_log_text_signal.emit(f"Delete file: {i} failed ({response.status_code}).")
                count += 1
                self.set_bar_value_signal.emit(int(count / tlen * 100))

            self.set_bar_visibility_signal.emit(False)
            self.show_msgbox_signal.emit("Tip", translate("MainWindow", "Commit finished."))
            if tlen > 0:
                self.commit_list.clear()
                self.refresh_all_ui_signal.emit()
        Thread(target=_).start()

    def show_preview_window(self, username: str, commit_time: str, file_hash: str, description: str, text: str):
        self.ui_preview.lineEdit_username.setText(username)
        self.ui_preview.lineEdit_hash.setText(file_hash)
        try:
            time_show = mtools.timestamp_to_text(int(commit_time))
        except:
            time_show = commit_time
        self.ui_preview.lineEdit_time.setText(time_show)
        self.ui_preview.textEdit_desc.setText(description)
        self.ui_preview.textEdit_file.setText(text)
        self.window_preview.show()

    def show_main_window(self):
        self.window.show()
        self.ui.lineEdit_api.setText(user_config.api_endpoint)
        self.ui.lineEdit_token.setText(user_config.token)

    def ui_run_main(self):
        self.show_main_window()
        exit_code = self.app.exec_()
        sys.exit(exit_code)
        # os._exit(self.app.exec_())

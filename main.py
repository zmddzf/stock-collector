from PyQt5 import QtWidgets
from mainUI import LogicalUI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = LogicalUI()
    ui.show()
    sys.exit(app.exec_())
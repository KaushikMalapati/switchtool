from PyQt5 import QtCore, QtGui, QtWidgets


class EnableDisableDialog(QtWidgets.QDialog):
    """
    Dialog to enable or disable port or device
    """

    def __init__(self, ports, devices, parent=None):
        super().__init__(parent)
        self.ports = ports
        self.devices = devices

        self.setModal(True)
        self.setWindowTitle("Enable/Disable Port")
        # Setup Combo Boxes
        self.portBox = QtWidgets.QComboBox(self)
        self.portBox.currentIndexChanged[str].connect(self.select_device)
        self.devBox = QtWidgets.QComboBox(self)
        self.devBox.addItem("-", userData=None)
        self.devBox.currentIndexChanged[str].connect(self.select_port)

        for port in ports:
            self.portBox.addItem(port)

        for device in devices.keys():
            if device:
                self.devBox.addItem(device, userData=devices[device]["port"])

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.addButton(
            "Enable", QtWidgets.QDialogButtonBox.AcceptRole
        ).clicked.connect(lambda: self.set_enable_disable_value("enable"))
        self.buttonBox.addButton(
            "Disable", QtWidgets.QDialogButtonBox.RejectRole
        ).clicked.connect(lambda: self.set_enable_disable_value("disable"))
        self.buttonBox.setCenterButtons(True)
        # Selection layout
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(QtWidgets.QLabel("Port: "))
        self.lay.addWidget(self.portBox)
        self.lay.addWidget(QtWidgets.QLabel("or Device: "))
        self.lay.addWidget(self.devBox)

        # Total Layout
        self.total_lay = QtWidgets.QVBoxLayout()
        self.total_lay.addLayout(self.lay)
        self.total_lay.addWidget(self.buttonBox, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.total_lay)

    def set_enable_disable_value(self, enable_disable_value):
        self.enable_disable_value = enable_disable_value
        super().accept()

    def current_enable_disable(self):
        """
        Return the port and enable/disable value from the dialog
        """
        return (str(self.portBox.currentText()), str(self.enable_disable_value))

    @QtCore.pyqtSlot(str)
    def select_port(self, device):
        """
        Select a port on the port Combo Box
        """
        if device in self.devices.keys():
            i = self.portBox.findText(self.devices[str(device)]["port"])
            if i != -1:
                self.portBox.setCurrentIndex(i)

    @QtCore.pyqtSlot(str)
    def select_device(self, port):
        """
        Select a device on the device combo box
        """
        i = self.devBox.findData(QtCore.QVariant(port))
        if i != -1:
            self.devBox.setCurrentIndex(i)
        else:
            self.devBox.setCurrentIndex(0)

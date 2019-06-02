from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, \
    QScrollArea
from PySide2.QtWidgets import QScrollBar, QGridLayout


class ImageScrollArea(QScrollArea):
    def __init__(self, pixmap, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = QLabel("ITEM", self)
        self.label.setStyleSheet("border: 1px solid red")
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setPixmap(pixmap)

        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.label)

        self.last_drag_pos = None

    def is_dragged(self):
        return self.last_drag_pos is not None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_drag_pos = event.pos()
            self.label.setStyleSheet("border: 1px solid blue")

    def mouseReleaseEvent(self, event):
        self.last_drag_pos = None

    def mouseMoveEvent(self, event):
        if self.is_dragged():
            pos = event.pos()
            delta: QPoint = self.last_drag_pos - pos
            self.last_drag_pos = pos

            self.scroll_by(delta.x(), delta.y())

    def scroll_by(self, x, y):
        v_scroll_bar: QScrollBar = self.verticalScrollBar()
        h_scroll_bar: QScrollBar = self.horizontalScrollBar()

        v_scroll_bar.setValue(v_scroll_bar.value() + y)
        h_scroll_bar.setValue(h_scroll_bar.value() + x)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_interface(5)

    def _build_interface(self, num_items):
        num_rows = 2 if num_items > 2 else 1

        self.setWindowTitle("MultiImgCmp")

        pixmap = QPixmap("testimg.png")

        common_v_scroll_bar = QScrollBar()
        common_h_scroll_bar = QScrollBar()

        self.layout = QGridLayout()
        for i in range(num_items):
            row = i % num_rows
            column = i // num_rows

            scroll_area = ImageScrollArea(pixmap)
            scroll_area.setVerticalScrollBar(common_v_scroll_bar)
            scroll_area.setHorizontalScrollBar(common_h_scroll_bar)

            self.layout.addWidget(scroll_area, row, column)

        self.setLayout(self.layout)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

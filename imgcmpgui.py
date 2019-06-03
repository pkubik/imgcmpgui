from PySide2.QtCore import Qt, QPoint, QSize, Signal, QObject
from PySide2.QtGui import QPixmap, QColor, QPainter, QBrush, QWheelEvent, QMouseEvent
from PySide2.QtWidgets import QApplication, QWidget, QOpenGLWidget
from PySide2.QtWidgets import QGridLayout


def size_to_point(size: QSize) -> QPoint:
    return QPoint(size.width(), size.height())


class Camera(QObject):
    transformed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = QPoint(0., 0.)
        self.scale_factor = 1.0


class ImageScrollArea(QOpenGLWidget):
    def __init__(self, camera: Camera, pixmap: QPixmap, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = camera
        self.pixmap = pixmap
        self.background_brush = QBrush(QColor(50., 50., 60.))

        self.last_drag_pos = None

        self.camera.transformed.connect(self.on_camera_transformed)

    def on_camera_transformed(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), self.background_brush)

        painter.translate(self.camera.position.x(), self.camera.position.y())
        painter.translate(self.pixmap.size().width() / 2, self.pixmap.size().height() / 2)
        painter.scale(self.camera.scale_factor, self.camera.scale_factor)
        painter.translate(-self.pixmap.size().width() / 2, -self.pixmap.size().height() / 2)
        painter.drawPixmap(QPoint(0., 0.), self.pixmap)

        painter.end()
        event.accept()

    def is_dragged(self):
        return self.last_drag_pos is not None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_drag_pos = event.pos()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.last_drag_pos = None
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_dragged():
            pos = event.pos()
            delta: QPoint = self.last_drag_pos - pos
            self.last_drag_pos = pos

            self.camera.position -= delta
            self.camera.transformed.emit()
            event.accept()

    def wheelEvent(self, event: QWheelEvent):
        increment = 0.01
        self.camera.scale_factor += event.angleDelta().y() / 8 * increment
        self.camera.transformed.emit()
        event.accept()


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_interface(5)

    def _build_interface(self, num_items):
        num_rows = 2 if num_items > 2 else 1

        self.setWindowTitle("MultiImgCmp")
        self.resize(QSize(1024, 800))

        camera = Camera()
        pixmap = QPixmap("testimg.png")

        self.layout = QGridLayout()
        for i in range(num_items):
            row = i % num_rows
            column = i // num_rows

            scroll_area = ImageScrollArea(camera, pixmap)
            self.layout.addWidget(scroll_area, row, column)

        self.setLayout(self.layout)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

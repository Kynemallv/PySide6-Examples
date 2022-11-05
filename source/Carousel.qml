import QtQuick 2.9
import QtQuick.Controls 2.2

Rectangle {
    visible: true
    width: 240
    height: 640
    Component {
        id: delegate
        Item {
            width: 128; height: 128
            scale: PathView.iconScale
            opacity: PathView.iconOpacity
            z: PathView.iconOrder
            Image { anchors.fill: parent; source: modelData }
        }
    }
    PathView {
        id: view
        anchors.fill: parent
        anchors.bottomMargin: 150
        anchors.topMargin: 50
        pathItemCount: 3
        preferredHighlightBegin: 0.5                         //
        preferredHighlightEnd: 0.5                           // That should center the current item
        highlightRangeMode: PathView.StrictlyEnforceRange    //
        model:
            [
            "textures/img.png",
            "textures/img_1.png",
            "textures/img_2.png",
            ]
        delegate: delegate
        path: Path {
            startX: view.width/2; startY: 0
            PathAttribute { name: "iconScale"; value: 0.7 }
            PathAttribute { name: "iconOpacity"; value: 0.5 }
            PathAttribute { name: "iconOrder"; value: 0 }
            PathLine {x: view.width/2; y: view.height/2 }
            PathAttribute { name: "iconScale"; value: 1.2 }
            PathAttribute { name: "iconOpacity"; value: 1 }
            PathAttribute { name: "iconOrder"; value: 4 }
            PathLine {x: view.width/2; y: view.height }
        }
        focus: true
        Keys.onPressed: {
            if (event.key === Qt.Key_Left) {
                decrementCurrentIndex()
            }
            else {
                if (event.key === Qt.Key_Right) {
                    incrementCurrentIndex()
                }
            }
            event.accepted = true
        }
    }
}
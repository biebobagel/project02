import maya.cmds as cmds
import maya.OpenMayaUI as omui

def createCamera(centerX, centerY, centerZ, maxSize):
     # Create a camera and make sure you don't have two
    if cmds.objExists("turntableCamera"):
        cmds.delete("turntableCamera")

    camera, cameraShape = cmds.camera(name="turntableCamera")
    # Position camera based on object size
    cmds.xform(camera, worldSpace=True, translation=[
        centerX, centerY + maxSize, centerZ + (maxSize * 3)
    ])
    # Aim camera at object
    cmds.viewPlace(camera, lookAt=[centerX, centerY, centerZ])

    return camera, cameraShape

def createKeyLight(centerX, centerY, centerZ, maxSize):
    keyLight = cmds.directionalLight(name="keyLight")
    keyLight = cmds.listRelatives(keyLight, parent=True)[0]
    cmds.xform(keyLight, worldSpace=True, translation=[
        centerX + (maxSize * 2), centerY + (maxSize * 2),
        centerZ + (maxSize * 2)
    ])
    cmds.xform(keyLight, worldSpace=True, rotation=[-35, 60, 0])
    cmds.setAttr(keyLight + ".intensity", 2.5)

    return keyLight

def createFillLight(centerX, centerY, centerZ, maxSize):
    fillLight = cmds.directionalLight(name="fillLight")
    fillLight = cmds.listRelatives(fillLight, parent=True)[0]

    cmds.xform(fillLight, worldSpace=True, translation=[
        centerX - (maxSize * 2),
        centerY + (maxSize * 1),
        centerZ + (maxSize * 2)
    ])

    cmds.xform(fillLight, worldSpace=True, rotation=[-10, 135, 0])
    cmds.setAttr(fillLight + ".intensity", 0.3)

    return fillLight

def createRimLight():
    rimLight = cmds.directionalLight(name="rimLight")
    rimLight = cmds.listRelatives(rimLight, parent=True)[0]
    cmds.xform(rimLight, worldSpace=True, translation=[
        centerX,
        centerY + (maxSize * 2),
        centerZ - (maxSize * 3)
    ])
    cmds.xform(rimLight, worldSpace=True, rotation=[-15, 180, 0])
    cmds.setAttr(rimLight + ".intensity", 1.8)

    return rimLight

def createTurntable(objName):
    startFrame = 1
    endFrame = 120

    parent = cmds.listRelatives(objName, parent=True)
    if parent:
        objName = parent[0]

    cmds.xform(objName, centerPivots=True)
    cmds.setAttr(objName + ".rotateY", 0)

    cmds.setKeyframe(objName, attribute="rotateY", value=0, time=startFrame)

    cmds.setKeyframe(objName, attribute="rotateY", value=360, time=endFrame)

    cmds.selectKey(objName, attribute="rotateY")
    cmds.keyTangent(inTangentType="linear", outTangentType="linear")

def main():   
    objectSelection = cmds.ls(selection=True)
    objName = objectSelection[0]
    boundingBox = cmds.exactWorldBoundingBox(objName)
    xmin, ymin, zmin, xmax, ymax, zmax = boundingBox

    centerX = (xmin + xmax) / 2
    centerY = (ymin + ymax) / 2
    centerZ = (zmin + zmax) / 2

    width = xmax - xmin
    height = ymax - ymin
    depth = zmax - zmin

    maxSize = max(width, height, depth)

    createCamera(centerX, centerY, centerZ, maxSize)
    createKeyLight(centerX, centerY, centerZ, maxSize)
    createFillLight(centerX, centerY, centerZ, maxSize)
    createRimLight()

    createTurntable(objName)

    print("Running tool")

if __name__ == "__main__":
    main()

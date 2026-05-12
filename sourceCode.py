import maya.cmds as cmds
import maya.OpenMayaUI as omui

def createTurntable(objName):
    # Set time range
    startFrame = 1
    endFrame = 120

    # Object is at start
    cmds.setKeyframe(objName, attribute="rotateY", value=0, time=startFrame)

    # Initiate full rotation
    cmds.setKeyframe(objName, attribute="rotateY", value=360, time=endFrame)

    # Make sure motion is linear and "readable"
    cmds.selectKey(objName, attribute="rotateY")
    cmds.keyTangent(inTangentType="linear", outTangentType="linear")

def main():   
    # Select the object in scene
    objectSelection = cmds.ls(selection=True)
    # If there's no object/selection, display warning/stop 

    # Generate a boudning box of object
    objName = objectSelection[0]
    boundingBox = cmds.exactWorldBoundingBox(objName)
    xmin, ymin, zmin, xmax, ymax, zmax = boundingBox
    # Return the center point value(s)
    centerX = (xmin + xmax) / 2
    centerY = (ymin + ymax) / 2
    centerZ = (zmin + zmax) / 2
    # Calculate object size for light placements
    width = xmax - xmin
    height = ymax - ymin
    depth = zmax - zmin

    maxSize = max(width, height, depth)

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

    # Create a key light positioned at 45 degrees north of camera
    keyLight = cmds.directionalLight(name="keyLight")
    # Return the light's transform node to move it
    keyLight = cmds.listRelatives(keyLight, parent=True)[0]
    cmds.xform(keyLight, worldSpace=True, translation=[
        centerX + (maxSize * 2), centerY + (maxSize * 2),
        centerZ + (maxSize * 2)
    ])
    cmds.xform(keyLight, worldSpace=True, rotation=[-45, 45, 0])
    # Set to relatively high intensity
    cmds.setAttr(keyLight + ".intensity", 1.5)
    
    # Create/position a fill light positioned at the opposite side
    fillLight = cmds.directionalLight(name="fillLight")
    fillLight = cmds.listRelatives(fillLight, parent=True)[0]

    cmds.xform(fillLight, worldSpace=True, translation=[
        centerX - (maxSize * 2),
        centerY + (maxSize * 1),
        centerZ + (maxSize * 2)
    ])

    # Rotate fill light to object
    cmds.xform(fillLight, worldSpace=True, rotation=[-20, 135, 0])
    # Set to low intensity
    cmds.setAttr(fillLight + ".intensity", 0.5)

    # Create a rim light
    rimLight = cmds.directionalLight(name="rimLight")
    rimLight = cmds.listRelatives(rimLight, parent=True)[0]
    # Position behind the object at low intensity
    cmds.xform(rimLight, worldSpace=True, translation=[
        centerX,
        centerY + (maxSize * 2),
        centerZ - (maxSize * 3)
    ])
    cmds.xform(rimLight, worldSpace=True, rotation=[-10, 180, 0])
    cmds.setAttr(rimLight + ".intensity", 1.2)

    # Create object animation rotating 360 degrees
    # 0-120 frame timeline
    createTurntable(objName)


    print("Running tool")

if __name__ == "__main__":
    main()

from maya import cmds
from maya.api import OpenMaya
import random

maya_useNewAPI = True

class grassNode(OpenMaya.MPxNode):
    kPluginNodeTypeName = "basicNode"
    kPluginNodeId = OpenMaya.MTypeId(0x00000111)

    input_amount = None
    input_angle = None
    output = None

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return grassNode()
    
    def initialize():
        numeric_attr = OpenMaya.MFnNumericAttribute()

        grassNode.input_amount = numeric_attr.create(
            'inputAmount', 
            'io',
            OpenMaya.MFnNumericData.kInt
        )
        numeric_attr.readable = False
        numeric_attr.writable = True
        numeric_attr.keyable = True
        grassNode.addAttribute(grassNode.input_amount)

        numeric_attr_2 = OpenMaya.MFnNumericAttribute()

        grassNode.input_angle = numeric_attr_2.create(
            'inputAngle',
            'ii',
            OpenMaya.MFnNumericData.kFloat
        )
        numeric_attr_2.readable = False
        numeric_attr_2.writable = True
        numeric_attr_2.keyable = True
        grassNode.addAttribute(grassNode.input_angle)

        grassNode.output = numeric_attr_2.create(
            'output',
            'o',
            OpenMaya.MFnNumericData.kFloat
        )
        numeric_attr_2.readable = True
        numeric_attr_2.writable = False
        grassNode.addAttribute(grassNode.output)

        grassNode.attributeAffects(grassNode.input_amount, grassNode.output)
        grassNode.attributeAffects(grassNode.input_angle, grassNode.output)

        grassShard = cmds.polyCube(name='grassShard', width=1, height=1, depth=1)[0]
        vertices_spots = [
            (-0.007, -0.0, 0.015),
            (0.007, -0.0, 0.015),
            (-0.007, 1.0, 0.005),
            (0.007, 1.0, 0.005),
            (-0.007, 1.0, -0.005),
            (0.007, 1.0, -0.005),
            (-0.007, -0.0, -0.015),
            (0.007, -0.0, -0.015)
        ]

        for i, pos in enumerate(vertices_spots):
            cmds.xform(f"{grassShard}.vtx[{i}]", translation=pos)

    def compute(self, plug, dataBlock):
        if plug == self.output:
            input_one_value = dataBlock.inputValue(self.input_amount).asInt()
            input_two_value = dataBlock.inputValue(self.input_amount).asFloat()

            cube = "grassShard"
            duplication(cube, input_one_value)

            output_handle = dataBlock.outputValue(self.output)
            output_handle.setFloat(input_one_value / input_two_value)
            output_handle.setClean()

def duplication(cube_creation, amount):
    print(f"Cube Creation: {cube_creation}, Amount: {amount}")

    existing_duplicates = cmds.ls(f"{cube_creation}_copy*")
    if existing_duplicates:
        print(f"Deleting existing duplicates: {existing_duplicates}")
        cmds.delete(existing_duplicates)

    for i in range(amount - 1):
        cmds.duplicate(cube_creation, name=f"{cube_creation}_copy_{i}")[0]

def shard_angles(angle, amount, base):
    base_pos = cmds.xform(base, query=True, translation=True, worldSpace=True)
    for i in range(amount - 1):
        cmds.setAttr(f"grassShard_copy_{i}.scaleY", random.uniform(0, 1.5))
        cmds.setAttr(f"grassShard_copy_{i}.scaleX", random.uniform(1, 4))
        if (angle < 0):
            angle = angle * -1
        
        if (angle != 0.0):
            temp_x = angle * random.uniform(1, 10)
            temp_y = angle * random.uniform(1, 10)
            temp_z = angle * random.uniform(1, 10)

            if (i % 2 == 0):
                temp_x = temp_x * -1
                temp_y = temp_y * -1
                temp_z = temp_z * -1

                if (temp_x < -100 and temp_y > -100 and temp_z > -100):
                    while (temp_x < -100):
                        temp_x = temp_x / 2
                if (temp_x > -100 and temp_y < -100 and temp_z > -100):
                    while (temp_y < -100):
                        temp_y = temp_y / 2
                if (temp_z > -100 and temp_y > -100 and temp_z < -100):
                    while (temp_z < -100):
                        temp_z = temp_z / 2

                if (temp_x < 0 and temp_x > -45):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", temp_x)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", random.uniform(-1, -45))

                if (temp_y < 0 and temp_y > -45):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", temp_y)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", random.uniform(-1, -45))

                if (temp_z < 0 and temp_z > -45):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", temp_z)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", random.uniform(-1, -45))
            elif (i % 3 == 0):
                temp_x = temp_x * -1

                if (temp_x < -100 and temp_y < 100 and temp_z < 100):
                    while (temp_x < -100):
                        temp_x = temp_x / 2
                if (temp_x > -100 and temp_y > 100 and temp_z < 100):
                    while (temp_y > 100):
                        temp_y = temp_y / 2
                if (temp_z > -100 and temp_y < 100 and temp_z > 100):
                    while (temp_z > 100):
                        temp_z = temp_z / 2

                if (temp_x < 0 and temp_x > -45):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", temp_x)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", random.uniform(-1, -45))

                if (temp_y < 45 and temp_y > 0):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", temp_y)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", random.uniform(1, 45))

                if (temp_z < 45 and temp_z > 0):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", temp_z)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", random.uniform(1, 45))
            else:
                if (temp_x > 100 and temp_y < 100 and temp_z < 100):
                    while (temp_x > 100):
                        temp_x = temp_x / 2
                if (temp_x < 100 and temp_y > 100 and temp_z < 100):
                    while (temp_y > 100):
                        temp_y = temp_y / 2
                if (temp_z < 100 and temp_y < 100 and temp_z > 100):
                    while (temp_z > 100):
                        temp_z = temp_z / 2

                if (temp_x > 0 and temp_x < 90):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", temp_x)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateX", random.uniform(1, 90))

                if (temp_y > 30 and temp_y < 90):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", temp_y)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateY", random.uniform(30, 90))

                if (temp_z > 0 and temp_z < 90):
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", temp_z)
                else:
                    cmds.setAttr(f"grassShard_copy_{i}.rotateZ", random.uniform(1, 90))

        cmds.xform(f"grassShard_copy_{i}", translation=base_pos, worldSpace=True)
    
def on_input_change():
    num_duplicates = cmds.getAttr('basicNode.inputAmount')
    num_angles = cmds.getAttr('basicNode.inputAngle')
    cube = "grassShard"
    duplication(cube, num_duplicates)
    shard_angles(num_angles, num_duplicates, cube)

def setup_script_job():
    cmds.scriptJob(attributeChange=['basicNode.inputAmount', on_input_change])
    cmds.scriptJob(attributeChange=['basicNode.inputAngle', on_input_change])

def initializePlugin(plugin):
    pluginFn = OpenMaya.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(grassNode.kPluginNodeTypeName, grassNode.kPluginNodeId, grassNode.creator, grassNode.initialize)
        print(f"Node type '{grassNode.kPluginNodeTypeName}' registered successfully.")

        cmds.createNode(grassNode.kPluginNodeTypeName, name="basicNode")
        setup_script_job()
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to register node: {e}")
        print(f"Error: {e}")

def uninitializePlugin(plugin):
    pluginFn = OpenMaya.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(grassNode.kPluginNodeId)
        print(f"Node type '{grassNode.kPluginNodeTypeName}' deregistered successfully.")
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to deregister node: {e}")
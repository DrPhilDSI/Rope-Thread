#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        units = design.unitsManager.defaultLengthUnits
        # Get Diameter of the rope thread
        ropeInput = ui.inputBox("Enter the diameter of the rope thread", "Diameter", "14.2")
        if ropeInput[0]:
            ropeDiameter = float(ropeInput[0])
        else:
            return
        # Get Tool Diameter
        toolInput = ui.inputBox("Enter the diameter of the tool", "Tool Diameter", "10")
        if toolInput[0]:
            toolDiameter = float(toolInput[0])
        else:
            return
        # Get the Step Over
        stepOverInput = ui.inputBox("Enter the step over", "Step Over", "0.3")
        if stepOverInput[0]:
            stepOver = float(stepOverInput[0])
        else:
            return
        # Get thread depth
        depth = ui.inputBox("Enter the thread depth", "thread depth", "7.1")
        if depth[0]:
            threadDepth = float(depth[0])
        else:
            return
        
        # get front side offset
        frontSideOffset = ui.inputBox("Enter the front side offset", "front side offset", "50")
        if frontSideOffset[0]:
            frontSideOffset = float(frontSideOffset[0])
        else:
            return

        positions = record_circle_positions(ropeDiameter, toolDiameter, stepOver, threadDepth)
        
        # Get the palette that represents the TEXT COMMANDS window.
        textPalette = ui.palettes.itemById('TextCommands')

        # Make sure the palette is visible.
        if not textPalette.isVisible:
            textPalette.isVisible = True
        textPalette.writeText("*** ROPE THREAD ***")
        textPalette.writeText(f"Rope Diameter: {ropeDiameter:.3f}")
        textPalette.writeText(f"Tool Diameter: {toolDiameter:.3f}")
        textPalette.writeText(f"Step Over: {stepOver:.3f}")
        textPalette.writeText(" ")
        textPalette.writeText("*** Positions: ***")
        textPalette.writeText("Z= Front stock offset \nX= Thread depth")
        for pos in positions:
            textPalette.writeText(f"Z: {frontSideOffset +pos[0]:.3f}, X: {pos[1]:.3f}")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def record_circle_positions(rope_diameter, tool_diameter, step_over, threadDepth):


    if tool_diameter >= rope_diameter:
        raise ValueError("Inner diameter must be smaller than outer diameter.")

    inner_radius = tool_diameter / 2
    outer_radius = rope_diameter / 2
    initial_depth = threadDepth - (outer_radius - inner_radius)

    initial_z = outer_radius - inner_radius
    initial_x = 0  # Centers are horizontally aligned

    positions = [] 
    current_z, current_x = initial_z, initial_x


    while current_z <= outer_radius:
        positions.append((current_z, initial_depth +current_x))
        current_z -= step_over
        
        if abs(current_z) <= outer_radius - inner_radius:
            current_x = math.sqrt((outer_radius - inner_radius) ** 2 - current_z ** 2)
        else:
            break

    return positions
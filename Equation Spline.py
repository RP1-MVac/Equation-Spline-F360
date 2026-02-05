import adsk.core, adsk.fusion, traceback
import math
import re

app = adsk.core.Application.get()
ui = app.userInterface
handlers = []

def is_input_safe(text):
    pattern = r'^[a-zA-Z0-9\s\+\-\*\/\.\(\),\^]*$'
    return bool(re.match(pattern, text) and "__" not in text)

class EquationSplinePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            inputs = eventArgs.command.commandInputs
            
            # --- GET INPUTS ---
            eqn_raw = inputs.itemById('equation').value
            x_start_cm = inputs.itemById('x_start').value 
            x_end_cm = inputs.itemById('x_end').value     
            res = inputs.itemById('res').valueOne
            scale = inputs.itemById('scale').value
            fit_type = inputs.itemById('fit_type').selectedItem.name # Get selection

            if res < 2 or not is_input_safe(eqn_raw):
                return 

            # Python uses ** for power, but users often type ^
            eqn = eqn_raw.replace('^', '**')

            design = adsk.fusion.Design.cast(app.activeProduct)
            rootComp = design.rootComponent
            sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
            
            safe_dict = {
                "math": math, "sin": math.sin, "cos": math.cos, 
                "tan": math.tan, "sqrt": math.sqrt, "pi": math.pi, "pow": pow
            }
            
            points = [] # Use a standard list for easier iteration
            step = (x_end_cm - x_start_cm) / (res - 1)
            
            for i in range(res):
                current_x_cm = x_start_cm + (i * step)
                x_for_eqn = (current_x_cm * 10.0) * scale
                
                safe_dict["x"] = x_for_eqn
                try:
                    y_result = eval(eqn, {"__builtins__": None}, safe_dict)
                    
                    # Safety Clamp: Prevent "Out of Bounds" crashes
                    if abs(y_result) > 1e6: continue 
                    
                    y_cm = (y_result / scale) / 10.0
                    points.append(adsk.core.Point3D.create(current_x_cm, y_cm, 0))
                except:
                    continue 

            if len(points) > 1:
                if fit_type == "Spline (Smooth)":
                    # Slow but smooth
                    obs = adsk.core.ObjectCollection.create()
                    for p in points: obs.add(p)
                    spline = sketch.sketchCurves.sketchFittedSplines.add(obs)
                    spline.isFixed = True
                else:
                    # Fast linear approximation
                    for i in range(len(points) - 1):
                        sketch.sketchCurves.sketchLines.addByTwoPoints(points[i], points[i+1])
            
            eventArgs.isValidResult = True
        except:
            if ui: ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class EquationSplineCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs
            
            inputs.addStringValueInput('equation', 'Equation (y=)', 'sin(x)')
            inputs.addValueInput('x_start', 'Start X', 'mm', adsk.core.ValueInput.createByReal(0))
            inputs.addValueInput('x_end', 'End X', 'mm', adsk.core.ValueInput.createByReal(2.0))
            inputs.addValueInput('scale', 'Scale (Units/mm)', '', adsk.core.ValueInput.createByReal(1.0))
            inputs.addIntegerSliderCommandInput('res', 'Resolution', 2, 200)

            dropdown = inputs.addDropDownCommandInput('fit_type', 'Fit Method', adsk.core.DropDownStyles.TextListDropDownStyle)
            dropdown.listItems.add('Lines (Fast)', True)
            dropdown.listItems.add('Spline (Smooth)', False)
            
            onPreview = EquationSplinePreviewHandler()
            cmd.executePreview.add(onPreview)
            handlers.append(onPreview)
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    try:
        cmdDef = ui.commandDefinitions.addButtonDefinition('PreviewCircleID', 'Equation Spline', 'Spline from Equation')
        onCreated = EquationSplineCreatedHandler()
        cmdDef.commandCreated.add(onCreated)
        handlers.append(onCreated)
        
        ui.allToolbarPanels.itemById('SolidCreatePanel').controls.addCommand(cmdDef)
    except:
        ui.messageBox('Run Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        cmdDef = ui.commandDefinitions.itemById('PreviewCircleID')
        if cmdDef: cmdDef.deleteMe()
        panel = ui.allToolbarPanels.itemById('SolidCreatePanel').controls.itemById('PreviewCircleID')
        if panel: panel.deleteMe()
    except:
        pass
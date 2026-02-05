# Equation Spline

An Autodesk Fusion 360 add-in that allows you to create spline curves from mathematical equations directly in your sketches. Tired of manually plotting points or using external tools? This add-in brings equation-based curve generation right into Fusion 360!

## Why I Made This

I was frustrated by Fusion 360's lack of an integrated equation renderer for creating mathematical curves.

## Features

- **Equation Input**: Enter any mathematical equation using standard Python math syntax
- **Safe Evaluation**: Built-in safety checks to prevent malicious code execution
- **Customizable Parameters**: Control start/end points, resolution, and scaling
- **Real-time Preview**: Generate splines instantly in your active sketch
- **Supported Functions**: Includes common math functions like sin, cos, tan, sqrt, pi, and more

## Installation

1. Download or clone this repository to your local machine
2. Copy the entire `Equation Spline` folder to your Fusion 360 Add-Ins directory:
   - Windows: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
3. Restart Fusion 360
4. The add-in should appear in the Scripts and Add-Ins panel under "My Add-Ins"

## Usage

1. Open Fusion 360 and create a new sketch
2. Click the "Equation Spline" button in the toolbar (it should be in the Solid Scripts Add-ins panel)
3. In the dialog that appears:
   - Enter your equation (e.g., `sin(x)`, `x**2`, `cos(x) + sin(2*x)`)
   - Set the X start and end values (in cm)
   - Adjust the resolution (number of points)
   - Apply a scale factor if needed
4. Click OK to generate the spline curve in your sketch

**Note**: Equations should use `x` as the variable and standard Python math syntax. Available functions include `sin`, `cos`, `tan`, `sqrt`, `pi`, `pow`, etc.

## Requirements

- Autodesk Fusion 360 (latest version recommended)
- Python environment (included with Fusion 360)

## Contributing

Feel free to fork this repository and submit pull requests! If you have ideas for new features or find bugs, please open an issue.

## License

This project is licensed under the terms specified in the LICENSE file.

## Disclaimer

This add-in is provided as-is. Use at your own risk. Always backup your work before using new add-ins.
import clr
import System.IO
import System
import pythoncom

from System.IO import Directory, Path, File
from System import String, Environment

# Initialize COM components
pythoncom.CoInitialize()

# Add references to DWSIM libraries
dwSimPath = r"C:\Users\viraj\AppData\Local\DWSIM\\"
clr.AddReference(dwSimPath + "CapeOpen.dll")
clr.AddReference(dwSimPath + "DWSIM.Automation.dll")
clr.AddReference(dwSimPath + "DWSIM.Interfaces.dll")
clr.AddReference(dwSimPath + "DWSIM.GlobalSettings.dll")
clr.AddReference(dwSimPath + "DWSIM.SharedClasses.dll")
clr.AddReference(dwSimPath + "DWSIM.Thermodynamics.dll")
clr.AddReference(dwSimPath + "DWSIM.UnitOperations.dll")
clr.AddReference(dwSimPath + "DWSIM.Inspector.dll")
clr.AddReference(dwSimPath + "System.Buffers.dll")

# Import DWSIM classes
from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
from DWSIM.Thermodynamics import Streams, PropertyPackages
from DWSIM.UnitOperations import UnitOperations
from DWSIM.Automation import Automation3
from DWSIM.GlobalSettings import Settings

# Set path to existing flowsheet
flowsheetPath = r"D:\08 Linked In\02 DWSim\00 Plan Personal\35 Automating DWSim\35 Automate DWSim.dwxmz"

# Create automation manager
interf = Automation3()

# Load existing flowsheet
sim = interf.LoadFlowsheet(flowsheetPath)

# Get feed stream
feedStream = sim.GetObject("Feed") # Get object with ID "1-1"

# Set new temperature and mass flow rate for feed stream
feedStream.Temperature = (300) # K

# Request a calculation
Settings.SolverMode = 0
errors = interf.CalculateFlowsheet2(sim)

# Save modified flowsheet
interf.SaveFlowsheet(sim, flowsheetPath, True)

# Clean up COM components
# pythoncom.CoUninitialize()

# save file

fileNameToSave = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "heatersample.dwxmz")

interf.SaveFlowsheet(sim, fileNameToSave, True)

# save the pfd to an image and display it

clr.AddReference(dwSimPath + "SkiaSharp.dll")
clr.AddReference("System.Drawing")

from SkiaSharp import SKBitmap, SKImage, SKCanvas, SKEncodedImageFormat
from System.IO import MemoryStream
from System.Drawing import Image
from System.Drawing.Imaging import ImageFormat

PFDSurface = sim.GetSurface()

bmp = SKBitmap(1024, 768)
canvas = SKCanvas(bmp)
canvas.Scale(1.0)
PFDSurface.UpdateCanvas(canvas)
d = SKImage.FromBitmap(bmp).Encode(SKEncodedImageFormat.Png, 100)
str = MemoryStream()
d.SaveTo(str)
image = Image.FromStream(str)
imgPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "pfd.png")
image.Save(imgPath, ImageFormat.Png)
str.Dispose()
canvas.Dispose()
bmp.Dispose()

from PIL import Image

im = Image.open(imgPath)
im.show()

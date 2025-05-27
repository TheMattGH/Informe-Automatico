import psutil
import wmi  


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


# Inicializar WMI
c = wmi.WMI()

print("------Usuario------")
usuario = psutil.users()
if usuario:
    print(usuario[0].name)
else:
    print("Ningun usuario loggeado")

# Información del sistema
print("------Informacion del Sistema------")
os_info = c.Win32_OperatingSystem()[0]
infoSO = (f"{os_info.Caption} {os_info.Version}")
print(infoSO)
architectureSO = (f"{os_info.OSArchitecture}")
print(architectureSO)
manufacturerSO = (f"{os_info.manufacturer}")
print(manufacturerSO)
userSO = (f"{os_info.RegisteredUser}")
print(userSO)

# Información de CPU
print("------Informacion del CPU------")
cpu_info = c.Win32_Processor()[0]
nameCPU = (f"{cpu_info.Name}")
print(nameCPU)
physicalCore = (f"{psutil.cpu_count(logical=False)}")
print(physicalCore)
logicalCore = (f"{psutil.cpu_count(logical=True)}")
print(logicalCore)

# Uso de memoria

print("------Informacion de Memoria RAM------")
mem = psutil.virtual_memory()
totalMem = (f"{mem.total / (1024**3):.2f} GB")
print(totalMem)
avaliableMem = (f"{mem.available / (1024**3):.2f} GB")
print(avaliableMem)
percentUsedMem = (f"{mem.percent}%")
print(percentUsedMem)
usedMem = (f"{mem.used / (1024**3):.2f} GB")
print(usedMem)
freeMem = (f"{mem.free / (1024**3):.2f} GB")
print(freeMem)
      
# Información de discos
print("------Informacion de Almacenamiento------")
for disk in c.Win32_DiskDrive():
    modelDisk = disk.Model
    sizeDisk = f"{int(disk.Size) / (1024**3):.2f} GB"
    serialDisk = disk.SerialNumber if disk.SerialNumber else "No disponible"
    interfaceDisk = disk.InterfaceType
    partitionsDisk = disk.Partitions
    mediaType = disk.MediaType if disk.MediaType else "Desconocido"

    print(f"Modelo: {modelDisk}")
    print(f"Tamaño: {sizeDisk}")
    print(f"Número de serie: {serialDisk}")
    print(f"Interfaz: {interfaceDisk}")
    print(f"Particiones: {partitionsDisk}")
    print(f"Tipo de medio: {mediaType}")
    print("-" * 40)

# Información de tarjetas de red
print("------Informacion de Tarjetas de Red------")
for nic in c.Win32_NetworkAdapter():
    if nic.MACAddress:
        print(f"Tarjeta de red: {nic.Name} - MAC: {nic.MACAddress}")

# Información de procesos activos
print("------Informacion de Procesos Activos------")
activeProcesses = (f"{len(psutil.pids())}")
print(activeProcesses)

print("------Perifericos Conectados------")

# Listar tarjetas de sonido
print("\nTarjetas de sonido:")
for sound in c.Win32_SoundDevice():
    print(f"- {sound.Name}")

# Listar monitores conectados
print("\nMonitores detectados:")
for monitor in c.Win32_DesktopMonitor():
    if monitor.ScreenHeight is None and monitor.ScreenWidth is None :
        print(f"- {monitor.Caption} (Sin resolucion)")
    else :
        print(f"- {monitor.Caption} ({monitor.ScreenHeight}x{monitor.ScreenWidth})")
    
#Bateria si aplica
print("------Bateria------")
def secs2hours (secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod (mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

battery = psutil.sensors_battery()
battery
print("Carga = %s%%, Tiempo Restante = %s" % (battery.percent, secs2hours(battery.secsleft)))




# Crear documento PDF
pdf = SimpleDocTemplate("Informe Tecnico.pdf", pagesize=A4)
contenido = []
# Estilos de texto
estilos = getSampleStyleSheet()

#Tabla Sistema Operativo
tituloSO = Paragraph("Informacion Sistema Operativo", estilos["Title"])
contenido.append(tituloSO)

datos = [["Informacion Sistema Operativo", "Arquitectura Sistema Operativo", "Fabricante", "Usuario Registrado"], 
         [infoSO, architectureSO, manufacturerSO, userSO]]
tablaRam = Table(datos)
tablaRam.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tablaRam)

#Tabla CPU
tituloCPU = Paragraph("Informacion CPU", estilos["Title"])
contenido.append(tituloCPU)

datos = [["Nombre", "Nucleos Fisicos", "Nucleos Ligicos"], 
         [nameCPU, physicalCore, logicalCore]]
tablaRam = Table(datos)
tablaRam.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tablaRam)

#Tabla Almacenamiento
tituloDisk = Paragraph("Informacion Almacenamniento", estilos["Title"])
contenido.append(tituloDisk)

datos = [["Modelo", "Tamaño", "Numero de Serie", "Interfaz", "Particiones", "Tipo de Medio"], 
         [modelDisk, sizeDisk, serialDisk, interfaceDisk, partitionsDisk, mediaType]]
tablaRam = Table(datos)
tablaRam.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tablaRam)

# Tabla Memoria RAM
tituloRam = Paragraph("Memoria ram", estilos["Title"])
contenido.append(tituloRam)

datos = [["Total RAM", "RAM disponible", "Porcentaje Ocupado", " RAM Utilizada", "RAM Libre"], 
         [totalMem, avaliableMem, percentUsedMem, usedMem, freeMem]]
tablaRam = Table(datos)
tablaRam.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
contenido.append(tablaRam)


# Guardar PDF
pdf.build(contenido)


# Sistema Creación de Informes Automáticos

> **Nota:** Este repositorio es una versión de demostración de una herramienta interna desarrollada durante mis prácticas en el **Banco del Austro**. La lógica sensible, activos propietarios y configuraciones internas han sido omitidos por confidencialidad.

---

### 📋 Descripción del Proyecto

Esta aplicación de escritorio fue diseñada para modernizar y optimizar el flujo de trabajo del área de **Soporte Técnico** del departamento de TI del banco. Su objetivo principal es reemplazar las auditorías manuales de hardware por un proceso de diagnóstico completamente automatizado, logrando reducir el tiempo promedio por ticket de mantenimiento en aproximadamente un **40%**.

La herramienta recopila automáticamente métricas del sistema (CPU, RAM, Almacenamiento, Procesos Activos, Periféricos conectados) mediante consultas WMI y APIs del sistema operativo Windows. Posteriormente, analiza el estado de salud del equipo y genera un **Informe Técnico en formato PDF** estandarizado, listo para impresión o archivo digital según los procedimientos internos del banco.

### ✨ Funcionalidades Principales

| Función                      | Descripción                                                                                                                                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Diagnóstico Automatizado** | Extracción con un solo clic de toda la telemetría de hardware y software utilizando `WMI` y `psutil`. Incluye información de CPU, memoria RAM, discos, usuarios del sistema y procesos en ejecución. |
| **Análisis Inteligente**     | Motor de lógica que evalúa el estado del equipo y sugiere acciones de mantenimiento basándose en umbrales predefinidos (por ejemplo: uso elevado de RAM, disco casi lleno, procesos sospechosos).    |
| **Generación de PDF**        | Creación de informes técnicos profesionales y estandarizados utilizando `ReportLab`, con el formato oficial requerido por el departamento.                                                           |
| **Interfaz Moderna**         | Interfaz gráfica responsive y compatible con modo oscuro, desarrollada con `PySide6` para una experiencia de usuario fluida.                                                                         |
| **Distribución Portable**    | Distribuido como un archivo ejecutable `.exe` independiente mediante `PyInstaller`, empaquetado con instalador profesional usando `Inno Setup`.                                                      |

### 🛠️ Tecnologías Utilizadas

| Tecnología                                                                                                                 | Uso                                                          |
| -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)                        | **Lógica Principal** - Lenguaje base para toda la aplicación |
| ![PySide6](https://img.shields.io/badge/PySide6-41CD52?style=flat-square&logo=qt&logoColor=white)                          | **Framework de Interfaz** - Construcción de la GUI moderna   |
| ![WMI](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)                         | **Telemetría del Sistema** - Consultas al sistema operativo  |
| ![ReportLab](https://img.shields.io/badge/PDF_Generation-FF0000?style=flat-square&logo=adobeacrobatreader&logoColor=white) | **Generación de Reportes** - Creación de PDFs profesionales  |
| ![Inno Setup](https://img.shields.io/badge/Inno_Setup-2C2C32?style=flat-square&logo=innosetup&logoColor=white)             | **Instalador** - Empaquetado para distribución               |

### 📁 Estructura del Proyecto

```
├── core/           # Módulos de recopilación de información del sistema
├── src/            # Código fuente principal (GUI y aplicación)
├── utils/          # Utilidades para generación de PDF
├── data/           # Archivos de datos y assets
├── tests/          # Pruebas unitarias
└── reports/        # Directorio de salida para los informes generados
```

---

_Desarrollado por Matías Echeverría - 2025_

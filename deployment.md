# 🚀 Guía de Despliegue Paso a Paso

Esta guía te llevará desde cero hasta tener ambas aplicaciones funcionando en la nube.

## 📋 Checklist Previo

Antes de comenzar, asegúrate de tener:

- [ ] Cuenta de GitHub (gratuita)
- [ ] Git instalado en tu computadora
- [ ] Python 3.8+ instalado (solo para pruebas locales)
- [ ] Editor de código (VS Code, Sublime, etc.)

## 🎯 Parte 1: Configurar el Repositorio en GitHub

### Paso 1: Crear el repositorio

1. Ve a [github.com](https://github.com) e inicia sesión
2. Click en el botón "+" arriba a la derecha → "New repository"
3. Configuración del repositorio:
   - **Repository name**: `seismic-simulator` (o el nombre que prefieras)
   - **Description**: "Simulador interactivo de respuesta sísmica SDOF"
   - **Visibilidad**: Public (necesario para GitHub Pages gratuito)
   - **Marcado**: ✅ Add a README file
4. Click en "Create repository"

### Paso 2: Clonar el repositorio a tu computadora

```bash
# Abre tu terminal/CMD y ejecuta:
git clone https://github.com/TU-USUARIO/seismic-simulator.git
cd seismic-simulator
```

Reemplaza `TU-USUARIO` con tu nombre de usuario de GitHub.

### Paso 3: Crear la estructura de carpetas

```bash
# Crear la carpeta docs
mkdir docs

# Crear la carpeta .streamlit
mkdir .streamlit
```

### Paso 4: Copiar los archivos

Copia cada archivo que te proporcioné en su ubicación correcta:

```
seismic-simulator/
├── streamlit_app.py          ← Archivo principal de Streamlit
├── requirements.txt          ← Dependencias
├── .gitignore               ← Archivos a ignorar
├── README.md                ← Ya existe, reemplázalo
├── docs/
│   ├── index.html           ← Página de inicio
│   └── simulator.html       ← Visualizador
└── .streamlit/
    └── config.toml          ← Configuración de Streamlit
```

**config.toml** (crear este archivo):
```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f1f5f9"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

### Paso 5: Hacer commit y push

```bash
# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: SDOF Seismic Simulator"

# Subir a GitHub
git push origin main
```

## ☁️ Parte 2: Desplegar en Streamlit Cloud

### Paso 1: Ir a Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Click en "Sign up" o "Sign in with GitHub"
3. Autoriza a Streamlit para acceder a tus repositorios

### Paso 2: Crear una nueva app

1. Click en "New app" (botón azul arriba a la derecha)
2. Configuración:
   - **Repository**: Selecciona `tu-usuario/seismic-simulator`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL** (opcional): Personaliza tu URL o deja el predeterminado
3. Click en "Deploy!"

### Paso 3: Esperar el despliegue

- El proceso toma 2-5 minutos
- Verás logs en tiempo real
- Cuando esté listo, aparecerá "Your app is live!"

### Paso 4: Copiar tu URL

Tu app tendrá una URL como:
```
https://tu-usuario-seismic-simulator-streamlit-app-xyz123.streamlit.app
```

**¡Guarda esta URL!** La necesitarás en el siguiente paso.

## 🌐 Parte 3: Activar GitHub Pages

### Paso 1: Configurar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Click en "Settings" (en el menú horizontal superior)
3. En el menú lateral izquierdo, busca "Pages" (en la sección "Code and automation")
4. En "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: Selecciona `main`
   - **Folder**: Selecciona `/docs`
5. Click en "Save"

### Paso 2: Esperar el despliegue

- GitHub tardará 2-3 minutos en construir y desplegar
- Verás un mensaje: "Your site is live at..."
- Tu URL será: `https://tu-usuario.github.io/seismic-simulator/`

### Paso 3: Verificar que funciona

1. Abre la URL de GitHub Pages en tu navegador
2. Deberías ver la página de inicio con dos opciones
3. Por ahora, solo el "Visualizador Web" funcionará completamente

## 🔗 Parte 4: Conectar Ambas Aplicaciones

### Paso 1: Actualizar index.html

En tu editor de código, abre `docs/index.html` y busca esta línea (~178):

```javascript
const STREAMLIT_URL = 'https://tu-app.streamlit.app'; // Actualizar después de deployar
```

Reemplázala con tu URL real de Streamlit:

```javascript
const STREAMLIT_URL = 'https://tu-usuario-seismic-simulator-streamlit-app-xyz123.streamlit.app';
```

### Paso 2: Actualizar streamlit_app.py

Abre `streamlit_app.py` y busca esta línea (~51):

```python
st.markdown("[Ver Animación →](https://tu-usuario.github.io/seismic-simulator/simulator.html)", 
            unsafe_allow_html=True)
```

Reemplaza con tu URL real de GitHub Pages:

```python
st.markdown("[Ver Animación →](https://TU-USUARIO.github.io/seismic-simulator/simulator.html)", 
            unsafe_allow_html=True)
```

### Paso 3: Actualizar README.md

En `README.md`, busca la sección "Demo en Vivo" y actualiza las URLs:

```markdown
## 🚀 Demo en Vivo

- **Aplicación Streamlit**: [tu-app.streamlit.app](https://tu-app-real.streamlit.app)
- **Visualizador Web**: [tu-usuario.github.io/seismic-simulator](https://tu-usuario-real.github.io/seismic-simulator)
```

### Paso 4: Subir los cambios

```bash
# Agregar cambios
git add .

# Commit
git commit -m "Update: Conectar URLs de despliegue"

# Push
git push origin main
```

### Paso 5: Esperar actualizaciones

- **Streamlit**: Se actualizará automáticamente en 1-2 minutos
- **GitHub Pages**: Tarda 2-3 minutos en reconstruir

## ✅ Parte 5: Verificación Final

### Checklist de Verificación

- [ ] Streamlit Cloud app funciona correctamente
- [ ] GitHub Pages muestra la página de inicio
- [ ] El botón "Streamlit - Análisis Completo" abre la app de Streamlit
- [ ] El botón "Visualizador Web" abre el simulador animado
- [ ] Desde Streamlit, el link "Ver Animación →" funciona
- [ ] Desde el visualizador, el botón "← Volver" regresa al inicio

### Probar funcionalidades

**En Streamlit:**
1. Ajusta los sliders de la barra lateral
2. Verifica que las gráficas se actualicen
3. Cambia entre las pestañas
4. Observa las métricas en tiempo real

**En el Visualizador:**
1. Ajusta los parámetros en la barra lateral
2. Click en "▶️ Reproducir"
3. Observa la animación de edificios
4. Usa la línea de tiempo
5. Prueba el botón "↻ Reiniciar"

## 🐛 Solución de Problemas Comunes

### Problema 1: Streamlit no despliega

**Error**: "ModuleNotFoundError"

**Solución**:
1. Verifica que `requirements.txt` esté en la raíz del repositorio
2. Asegúrate de que todas las librerías estén listadas
3. Revisa los logs en Streamlit Cloud para ver qué librería falta

### Problema 2: GitHub Pages muestra 404

**Solución**:
1. Ve a Settings → Pages
2. Verifica que la carpeta sea `/docs` (no `/` ni `/root`)
3. Asegúrate de que `index.html` esté dentro de `docs/`
4. Espera 5 minutos más (puede tardar)

### Problema 3: El botón de Streamlit no funciona

**Solución**:
1. Abre la consola del navegador (F12)
2. Verifica el error
3. Asegúrate de haber actualizado `STREAMLIT_URL` en `index.html`
4. Verifica que la URL de Streamlit esté correcta (sin espacios)

### Problema 4: Streamlit se "duerme"

**Comportamiento normal**: Streamlit Cloud pone las apps en "sleep mode" después de inactividad.

**Solución**: 
- Simplemente vuelve a cargar la página
- La app "despertará" en 10-30 segundos
- Esto es normal en el plan gratuito

## 🎉 ¡Listo!

Ahora tienes:

✅ Aplicación Streamlit funcionando en la nube
✅ Visualizador web en GitHub Pages
✅ Ambas aplicaciones conectadas
✅ URLs permanentes para compartir

## 📤 Compartir tu Proyecto

Puedes compartir estas URLs:

1. **Página principal**: `https://tu-usuario.github.io/seismic-simulator/`
   - Deja que los usuarios elijan qué versión usar

2. **Directamente al análisis**: Tu URL de Streamlit
   - Para usuarios que quieran análisis detallado

3. **Directamente al visualizador**: `https://tu-usuario.github.io/seismic-simulator/simulator.html`
   - Para demostraciones rápidas

## 🔄 Actualizar el Proyecto

Para hacer cambios en el futuro:

```bash
# 1. Edita los archivos que necesites
# 2. Guarda los cambios
# 3. Ejecuta:

git add .
git commit -m "Descripción de tus cambios"
git push origin main

# Streamlit se actualizará automáticamente
# GitHub Pages tardará 2-3 minutos
```

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en Streamlit Cloud
2. Revisa la consola del navegador (F12) para GitHub Pages
3. Verifica que todas las URLs estén correctamente actualizadas
4. Asegúrate de que los archivos estén en las carpetas correctas

---

**¿Necesitas ayuda?** Abre un issue en tu repositorio de GitHub describiendo el problema.

**¡Éxito con tu proyecto!** 🚀
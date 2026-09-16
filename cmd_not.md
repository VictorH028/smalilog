# Instala el paquete localmente en modo editable
pip install -e .

# Verifica que el CLI reconoce los módulos
python -c "import smalilog; print(smalilog.__file__)"


invoke-static {p0}, Lcom/deadnote/LifecycleTracker;->init(Landroid/app/Application;)V

Puntos clave:
​Ubicación: Se coloca tras invoke-super {p0}, Ltc0/i;->onCreate()V para garantizar que el contexto base de la aplicación esté completamente inicializado por Hilt/Android.  
​Parámetro p0: p0 hace referencia a this (la instancia de CrunchyrollApplication), la cual hereda de android.app.Application y se pasa a LifecycleTracker.init().


# Ideas para agregar 
> [!NOTE]
> No intalar desede pip3 da error sique los pasos de la wep 
- [androguard](https://androguard.github.io/androguard/contributing.html)

Se intala bien pero `cryptography` falla aunque se intale. 

Solucion usar la vercion de termux 
```
apt install python-cryptography
```

Verificar la ruta de el venv 

```
poetry env info --path
```
---

Esto es pra auto Backup manda la informacion a Google Drive 
> [!NOTE]
> Tener esto es cuenta para explotar 
```
<application
    android:allowBackup="true"
    android:fullBackupContent="@xml/backup_rules">
```


# Git revisar despues

- [document-api](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/document-api) 

- 

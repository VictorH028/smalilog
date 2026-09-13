# Instala el paquete localmente en modo editable
pip install -e .

# Verifica que el CLI reconoce los módulos
python -c "import smalilog; print(smalilog.__file__)"


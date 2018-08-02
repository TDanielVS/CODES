* Descargar "Miniconda3-4.3.30-Linux-x86_64.sh" https://repo.continuum.io/miniconda/

* Instalar
```
bash Miniconda3-4.3.30-Linux-x86_64.sh
```

* Actualizar miniconda
```
conda update conda
```

* Crear ambiente
```
conda env create -f environment.yml
```

Activar ambiente:
```
source activate envpy3
```

Una vez activado el ambiente, ejecutar los siguientes comandos:
```
pip install pyros_setup
pip install catkin_pkg
pip install -U rospkg
```
En caso de ser necesario incluir el comando:
```
pip install opencv-python
```

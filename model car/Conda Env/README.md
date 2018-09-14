* Download/Descargar "Miniconda3-4.3.30-Linux-x86_64.sh" https://repo.continuum.io/miniconda/

* Install/Instalar
```
bash Miniconda3-4.3.30-Linux-x86_64.sh
```

* Update/Actualizar miniconda
```
conda update conda
```

* Create environment / Crear ambiente
```
conda env create -f environment.yml
```

Activate environment / Activar ambiente:
```
source activate envpy3
```

Once activated the environment, execute the following commands:
/ Una vez activado el ambiente, ejecutar los siguientes comandos:
```
pip install pyros_setup
pip install catkin_pkg
pip install -U rospkg
```
If is necessary, include the command:
/En caso de ser necesario incluir el comando:
```
pip install opencv-python
```

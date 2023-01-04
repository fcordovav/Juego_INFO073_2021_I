import cx_Freeze
import sys

cx_Freeze.setup(
	name="Soy Qbertito v1.1",
	version="1.1",
	options={"build_exe": {"packages": ["pygame"],
						   "include_files":["imagenes",
                                            "sonidos",
                                            "pantallas.py",
                                            "tablero.py",
                                            "utiles.py"]}
		    },
	executables=[cx_Freeze.Executable("principal.py")]
)
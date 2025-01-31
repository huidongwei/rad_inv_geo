@ECHO OFF
setlocal
set OPENRADIOSS_PATH=F:\Openradioss\OpenRadioss-main
echo %OPENRADIOSS_PATH%
set RAD_CFG_PATH=%OPENRADIOSS_PATH%\hm_cfg_files
echo %RAD_CFG_PATH%
set OMP_NUM_THREADS=1
set RAD_H3D_PATH=%OPENRADIOSS_PATH%\extlib\h3d\lib\win64
echo %RAD_H3D_PATH%
set KMP_STACKSIZE=400m
set PATH=%OPENRADIOSS_PATH%\extlib\hm_reader\win64;%PATH%;%OPENRADIOSS_PATH%\extlib\intelOneAPI_runtime\win64;%PATH%;"C:\Program Files (x86)\Intel\oneAPI\mpi\2021.8.0\bin"
set MPI_PATH="C:\Program Files (x86)\Intel\oneAPI\mpi\2021.13\bin"
echo %PATH%
echo "**Run Starter**"
%OPENRADIOSS_PATH%\exec\starter_win64.exe -i pressure_LAW42_0000.rad -np 6 >starter.out 
echo "**Run Engine**"
%MPI_PATH%\mpiexec.exe -delegate -np 6 %OPENRADIOSS_PATH%\exec\engine_win64_impi.exe -i pressure_LAW42_0001.rad  >engine.out
echo "Done"

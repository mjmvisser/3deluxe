# get the absolute path for this script
etc_dir=$(dirname ${BASH_SOURCE[0]})
etc_dir=$(cd "$etc_dir"; pwd)

maya_version=$(maya -v | head -1 | awk '{print $2}')
delight_version=$(( renderdl -v 2>&1 ) | head -1 | awk '{print $3}')

export DLDIR=$(dirname $etc_dir)

export PYTHONPATH=$DLDIR/python:$DLDIR/3rdparty/lib/python2.6/site-packages:$PYTHONPATH
export PATH=$DLDIR/python/scripts:$DLDIR/3rdparty/bin:$PATH

export MAYA_SCRIPT_PATH=$DLDIR/maya/scripts:$DLDIR/3dfm/$delight_version/maya/$maya_version/scripts:$MAYA_SCRIPT_PATH
export MAYA_PLUG_IN_PATH=$DLDIR/maya/plug-ins:$DLDIR/python/shaders:$MAYA_PLUG_IN_PATH
export XBMLANGPATH=$DLDIR/maya/icons:$DLDIR/python/shaders:$XBMLANGPATH

export _3DFM_SL_INCLUDE_PATH=$DLDIR/python/shaders:$DLDIR/python/shaders/include:$DLDIR/python/shaders/include:$DLDIR/shadeops:$_3DFM_SL_INCLUDE_PATH

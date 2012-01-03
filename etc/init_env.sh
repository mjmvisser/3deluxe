# get the absolute path for this script
etc_dir=$(dirname ${BASH_SOURCE[0]})
etc_dir=$(cd "$etc_dir"; pwd)

maya_version=$(maya -v | head -1 | awk '{print $2}')
delight_version=$(( renderdl -v 2>&1 ) | head -1 | awk '{print $3}')

if [ -n "${_3DFM_SL_INCLUDE_PATH:-x}" ]; then
    # set some sane defaults
    export _3DFM_SL_INCLUDE_PATH=$DELIGHT/maya/rsl
fi

export DELUXE=$(dirname $etc_dir)

export PYTHONPATH=$DELUXE/python:$DELUXE/3rdparty/lib/python2.6/site-packages:$PYTHONPATH
export PATH=$DELUXE/python/scripts:$DELUXE/3rdparty/bin:$PATH

export MAYA_SCRIPT_PATH=$DELUXE/maya/scripts:$DELUXE/3dfm/$delight_version/maya/$maya_version/scripts:$MAYA_SCRIPT_PATH
export MAYA_PLUG_IN_PATH=$DELUXE/maya/plug-ins:$DELUXE/python/shaders:$MAYA_PLUG_IN_PATH
export XBMLANGPATH=$DELUXE/maya/icons:$DELUXE/python/shaders:$XBMLANGPATH

export _3DFM_SL_INCLUDE_PATH=$DELUXE/python/shaders:$DELUXE/python/shaders/include:$DELUXE/python/shaders/include:$DELUXE/shadeops:$_3DFM_SL_INCLUDE_PATH

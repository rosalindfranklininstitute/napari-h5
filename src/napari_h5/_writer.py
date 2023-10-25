"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

import h5py
import numpy as np

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


#https://napari.org/stable/plugins/guides.html#single-layer-writer
def single_layer_writer(path: str, data: Any, attributes: dict) -> List[str]:
    """Writes a single image layer"""

    if not isinstance(data, np.ndarray):
        raise ValueError("data is not ndarray. Not saving.")

    with h5py.File(path,'w') as f:
        f.create_dataset('data', data=data)

    # return path to any file(s) that were successfully written
    return [path]

def multi_layer_writer(path: str, layer_data: List[FullLayerData]) -> List[str]:
    """Writes multiple layers of different types."""
    
    paths=[]

    from pathlib import Path
    path0 = Path(path)
    #print("path0:"+str(path0))

    for i, ld0 in enumerate(layer_data):
        #layer data is a list of FullLayerData
        # FullLayerData = Tuple[DataType, LayerAttributes, LayerName]
        # https://napari.org/stable/plugins/guides.html#multi-layer-writer
        # DataType is usually a ndarray, depending of the layer type

        datatype0, layerattibs0, layername0 = ld0

        if layername0=='image' or layername0=='labels':
            if isinstance(datatype0,np.ndarray):
                path1 = Path.joinpath(path0.parent, path0.stem + f"_{i:03d}"+ path0.suffix)
                
                #print(f"data i:{i} , path1:{path1}")

                try:
                    with h5py.File(path1,'w') as f:
                        f.create_dataset('data', data=datatype0.data)
                    paths.append(str(path1))
                except:
                    #if it fails to save... bad luck
                    pass
    # return path to any file(s) that were successfully written
    return paths

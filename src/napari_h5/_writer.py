"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

import h5py

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]

#https://napari.org/dev/plugins/guides.html?highlight=napari_get_writer
def single_layer_writer(path: str, data: Any, attributes: dict) -> List[str]:
    """Writes a single image layer"""

    with h5py.File(path,'w') as f:
        f.create_dataset('data', data=data)

    # return path to any file(s) that were successfully written
    return [path]

def multi_layer_writer(path: str, layer_data: List[FullLayerData]) -> List[str]:
    """Writes multiple layers of different types."""
    
    paths=[]

    from pathlib import Path
    path0 = Path(str)
    for i, d0 in enumerate(data):
        path1 = f"{path0.stem()}_{i:03d}{path0.suffix()}"
        
        try:
            with h5py.File(path,'w') as f:
                f.create_dataset('data', data=d0)
            paths.append(path1)
        except:
            pass
    # return path to any file(s) that were successfully written
    return paths

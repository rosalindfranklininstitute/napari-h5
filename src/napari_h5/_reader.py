"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
import numpy as np
#import xarray

def get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if not path.endswith(".h5"):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path
    
    
    # # load all files into array
    # arrays = [np.load(_path) for _path in paths]
    # # stack arrays into single array
    # data = np.squeeze(np.stack(arrays))
    
    #print("reader_function()") #Debug
    import pathlib
    import h5py

    data_list = None
    for p0 in paths:
        with h5py.File(str(p0),'r') as f:
            data_list = []
            # If not ask user to help choosing data to display

            #data0 = np.array(f['data']) #Loads 'data' by default

            #Get keys available
            fkeys = list(f.keys())

            if len(fkeys)>=1:
                #Check which ones are "Datasets"
                
                for k0,i0 in list(f.items()):
                    if isinstance(i0, h5py._hl.dataset.Dataset):
                        #Grab data from this dataset
                        #print(f"Dataset name:{k0} found") #Debug

                        f_path = pathlib.Path(str(p0))
                        fname_stem = f_path.stem
                        add_kwargs = {'name':fname_stem+" "+k0}
                        layer_type = "image"

                        data0 = np.array(i0) #Loads 'data' by default
                        data_list.append( (data0, add_kwargs, layer_type) )

                if len(data_list)==0:
                    data_list=None
                
    # optional kwargs for the corresponding viewer.add_* method
    

    #layer_type = "image"  # optional, default is "image"
    #return [(data, add_kwargs, layer_type)]

    return data_list


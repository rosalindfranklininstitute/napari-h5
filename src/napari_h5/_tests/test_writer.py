# from napari_h5 import write_single_image, write_multiple

# add your tests here...
import h5py
import numpy as np

from napari_h5 import single_layer_writer, multi_layer_writer

from napari.types import FullLayerData

def test_writer(tmp_path):
    # write some fake data using your supported file format
    original_data = np.random.rand(20, 20,20)
    my_test_file = str(tmp_path / "myfile.h5")

    write_paths = single_layer_writer(my_test_file, original_data, None)
    
    # try to read it back in using h5py
    with h5py.File(my_test_file,'r') as f:
        data0 = np.array(f['data']) #Loads 'data' by default

    # make sure it's the same as it started
    np.testing.assert_allclose(original_data, data0)

def test_multi_writer(tmp_path):
    # write some fake data using your supported file format
    original_data = np.random.rand(20, 20,20)
    original_labels = np.random.randint(0, 100,size = (20,20,20) )

    my_test_filename = str(tmp_path / "myfiles.h5")

    fulllayerdata0 = [
        (original_data, None, "image"),
        (original_labels, None, "labels")
        ]

    write_paths = multi_layer_writer(my_test_filename, fulllayerdata0)

    assert len(write_paths)==2

    with h5py.File(write_paths[0],'r') as f:
        data0 = np.array(f['data']) #Loads 'data' by default
    # make sure it's the same as it started
    np.testing.assert_array_equal(original_data, data0)

    with h5py.File(write_paths[1],'r') as f:
        data1 = np.array(f['data']) #Loads 'data' by default
    # make sure it's the same as it started
    np.testing.assert_array_equal(original_labels, data1)
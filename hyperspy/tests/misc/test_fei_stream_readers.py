"""Test the FEI stream readers.

Because there is no official description of the format, these tests just tests
consistency between ``array_to_stream`` and ``stream_to*array``. In the
particular case of stream to sparse array, we use dask to compute the array
in order to mimic the usage in the FEI EMD reader.

"""
import numpy as np
import dask.array as da

from hyperspy.misc.io.fei_stream_readers import (
    array_to_stream, stream_to_array, stream_to_sparse_COO_array)


def test_dense_stream():
    arr = np.random.randint(0, 65535, size=(2, 3, 4, 5)).astype("uint16")
    stream = array_to_stream(arr)
    # Lazy
    arrs = da.from_array(stream_to_sparse_COO_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2), chunks=(1, 1, 2, 5))
    arrs = arrs.compute()
    assert (arrs == arr).all()
    # Dense
    arrs = stream_to_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2)
    assert (arrs == arr).all()

def test_empty_stream():
    arr = np.zeros((2, 3, 4, 5), dtype="uint16")
    stream = array_to_stream(arr)
    arrs = da.from_array(stream_to_sparse_COO_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2), chunks=(1, 1, 2, 5))
    arrs = arrs.compute()
    # Dense
    arrs = stream_to_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2)
    assert not arrs.any()

def test_sparse_stream():
    arr = np.zeros((2, 3, 4, 5), dtype="uint16")
    arr[0, 0, 0, 0] = 1
    arr[-1, -1, -1, -1] = 2
    arr[1, 1, 3, 3] = 3
    stream = array_to_stream(arr)
    arrs = da.from_array(stream_to_sparse_COO_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2), chunks=(1, 1, 2, 5))
    arrs = arrs.compute()
    assert (arrs == arr).all()
    # Dense
    arrs = stream_to_array(
        stream, spatial_shape=(3, 4), sum_frames=False, channels=5,
        last_frame=2)
    assert (arrs == arr).all()

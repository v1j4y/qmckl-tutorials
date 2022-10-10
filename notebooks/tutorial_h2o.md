---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.12.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---


# QMCkl Tutorial


This tutorial covers some basic use cases of the QMCkl library based on the Python API. 
At this point, it is assumed that the QMCkl Python package has been successfully installed on the user machine 
or in the virtual environment. If this is not the case, feel free to follow the [installation guide](https://github.com/TREX-CoE/qmckl/blob/master/python/README.md).

## Importing QMCkl

```python
try:
    import qmckl as pq
except ImportError:
    raise Exception("Unable to import qmckl. Please check that qmckl is properly installed.")
```

## Importing packages

```python
import numpy as np
import time

from data.data import coord, mo_index_alpha, mo_index_beta
```

## Initialize parameters

Here we initialiez the parameters for the calculation
such as the number of electrons `elec_num` and the number of walkers `walk_num`. 

The context `ctx`, which will be used throughout the calculation, is also initialized. 

```python
ITERMAX = 10 # Maximum number of iterations for the timing

walk_num = 100
elec_num = 10

ctx = pq.context_create()
```

## Read the data

We read basic information about the molecule such as:

- Basis functions
- Electron and nucleii information
- Molecular orbital coefficients
- Jastrow function related data

```python
try:
    pq.trexio_read(ctx, 'fake.hdf5')
except RuntimeError:
    print('Error handling check: passed')
    
fname = join('data', 'h2o-sto3g.h5')

pq.trexio_read(ctx, fname)
print('trexio_read: passed')
```

## Check data 

Here we check whether the data has been properly initialized 
via the `trexio` file.

We also set the electron coordinates of the walkers. 

```python
mo_num = pq.get_mo_basis_mo_num(ctx)
assert mo_num == 7

pq.set_electron_coord(ctx, 'T', walk_num, coord)

ao_type = pq.get_ao_basis_type(ctx)
assert 'G' in ao_type

size_max = 5*walk_num*elec_num*mo_num

mo_vgl = pq.get_mo_basis_mo_vgl(ctx, size_max)
assert mo_vgl.size == size_max
```

## Set determinant information

Now we need to supply the information concerning determinants
for the calculation of the Local energy.

```python
pq.set_determinant_type(ctx, 'G')
det_num_alpha = 1
det_num_beta  = 1
pq.set_determinant_det_num_alpha(ctx, det_num_alpha)
pq.set_determinant_det_num_beta (ctx, det_num_beta )
pq.set_determinant_det_num_beta (ctx, det_num_beta )
elec_up_num = elec_num//2
elec_down_num = elec_num//2

pq.set_determinant_mo_index_alpha(ctx, mo_index_alpha)
pq.set_determinant_mo_index_beta (ctx, mo_index_beta )
```

## Testing 

We can check the time required to calculate the value, gradient,
and Laplacian of the MOs with respect to the coordinates for each walker.

```python
start = time.clock_gettime_ns(time.CLOCK_REALTIME)

for _ in range(ITERMAX):
    mo_vgl_in = pq.get_mo_basis_mo_vgl_inplace(ctx, size_max)

end = time.clock_gettime_ns(time.CLOCK_REALTIME)

print(f'Time for the calculation of 1 step : {(end-start)*.000001/ITERMAX} ms')
```

## Calculation of Local Energy

Finally, we can check that all the information required for the
calculation of the local energy has been initialized. Following 
this, we can check that the local energy can also be provided.

```python
provided_elec = pq.electron_provided(ctx)
assert (provided_elec == True)

provided_nucl = pq.nucleus_provided(ctx)
assert (provided_nucl == True)

provided_ao_basis = pq.ao_basis_provided(ctx)
assert (provided_ao_basis == True)

provided_mo_basis = pq.mo_basis_provided(ctx)
assert (provided_mo_basis == True)

provided_det = pq.determinant_provided(ctx)
assert (provided_det == True)

provided_local_energy = pq.local_energy_provided(ctx)
assert (provided_local_energy == True)
```

## Generate coordinates

Generate trial coordinates for the initial walker distribution.

```python
r = 10

def generate_walkers(r):
    """
    Generate coordinates
    """
    import itertools

    n_samples = 10

    x = np.random.uniform(-r, r, size=n_samples)
    y = np.random.uniform(-r, r, size=n_samples)
    z = np.random.uniform(-r, r, size=n_samples)

    coordsall = np.array(list(itertools.product(x,y,z)))
    #np.savetxt("/tmp/coordsall.txt", coordsall, delimiter=',\t', fmt='%18.15f')
    return(coordsall)
```

## Plot Local Energy

Plot the local energy of each walker.

```python
if False:
    import matplotlib.pyplot as plt
    # Plotting
    plt.figure(figsize=(7,7))
    plt.plot(range(walk_num),local_energy, marker='o',  label='Samples')
    plt.grid()
    plt.legend(loc='upper right')
    plt.show(block=True)
```

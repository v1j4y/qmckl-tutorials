""" 
This is the test of the Python API of the QMCkl library.
It is the `bench_mos.c` C code adapted from the `bench`
repo and translated into Python with some modifications.
"""

from os.path import join
import time

import numpy as np

import qmckl as pq
from data.data import coord


walk_num  = 100
elec_num  = 10

ITERMAX = 10

ctx = pq.context_create()

try:
    pq.trexio_read(ctx, 'fake.h5')
except RuntimeError:
    print('Error handling check: passed')

fname = join('data', 'h2o-sto3g.h5')

pq.trexio_read(ctx, fname)
print('trexio_read: passed')

mo_num = pq.get_mo_basis_mo_num(ctx)
assert mo_num == 7

pq.set_electron_coord(ctx, 'T', walk_num, coord)

ao_type = pq.get_ao_basis_type(ctx)
assert 'G' in ao_type

size_max = 5*walk_num*elec_num*mo_num

mo_vgl = pq.get_mo_basis_mo_vgl(ctx, size_max)
assert mo_vgl.size == size_max

start = time.clock_gettime_ns(time.CLOCK_REALTIME)

for _ in range(ITERMAX):
    mo_vgl_in = pq.get_mo_basis_mo_vgl_inplace(ctx, size_max)

end = time.clock_gettime_ns(time.CLOCK_REALTIME)

print(f'Time for the calculation of 1 step : {(end-start)*.000001/ITERMAX} ms')

provide_elec = pq.electron_provided(ctx)
assert (provide_elec == True)
provide_nucl = pq.nucleus_provided(ctx)
assert (provide_nucl == True)
provide_ao_basis = pq.ao_basis_provided(ctx)
assert (provide_ao_basis == True)
provide_mo_basis = pq.mo_basis_provided(ctx)
assert (provide_mo_basis == True)
local_energy = pq.get_local_energy(ctx, 1)

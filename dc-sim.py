import dolfinx
from dolfinx import mesh, fem
import numpy as np
from typing import *
import typing


from mpi4py import MPI

# Define the mesh
nx, ny, nz = 20, 20, 20
lx, ly, lz = 2.0, 2.0, 2.0
# mesh = dolfinx.RectangleMesh(dolfinx.MPI.comm_world,
#                              dolfinx.geometry.Cuboid(0, 0, 0, lx, ly, lz),
#                              nx, ny, nz)

msh = mesh.create_rectangle(comm=MPI.COMM_WORLD,
                            points=((0.0, 0.0), (2.0, 1.0)), n=(32, 16),
                            cell_type=mesh.CellType.triangle,)
# Define the function space
V = fem.FunctionSpace(msh, ("Lagrange", 1))

# Define the boundary conditions
def joe(x: np.ndarray) -> np.ndarray:
    print('t- x', type(x))
    calc1 = np.logical_and(0.25 <= x[0], x[0] <= 0.75)
    calc2 = np.logical_and(0.25 <= x[1], x[1] <= 0.75)
    calc3 = np.logical_and(0.25 <= x[2], x[2] <= 0.75)
    calc = np.logical_and(calc1, calc2, calc3)
    # calc = ((0.25 <= x[0] <= 0.75) and (0.25 <= x[1] <= 0.75) and (0.25 <= x[2] <= 0.75))
    print('t- calc', type(calc))
    print('t- all', type(np.all(calc)))
    return calc

def mama(x: np.ndarray) -> np.ndarray:
    print('t- x', type(x))
    calc1 = np.logical_and(1.25 <= x[0], x[0] <= 1.75)
    calc2 = np.logical_and(1.25 <= x[1], x[1] <= 1.75)
    calc3 = np.logical_and(1.25 <= x[2], x[2] <= 1.75)
    calc = np.logical_and(calc1, calc2, calc3)
    # calc = ((1.25 <= x[0] <= 1.75) and (1.25 <= x[1] <= 1.75) and (1.25 <= x[2] <= 1.75))
    print('t- calc', type(calc))
    print('t- all', type(np.all(calc)))
    return calc

box1 = mesh.locate_entities_boundary(msh, dim=(msh.topology.dim - 1), marker=joe)
box2 = mesh.locate_entities_boundary(msh, dim=(msh.topology.dim - 1), marker=mama)
bc_box1 = fem.dirichletbc(V, dolfinx.Constant(100), box1)
bc_box2 = fem.dirichletbc(V, dolfinx.Constant(-100), box2)
bc = [bc_box1, bc_box2]

# Define the variational problem
u = dolfinx.Function(V)
v = dolfinx.TestFunction(V)
f = dolfinx.Constant(0)
a = dolfinx.inner(dolfinx.grad(u), dolfinx.grad(v)) * dolfinx.dx
L = f * v * dolfinx.dx

# Solve the variational problem
problem = dolfinx.fem.LinearProblem(a, L, bcs=bc)
solver = dolfinx.fem.PETScKrylovSolver(comm=dolfinx.MPI.comm_world, method="cg")
solver.parameters.absolute_tolerance = 1e-10
solver.solve(problem, u.vector)

# Compute the electric field
E = dolfinx.Function(V)
E.vector[:] = -dolfinx.interpolate(dolfinx.grad(u), V).vector[:]


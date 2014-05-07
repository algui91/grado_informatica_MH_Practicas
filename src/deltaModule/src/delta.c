/*
 *
 *  Created on: Mar 19, 2013
 *  Last commit: $Date$
 *  Author: Alejandro Alcalde <algui91@gmail.com>
 *
 *  A simple tool for show network traffic in a graphic way
 *  Copyright (C) 2013 Alejandro Alcalde
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <Python.h>

#include <stdlib.h>

/* TODO: Check Python version: http://docs.python.org/3/howto/cporting.html */

struct module_state {
  PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *error_out(PyObject *m) {
  struct module_state *st = GETSTATE(m);
  PyErr_SetString(st->error, "something bad happened");
  return NULL;
}

long **f; /* Stream Matrix */
long **d; /* Distance Matrix */

/**
 * Initialize a two dimensional array with only one call to malloc
 *
 * @see http://stackoverflow.com/questions/8740195/how-do-we-allocate-a-2-d-array-using-one-malloc-statement
 */
void **createMatrix(uint rows, uint cols) {

  long **matrix;

  const size_t row_pointers_bytes = rows * sizeof(*matrix);
  const size_t row_elements_bytes = cols * sizeof(**matrix);
  matrix = PyObject_Malloc(row_pointers_bytes + rows * row_elements_bytes);

  if (!matrix) {
    printf("Dentro de !matrix!!!");
    PyErr_NoMemory();
    return NULL;
  }

  size_t i = 0;
  long *data = matrix + rows;
  for (i = 0; i < rows; i++)
    matrix[i] = data + i * cols;

  Py_INCREF(matrix);

  return matrix;
}

/**
 * Pretty print a matrix
 */
void printMatrix(long **m, uint size) {
  int i, j;
  for (i = 0; i < size; ++i) {
    for (j = 0; j < size; ++j) {
      printf(" %d ", m[i][j]);
    }
    printf("\n");
  }
}

static PyObject *initMatrix(PyObject *self, PyObject *args) {
  struct module_state *st = GETSTATE(self);

  PyObject *streamMatrixObj; /* List containing stream matrix */
  PyObject *distanceMatrixObj; /* List containing distance matrix */

  if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &streamMatrixObj,
                        &PyList_Type, &distanceMatrixObj)) {
    return NULL;
  }

  int numLines = PyList_Size(streamMatrixObj);

  f = createMatrix(numLines, numLines);
  /* Populate MAtrix */
  long i_k;

  for (int k = 0; k < numLines; k++) {
    PyObject *first = PyList_GetItem(streamMatrixObj, k);
    for (int i = 0; i < numLines; i++) {
      PyObject *second = PyList_GetItem(first, i);
      i_k = PyLong_AsLong(second);
      f[k][i] = 5l;
      printf("Elemento de matrix %d\n", i_k);
    }
  }

  return (PyObject *) 1;
}

static PyObject *deltaC(PyObject *self, PyObject *args) {
  struct module_state *st = GETSTATE(self);

  int r; /* delimiter tokens for strtok */
  int s; /* number of cols to parse, from the left */

  int numLines; /* how many lines we passed for parsing */
  int line; /* pointer to the line as a string */
  int token; /* token parsed by strtok */

  PyObject *listSolutionObj; /* the list of strings */

  PyObject *itemObj; /* one string in the list */

  /* the O! parses for a Python object (listObj) checked
   to be of type PyList_Type */
  if (!PyArg_ParseTuple(args, "iiO!", &r, &s, &PyList_Type, &listSolutionObj)) {
    return NULL;
  }

  /* get the number of lines passed to us */
  numLines = PyList_Size(listSolutionObj);

  /* should raise an error here. */
  if (numLines < 0)
    return NULL; /* Not a list */

  printMatrix(f, numLines);

  /* iterate over items of the list */
  int i;
  for (i = 0; i < numLines; i++) {

    /* grab the string object from the next element of the list */
    itemObj = PyList_GetItem(listSolutionObj, i); /* Can't fail */

    int item = PyLong_AsLong(itemObj);
    if (item == -1 && PyErr_Occurred())
      /* Integer too big to fit in a C long, bail out */
      return -1;
    printf("Element %d\n", item);

  }
  return (PyObject *) itemObj;  //raise an exception
}

static PyMethodDef delta_methods[] = {
    { "error_out", (PyCFunction) error_out, METH_NOARGS, NULL },
    { "delta", (PyCFunction) deltaC, METH_VARARGS, "QAP Factorization" },
    { "initMatrix", (PyCFunction) initMatrix, METH_VARARGS, "Stream and Distance matrix" },
    { NULL, NULL, 0, NULL } /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static int delta_traverse(PyObject *m, visitproc visit, void *arg) {
  Py_VISIT(GETSTATE(m)->error);
  return 0;
}

static int delta_clear(PyObject *m) {
  Py_CLEAR(GETSTATE(m)->error);
  return 0;
}

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "delta", /* m_name */
  "Module doc, TODO", /* m_doc */
  sizeof(struct module_state), /* m_size */
  delta_methods, /* m_methods */
  NULL, /* m_reload */
  delta_traverse, /* m_traverse */
  delta_clear, /* m_clear */
  NULL /* m_free */
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_gnm(void)

#else
#define INITERROR return

void initdelta(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("delta", delta_methods);
#endif

  if (module == NULL)
    INITERROR;
  struct module_state *st = GETSTATE(module);

  st->error = PyErr_NewException("delta.Error", NULL, NULL);
  if (st->error == NULL) {
    Py_DECREF(module);
    INITERROR;
  }

#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}

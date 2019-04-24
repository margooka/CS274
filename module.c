#include <Python.h>
#include "predicates.c"

static PyObject* mod_sum(PyObject *self, PyObject *args)
{
    int a;
    int b;
    int s;
    if (!PyArg_ParseTuple(args,"ii",&a,&b))
       return NULL;
    s = (a,b);
    return Py_BuildValue("i",s);
}

static PyMethodDef ModMethods[] = {
    {"sum", mod_sum, METH_VARARGS, "Description.."},
    {NULL,NULL,0,NULL}
};

PyMODINIT_FUNC initmod(void)
{
    PyObject *m;
    m = Py_InitModule("module",ModMethods);
    if (m == NULL)
       return;
}
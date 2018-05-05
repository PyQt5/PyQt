#include <Python.h>

// 无参数
PyObject *pydext_hello(PyObject *self) {
	return Py_BuildValue("s", "this is hello function");
}

// 可以解析普通参数
// 这里就解析一个好了
PyObject *pydext_hello2(PyObject *self, PyObject *args) {
	char *name = "";

	if (!PyArg_ParseTuple(args, "s", &name)) {
		PyErr_SetString(PyExc_ValueError, "parameter must be str");
		return NULL;
	}
	return Py_BuildValue("s", name);
}

PyDoc_STRVAR(pydext_sum_doc, "sum(x, y, minus=False)\
\
sum function, if minus=True then return -(x+y)");
// 可以解析普通参数和指定参数
PyObject *pydext_sum(PyObject *self, PyObject *args, PyObject *kwargs) {
    /* Shared references that do not need Py_DECREF before returning. */
    int x = 0;
	int y = 0;
	int minus = 0;

    /* Parse positional and keyword arguments */
    static char* keywords[] = { "x", "y", "minus", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ii|$p", keywords, &x, &y, &minus)) {
		PyErr_SetString(PyExc_ValueError, "x and y must be int, and minus must be True or False");
        return NULL;
    }

    /* Function implementation starts here */
	if (minus == 1)
		return Py_BuildValue("i", -(x + y));
	return Py_BuildValue("i", x + y);
}

/*
 * List of functions to add to pydext in exec_pydext().
 */
static PyMethodDef pydext_functions[] = {
	{ "hello", (PyCFunction)pydext_hello, METH_NOARGS, NULL },
	{ "hello2", (PyCFunction)pydext_hello2, METH_VARARGS, NULL },
    { "sum", (PyCFunction)pydext_sum, METH_VARARGS | METH_KEYWORDS, pydext_sum_doc },
    { NULL, NULL, 0, NULL } /* marks end of array */
};

/*
 * Initialize pydext. May be called multiple times, so avoid
 * using static state.
 */
int exec_pydext(PyObject *module) {
    PyModule_AddFunctions(module, pydext_functions);

    PyModule_AddStringConstant(module, "__author__", "Irony");
	PyModule_AddStringConstant(module, "__mail__", "892768447@qq.com");
    PyModule_AddStringConstant(module, "__version__", "1.0.0");

    return 0; /* success */
}

/*
 * Documentation for pydext.
 */
PyDoc_STRVAR(pydext_doc, "The pydext module");


static PyModuleDef_Slot pydext_slots[] = {
    { Py_mod_exec, exec_pydext },
    { 0, NULL }
};

static PyModuleDef pydext_def = {
    PyModuleDef_HEAD_INIT,
    "pydext",
    pydext_doc,
    0,              /* m_size */
    NULL,           /* m_methods */
    pydext_slots,
    NULL,           /* m_traverse */
    NULL,           /* m_clear */
    NULL,           /* m_free */
};

PyMODINIT_FUNC PyInit_pydext() {
    return PyModuleDef_Init(&pydext_def);
}

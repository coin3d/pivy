/* FIXME: is there a way to overload static class member methods with SWIG? 
 *        20040316 tamer.
 */
%rename(SoNode_getByName_nl) SoNode::getByName(const SbName & name, SoNodeList & l);

/*
%feature("shadow") * SoNode::getByName(const SbName & name) %{
def getByName(*args):
   if len(args) == 3:
  return apply(_pivy.SoNode_getByName_nl,SoNode()+args)
   return apply(_pivy.SoNode_getByName,SoNode()+args)
%}
*/

%extend SoNode {
  static PyObject * getByName_nl(const SbName & name, SoNodeList & l) {
    int nr_of_nodes = SoNode::getByName(name, l);
    return  PyLong_FromLong(nr_of_nodes);
  }
}

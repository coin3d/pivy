%rename(appendConnection_fie) SoField::appendConnection(SoField *master, SbBool notnotify=FALSE);
%rename(appendConnection_vrm) SoField::appendConnection(SoVRMLInterpOutput *master, SbBool notnotify=FALSE);

%feature("shadow") SoField::appendConnection(SoEngineOutput *master, SbBool notnotify=FALSE) %{
def appendConnection(*args):
   if isinstance(args[1], SoField):
      return apply(_coin.SoField_appendConnection_fie,args)
   elif isinstance(args[1], SoVRMLInterpOutput):
      return apply(_coin.SoField_appendConnection_vrm,args)
   return apply(_coin.SoField_appendConnection,args)
%}

%rename(connectFrom_fie) SoField::connectFrom(SoField *master, SbBool notnotify=FALSE, SbBool append=FALSE);

%feature("shadow") SoField::connectFrom(SoEngineOutput *master, SbBool notnotify=FALSE, SbBool append=FALSE) %{
def connectFrom(*args):
   if isinstance(args[1], SoField):
      return apply(_coin.SoField_connectFrom_fie,args)
   return apply(_coin.SoField_connectFrom,args)
%}

%rename(disconnect_eng) SoField::disconnect(SoEngineOutput *engineoutput);
%rename(disconnect_fie) SoField::disconnect(SoField *field);
%rename(disconnect_vrm) SoField::disconnect(SoVRMLInterpOutput *interpoutput);

%feature("shadow") SoField::disconnect(void) %{
def disconnect(*args):
   if isinstance(args[1], SoEngineOutput):
      return apply(_coin.SoField_disconnect_fie,args)
   elif isinstance(args[1], SoField):
      return apply(_coin.SoField_disconnect_fie,args)
   elif isinstance(args[1], SoVRMLInterpOutput):
      return apply(_coin.SoField_disconnect_vrm,args)
   return apply(_coin.SoField_disconnect,args)
%}

%ignore SoField::get(SbString & valuestring);

%extend SoField {
  SbString get() {
    SbString valuestring;
    self->get(valuestring);
    return valuestring;
  }
}

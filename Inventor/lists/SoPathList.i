// add a method for wrapping c++ operator[] access
%extend SoPathList {
  SoPath * __getitem__(int i) {
    return (*self)[i];
  }
}

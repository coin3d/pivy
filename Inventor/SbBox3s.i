#ifndef PIVY_WIN32
%rename(SbBox3s_eq) operator ==(const SbBox3s & b1, const SbBox3s & b2);
%rename(SbBox3s_neq) operator !=(const SbBox3s & b1, const SbBox3s & b2);
#endif

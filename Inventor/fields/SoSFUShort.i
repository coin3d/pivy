// SPDX-License-Identifier: ISC

%extend SoSFUShort {
  void setValue(const SoSFUShort * other) { *self = *other; }
}

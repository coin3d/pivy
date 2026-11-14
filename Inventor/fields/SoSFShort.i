// SPDX-License-Identifier: ISC

%extend SoSFShort {
  void setValue(const SoSFShort * other) { *self = *other; }
}

// SPDX-License-Identifier: ISC

%extend SoSFMatrix {
  void setValue(const SoSFMatrix * other) { *self = *other; }
}

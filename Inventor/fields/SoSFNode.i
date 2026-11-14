// SPDX-License-Identifier: ISC

%extend SoSFNode {
  void setValue(const SoSFNode * other) { *self = *other; }
}

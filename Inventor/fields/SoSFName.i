// SPDX-License-Identifier: ISC

%extend SoSFName {
  void setValue(const SoSFName * other) { *self = *other; }
}

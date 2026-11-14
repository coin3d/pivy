// SPDX-License-Identifier: ISC

%extend SoSFTrigger {
  void setValue(const SoSFTrigger * other) { *self = *other; }
}

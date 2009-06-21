# Copyright 1999-2007 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

inherit eutils distutils subversion

ESVN_REPO_URI="svn://svn.tammura.at/pivy/trunk"

DESCRIPTION="Python Coin bindings"
HOMEPAGE="http://pivy.tammura.at/"
LICENSE="as-is"
SLOT="0"
KEYWORDS="-* ~amd64 ~x86"
IUSE=""

DEPEND="virtual/python
	dev-lang/swig
	media-libs/coin
	media-libs/SoQt"
RDEPEND="${DEPEND}"

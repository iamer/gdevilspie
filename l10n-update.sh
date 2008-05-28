#!/bin/bash

function gen_pot {
	xgettext -L Python -o po/gdevilspie.pot gdevilspie
	xgettext -j -o po/gdevilspie.pot gdevilspie.glade
}

function gen_mo {
	for i in po/*.po; do
		msgfmt -cv $i -o ${i/.po/.mo}
	done
}

function update_po {
	for i in po/*.po; do
		msgmerge -U $i po/gdevilspie.pot
	done
}

case "$@" in
	"update")
		gen_pot; update_po;
		;;
	"updatepot") 
		gen_pot;
		;;
	"generate")
		gen_mo;
		;;
	*)
		echo "Usage: $0 [update|updatepot|generate]";
		;;
esac

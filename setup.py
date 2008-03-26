#!/usr/bin/env python

from distutils.core import setup

setup(name='gdevilspie',
      version='0.3',
      description='GTK GUI for devilspie',
      author='Islam Amer',
      author_email='iamer@open-craft.com',
      url='http://code.google.com/p/gdevilspie/',
	  license='GPLv2',
      packages=['gDevilspie'],
	  scripts=['gdevilspie'],
	  data_files=[('share/gdevilspie',['gdevilspie.glade', 'gdevilspie.png']),
		  ('share/pixmaps/',['gdevilspie.png'])],
     ) 
#FIXME: Add README, etc.	

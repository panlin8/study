#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
	first python 
	hello world
'''

import os
import sys
from configobj import ConfigObj


filename = "./config.ini";

class Basecfg(object):
	def __init__(self, config):

		sbase		= config['BASE'];
		self.tdir	= sbase['tdir'];
		self.cdir	= sbase['cdir'];
		self.main	= sbase['main'];
		self.sub	= sbase['sub'];
	
	def prepare(self):

		if not os.path.exists(self.tdir):
			os.makedirs(self.tdir);		

		if not os.path.exists(self.cdir):
			sys.exit(0);		

	def show(self):

		print "base module [%s]:" %('BASE');

		print "base tdir:			%r" %(self.tdir); 
		print "base cdir:			%r" %(self.cdir); 
		print "base main:			%r" %(self.main); 
		print "base sub:			%r" %(self.sub);  


class Subcfg(Basecfg):
	def __init__(self, config, subname):

		super(Subcfg, self).__init__(config);		

		subbase			= config[subname];
		self.subname	= subname;
		self.subtdir	= subbase['tdir'];
		self.subcdir	= subbase['cdir'];
		self.target		= subbase['target'];
		self.mode		= subbase['mode'];
		self.dep		= subbase['dep'];
		
		self.fulltdir	= self.tdir + self.subtdir;
		self.fullcdir	= self.cdir + self.subcdir;
		self.fullcmd	= 'make '	+ self.mode;

	def prepare(self):

		if not os.path.exists(self.tdir):
			os.makedirs(self.tdir);		

		if not os.path.exists(self.cdir):
			sys.exit(0);

	def domake(self):
		current = os.getcwd();
		os.chdir(self.fullcdir);	
		ret = os.popen(self.fullcmd);
		if not ret.find('make debug is ok'):

		os.chdir(current);	

	def show(self):

		print "sub module [%s]:" %(self.subname);

		print "%s tdir:			%r" %(self.subname, self.subtdir); 
		print "%s cdir:			%r" %(self.subname, self.subcdir); 
		print "%s target:		%r" %(self.subname, self.target); 
		print "%s mode:			%r" %(self.subname, self.mode);  
		print "%s dep:			%r" %(self.subname, self.dep);  
		print "%s fulltdir:		%r" %(self.subname, self.fulltdir);  
		print "%s fullcdir:		%r" %(self.subname, self.fullcdir);  
		print "%s fullcmd:		%r" %(self.subname, self.fullcmd);  

if __name__ == "__main__":

	config = ConfigObj(filename);
	
	base = Basecfg(config);
	base.show();
	
	for i in base.sub:

		submodule = Subcfg(config, i);	
		submodule.show();

		if submodule.dep:

			depmodule = Subcfg(config, submodule.dep);	


	




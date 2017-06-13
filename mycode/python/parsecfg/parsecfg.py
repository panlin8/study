#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
	first python 
	hello world
'''

import os
import sys
import logging
import subprocess
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
			logging.error('[%s]: %r is not exists!' %('BASE' ,self.cdir));
			sys.exit(0);		

	def show(self):
		logging.debug('base module [%s]:' %('BASE'));
		logging.debug('base tdir:			%r' %(self.tdir)); 
		logging.debug('base cdir:			%r' %(self.cdir)); 
		logging.debug('base main:			%r' %(self.main)); 
		logging.debug('base sub:			%r' %(self.sub));  


class Subcfg(Basecfg):
	def __init__(self, config, subname):
		super(Subcfg, self).__init__(config);		

		subbase			= config[subname];
		self.subname	= subname;
		self.subtdir	= subbase['tdir'];
		self.subcdir	= subbase['cdir'];
		self.target		= subbase['target'];
		self.cmd		= subbase['cmd'];
		self.move		= subbase['move'];
		self.deps		= subbase['deps'];
		
		self.fulltdir	= self.tdir + self.subtdir;
		self.fullcdir	= self.cdir + self.subcdir;
		self.movecmd    = [];

		for target in self.target:
			##self.movecmd.append('mv '	+ self.fullcdir + '/' + target + ' ' + self.fulltdir);
			self.movecmd.append('cp '	+ self.fullcdir + '/' + target + ' ' + self.fulltdir + ' -rf');

	def prepare(self):
		if not os.path.exists(self.fulltdir):
			os.makedirs(self.fulltdir);		

		if not os.path.exists(self.fullcdir):
			logging.error('[%s]: dir %r is not exists!' %(self.subname, self.fullcdir));
			sys.exit(0);

	def domake(self):
		for cmd in self.cmd:
			ret = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
					shell = True, cwd = self.fullcdir).stdout.read();

			if not ret.find('make: ***') < 0:
				logging.debug(ret);
				logging.error('[%s]: exec cmd %s is error!' %(self.subname, cmd));
				sys.exit(0);
		
		for target in self.target:
			if not os.path.isfile(self.fullcdir+'/'+target):
				logging.error('[%s]: target %s is missing' %(self.subname, target));
				sys.exit(0);

	def domove(self):
		if self.move == 'yes':
			for cmd in self.movecmd:
				subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = None, shell = True);
		logging.info('[%s]: is success!' %(self.subname));

	def show(self):
		logging.debug('sub module [%s]:' %(self.subname));
		logging.debug('%-15s target:		%r' %(self.subname, self.target)); 
		logging.debug('%-15s cmd:			%r' %(self.subname, self.cmd));  
		logging.debug('%-15s move:			%r' %(self.subname, self.move));  
		logging.debug('%-15s deps:			%r' %(self.subname, self.deps));  
		logging.debug('%-15s fulltdir:		%r' %(self.subname, self.fulltdir));  
		logging.debug('%-15s fullcdir:		%r' %(self.subname, self.fullcdir));  
		logging.debug('%-15s movecmd:		%r' %(self.subname, self.movecmd));  

def loginit():
	logging.basicConfig(level=logging.DEBUG, 
		format='%(filename)s %(levelname)s %(message)s', 
		datafmt='%a, %d %b %Y %H:%M:%S', 
		filename='parsecfg.log',
		filemode='w' );

	console = logging.StreamHandler();
	console.setLevel(logging.INFO);
	formatter = logging.Formatter('%(filename)-12s [line:%(lineno)d] : %(levelname)-8s %(message)s');
	console.setFormatter(formatter);
	logging.getLogger('').addHandler(console);


if __name__ == "__main__":

	loginit();

	config = ConfigObj(filename);
	
	base = Basecfg(config);
	base.show();
	
	for i in base.sub:

		submodule = Subcfg(config, i);	
			
		for dep in submodule.deps:
			depmodule = Subcfg(config, dep);	
			depmodule.show();
			depmodule.prepare();
			depmodule.domake();
			depmodule.domove();

		submodule.show();
		submodule.prepare();
		submodule.domake();
		submodule.domove();



	




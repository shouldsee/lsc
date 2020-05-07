import importlib
from ._shell import pipe__getResult,pipe__getSafeResult,shellpopen
from ._shell import _shellcmd, shellcmd, list_flatten, list_flatten_strict
import io,time
# from spiper._types import Path

import json
import warnings

import json
import os
import tempfile
import six
VERSION = '0.0.1'


def SafeShellCommand(CMD, check=1, shell=0, encoding='utf8',stdin=None,stdout = None,stderr = None, silent=1):
	suc,stdout,stderr = _shellcmd(CMD,check,shell,encoding,stdin,stdout,stderr,silent)
	return stdout

if 1:
	def LoggedShellCommand(
		CMD, file='/dev/null', check=1, mode='w', encoding = 'utf8',
		stdin = None,stdout=None, stderr=None, 
		silent=1,
		shell=0,
		):
		'''
		CMD:
			a list of commands to be joined with ' ' and executed in bash
		file: None or a string-like filename or a file-handle
			if None, use a StringIO
		check:
			whether to raise error if the shell execution fails.
		shell:
			whether to treat CMD as a joined string or a list of string.

		'''
		if file is None:
			file = io.StringIO()
		if not isinstance(file,io.IOBase):
			file = open(file,'a',buffering=1)
		# if not shell:
		assert not shell
		CMD = list_flatten_strict(CMD)
		CMD = ['set','-euxo','pipefail;'] + CMD
		# shell = 1
		# with file:
		t0 = time.time()
		def _dump(o,f,**kw):
			return json.dump(list(o)+['VERSION',VERSION],f,**kw)
		_dump( ['CommandStart',-1, t0, ],file)
		file.write('\n')
		_dump( ['CommandText',] + ' '.join(CMD).splitlines(), file,indent=2)
		file.write('\n')
		# stdout = io.BytesIO(mode='w')
		# stderr = io.BytesIO()
		suc,stdout,stderr = _shellcmd(CMD,check,shell,encoding,stdin,stdout,stderr,silent)
		t1 = time.time()
		_dump( ['CommandEnd', suc, t1, (size_humanReadable(t1-t0,'s'), t1-t0)],file)
		file.write('\n')
		_dump( ['CommandResult',
			'stdout',stdout.splitlines(),
			'stderr',stderr.splitlines()],file,indent=2,default=repr)
		file.write('\n')
		file.flush()
		if check:
			if not suc:
				errmsg = 'Command "{CMD}" returned error:\n[stdout]:{stdout}\n[stderr]:{stderr}'.format(**locals())		
				raise Exception(errmsg)
			return stdout
		return suc, stdout, stderr, file


	def size_humanReadable(num,suffix='B',fmt='{0:.2f}',units=['','K','M','G','T', 'P','E'],):
	    """ Returns a human readable string reprentation of bytes,
	    Source: https://stackoverflow.com/a/43750422/8083313"""
	    if num < 1024:
	    	return fmt.format(num) + units[0] + suffix 
	    else:
	    	return size_humanReadable( num/1024.,fmt, suffix,units[1:])



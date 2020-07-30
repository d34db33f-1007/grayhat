#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, requests, json
import asyncio

from typing import List
from concurrent.futures import ThreadPoolExecutor
from strongtyping.config import SEVERITY_LEVEL
from strongtyping.strong_typing import match_typing



class ForbiddenAccess(Exception):
	pass


class Build:

	@match_typing(severity=SEVERITY_LEVEL.WARNING)
	def __init__(self, api_k: str = None):
		self.api_k = api_k
		self.url = 'https://buckets.grayhatwarfare.com/api/v1'

	@match_typing
	def Buckets(self, start = 0, stop=None, b_id=None, kw: List[str] = []):
		buck = self.url
		buck += f'/bucket/{b_id}/files' if b_id else '/buckets'
		buck += f'/{start}/{stop}' if stop else f'/{start}'
		buck += f'?access_token={self.api_k}'
		if len(kw) > 0 and b_id:
			buck += f'&keywords='
			e = '%20' if len(kw) > 1 else ''
			for k in kw:
				n = kw.index(k)
				if n > 0 and not k.startswith('-'):
					continue
				buck += f'{k}{e}' if n < (len(kw) -1) else f'{k}'
		elif len(kw) > 0 and not b_id:
			buck += f'&keywords={kw[0]}'
		return buck

	@match_typing
	def Files(self, start = 0, stop=None, kw: List[str] = [], ext: List[str] = []):
		file = f'{self.url}/files'
		if kw and 0 < len(kw) < 5:
			with open('exclude.txt', 'r') as negative:
				for trash in negative.read().split(','):
					if trash.startswith('-'):
						kw += trash.split()
		if kw and len(kw) > 0:
			e = '%20' if len(kw) > 1 else ''
			file += '/'
			for k in kw:
				n = kw.index(k)
				if n > 0 and not k.startswith('-'):
					continue
				file += f'{k}{e}' if n < (len(kw) -1) else f'{k}'
		file += f'/%20' if len(kw) < 1 else ''
		file += f'/{start}/{stop}' if stop else f'/{start}'
		file += f'?access_token={self.api_k}'
		if ext and len(ext) > 0:
			e = '%2C' if len(ext) > 1 else ''
			file += f'&extensions='
			for ex in ext:
				if ex.startswith('.'):
					ex = ex.replace('.', '')
				file += f'{ex}{e}'
		return file


class s3:

	@match_typing(severity=SEVERITY_LEVEL.WARNING)
	def __init__(self, url: str, var: int = None):
		self.pl = url
		self.list = []
		self.var = var
		self.executor = ThreadPoolExecutor(200)

		typ = self.pl.split('/')
		if 'bucket' in typ or 'files' in typ:
			self.call = self.files(self.var)
		elif 'buckets' in typ:
			self.call = self.buckets(self.var)

	def search(self):
		resp = requests.get(self.pl, timeout=5)
		if resp.status_code == 200:
			return resp.json()
		elif resp.status_code == 401:
			raise ForbiddenAccess('Check your access token.')
		else:
			print(f'[Code: {resp.status_code}] Connection error..')
			sys.exit(0)

	async def buckets(self, fc: int = None):
		Buckets = self.search()
		self.list.append(f"Bucket count: {Buckets['buckets_count']}")
		for buck in Buckets['buckets']:
			buc = {}
			buc['bid'] = buck['id']
			buc['bucket'] = buck['bucket']
			buc['file_count'] = buck['fileCount']
			if fc and int(buck['fileCount']) < fc:
				continue
			self.list.append(buc)
		return self.list

	async def files(self, size: int = None):
		Files = self.search()
		self.list.append(f"File count: {Files['results']}")
		await asyncio.gather(*[self.f_proc(file, size) for file in Files['files']])
		return self.list

	async def f_proc(self, file, size: int = None, gap=False):
		buc = {}
		buc['fid'] = file['id']
		buc['bid'] = file['bucketId']
		buc['bucket'] = file['bucket']
		buc['filename'] = file['filename']
		buc['file_path'] = file['fullPath']
		buc['file_url'] = file['url']
		if 'bucket' in self.pl.split('/'):
			mb = float(f"{int(file['size']) / 1048576}")
			buc['file_size'] = f'{int(mb)}Mb'
			gap = True

		"""This chunk of shit-code bypasses grayhats' free account limitation
			and letting us use keywords + extensions and filter by files size
			at same time in 200 parallel threads ;) """

		if size and not gap:
			if int(file['size']) < 1: # '%20' not in self.pl.split('/')
				try:
					req = asyncio.get_event_loop().run_in_executor(self.executor, requests.head, file['url'])
					r = await req
					mb = int(r.headers['Content-Length']) / 1048576
				except:
					return False
				buc['file_size'] = f'{int(mb)}Mb'
				if mb < size:
					return False
			else:
				gap = True
				mb = float(f"{int(file['size']) / 1048576}")
				buc['file_size'] = f'{int(mb)}Mb'
		if size and gap:
			if mb < size:
				return False
		self.list.append(buc)

	@match_typing
	def warfare(self, var: int = None):
		return asyncio.run(self.call)


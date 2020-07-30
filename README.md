### Python library for grayhatwarfare.com with small hacks

The author of this code **is not responsible** for any illegal actions. \
For educational purposes only..

This code requires an free account at grayhatwarfare.com \
I've also implemented small hack to avoid one of limitations for free plan users. \
So now you can easily use multiple keyword and extension filters with files size sorting while searching for files ;)

#### Install

* `git clone https://github.com/d34db33f-1007/grayhat.git`
* `cd grayhat && pip3 install -r requirements.txt`

#### Basic Usage

```
token = 'fill_ur_token'
keywords = ['sql', 'data', '-html']
extensions = ['bak', 'bac', 'dmp', 'dat']

# search files by keywords and file extensions and 100Mb minimum file size
bless = Build(token)
bless = bless.Files(start=0, stop=998, kw=keywords, ext=extensions)
god = s3(bless, var=100).warfare()

# list all files from specific bucket defined by "b_id" and filter them by size and keyword
bless = Build(token)
bless = bless.Buckets(b_id=2456, stop=200, kw=['Full'])
god = s3(bless, 100).warfare()

# search all buckets by keyword for bugbounty or dely search and filter buckets with at least 10 files exposed
bless = Build(token)
bless = bless.Buckets(kw=keywords)
god = s3(bless, 10).warfare()


# "s3(bless).warfare()" returns list with each result as dictionary

print(god[0])
for tears in god[1:]:
	print(tears['bid'], tears['file_url'], tears['file_size']) # 1st and 2nd methods
  print(tears['bid'], tears['bucket'], tears['file_count']) # 3d method

# "fid", "bucket", "filename", "file_path"] keys are also for methods 1 and 2.

# "kw" and "ext" are optional and theese must be list type. "var" is digit and is optional either.
# you can get only 1000 results per one request with free plan account
# so "start" is for results index, and "stop" means count of results
# e.q. page one: start = 0, stop = 999; page two: start = 999, stop = 999; and so on
# you can exclude from search results unlimited count of queries
# to do this just add them to excludes.txt file
# to exclude specific bucket add "-sbuc34682" to excludes
# where "34682" is bucket id.
```

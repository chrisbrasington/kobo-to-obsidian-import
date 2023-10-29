## Columns in table
```
PRAGMA table_info(Bookmark);
```
```
0|BookmarkID|TEXT|1||1
1|VolumeID|TEXT|1||0
2|ContentID|TEXT|1||0
3|StartContainerPath|TEXT|1||0
4|StartContainerChildIndex|INTEGER|1||0
5|StartOffset|INTEGER|1||0
6|EndContainerPath|TEXT|1||0
7|EndContainerChildIndex|INTEGER|1||0
8|EndOffset|INTEGER|1||0
9|Text|TEXT|0||0
10|Annotation|TEXT|0||0
11|ExtraAnnotationData|BLOB|0||0
12|DateCreated|TEXT|0||0
13|ChapterProgress|REAL|1|0|0
14|Hidden|BOOL|1|0|0
15|Version|TEXT|0||0
16|DateModified|TEXT|0||0
17|Creator|TEXT|0||0
18|UUID|TEXT|0||0
19|UserID|TEXT|0||0
20|SyncTime|TEXT|0||0
21|Published|BIT|0|false|0
22|ContextString|TEXT|0||0
23|Type|TEXT|0||0
```
## Bookmark
```
select Type, Text, ContentID from Bookmark;
```
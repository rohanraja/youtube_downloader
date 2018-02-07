processUrl:
	celery worker -A processUrl -l info -c 2 -Q processUrl

youdl:
	celery worker -A processUrl -l info -c 3 -Q youdownload

flower:
	celery -A processUrl flower

listen:
	python linksCacher.py 1> ${HOME}/log/linkscatcher.log

processUrlVLC:
	celery worker -A processUrl -l info -c 2 -Q processVLCUrl

checkMusic:
	celery worker -A processUrl -l info -c 8 -Q checkMusic

convertmp3:
	celery worker -A processUrl -l info -c 2 -Q convertmp3

sync:
	while inotifywait -r -e modify,create,delete /Volumes/Fireice/Users/rohanraja/Downloads/youdl/yoump3; do
			rsync -avz /Volumes/Fireice/Users/rohanraja/Downloads/youdl/yoump3 /Volumes/CMP3
	done

onesync:
		rsync --progress -avz /Volumes/Fireice/Users/rohanraja/Downloads/youdl/yoump3/ /Volumes/CMP3/

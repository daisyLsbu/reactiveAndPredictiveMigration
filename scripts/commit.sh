pip freeze > requirement.txt
git pull origin monitor
git add .
git commit -m $1
git pull origin monitor
git push -u origin monitor
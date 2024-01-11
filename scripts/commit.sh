#this file is used to commit the changes to telemetry branch, add the comment as argument
pip freeze > requirement.txt
git pull origin telemetry
git add .
git commit -m $1
git pull origin telemetry
git push -u origin telemetry

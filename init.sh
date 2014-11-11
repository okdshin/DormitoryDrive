set -o pipefail
set -e
rm /tmp/test.db
rm static/upload/*
python init_db.py


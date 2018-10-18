all: app.py
	rm data/bigData.db
	python app.py

db:
	rm data/bigData.db

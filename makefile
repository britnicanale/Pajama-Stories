all:
	echo "You can type <make db> to delete the database and create a new one."

db:
	rm data/bigData.db
	python util/makeData.py
	echo "Now you have an empty database. Go register in some users!"

makeData:
	python util/makeData.py
	echo "Now you have an empty database. Go register in some users!"

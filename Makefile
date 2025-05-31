build: clean
	./scripts/build.sh $$(pwd)

clean:
	./scripts/clean.sh dist

cleanall:
	./scripts/clean.sh dist .venv

init:
	./scripts/init.sh $$(pwd)
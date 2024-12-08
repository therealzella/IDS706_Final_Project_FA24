.PHONY: install run-backend run-frontend test clean

install:
	cd review_service && make install
	cd frontend_service && make install

run-backend:
	cd review_service && make run

run-frontend:
	cd frontend_service && make run

run: run-backend run-frontend

clean:
	cd review_service && make clean
	cd frontend_service && make clean
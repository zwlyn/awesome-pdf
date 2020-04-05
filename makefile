dev:
	python reportdesigner.py

deps:
	npm install -s --registry=https://registry.npm.taobao.org

vue:
	cd vue-sites && npm run build
	cp -rf vue-sites/dist/* static/
	cd ..
	python build.py static/index.html

release:
	rm -rf release
	mkdir -p release
	cp -rf controller release
	cp -rf jsontemplates release
	cp -rf data release
	cp -rf log release
	cp -rf logo release
	cp -rf reportbro release 
	cp -rf site-packages-27 release
	cp -rf site-packages-37 release
	cp -rf static release
	cp -rf utils release
	cp -rf view release
	cp -rf reportdesigner.py release
	cp -rf setup.py release
	cd release && python setup.py build_ext --inplace

	cp release/controller/controller/*.so  release/controller/ && rm -rf release/controller/controller/ && rm -rf release/controller/build
	cp release/reportbro/reportbro/*.so  release/reportbro/ && rm -rf release/reportbro/reportbro/ && rm -rf release/reportbro/build
	cp release/view/view/*.so  release/view/ && rm -rf release/view/view/ && rm -rf release/view/build
	tar -cvf release.tar release
.PHONY: dev deps release

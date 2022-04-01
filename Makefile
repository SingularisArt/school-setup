install:
	./init-config.sh
	mkdir -p ~/.config/lesson-manager/
	cp ./config.yaml ~/.config/lesson-manager/
uninstall:
	rm -rf ~/.config/lesson-manager/

install:
	mkdir -p ~/.config/lesson-manager
	cp -r ~/.config/lesson-manager/config.yaml ~/.config/lesson-manager/config.yaml.back || echo ""
	./init-config.sh
uninstall:
	rm -rf ~/.config/lesson-manager/

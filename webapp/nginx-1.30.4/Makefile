
default:	build

clean:
	rm -rf Makefile objs

.PHONY:	default clean

build:
	$(MAKE) -f objs/Makefile

install:
	$(MAKE) -f objs/Makefile install

modules:
	$(MAKE) -f objs/Makefile modules

upgrade:
	/Users/jenilbuha/Desktop/sem7/Mlops/p3/nginx-1.30.4/sbin/nginx -t

	kill -USR2 `cat /Users/jenilbuha/Desktop/sem7/Mlops/p3/nginx-1.30.4/logs/nginx.pid`
	sleep 1
	test -f /Users/jenilbuha/Desktop/sem7/Mlops/p3/nginx-1.30.4/logs/nginx.pid.oldbin

	kill -QUIT `cat /Users/jenilbuha/Desktop/sem7/Mlops/p3/nginx-1.30.4/logs/nginx.pid.oldbin`

.PHONY:	build install modules upgrade

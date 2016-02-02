# Dockerfile

## el7

If you want to build in el7, use [Dockerfile](https://github.com/kazuhisya/nodejs-rpm/blob/master/Dockerfile) in the project root directory.


```bash
# Example
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ docker build -t el7-nodejs:XXXX .
```

## el6

If you want to build in el6, use [Dockerfile-el6](https://github.com/kazuhisya/nodejs-rpm/blob/master/docker/Dockerfile-el6) in the [docker](https://github.com/kazuhisya/nodejs-rpm/tree/master/docker) directory.

```bash
# Example
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ docker build -t el6-nodejs:XXXX -f docker/Dockerfile-el6 .
```

## el5

If you want to build in el5, use [Dockerfile-el5](https://github.com/kazuhisya/nodejs-rpm/blob/master/docker/Dockerfile-el5) in the [docker](https://github.com/kazuhisya/nodejs-rpm/tree/master/docker) directory.

```bash
# Example
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ docker build -t el5-nodejs:XXXX -f docker/Dockerfile-el5 .
```

FROM mysql:latest

EXPOSE 3306

ENV MYSQL_ROOT_PASSWORD=testtest

ADD ./my.cnf /etc/mysql/conf.d/my.cnf

CMD ["mysqld"]
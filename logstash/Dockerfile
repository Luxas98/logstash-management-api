FROM docker.elastic.co/logstash/logstash:7.6.0
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
ADD presto-jdbc-0.234.jar /usr/share/logstash/logstash-core/lib/jars/presto-jdbc-0.234.jar
ADD sqljdbc_8.2/enu/mssql-jdbc-8.2.0.jre11.jar /usr/share/logstash/logstash-core/lib/jars/mssql-jdbc-8.2.0.jre11.jar

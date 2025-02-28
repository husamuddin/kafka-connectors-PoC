  FROM confluentinc/cp-kafka-connect-base:7.9.0
  USER root

  # Create directory and copy the correct AWS RDS CA bundle
  RUN mkdir -p /tmp/certs
  RUN curl -o /tmp/certs/rds-combined-ca-bundle.pem \
    -sSL https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
  RUN cp /tmp/certs/rds-combined-ca-bundle.pem /etc/pki/ca-trust/source/anchors/aws-rds-ca.crt &&\
    update-ca-trust extract

  # Import into Java truststore
  RUN keytool -importcert -alias aws-rds-ca \
      -file /tmp/certs/rds-combined-ca-bundle.pem \
      -keystore /etc/pki/java/cacerts \
      -storepass changeit -trustcacerts -noprompt

  # Set Java truststore explicitly
  ENV JAVA_OPTS="-Djavax.net.ssl.trustStore=/etc/pki/java/cacerts -Djavax.net.ssl.trustStorePassword=changeit"

  USER appuser

  RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:1.9.1
  RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest

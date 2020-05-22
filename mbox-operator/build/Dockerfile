FROM quay.io/operator-framework/ansible-operator:v0.16.0

USER root
RUN dnf install gcc libpq libpq-devel python3-devel krb5-devel -y
RUN pip3.6 install psycopg2 koji
USER ${USER_ID}

COPY requirements.yml ${HOME}/requirements.yml
RUN ansible-galaxy collection install -r ${HOME}/requirements.yml \
    && chmod -R ug+rwx ${HOME}/.ansible

COPY watches.yaml ${HOME}/watches.yaml

COPY roles/ ${HOME}/roles/

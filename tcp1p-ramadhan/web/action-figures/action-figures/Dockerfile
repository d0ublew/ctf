FROM php:7.4.33-bullseye

RUN apt-get update && apt-get upgrade -y

RUN apt-get install cron supervisor -y

RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN echo "fake{wih_gg_sih_kalian}" > /flag.txt

COPY dist /chall/
COPY dist /root/dist_cleanup
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY conf/cleanup-cron /etc/cron.d/cleanup-cron
COPY conf/cleanup.sh /root/cleanup.sh

RUN chmod 0644 /etc/cron.d/cleanup-cron
RUN crontab /etc/cron.d/cleanup-cron
RUN chmod +x /root/cleanup.sh
RUN chmod 0644 /etc/supervisor/conf.d/supervisord.conf
RUN chmod -R 777 /chall/

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
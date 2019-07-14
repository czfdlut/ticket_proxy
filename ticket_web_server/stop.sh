ps -ef|grep ticket_web_server | awk '{print $2}' | grep -v 'grep' | xargs kill -9

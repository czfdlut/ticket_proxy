ps -ef|grep ticket_server | awk '{print $2}' | grep -v 'grep' | xargs kill -9

// socket_pool.h (2014-04-23)
// Li Xinjie (xjason.li@gmail.com)

#ifndef QLOG_SOCKET_POOL_H_
#define QLOG_SOCKET_POOL_H_

#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <set>
#include <deque>
#include <list>
#include <string>
#include <vector>
#include <log4cplus/helpers/timehelper.h>
#include <poll.h>

namespace qlog {

struct SocketOptions {
    int snd_timeout;
    int snd_buffer;
    int rcv_timeout;
    int rcv_buffer;
    bool keep_alive;
    bool cloexec;
    bool nonblock;
    int connect_delay;
    int connect_timeout;
    int poll_interval;
    int count;
    bool check;

    SocketOptions();
};

class SocketPool;
class Peer {
public:
    Peer(const std::string& host, int port, SocketPool* pool);
    ~Peer() {}

    bool Resolve();
    bool IsResolved() const { return addr_.s_addr != 0; }

    const std::string& host() const { return host_; }
    int port() const { return port_; }
    const struct in_addr& addr() const { return addr_; }

    const SocketOptions& options() const;
private:
    const std::string host_;
    int port_;
    struct in_addr addr_;
    SocketPool* pool_;
};

class Socket {
public:
    Socket(const Peer* peer);
    ~Socket();

    bool Open();
    void Close();
    bool Check();

    const Peer* peer() const { return peer_; }
    int socket() const { return socket_; }
private:
    const Peer* peer_;
    int socket_;
};


class SocketPool {
public:
    SocketPool(const SocketOptions& options);
    ~SocketPool();

    bool AddPeer(const std::string& host, int port);

    Socket* Get(pthread_mutex_t* mtx,
            const log4cplus::helpers::Time& time);
    void Release(Socket* socket);

    const SocketOptions& options() const { return options_; }

private:
    void Poll(log4cplus::helpers::Time now, int wait);

    SocketOptions options_;
    log4cplus::helpers::Time poll_time_;
    pthread_cond_t cond_;

    struct TimedSocket {
    public:
        TimedSocket(Socket* socket,
                const log4cplus::helpers::Time& time)
            : socket_(socket), time_(time) {}
        Socket* socket() const { return socket_; }
        const log4cplus::helpers::Time& time() const { return time_; }
    private:
        Socket* socket_;
        log4cplus::helpers::Time time_;
    };

    std::vector<Peer*> peers_;
    std::vector<Socket*> sockets_;
    size_t using_sockets_;
    std::list<Socket*> ready_sockets_;
    std::list<TimedSocket> polling_sockets_;
    std::list<TimedSocket> closed_sockets_;

    std::vector<struct pollfd> pfds_;
    std::vector<std::list<TimedSocket>::iterator> ppos_;
};

} // namespace qlog

#endif // QLOG_SOCKET_POOL_H_

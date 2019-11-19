#ifndef QLOG_SOCKET_BUFFER_H_
#define QLOG_SOCKET_BUFFER_H_

#include <string>
#include <log4cplus/config.hxx>


namespace qlog {

class SocketBuffer
{
public:
    explicit SocketBuffer(size_t max);
    virtual ~SocketBuffer();

    char *getBuffer() const { return buffer; }
    std::size_t getMaxSize() const { return maxsize; }
    std::size_t getSize() const { return size; }
    void setSize(std::size_t s) { size = s; }
    std::size_t getPos() const { return pos; }

    unsigned char readByte();
    unsigned short readShort();
    unsigned int readInt();
    std::string readString(unsigned char sizeOfChar);

    void appendByte(unsigned char val);
    void appendShort(unsigned short val);
    void appendInt(unsigned int val);
    void appendString(const std::string& str);
    void appendBuffer(const SocketBuffer& buffer);

    void Clear() {
        size = 0;
        pos = 0;
    }

private:
    // Data
    std::size_t maxsize;
    std::size_t size;
    std::size_t pos;
    char *buffer;

    SocketBuffer(SocketBuffer const & rhs);
    SocketBuffer& operator= (SocketBuffer const& rhs);
};

} // namespace qlog

#endif // LOG4CPLUS_HELPERS_SOCKET_HEADER_

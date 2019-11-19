#ifndef QLOG_QLOG_H_
#define QLOG_QLOG_H_

#include <stdarg.h>
#include <cerrno>
#include <cstring>
#include <string>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include "level.h"

namespace qlog {

const size_t kMaxLogSize = 2 << 20;

/**
 * key/value数组类型定义
 */
typedef std::pair<std::string, std::string> KeyValue;
typedef std::vector<KeyValue> ConfigList;

/**
 * 从配置文件加载日志设置
 *
 * @param configfile 配置文件名。
 */
void qLogConfig(const std::string& configfile);

/**
 * 从key/value数组加载日志配置
 *
 * @param mlist  key/value数组
 */
void qLogConfig(ConfigList& mlist);

/**
 * 快速配置日志
 *
 * @note 如果filename等于CONSOLE，日志显示在屏幕上。
 * @param level    记录级别
 * @param filename 日志文件名前缀("CONSOLE","","/home/s/log/","../myapp_")
 */
void qLogQuickConfig(Level level=QLOG_INFO, const std::string& filename="CONSOLE");

/**
 * 显示当前全部类别日志信息
 */
void qLogViewConfig();

/**
 * 清除所有日志设置
 */
void qLogCleanConfig();

/**
 * 在对象生存周期内监视配置文件，动态配置
 */
class qLogMonitor {
public:
    qLogMonitor(const std::string& filename, unsigned int millis = 60 * 1000);
    ~qLogMonitor();

private:
    // Disable copy
    qLogMonitor(const qLogMonitor&);
    qLogMonitor& operator=(qLogMonitor&);
    void* handle;
};

/**
 * 判断日志是否记录
 *
 * @param name     日志类别
 * @param level    日志级别
 *
 * @return true: 记录日志
 */
bool isLog(const std::string& name, int level);

void qLogInternalDebug(bool isDebug);

void qLogAllv(const std::string& name
        , int level
        , int eNo
        , bool bThrow
        , const char* file
        , int line
        , const char* fmt, va_list ap);

//用于支持变参格式化输出
void qLogAll(const std::string& name
        , int level
        , int eNo
        , bool bThrow
        , const char* file
        , int line
        , const char* fmt,...)
    __attribute__ ((format (printf, 7, 8)));

//用于支持流式输出
void qLogAllStream(const std::string& name
        , int level
        , const std::string& message
        , const char* file
        , int line);

/**
 * qlog的stream接口
 */
class logstream : public std::ostringstream {
public:
    logstream(const std::string& name
            , int level
            , int eNo
            , const char* file
            , int line)
        : m_name(name)
          , m_level(level)
          , m_eNo(eNo)
          , m_file(file)
          , m_line(line) {}

    logstream& l_value() { return *this; }

    ~logstream()
    {
        if ( isLog(m_name, m_level) ) {
            logstream& _s = *this;
            if ( m_eNo != 0 ) {
                _s << " -- (" << m_eNo << ')' << strerror(m_eNo);
            }

            qLogAllStream(m_name, m_level, _s.str(), m_file, m_line);
        }
    }

private:
    std::string m_name;
    int m_level;
    int m_eNo;
    const char* m_file;
    int m_line;
    logstream( const logstream& );
    logstream& operator=( const logstream& );
};

} // namespace qlog

/**
 * 变参记录level级别信息到日志类别类别 name 中，fmt格式与 printf 相同.
 */
#define qLog(name, level, fmt, ...)	\
    qlog::qLogAll(name, level, 0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录跟踪信息到日志类别 name 中，fmt格式与 printf 相同.
 */
#define qLogTrace(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_TRACE, 0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录调试信息到日志类别 name 中，fmt格式与 printf 相同.
 */
#define qLogDebug(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_DEBUG, 0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录提示信息到日志类别 name 中，fmt格式与 printf 相同.
 */
#define qLogInfo(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_INFO,  0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )


#define qLogWarn(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_WARN, 0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录应用错误信息到日志类别 name 中，fmt格式与 printf 相同.
 */
#define qAppError(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, 0, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录系统错误信息到日志类别 name 中，fmt格式与 printf 相同.(附加系统错误信息)
 */
#define qSysError(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, errno, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录应用错误信息到日志类别 name 中并抛出异常整数 0，fmt格式与 printf 相同.
 */
#define qAppThrow(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, 0, true, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录系统错误信息到日志类别 name 中并抛出异常整数 errno，fmt格式与 printf 相同.
 */
#define qSysThrow(name, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, errno, true, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录错误信息到日志类别 name 中，fmt格式与 printf 相同.(附加eNo对应的系统错误信息)
 */
#define qLogError(name, eNo, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, eNo, false, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )

/**
 * 变参记录错误信息到日志类别 name 中并抛出异常整数 eNo，fmt格式与 printf 相同.
 */
#define qLogThrow(name, eNo, fmt, ...)	\
    qlog::qLogAll(name, qlog::QLOG_ERROR, eNo, true, __FILE__, __LINE__, fmt, ## __VA_ARGS__ )


/**
 * 流式记录level级别信息到日志类别 name 中.
 */
#define qLogs(name,level)	 \
    qlog::logstream(name,level,0,__FILE__,__LINE__).l_value()

/**
 * 流式记录跟踪信息到日志类别 name 中.
 */
#define qLogTraces(name)	 \
    qlog::logstream(name,qlog::QLOG_TRACE,0,__FILE__,__LINE__).l_value()

/**
 * 流式记录调试信息到日志类别 name 中.
 */
#define qLogDebugs(name)	 \
    qlog::logstream(name,qlog::QLOG_DEBUG,0,__FILE__,__LINE__).l_value()

/**
 * 流式记录提示信息到日志类别 name 中.
 */
#define qLogInfos(name)		 \
    qlog::logstream(name,qlog::QLOG_INFO, 0,__FILE__,__LINE__).l_value()

/**
 * 流式记录提示信息到日志类别 name 中.
 */
#define qLogWarns(name)		 \
    qlog::logstream(name,qlog::QLOG_WARN, 0,__FILE__,__LINE__).l_value()

/**
 * 流式记录应用错误信息到日志类别 name 中.
 */
#define qAppErrors(name) 	 \
    qlog::logstream(name,qlog::QLOG_ERROR,0,__FILE__,__LINE__).l_value()

/**
 * 流式记录系统错误信息到日志类别 name 中.(附加系统错误信息)
 */
#define qSysErrors(name) 	 \
    qlog::logstream(name,qlog::QLOG_ERROR,errno,__FILE__,__LINE__).l_value()

/**
 * 流式记录错误信息到日志类别 name 中.(附加eNo对应的系统错误信息)
 */
#define qLogErrors(name,eNo) \
    qlog::logstream(name,qlog::QLOG_ERROR,eNo,__FILE__,__LINE__).l_value()

/**
 * 记录应用错误信息到日志类别 name 中并抛出异常整数 0，logEvent为输出流.
 */
#define qAppThrows(name, logEvent) \
    qLogAndThrows(name, qlog::QLOG_ERROR, 0, logEvent)

/**
 * 记录系统错误信息到日志类别 name 中并抛出异常整数 errno，logEvent为输出流.
 */
#define qSysThrows(name, logEvent) \
    qLogAndThrows(name, qlog::QLOG_ERROR, errno, logEvent)

/**
 * 记录错误信息到日志类别 name 中并抛出异常整数 eNo，logEvent为输出流.
 */
#define qLogThrows(name, eNo, logEvent) \
    qLogAndThrows(name, qlog::QLOG_ERROR, eNo, logEvent)



#define qLogAndThrows(name, level, eNo, logStream) \
    do \
    { \
        int m_eNo = eNo; \
        std::ostringstream _qbuf; \
        _qbuf << logStream; \
        if ( m_eNo != 0 ) \
            _qbuf << " -- (" << m_eNo << ')' << strerror(m_eNo); \
        if ( qlog::isLog(name, level) ) \
            qlog::qLogAllStream(name, level, _qbuf.str(), __FILE__, __LINE__); \
        throw std::runtime_error(_qbuf.str()); \
    } while(0)



#endif  // QLOG_QLOG_H_


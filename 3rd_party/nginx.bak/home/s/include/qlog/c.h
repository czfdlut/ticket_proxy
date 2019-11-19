// c.h (2014-01-18)
// Li Xinjie (xjason.li@gmail.com)

#ifndef QLOG_C_H_
#define QLOG_C_H_

#ifndef __cplusplus

#include <errno.h>

#define CLOG_ALL (0)
#define CLOG_TRACE (0)
#define CLOG_DEBUG (10000)
#define CLOG_INFO  (20000)
#define CLOG_WARN  (30000)
#define CLOG_ERROR (40000)
#define CLOG_FATAL (50000)
#define CLOG_OFF   (60000)

void cLogAll(const char* name, int level, int eNo, const char* file, int line,
        const char* fmt,...) __attribute__ ((format (printf, 6, 7)));

void cLogConfig(const char* configfile);

void cLogCleanConfig();

#define qLog(name, level, fmt, args...) \
    cLogAll(name, level, 0, __FILE__, __LINE__, fmt, ##args)

#define qLogTrace(name, fmt, args...)   \
    cLogAll(name, CLOG_TRACE, 0, __FILE__, __LINE__, fmt, ##args)

#define qLogDebug(name, fmt, args...)   \
    cLogAll(name, CLOG_DEBUG, 0, __FILE__, __LINE__, fmt, ##args)

#define qLogInfo(name, fmt, args...)    \
    cLogAll(name, CLOG_INFO,  0, __FILE__, __LINE__, fmt, ##args)

#define qLogWarn(name, fmt, args...)    \
    cLogAll(name, CLOG_WARN,  0, __FILE__, __LINE__, fmt, ##args)

#define qAppError(name, fmt, args...)   \
    cLogAll(name, CLOG_ERROR, 0, __FILE__, __LINE__, fmt, ##args)

#define qSysError(name, fmt, args...)   \
    cLogAll(name, CLOG_ERROR, errno, __FILE__, __LINE__, fmt, ##args)

#define qLogError(name, eNo, fmt, args...) \
    cLogAll(name, CLOG_ERROR, eNo, __FILE__, __LINE__, fmt, ##args)

#define qLogConfig cLogConfig
#define qLogCleanConfig cLogCleanConfig

#endif // __cplusplus

#endif // QLOG_C_H_

// level.h (2014-01-20)
// Li Xinjie (xjason.li@gmail.com)

#ifndef QLOG_LEVEL_H_
#define QLOG_LEVEL_H_

#include <log4cplus/loglevel.h>

namespace qlog {

enum Level {
    QLOG_ALL     = log4cplus::ALL_LOG_LEVEL,
    QLOG_TRACE   = log4cplus::TRACE_LOG_LEVEL,
    QLOG_DEBUG   = log4cplus::DEBUG_LOG_LEVEL,
    QLOG_INFO    = log4cplus::INFO_LOG_LEVEL,
    QLOG_WARN    = log4cplus::WARN_LOG_LEVEL,
    QLOG_ERROR   = log4cplus::ERROR_LOG_LEVEL,
    QLOG_FATAL   = log4cplus::FATAL_LOG_LEVEL,
    QLOG_OFF     = log4cplus::OFF_LOG_LEVEL,
};

} // namespace qlog

#endif // QLOG_LEVEL_H_

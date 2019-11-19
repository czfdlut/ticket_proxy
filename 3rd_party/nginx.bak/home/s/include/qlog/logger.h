// logger.h (2014-03-06)
// Yan Gaofeng (yangaofeng@360.cn)

#ifndef __LOGGER_H__
#define __LOGGER_H__

#include <log4cplus/logger.h>

#include "logger_impl.h"

namespace qlog {

class Logger : public log4cplus::Logger {
public:
    Logger(qlog::LoggerImpl *ptr) {
        value = ptr;
        if (value) {
            value->addReference();
        }
    }
    void callAppenders(const log4cplus::spi::InternalLoggingEvent& event
            ,bool is_relay_msg) const {
        return ((qlog::LoggerImpl *)value)->callAppenders(event, is_relay_msg); 
    }
};

} //namespace qlog

#endif /*__LOGGER_H__*/

// logger_factory.h (2014-03-05)
// Yan Gaofeng (yangaofeng@360.cn)

#ifndef __LOGGER_FACTORY_H__
#define __LOGGER_FACTORY_H__

#include <log4cplus/spi/loggerfactory.h>
#include <log4cplus/hierarchy.h>
#include "logger.h"
#include "logger_impl.h"

namespace qlog {

class LoggerFactory : public log4cplus::spi::LoggerFactory {
public:
    log4cplus::Logger makeNewLoggerInstance(const log4cplus::tstring& name,
            log4cplus::Hierarchy& h) {
        return static_cast<log4cplus::Logger>(
                qlog::Logger(new qlog::LoggerImpl(name, h)));
    }
}; 

} //namespace qlog

#endif /*__LOGGER_FACTORY_H__*/


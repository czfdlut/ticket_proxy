// logger_impl.h (2014-03-06)
// Yan Gaofeng (yangaofeng@360.cn)

#ifndef __LOGGER_IMPL_H__
#define __LOGGER_IMPL_H__

#include <log4cplus/helpers/pointer.h>
#include <log4cplus/spi/loggerimpl.h>
#include <pthread.h>

namespace qlog {

class LoggerImpl : public log4cplus::spi::LoggerImpl {
public:
    LoggerImpl(const log4cplus::tstring& name, log4cplus::Hierarchy& h) 
        : log4cplus::spi::LoggerImpl(name, h) {
            pthread_rwlock_init(&rwlock_, NULL);
        }
    virtual ~LoggerImpl() { pthread_rwlock_destroy(&rwlock_); }

    virtual void callAppenders(
            const log4cplus::spi::InternalLoggingEvent& event);

    void callAppenders(
            const log4cplus::spi::InternalLoggingEvent& event, bool is_relay_msg);

    virtual void addAppender(log4cplus::SharedAppenderPtr newAppender);
    void addAppender(log4cplus::SharedAppenderPtr newAppender, bool is_relay_msg);
    virtual AppenderAttachableImpl::ListType getAllAppenders();
    virtual log4cplus::SharedAppenderPtr
        getAppender(const log4cplus::tstring& name);
    virtual void removeAllAppenders();
    virtual void removeAppender(log4cplus::SharedAppenderPtr appender);

    int appendLoopOnAppenders(
            const log4cplus::spi::InternalLoggingEvent& event) const;
    int appendLoopOnAppenders(
            const log4cplus::spi::InternalLoggingEvent& event, bool is_relay_msg) const;

private:
    pthread_rwlock_t rwlock_;
};

} //namespace qlog

#endif /*__LOGGER_IMPL_H__*/


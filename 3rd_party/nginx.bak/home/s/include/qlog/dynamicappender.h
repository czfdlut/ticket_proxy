// Module:  Log4CPLUS
// File:    dynamicappender.h
// Created: 6/2003
// Author:  Tad E. Smith
//
//
// Copyright (C) Tad E. Smith  All rights reserved.
//
// This software is published under the terms of the Apache Software
// License version 1.1, a copy of which has been included with this
// distribution in the LICENSE.APL file.
//

/** @file */

#ifndef _QLOG_DYNAMIC_APPENDER_HEADER_
#define _QLOG_DYNAMIC_APPENDER_HEADER_

#include <log4cplus/config.hxx>
#include <log4cplus/appender.h>
#include <log4cplus/helpers/property.h>

namespace qlog {

struct LogAttr {
    unsigned int sec_;
    unsigned int usec_;
    std::string host_;
    unsigned int level_;
};

/**
 * Appends log events to a file.
 */
class LOG4CPLUS_EXPORT DynamicAppender : public log4cplus::Appender {
public:
  // Ctors
    DynamicAppender(const log4cplus::tstring& path
                        , const log4cplus::tstring& conf);
    DynamicAppender(const log4cplus::helpers::Properties& properties);

    typedef bool (*InitFunc)(const char *conf);
    typedef void (*ProcessFunc)(const LogAttr *log_attr, const char *log_data, unsigned int log_len);

  // Dtor
    virtual ~DynamicAppender();

  // Methods
    virtual void close();

    //virtual log4cplus::tstring getInfo() const { return LOG4CPLUS_TEXT("DynamicAppender"); }

protected:
    virtual void append(const log4cplus::spi::InternalLoggingEvent& event);

private:
  // Disallow copying of instances of this class
    DynamicAppender(const DynamicAppender&);
    DynamicAppender& operator=(const DynamicAppender&);

    bool LoadSo();

private:
    log4cplus::tstring mod_path_; //模块文件路径
    log4cplus::tstring mod_conf_path_; //模块配置文件路径

    InitFunc init_func_;
    ProcessFunc process_func_;

    void *so_handler_;
};

} /*qlog*/

#endif // _QLOG_DYNAMIC_APPENDER_HEADER_


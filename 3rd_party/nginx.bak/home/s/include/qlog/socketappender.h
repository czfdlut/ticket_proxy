// Module:  qlog
// File:    socketappender.h
// Created: 5/2003
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

#ifndef _QLOG_SOCKET_APPENDER_HEADER_
#define _QLOG_SOCKET_APPENDER_HEADER_

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>

#include <log4cplus/config.hxx>
#include <log4cplus/appender.h>
#include <log4cplus/helpers/timehelper.h>
#include <log4cplus/helpers/socket.h>
#include <log4cplus/helpers/property.h>
#include <stdio.h>
#include <boost/thread/tss.hpp>
#include <boost/scoped_ptr.hpp>

#include "socketbuffer.h"
#include "socket_pool.h"
#include "qlog.h"

namespace qlog {

const size_t kMaxMsgSize = kMaxLogSize + 4096;

class LOG4CPLUS_EXPORT SocketAppender : public log4cplus::Appender {
public:
    SocketAppender(const log4cplus::tstring& host
            , const log4cplus::tstring& serverName
            , uint32_t send_timeout
            , time_t recordInterval
            , log4cplus::tstring recordPath);

    SocketAppender(const log4cplus::helpers::Properties& properties);

    // Dtor
    ~SocketAppender();
    void doAppend(const log4cplus::spi::InternalLoggingEvent& event, bool is_relay_msg);

    // Methods
    virtual void close();
protected:
    virtual void append(const log4cplus::spi::InternalLoggingEvent& event);
    virtual bool appendSocket(
            const log4cplus::spi::InternalLoggingEvent& event);
    void HandleFailMessage(const log4cplus::spi::InternalLoggingEvent& event);
    void InitSockets(log4cplus::tstring rawhost, int defaultPort);
    void recordMissed(log4cplus::helpers::Time now);
    void OpenMissingFile();

    // Data
    time_t reconnectDelay; //delay in second
    int port;
    log4cplus::tstring serverName;

    int lostCount;
    int successCount;

    log4cplus::helpers::Time recordTime;

    int32_t sendTimeout;
    int32_t recvTimeout;
    int sendBufferSize;

    time_t recordInterval;
    log4cplus::tstring recordPath;
    FILE* recordFile;

    log4cplus::tstring currentPath;
    log4cplus::tstring currentLogPath;
    log4cplus::tstring compress;

    boost::scoped_ptr<SocketPool> sockets;
    uint32_t maxConnections;
    uint32_t connectTimeout;
    uint32_t connectCheckInterval;
    int maxRetry;

    log4cplus::helpers::Time latestTime;
    
    boost::thread_specific_ptr<SocketBuffer> socketBuffer;
    bool cachedTime;
    bool isInternalRelayMsg;

private:
    // Disallow copying of instances of this class
    SocketAppender(const SocketAppender&);
    SocketAppender& operator=(const SocketAppender&);
};


log4cplus::tstring& ltrim(log4cplus::tstring& ss);
log4cplus::tstring& rtrim(log4cplus::tstring& ss);
log4cplus::tstring& trim(log4cplus::tstring& ss);

bool convertToBuffer(SocketBuffer *socket_buffer
        , const log4cplus::spi::InternalLoggingEvent& event
        , const log4cplus::tstring& serverName
        , const log4cplus::tstring& compress
        , bool  isInternalRelayMsg);

} // end namespace qlog

#endif // _QLOG_SOCKET_APPENDER_HEADER_


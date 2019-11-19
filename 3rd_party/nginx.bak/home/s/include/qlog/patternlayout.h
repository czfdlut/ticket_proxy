#ifndef _QLOG_LAYOUT_HEADER_
#define _QLOG_LAYOUT_HEADER_

#include <log4cplus/layout.h>

namespace qlog {

// Forward Declarations
namespace pattern {
    class PatternConverter;
}

class PatternLayout : public log4cplus::Layout {
public:
  // Ctors and dtor
    PatternLayout(const log4cplus::tstring& pattern);
    PatternLayout(const log4cplus::helpers::Properties& properties);
    virtual ~PatternLayout();

    virtual void formatAndAppend(log4cplus::tostream& output, 
                                 const log4cplus::spi::InternalLoggingEvent& event);

protected:
    void init(const log4cplus::tstring& pattern, unsigned ndcMaxDepth = 0);

  // Data
    log4cplus::tstring pattern;
    std::vector<pattern::PatternConverter*> parsedPattern;

private: 
  // Disallow copying of instances of this class
    PatternLayout(const PatternLayout&);
    PatternLayout& operator=(const PatternLayout&);
};


} // end namespace log4cplus

#endif // LOG4CPLUS_LAYOUT_HEADER_


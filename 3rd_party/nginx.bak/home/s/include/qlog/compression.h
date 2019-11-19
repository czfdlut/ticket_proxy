#ifndef _QLOG_COMPRESSION_H_
#define _QLOG_COMPRESSION_H_

namespace qlog {

enum compress_type
{
    Z_DEFLATE = 1
};

enum compress_ret
{
    COMPRESS_OK,
    COMPRESS_FAILED,
    COMPRESS_BUFFER_ERROR,
    COMPRESS_INVALID_PARAMETER,
    COMPRESS_INVALID_TYPE,
    COMPRESS_INVALID_FORMAT
};

compress_ret
q_compress(const char* source, long source_len,
        char* dest, long* dest_len, 
        compress_type type);

compress_ret
q_uncompress(const char* source, long source_len,
        char* dest, long* dest_len);

long
q_compressBound(long source_len);

} // namespace qlog

#endif


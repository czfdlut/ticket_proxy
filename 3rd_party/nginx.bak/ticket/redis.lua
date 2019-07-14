-- redis lua 模块封装
local redis = require("resty.redis")
local _M = {}

local config = {
    host = '127.0.0.1',
    port = 6379,
    passwd = 'abCD1234%$',
    timeout = 200, 
    database = 0
}

function _M.connect()
    --local redis = require "resty.redis"
    local red = redis:new()

    red:set_timeout(1000) -- 1 sec

    local ok, err = red:connect(config["host"], config["port"], 0)
    if not ok then
        ngx.log(ngx.ERR, string.format("failed to connect: %s", err))
        return
    end

    local res, err = red:auth(config["passwd"])
    if not res then
        ngx.log(ngx.ERR, string.format("failed to authenticate: ", err))
        return
    end

    ngx.log(ngx.NOTICE, res)

    return red
end

function keepalive(red)
    -- put it into the connection pool of size 100,
    -- with 10 seconds max idle time
    local ok, err = red:set_keepalive(10000, 100)
    if not ok then
        ngx.log(ngx.ERR, string.format("failed to set keepalive: ", err))
        return
    end
end 

function _M.set(red, key)
    local res, err = red:set(key)
    if not res then
        ngx.log(ngx.ERR, string.format("failed to set: ", err))
        return nil
    end
    return res
end


function _M.get(red, key)
    local res, err = red:get(key)
    if not res then
        ngx.log(ngx.ERR, string.format("failed to get: ", err))
        return nil
    end
    return res
end

function _M.hset(red, hkey, key, value)
    local res, err = red:hset(hkey, key, value)
    if not res then
        ngx.log(ngx.ERR, string.format("failed to get: ", err))
        return nil
    end
    return res
end

function _M.hget(red, hkey, key)
    local res, err = red:hget(hkey, key)
    if not res then
        ngx.log(ngx.ERR, string.format("failed to get: ", err))
        return nil
    end
    return res
end

return _M



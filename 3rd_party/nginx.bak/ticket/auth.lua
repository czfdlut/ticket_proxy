local redis = require "ticket.redis"
--local cjson = require("cjson")

local _M = {}

function _M.auth(redis_client, is_clean_uid) 
    local ticket_uid = ngx.req.get_headers()["ticket-uid"]

    if ticket_uid == nil then
        ngx.log(ngx.ERR, "not found ticket uid from header")
        return ngx.exit(403)
    end

    ngx.log(ngx.NOTICE, string.format("ticket-uid: %s", ticket_uid))

    if string.len(ticket_uid) < 3 or string.len(ticket_uid) > 128 then
        ngx.log(ngx.ERR, "ticket uid is valid")
        return ngx.exit(403)
    end 

    local uid  = redis.hget(redis_client, "ticket-uid", ticket_uid)
    if uid == nil then
        ngx.log(ngx.ERR, "not found ticket uid from redis")
        return ngx.exit(403)
    end

    if is_clean_uid == true then
        ngx.req.clear_header("ticket-uid")
    end

    ngx.log(ngx.NOTICE, "auth is ok")
end

return _M


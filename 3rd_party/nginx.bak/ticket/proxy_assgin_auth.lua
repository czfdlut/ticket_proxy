local redis = require "ticket.redis"
local auth = require "ticket.auth"

local redis_db = redis.connect()
auth.auth(redis_db, false)

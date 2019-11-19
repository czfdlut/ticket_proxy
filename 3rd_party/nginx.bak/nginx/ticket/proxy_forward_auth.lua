local redis = require "ticket.redis"
local auth = require "ticket.auth"

local redis_client = redis.connect()
auth.auth(redis_client, true)

local h = require("lib.helpers")
local file = 'day4.txt'
local lines = h.lines_from(file)
local answers = {}

local part1 = 0;
local part2 = 0;
for _, range in pairs(lines) do
  for a, b, c, d in string.gmatch(range, "(%d+)-(%d+),(%d+)-(%d+)") do
    local x1 = tonumber(a)
    local x2 = tonumber(b)
    local y1 = tonumber(c)
    local y2 = tonumber(d)

    if (x1 >= y1 and x2 <= y2) then
      part1 = part1 + 1
      part2 = part2 + 1
      break;
    end
    if (x1 <= y1 and x2 >= y2) then
      part1 = part1 + 1
      part2 = part2 + 1
      break;
    end
    if (x1 <= y2 and y1 <= x2) then
      part2 = part2 + 1
    end
  end
end

answers.part1 = part1
answers.part2 = part2

P(answers)

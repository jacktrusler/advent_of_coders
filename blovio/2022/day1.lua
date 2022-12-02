local h = require("lib.helpers")
local file = 'day1.txt'
local lines = h.lines_from(file)
local sum = 0
local totals = {}
local answers = {}

for _, v in pairs(lines) do
  if v ~= "" then
    sum = sum + v
  else
    table.insert(totals, sum)
    sum = 0
  end
end

local max = 0
for _, v in pairs(totals) do
  if v > max then
    max = v
  end
end

answers.part1 = max

local function bubbleSort(t)
  local i = 0
  local j = 0
  for _, _ in pairs(t) do
    i = i + 1
    for _, _ in pairs(t) do
      j = j + 1
      if t[j + 1] == nil then break end
      if t[j] > t[j + 1] then
        local temp = t[j]
        t[j] = t[j + 1]
        t[j + 1] = temp
      end
    end
    j = 0
  end
  return t
end

local sortedT = bubbleSort(totals)
answers.part2 = sortedT[#sortedT] + sortedT[#sortedT - 1] + sortedT[#sortedT - 2]

P(answers)
